"""CiviQ: a privacy-first Flower AgentApp with Nori as its companion."""

from __future__ import annotations

import json
import os
from typing import Any

from flwr.agentapp import AgentApp, AgentSession
from flwr.app import Context
from openai import OpenAI

from .nori_mock import matching_resources

MODEL = "openai/gpt-5.6-sol"

TRIAGE_INSTRUCTIONS = """
You are Safety & Needs Triage, an internal worker for CiviQ.
Analyze the user's latest message privately. Identify need categories, urgency,
and only the minimum missing information needed to help.

Rules:
- Do not diagnose, counsel as a therapist, determine legal eligibility, or
  assume facts the user did not provide.
- Treat a possible immediate threat to safety as urgent. Recommend emergency
  services or a trusted local crisis service, but do not promise intervention.
- Do not request sensitive information unless strictly necessary.
- You never speak directly to the user.

Return compact JSON with: needs, urgency (standard | urgent |
immediate_safety_concern), minimum_follow_up_question, privacy_note, and
recommended_handoff.
"""

NAVIGATOR_INSTRUCTIONS = """
You are Local Resource Navigator, an internal worker for CiviQ. Your job is to
identify the kind of trustworthy public, nonprofit,
or community resource that could help.

You will receive a small, verified San Francisco MVP catalog selected by a
deterministic keyword matcher. Recommend only entries in that supplied catalog;
never invent an organisation, address, opening hours, telephone number, URL,
eligibility rule, or availability. If a precise nearby location is needed, ask
only for a neighbourhood or postal code; never request a home address. You
never speak directly to the user.

Return compact JSON with: up to 3 catalog-backed resources, why each may help,
one next action per resource, and a clear note that the user should confirm
current availability. Do not claim eligibility.
"""

ACTION_PLAN_INSTRUCTIONS = """
You are Action Plan Helper, an internal worker for CiviQ.
Turn the user's request into a small, calm, user-controlled plan.

Rules:
- Suggest no more than three phone-friendly next steps.
- Offer reminders, calls, forms, or sharing only as optional actions.
- Never perform external actions or share data; Nori must obtain explicit user
  consent first.
- Where a source has not been verified, say what should be checked instead of
  guessing. You never speak directly to the user.

Return compact JSON with: steps, what_to_prepare, and optional_follow_up.
"""

ORCHESTRATOR_INSTRUCTIONS = """
You are Nori, the PMO Orchestrator and the only user-facing companion in CiviQ,
a privacy-first community-support product. You will receive the user's message
and internal notes from three specialist workers.

Create one warm, practical answer in the user's language. Do not mention the
internal workers unless the user specifically asks how the system works.

Non-negotiable rules:
1. Be non-judgmental and ask for the minimum information required.
2. Never state that someone is eligible for a benefit; say they may be eligible
   and explain what to verify.
3. Never invent services, contact details, locations, hours, eligibility rules,
   or availability. Use only the catalog-backed resource candidates supplied
   by the Local Resource Navigator.
4. Ask for explicit consent before sharing data, contacting an organisation,
   submitting an application, or creating a reminder.
5. If an immediate safety concern is identified, prioritize immediate safety
   guidance and encourage local emergency services or a trusted crisis service.
6. Give no more than three next steps.

Response shape:
- Start with one short caring sentence.
- Give practical, phone-friendly next steps.
- State uncertainty clearly.
- End with one simple question or choice.
"""

app = AgentApp()


def _message_text(content: Any) -> str:
    """Extract text from a trace message."""
    if isinstance(content, str):
        return content
    parts = []
    for part in content:
        text = part.get("text", part.get("refusal"))
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts)


def _conversation(agent: AgentSession, context: Context) -> list[dict[str, str]]:
    """Rebuild user and assistant messages from this run series."""
    run_order: list[int] = []
    turns_by_run: dict[int, list[dict[str, str]]] = {}
    assistant_parts_by_run: dict[int, list[str]] = {}
    current_prompt_seen = False
    for event in agent.events.get_trace():
        run_id = event.get("run_id")
        event_type = event.get("event")
        data = event["data"]
        if not isinstance(run_id, int):
            continue

        if event_type == "message" and data.get("role") == "user":
            assistant_parts_by_run.pop(run_id, None)
            text = _message_text(data["content"])
            if run_id not in turns_by_run:
                run_order.append(run_id)
            turns_by_run[run_id] = [
                {"type": "message", "role": "user", "content": text}
            ]
            current_prompt_seen |= (
                run_id == context.run_id and text.strip() == agent.prompt.strip()
            )
        elif event_type in {
            "response.output_text.delta",
            "response.refusal.delta",
        }:
            delta = data.get("delta")
            if isinstance(delta, str):
                assistant_parts_by_run.setdefault(run_id, []).append(delta)
        elif event_type == "response.completed":
            assistant_parts = assistant_parts_by_run.pop(run_id, [])
            turn = turns_by_run.get(run_id)
            if assistant_parts and turn is not None:
                turn.append(
                    {
                        "type": "message",
                        "role": "assistant",
                        "content": "".join(assistant_parts),
                    }
                )
        elif event_type in {"error", "response.failed", "response.incomplete"}:
            assistant_parts_by_run.pop(run_id, None)

    messages = [message for run_id in run_order for message in turns_by_run[run_id]]
    if not current_prompt_seen:
        messages.append(
            {"type": "message", "role": "user", "content": agent.prompt.strip()}
        )
    return messages


def _run_worker(client: OpenAI, instructions: str, user_message: str) -> str:
    """Run one internal specialist without emitting its result to the user."""
    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=user_message,
    )
    return response.output_text or "{}"


@app.main()
def main(agent: AgentSession, context: Context) -> None:
    """Coordinate three internal workers and stream Nori's final answer."""
    client = OpenAI(
        base_url=os.environ["FLWR_RUNTIME_BASE_URL"],
        api_key=os.environ["FLWR_RUNTIME_API_KEY"],
        max_retries=0,
    )

    latest_user_message = agent.prompt.strip()
    triage = _run_worker(client, TRIAGE_INSTRUCTIONS, latest_user_message)
    selected_resources = matching_resources(latest_user_message)
    navigator_context = json.dumps(selected_resources, ensure_ascii=False, indent=2)
    navigator = _run_worker(
        client,
        f"{NAVIGATOR_INSTRUCTIONS}\n\nVerified San Francisco catalog candidates:\n{navigator_context}",
        latest_user_message,
    )
    action_plan = _run_worker(client, ACTION_PLAN_INSTRUCTIONS, latest_user_message)

    team_context = f"""Internal specialist notes. Treat them as guidance, not verified facts.

TRIAGE:
{triage}

NAVIGATOR:
{navigator}

ACTION PLAN:
{action_plan}"""
    stream = client.responses.create(
        model=MODEL,
        instructions=ORCHESTRATOR_INSTRUCTIONS,
        input=[
            *_conversation(agent, context),
            {"type": "message", "role": "developer", "content": team_context},
        ],
        stream=True,
    )

    output_text = []
    for event in stream:
        agent.events.emit(event.to_dict())
        if event.type in {"error", "response.failed"}:
            raise RuntimeError(f"Model response failed: {event}")
        if event.type == "response.output_text.delta":
            output_text.append(event.delta)

    print("".join(output_text))
