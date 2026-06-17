# HANDOFF — Phase 4 SEO Parity, Batch C (in progress)

**Last updated:** 2026-06-17, mid-Batch-C. **HEAD at this write:** fb77bf2.

## What Batch C is
Killing the 31× duplicated firm NAP in the JSON-LD @graph. Created ONE shared
data module — `src/data/firm.ts` — exporting `firmNode` (@id `https://ericblanklaw.com/#legalservice`)
and `attorneyNode` (@id `https://ericblanklaw.com/#attorney`). Every page imports the
shared node into its @graph instead of re-declaring the NAP inline.

Pattern: import `firmNode`, put it FIRST in the @graph, then slim the page's own
page-scoped `#service` LegalService node — remove inline telephone/address/areaServed,
add `provider: { "@id": "https://ericblanklaw.com/#legalservice" }`, keep the page's
own name/serviceType/url/image/(priceRange)/employee + its own `#service` @id.

## Decisions locked
- Option 1: full firm node on every page, all sharing one @id (self-valid per page,
  no dangling cross-doc refs — correct for a static site). Source = one TS module.
- @type stays LegalService. Shared node = the homepage's RICHER node (email, geo,
  hours, 5 sameAs, 8-entry areaServed). firmNode omits per-page `description`.
- attorneyNode has NO url (the /attorneys/eric-r-blank bio doesn't exist yet — a url
  would be a sitewide 404 in schema). TODO comment is in firm.ts. Tracked in ClickUp.
- Attorney consolidation = WAVE 2, deliberately deferred (see below).

## Progress
- ✅ firm.ts created + committed (e6429bb).
- ✅ ALL 20 practice-area pages wired to firmNode (Waves 1–4: 0eb591d, 43f7284,
  85f499c, fb77bf2). ~200 lines of duplicated NAP removed.
- ⬜ 10 LP pages (src/pages/lp/) — NOT done. Need a Step-A shape check FIRST: their
  @graph differs (no FAQPage, different line offsets, possibly non-standard import
  blocks). Do not assume practice-page anchors transfer.
- ⬜ homepage (index.astro) — NOT done. SPECIAL CASE: it already defines the canonical
  #legalservice + #attorney inline. Wiring = REPLACE inline nodes with firmNode/
  attorneyNode imports (not slim). Use `{ ...firmNode, description }` so the homepage
  keeps its page-level description on the firm node. Fix the stale
  Attorney.url → /our-firm/eric-r-blank/ (404) here too.
- ⬜ WAVE 2 (after firm rollout): consolidate the Attorney node. It's currently
  re-declared inline on every page with @id #attorney. Replace inline copies with
  imported attorneyNode. This also auto-fixes criminal-law's jobTitle drift
  ("Attorney" vs "Personal Injury Attorney").

## Outlier files (learned during rollout)
- criminal-law.astro + sexual-assault.astro: imports stop at ContactForm (no Lightbox
  import) — firmNode import goes after ContactForm, not Lightbox.
- criminal-law #service node has NO priceRange (correct — criminal defense isn't
  contingency; a contingency claim there is false). Keep it priceRange-free.

## Flagged for Eric (logged in ClickUp task 86bafjx5c)
- criminal-law: the shared firm node still renders priceRange "Contingency Fee…" on
  that page (it's the firm-wide node). Service node is clean; firm node isn't.
  Bar-advertising judgment call — Eric to decide if firm-level contingency language is
  OK on the criminal page or if priceRange should leave the shared node entirely.

## After Batch C
Validate in Google Rich Results Test: LegalService on a couple practice URLs,
Article+Breadcrumb on a couple blog URLs, once Cloudflare redeploys.

## Standing rules
Recon read-only before edits. One change at a time, explicit filenames, no `git add .`,
git status before+after, build before push, push every commit.
