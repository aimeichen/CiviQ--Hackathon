# CiviQ — Meet Nori

## A calm first step toward support that already exists

When someone needs food, housing support, legal help, or a job, the hardest
part is often not that help does not exist. It is knowing where to begin.
Support is fragmented across agencies, nonprofit sites, phone lines, forms,
eligibility rules, and office hours. For a person already under stress, a
desktop-first service directory can feel like another barrier.

**CiviQ is a privacy-first mobile companion that helps people find a verified
local starting point and take one safe next step.** Its friendly interface is
**Nori**: a small, ambient companion designed to live where people already are
on their phones—through a widget, notification, voice prompt, or lightweight
workspace—instead of asking them to learn another portal.

Our San Francisco MVP begins with a simple moment: someone says, *“I need food
support this week.”* Nori responds with care, asks only for the minimum useful
context (such as a neighborhood or ZIP code, never a home address), and turns a
large, confusing search into a few source-backed options and an achievable
plan. The person remains in control of what they share and what they do next.

## Why now

Public-benefit and community-support systems contain an enormous amount of
value, but access is uneven. The people most likely to need support are often
least well served by systems that assume time, language confidence, stable
internet, a laptop, or comfort with complex forms. AI can widen that gap if it
confidently invents answers. CiviQ takes the opposite approach: it uses AI to
make the first step warmer and simpler while making the evidence, uncertainty,
and user control visible.

## One companion, three accountable specialists

Nori is intentionally the only character a person sees. Behind that simple
experience, a Flower AgentApp coordinates three internal specialists:

1. **Safety & Needs Triage** identifies the support category, urgency, and the
   smallest safe follow-up question. A possible immediate safety concern takes
   priority over ordinary resource matching.
2. **Local Resource Navigator** can recommend only resources from a compact,
   source-backed San Francisco catalog. It never fabricates addresses, hours,
   eligibility, availability, or contact details.
3. **Action Plan Helper** converts a recommendation into no more than three
   phone-friendly next steps. It never contacts an organization, shares data,
   or acts on a user's behalf without explicit consent.

The **Nori PMO Orchestrator** combines those specialist outputs into one warm,
non-technical answer. This is not multi-agent theater: the roles separate the
decisions that need different guardrails. Triage should not invent services;
resource matching should not determine eligibility; and planning should never
be mistaken for permission to act.

## What we built

- A public phone-first CiviQ interaction prototype, including an ambient
  companion mode, local-support discovery, and a small task-oriented action
  flow.
- A published Flower AgentApp that packages Nori and the three-agent team for
  transparent review and reuse.
- A deterministic, no-key MVP fallback for reliable demonstrations before
  runtime access is available.
- A small, verified San Francisco catalog covering 211, food support,
  CalFresh guidance, homelessness navigation, jobs, health services, eviction
  information, and SF 311. Every resource record includes a source URL and
  last-verified date.
- Guardrails for privacy and trust: no home-address request, no eligibility
  guarantee, no made-up local details, no document collection, and no external
  action without consent.

## The demo story

Maria opens CiviQ and speaks naturally: *“I need food support in San Francisco
this week.”* Nori does not ask her to complete a form or disclose her address.
It offers a verified starting point, makes clear that availability must be
confirmed with the provider, and lets Maria save a small preparation task.
Behind the scenes, triage checks for safety, the navigator grounds the answer
in a source catalog, and the action helper keeps the next step manageable.

The result is deliberately modest: not an assistant that promises to solve
someone's life, but a companion that can help them take the next real step.

## Why Flower

Flower gives CiviQ a clear, publishable home for the agent system itself. The
AgentApp makes the collaboration boundary inspectable: reviewers can see the
orchestrator, specialist responsibilities, local data contract, and safety
rules rather than evaluating a black-box chat experience. It also gives us a
path toward our longer-term vision: community partners can eventually improve
resource coverage and learn aggregate unmet needs without centralizing a
person's private story.

## What comes next

The MVP is intentionally a narrow San Francisco pilot. The next phase is not
to add more generic AI conversation; it is to co-design verification workflows
with community partners, add language and accessibility support, connect
consent-based reminders, and make resource freshness auditable. Over time,
CiviQ can become a federated community-intelligence layer: helping each person
find support today while helping trusted local ecosystems understand where
support is missing tomorrow.

**CiviQ does not replace frontline workers or public services. It makes the
first connection to them feel possible.**

## Links

- **Live demo:** https://civiq-hackathon.replit.app/
- **Flower AgentApp:** https://flower.ai/apps/norahhxx/civiq-community-companion
- **Source code and submission materials:** https://github.com/aimeichen/CiviQ--Hackathon
- **Pitch deck:** `docs/CiviQ-Meet-Nori-Hackathon-Pitch.pdf`
