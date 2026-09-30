# CiviQ — Nori Community Companion

## Submission identity

- **Project:** CiviQ
- **User-facing companion:** Nori
- **Category:** Safe, human-supervised collaborative agents for public services
- **Pilot:** San Francisco, California
- **Public demo:** https://civiq-hackathon.replit.app/
- **Deck:** https://gamma.app/docs/Nori-Community-Companion-yq59aw2rzqw67ot?mode=doc
- **Flower Hub app spec (publish after final review):** `@norahhxx/civiq-community-companion`
- **License:** Apache-2.0

## One-sentence pitch

CiviQ is a privacy-first mobile companion; Nori helps people discover verified
local support and choose one safe next step without navigating a fragmented
social-services system alone.

## Short submission description

CiviQ turns a plain-language request—such as “I need food support this
week”—into a small, human-controlled plan. Nori is the friendly mobile
companion people see in a widget, notification, voice prompt, or app workspace.
Behind Nori, a Flower AgentApp coordinates three internal specialists: Safety &
Needs Triage, Local Resource Navigator, and Action Plan Helper. The San
Francisco MVP uses a small source-backed public-resource catalog, asks only for
minimal context such as a neighborhood or ZIP code, and never claims benefit
eligibility or acts for a person without consent.

## The problem

Useful support exists, but it is fragmented across food, benefits, housing,
employment, health, and legal systems. People often do not know where to begin,
and desktop-first forms can feel overwhelming when help is needed quickly.

## The solution

CiviQ presents one calm, phone-first entry point. Nori gives a person a clear
option and one small next step; the person keeps control over what they share
and whether they take action.

## Collaborative Agent Team

```text
User
  → Nori PMO Orchestrator
      → Safety & Needs Triage
      → Local Resource Navigator
      → Action Plan Helper
  → One safe, source-backed, phone-friendly response
```

- **Nori PMO Orchestrator:** combines specialist results into one concise,
  user-facing answer.
- **Safety & Needs Triage:** identifies urgency and asks the minimum safe
  follow-up.
- **Local Resource Navigator:** recommends only catalog-backed public or
  nonprofit resources.
- **Action Plan Helper:** gives at most three next steps and asks consent before
  any external action.

## What works today

- Public CiviQ mobile demo with an ambient Nori companion, simulated voice entry,
  local-resource discovery, and My Tasks action-plan views.
- Flower AgentApp source for the orchestrator plus the three internal
  specialists.
- Deterministic local matching for a stable, no-key demonstration.
- San Francisco pilot catalog covering food, benefits, homelessness/housing
  navigation, jobs, legal/eviction information, health, and 211.
- Privacy guardrails: no home-address request, no eligibility guarantee, no
  invented resource details, no document collection, and no external action
  without consent.

## Data sources and boundaries

The MVP catalog uses official public/community sources including 211 Bay Area,
SF-Marin Food Bank, SF Human Services Agency, SF 311, OEWD, San Francisco
Superior Court, and SF Health Network. Every recommendation should display its
source URL and last-verified date. Availability and eligibility must be checked
with the provider.

This is an MVP, not legal, medical, or benefits advice. In immediate danger or
an urgent medical emergency, Nori directs people to call 911 rather than running
ordinary resource matching.

## Two-minute demo script

### 0:00–0:15 — Open with the person, not the technology

“Help may already exist, but finding the right starting point is often the hard
part. CiviQ puts Nori—a small mobile companion—where people already are.”

### 0:15–0:35 — Show the ambient phone experience

Open **Light Mode**. Tap Nori and explain that the companion can be reached from
the phone surface instead of requiring a new portal.

### 0:35–1:05 — Run one user case

Enter: **“I need food support in San Francisco this week.”**

Say: “Nori asks only for the minimum useful context, such as a neighborhood or
ZIP—not a home address. It then matches source-backed local support.”

### 1:05–1:25 — Show a resource and its next action

Open the food result. Point out the official source, last-verified date,
availability disclaimer, and the user’s choice to save it as a task.

### 1:25–1:45 — Show My Tasks

Open **My Tasks**. Explain that Nori turns a recommendation into a small,
consent-based preparation path rather than taking action for the user.

### 1:45–2:00 — Explain safe collaboration

Show the Agent Team slide. “Nori is one friendly interface. Behind it, triage
protects the user, the navigator uses verified sources, and the Action Plan
Helper keeps the next step manageable.”

## Judge Q&A answers

**Why multiple agents?** Different responsibilities need different guardrails:
triage should not invent resources, and resource matching should not decide to
act for a person. The orchestrator keeps the experience simple while preserving
those boundaries.

**How do you avoid hallucinations?** The MVP filters a compact, verified local
catalog before the Resource Navigator responds. It asks the user to check
current provider availability rather than claiming eligibility or openings.

**What is private?** The user is asked for only the context needed to help,
such as a neighborhood or ZIP. The public demo stores progress in the browser
and does not upload documents.

**What happens next?** Co-design with local community partners, verification
workflows for resources, more languages and neighborhoods, and only
consent-based integrations.

## Final delivery checklist

- [ ] Public demo opens without login.
- [ ] Demo brand is consistently **CiviQ / Nori**.
- [ ] Food result exposes source, last-verified date, and “check availability.”
- [ ] One emergency-safe response is present and tested.
- [ ] Gamma deck uses real CiviQ screenshots and the public demo link.
- [ ] This README/SUBMISSION file and the Flower source are ready for review.
- [ ] Flower source has no credentials, personal data, or private connector
      files before publishing.
- [ ] `uv run python -m unittest agent.test_mock` and `uv run flwr build` pass.
- [ ] A 60–90 second backup screen recording is saved locally.

## Flower Hub release checklist

1. Review every source file that will be public.
2. Confirm the metadata uses `civiq-community-companion` and the signed-in
   publisher `norahhxx`.
3. Run:

   ```shell
   uv sync
   uv run python -m unittest agent.test_mock
   uv run flwr build
   uv run flwr login supergrid
   ```

4. Only after that final review, publish with:

   ```shell
   uv run flwr app publish .
   ```

Flower Hub publishes source code, not only the local FAB bundle. Runtime access
and Hub publishing remain separate: the public Replit demo is the primary
presentation surface until Flower runtime access is available.
