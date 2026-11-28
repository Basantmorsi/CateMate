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

- [x] **T3. Owner profile & location** — done 2026-11-28
  Owner can view and edit their own profile (name, gender, age, city, phone, bio, messaging preference) and set an approximate location on a map (Leaflet + OpenStreetMap) at registration and later. Owners who don't pick a spot get their city's centre stored as their coordinates. Also added: change password.
  *Done:* `PATCH /owners/me`, `POST /owners/me/password`, city latitude/longitude, coordinates rounded to 2 decimals (~1 km), `profile.html` and `register.html` with the map picker, seed owners and the migrated `catemate.db` have coordinates, tests in `tests/test_owners.py`.
  *Moved to T2:* the contact-sharing choice (opt-in to share phone/email) is not part of this task and is still open.
  *Depends on:* T2 (built ahead of it by choice).

- [x] **T3.1. Show cat photos on My Cats** — done 2026-11-28
  Found while testing T3: every card on `my-cats.html` showed "View photos" even with no photos, and an uploaded photo never appeared on the card. Cards now show the first photo as a cover (default cat image when there is none) with a photo-count chip, "View photos" only appears when the cat has photos ("Add photos" otherwise), and the card updates right after an upload or delete. Frontend only, same pattern as `browse.html` and `liked.html`.
  *Related:* the photo and delete parts of T4 (delete a cat with its photos) are still open.

- [ ] **T4. Complete the cat profile**
  Owner can delete a cat (and its photos); anyone logged in can open a public cat detail page (photos, breed, age, colour, gender, notes, owner's public info and approximate distance). Decide whether cats need an "available for mating" flag so unavailable cats stay out of search.
  *Done when:* full create/edit/delete lifecycle works from `my-cats.html`, and a cat detail page exists and is linkable.
  *Depends on:* T2.
  *Progress:* editing a cat is done (T4.1). Delete a cat (with its photos), the public cat detail page and the availability flag are still open.

- [x] **T4.1. Edit a cat** — done 2026-11-28
  Each cat card on `my-cats.html` has an Edit button, and the cat's detail dialog has one too. Both open a form (name, age, breed, gender, colour, notes) with Save/Cancel, using the existing `PATCH /cats/{id}`. The card updates right after saving. Frontend only.

- [x] **T4.2. Browse page improvements** — done 2026-11-28
  Browse got `GET /cats/search`: city, breed, gender, colour (dropdown from `GET /cats/colors`) and an age range all combine, plus a "Hide my cats" switch for logged-in owners. Each cat shows its city and an approximate distance ("about N km away") when the visitor is logged in; the server computes it and never returns coordinates, email or phone. Clicking a card opens a cat detail dialog (photos, details, owner name, city, distance, Like and Message). Order is newest cat first, and your own cats have no "Message owner" button.
  *Still open for T5:* pick one of my cats and match against opposite-gender cats only, a distance radius filter and ordering by distance. The old `/cats/all`, `/cats/city/{id}` and `/cats/breed/{id}` endpoints are still there but Browse no longer uses them.

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

## Follow-ups found while building (small, can be done any time)

- [ ] **F1. Validate cat input in the API**
  `POST` and `PATCH /cats` accept an empty name or colour and a negative age (demo cat "Miau" has age -2). Add limits (non-empty name and colour, age 0–40, notes length) in `CatCreate` / `CatUpdate` and tests. Overlaps T1's input validation; do it there if T1 comes first.

- [ ] **F2. Retire the old cat list endpoints**
  Browse now uses `GET /cats/search`, so `/cats/all`, `/cats/city/{id}` and `/cats/breed/{id}` are unused by the frontend. Remove them with their tests, and update the README endpoint table and the Postman collection (both still list `/cats/city/{id}` and `/cats/breed/{id}`, and neither mentions `/cats/search` or `/cats/colors`).

- [ ] **F3. Share the photo-loading code between pages**
  `browse.html`, `liked.html` and `my-cats.html` each have their own copy of fetching a cat's photos, `hasPhotos` and `catCover`. Move them into `shared.js` now that there are three copies.

- [ ] **F4. Clean up the demo data**
  Some seeded or hand-edited records look wrong (cat age -2, an owner in Munich whose saved pin is about 5,400 km away, cat renamed "Miloooooo"). Fix them in the seeds and the local DB, and document how to reseed a fresh database.

## Backlog (Nice to have — not planned)
- Support other pet types beyond cats
- Pet hosting by neighbours during travel
- Recommendations for vets, pet shops and facilities nearby
- Pet-lovers community features
- Push notifications / mobile app (from README roadmap)
