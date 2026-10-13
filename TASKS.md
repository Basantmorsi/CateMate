# CateMate — Development Tasks

Ordered task list derived from the Week 1 worksheet. Each task is full-stack (API + page + tests): it's done when a user can actually do it in the browser.

## Scope decisions
- Scope = **MVP + Should haves**; nice-to-haves stay in the backlog.
- "Nearby" = **distance radius** (lat/long) in the MVP.
- Match rules: **search is per cat**, **opposite gender only**, **exclude my own cats**, filters for **breed / colour / age**.
- Safety: **contact-info hiding + security hardening in MVP**; block/report + verification immediately after MVP.
- Meetup scheduling = **Should have**.

---

## Phase 0 — Baseline

- [ ] **T0. Stabilise current work**
  Commit the in-progress frontend changes (`chat.html`, browse/liked/messages edits), confirm the test suite is green, and decide whether `catemate.db` should stay tracked in git.
  *Done when:* clean working tree, `uv run pytest -v` passes, app runs.

## Phase 1 — MVP (profile → search → chat, safely)

- [ ] **T1. Security hardening**
  Load `SECRET_KEY` from `.env`; require authentication on every endpoint that exposes user data or acts on behalf of a user; validate inputs (email format, password rules, sensible age ranges, message length/empty content); frontend handles expired/invalid tokens by sending the user to login.
  *Done when:* no secrets in code, unauthenticated calls to protected data are rejected, invalid input returns clear 4xx errors, tests cover these cases.
  *Depends on:* T0.

- [ ] **T2. Hide owner contact information**
  Separate what the public sees about an owner (name, city, bio…) from private data (email, phone, exact coordinates). Owners can opt in to sharing phone/email. Pages that list owners (messages, chat) use only the public view.
  *Done when:* no endpoint returns another owner's email/phone/coordinates unless they opted in; tests prove it.
  *Depends on:* T1.

- [ ] **T3. Owner profile & location**
  Owner can view and edit their own profile (name, bio, messaging preference, contact-sharing choice) and set their location (lat/long, e.g. from browser location or a map pick) at registration and later.
  *Done when:* a logged-in owner has a "My profile" page, can update it, and has coordinates stored for distance search. Seed owners have coordinates.
  *Depends on:* T2.

- [ ] **T4. Complete the cat profile**
  Owner can delete a cat (and its photos); anyone logged in can open a public cat detail page (photos, breed, age, colour, gender, notes, owner's public info and approximate distance). Decide whether cats need an "available for mating" flag so unavailable cats stay out of search.
  *Done when:* full create/edit/delete lifecycle works from `my-cats.html`, and a cat detail page exists and is linkable.
  *Depends on:* T2.

- [ ] **T5. Match search (per cat, within a radius)**
  Owner picks one of their cats; results show only opposite-gender cats, never their own, within a chosen distance, with optional breed / colour / age-range filters combined together, ordered by distance. Replaces the separate city/breed filters on `browse.html`.
  *Done when:* an owner can find suitable nearby mates for a specific cat in the browser; tests cover gender rule, own-cat exclusion, radius and each filter.
  *Depends on:* T3, T4.

- [ ] **T6. Contact the owner from a match**
  From a search result or cat page the owner can start a conversation tied to that cat; a conversations list shows one entry per other owner (with the cat it's about); the chat thread shows history and sends messages; privacy rule failures show a clear message.
  *Done when:* search → cat page → message → reply works end-to-end for two real users.
  *Depends on:* T5.

- [ ] **T7. MVP readiness check**
  End-to-end test of the core journey (register → set location → add cat → search → message → reply), seeds updated so the flow is demoable, README/Postman/CLAUDE.md updated to reflect the new endpoints.
  *Done when:* a new user can complete the whole journey on a fresh seeded DB; docs match the app.
  *Depends on:* T1–T6.

## Phase 2 — Safety (immediately after MVP)

- [ ] **T8. Block users**
  Owner can block another owner; blocked owners can't message them and don't see each other's cats in search; owner can view and undo blocks.
  *Depends on:* T7.

- [ ] **T9. Report users / messages / cat profiles**
  Owner can report a message, owner, or cat profile with a reason; reports are stored for review. Decide how reports are reviewed (simple admin view vs. manual DB review for now).
  *Depends on:* T7.

- [ ] **T10. Owner verification**
  Owners must verify their email (optionally phone) before they can send messages; unverified owners see why and can resend verification.
  *Depends on:* T7. Needs a decision on email-sending provider.

## Phase 3 — Should haves

- [ ] **T11. Saved matching criteria per cat**
  Owner saves preferred criteria (breed, colour, age range, max distance) on each cat; search pre-fills from them.
  *Depends on:* T5.

- [ ] **T12. Recommendations for new matches**
  After login, the owner sees newly added cats that match their saved criteria since their last visit.
  *Depends on:* T11.

- [ ] **T13. Meetup scheduling**
  Inside a conversation, an owner can propose a meetup date/time (and optionally a place); the other owner accepts, declines, or proposes another; both see upcoming meetups.
  *Depends on:* T6.

## Backlog (Nice to have — not planned)
- Support other pet types beyond cats
- Pet hosting by neighbours during travel
- Recommendations for vets, pet shops and facilities nearby
- Pet-lovers community features
- Push notifications / mobile app (from README roadmap)
