# CiviQ / Nori — Replit Final-Polish Brief

This is the final, scoped update list for the public demo at
https://civiq-hackathon.replit.app/. Do not add unrelated features before the
Hackathon presentation.

## P0 — Keep the product identity consistent

- **Platform:** CiviQ
- **User-facing companion:** Nori
- **Tagline:** `Verified local support. One safe next step.`
- Replace any remaining product-facing `Bee` copy with `CiviQ` or `Nori`.
- In the presentation and Flower code, use the same naming convention.

## P0 — Make the food demo evidence-based

The main Food flow should follow this exact path:

1. User says: `I need food support in San Francisco this week.`
2. Nori replies: `I can help you find a verified starting point. If you want a
   closer option, you can share only a neighborhood or ZIP—not your home
   address.`
3. Show two cards, each with **official source**, **last verified**, and
   **check availability** language.
4. User selects one and sees a one-to-three-step plan in **My Tasks**.

### Food cards to display

**San Francisco-Marin Food Bank — Food Locator**

- Description: Free groceries, emergency food, senior food boxes, and CalFresh
  application help in San Francisco or Marin.
- Action: `Find a nearby option in the official Food Locator.`
- Source: https://www.sfmfoodbank.org/find-food/
- Last verified: `2026-09-29`
- Disclaimer: `Hours and availability can change. Please confirm before going.`

**San Francisco Human Services Agency — Apply for CalFresh**

- Description: Official application guidance for San Francisco food assistance.
- Action: `Review official steps or call (855) 355-5757 for application help.`
- Source: https://www.sfhsa.org/services/food/calfresh/apply-calfresh
- Last verified: `2026-09-29`
- Disclaimer: `The agency decides eligibility; Nori does not make eligibility decisions.`

## P0 — Add the collaboration trace

On the food-result screen, add a collapsed, non-technical panel called
**How Nori prepared this**:

```text
✓ Understood your request
✓ Checked for urgent safety concerns
✓ Matched verified local sources
✓ Prepared your next step
```

This makes the multi-agent design visible without exposing chain-of-thought or
internal prompts.

## P0 — Add an emergency-safe branch

If the message includes `immediate danger`, `medical emergency`, `not
breathing`, `overdose`, `weapon`, `suicide`, or `self harm`, do not show normal
resource cards. Display:

> I’m sorry this feels urgent. If you are in immediate danger or need urgent
> medical help, call 911 now. If you can, ask a trusted person nearby to stay
> with you while you call.

Button: `Call 911` (or a clearly labelled simulated-demo action if telephone
actions are not enabled).

## P1 — Small UI refinements

- Keep the Light Mode screen; it is the strongest expression of the mobile
  companion concept.
- On resource cards, replace generic `Local support` with the verified source
  and a clear action.
- Keep the existing privacy notices. Add: `Nori never contacts a provider or
  shares your information without asking.`
- Preserve the current local-only demo-state notice in My Tasks.
- Label any non-functional controls as `Demo` or `Coming later`; do not imply
  background document upload, provider booking, or real-time availability.

## Acceptance test before presenting

- The public URL opens in an incognito browser without login.
- Food query shows the two named official sources above.
- The user can see that a home address is not required.
- Selecting a food card creates or reveals a corresponding My Tasks plan.
- Emergency terms show the 911-safe response only.
- The visible UI calls the product CiviQ and the companion Nori everywhere.
