"""Deterministic, no-key MVP engine for the CiviQ / Nori frontend and demos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RESOURCE_CATALOG_PATH = Path(__file__).parent / "resources" / "san_francisco_resources.json"

EMERGENCY_TERMS = (
    "immediate danger",
    "medical emergency",
    "overdose",
    "weapon",
    "suicide",
    "self harm",
    "not breathing",
    "紧急危险",
    "医疗急救",
    "自杀",
)


def load_resources() -> list[dict[str, Any]]:
    """Load the small source-backed San Francisco pilot catalog."""
    return json.loads(RESOURCE_CATALOG_PATH.read_text(encoding="utf-8"))["resources"]


def matching_resources(user_message: str) -> list[dict[str, Any]]:
    """Return up to three catalog entries using transparent keyword matching."""
    query = user_message.casefold()
    scored: list[tuple[int, dict[str, Any]]] = []
    for resource in load_resources():
        score = sum(tag.casefold() in query for tag in resource["tags"])
        if score:
            scored.append((score, resource))

    scored.sort(key=lambda item: item[0], reverse=True)
    if scored:
        return [resource for _, resource in scored[:3]]

    return [
        resource for resource in load_resources() if resource["id"] == "211-bay-area"
    ]


def _need_category(resources: list[dict[str, Any]]) -> str:
    if not resources:
        return "general support"
    categories = resources[0]["categories"]
    return categories[0] if categories else "general support"


def build_demo_response(user_message: str) -> dict[str, Any]:
    """Build a stable response contract for the mobile MVP without an LLM."""
    normalized = user_message.casefold()

    if any(term in normalized for term in EMERGENCY_TERMS):
        return {
            "message": (
                "I’m sorry this feels urgent. If you are in immediate danger or "
                "need urgent medical help, call 911 now."
            ),
            "needs": ["immediate safety"],
            "urgency": "immediate_safety_concern",
            "resources": [],
            "plan": [
                {
                    "title": "Get immediate help",
                    "description": "Call 911 or ask a trusted person nearby to help you call.",
                    "consentRequired": False,
                }
            ],
            "followUpQuestion": "Are you somewhere safer right now?",
            "privacyNote": "Do not share private details unless needed to get immediate help.",
        }

    resources = matching_resources(user_message)
    category = _need_category(resources)
    names = [resource["name"] for resource in resources]

    if category in {"food", "groceries"}:
        message = (
            "I’m glad you reached out. You do not need to share your home address. "
            "Here are a couple of verified San Francisco food-support starting points."
        )
        question = "Would you rather find free food today, or explore CalFresh support?"
    elif category == "legal":
        message = (
            "That sounds stressful. Here is a verified official starting point for "
            "San Francisco eviction information; it is information, not legal advice."
        )
        question = "Would you like a small checklist of what to keep with you?"
    elif category == "employment":
        message = (
            "I can help you start with a verified San Francisco job-support pathway."
        )
        question = "Are you looking for training, a first job, or a career change?"
    elif category in {"homelessness", "housing navigation"}:
        message = (
            "You deserve practical support. Here is a verified non-emergency San Francisco "
            "starting point; you never need to share a home address with Nori."
        )
        question = "Would a neighborhood or ZIP code be comfortable to share?"
    elif category == "health":
        message = (
            "Here is a verified San Francisco health and service-connection starting point."
        )
        question = "Would you like help finding a nearby option, using only a neighborhood or ZIP code?"
    else:
        message = (
            "I’m here with you. A confidential local resource navigator is a good first step."
        )
        question = "What kind of support would be most helpful today: food, housing, work, health, benefits, or legal help?"

    plan = [
        {
            "title": "Choose one starting point",
            "description": f"Open {names[0]} and review the official current information.",
            "consentRequired": False,
        },
        {
            "title": "Keep it private",
            "description": "Share only a San Francisco neighborhood or ZIP code if you want a more local match.",
            "consentRequired": False,
        },
        {
            "title": "Optional reminder",
            "description": "Nori can prepare a reminder, but only if you choose to create one.",
            "consentRequired": True,
        },
    ]

    return {
        "message": message,
        "needs": [category],
        "urgency": "standard",
        "resources": [
            {
                "id": resource["id"],
                "name": resource["name"],
                "whyItMayHelp": resource["who_it_may_help"],
                "nextAction": resource["next_action"],
                "contact": resource["contact"],
                "sourceUrl": resource["source_url"],
                "lastVerified": resource["last_verified"],
                "verifyAvailability": True,
            }
            for resource in resources
        ],
        "plan": plan,
        "followUpQuestion": question,
        "privacyNote": "Nori asks for the minimum information needed and does not contact providers for you.",
    }
