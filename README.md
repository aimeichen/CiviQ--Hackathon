---
tags: [agentapp]
dataset: []
framework: []
---

# CiviQ — Nori Community Companion

CiviQ is a privacy-first community-support product. **Nori** is its friendly,
mobile-companion style interface: the one character a person speaks with while
the specialist agents work privately in the background.

## Live project links

- **Public demo:** https://civiq-hackathon.replit.app/
- **Hackathon deck:** https://gamma.app/docs/Nori-Community-Companion-yq59aw2rzqw67ot?mode=doc
- **Final pitch PDF:** [`docs/CiviQ-Meet-Nori-Hackathon-Pitch.pdf`](docs/CiviQ-Meet-Nori-Hackathon-Pitch.pdf)
- **Submission narrative:** [`SUBMISSION.md`](SUBMISSION.md)
- **Judge-facing narrative:** [`SUBMISSION_NARRATIVE.md`](SUBMISSION_NARRATIVE.md)

## Agent Team

- **Nori PMO Orchestrator** — the only user-facing companion; combines worker
  outputs into one warm, practical response.
- **Safety & Needs Triage** — identifies needs, urgency, and the minimum safe
  follow-up question.
- **Local Resource Navigator** — identifies resource categories and safely
  requests a city, neighbourhood, or postal code when needed. It deliberately
  does not invent local services before verified source data is connected.
- **Action Plan Helper** — turns a request into up to three user-controlled,
  phone-friendly next steps.

All model calls use the Flower Runtime credentials injected at run time; no
model-provider key is stored in this repository.

## Build

Install the project and build its Flower App Bundle (FAB):

```shell
uv sync
uv run flwr build
```

## Try the deterministic MVP locally

The project includes a no-key mock engine for a Replit or mobile frontend. It
uses the same verified San Francisco catalog as the Flower AgentApp:

```shell
uv run python demo_cli.py "I need food support this week"
uv run python -m unittest agent.test_mock
```

This fallback is deliberately deterministic, so the demo still works before
Flower Agent runtime access is enabled.

## Customize

The Agent Team is defined in `agent/agent_app.py`. The current prompt is
available as `agent.prompt`, and the run-series history is reconstructed from
`agent.events.get_trace()`.

## MVP limitation

The first pilot is **San Francisco**. The MVP includes a small, local verified
catalog in `agent/resources/san_francisco_resources.json`: 211 Bay Area,
SF-Marin Food Bank, SFHSA CalFresh, SF 311, OEWD job help, SF Superior Court
eviction self-help, and SF Health Network homelessness services.

The catalog is matched deterministically before the Local Resource Navigator
receives it. Nori never fabricates a resource, address, hour, or eligibility
rule; users are asked to confirm current availability with the source.

## Learn more

See the [Flower Agent documentation](https://flower.ai/docs/agent/) for more
tutorials and guides.
