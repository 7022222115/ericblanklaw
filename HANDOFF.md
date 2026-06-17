# HANDOFF — Phase 4 SEO Parity, Batch C (firmNode rollout COMPLETE)

**Last updated:** 2026-06-17, end of session. **HEAD at this write:** e914362.

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
- Homepage attorney: kept its description via `{ ...attorneyNode, description: "..." }`;
  dropped the stale url by omission (killed the schema 404).
- Attorney consolidation = WAVE 2, deliberately deferred (see below).

## Progress
- ✅ firm.ts created + committed (e6429bb).
- ✅ ALL 20 practice-area pages wired to firmNode (Waves 1–4: 0eb591d, 43f7284,
  85f499c, fb77bf2). ~200 lines of duplicated NAP removed.
- ✅ ALL 10 LP pages wired (canary las-vegas-car-accident 1de1928 + batch of 9 8c3b454).
  LPs were uniform — no FAQPage, standard Lightbox import anchor, priceRange on all 10.
- ✅ homepage (index.astro) wired (e914362). SPECIAL CASE done: replaced its inline
  canonical #legalservice + #attorney nodes with `{ ...firmNode, description }` and
  `{ ...attorneyNode, description: "..." }`. Stale schema Attorney.url 404 dropped.
  index.astro is now the FIRST and ONLY consumer of attorneyNode.

**firmNode rollout = 31/31 pages COMPLETE.** firm.ts is the single source of truth
for the firm NAP. The duplicated inline NAP that started this batch is gone.

## Still open
- ⬜ WAVE 2: consolidate the Attorney node across the other 30 pages (practice + LP).
  They still re-declare #attorney inline; only homepage uses attorneyNode so far.
  Replace inline copies with imported attorneyNode. Also auto-fixes criminal-law's
  jobTitle drift ("Attorney" vs "Personal Injury Attorney").
- ⬜ BROKEN BODY LINKS (distinct from the schema fix): two live user-facing links to
  /our-firm/eric-r-blank/ still 404 — AboutEric.astro:81 (homepage CTA button) and
  about.astro:29 (bioUrl). GATED on the bio-page decision: when the real
  /attorneys/eric-r-blank page exists (alongside Miller/Hernandez bios), fix both links
  AND add url to attorneyNode in one pass — they all resolve together. Don't guess a
  destination (e.g. /about) before that decision.
- ⬜ VALIDATE in Google Rich Results Test once Cloudflare redeploys: LegalService on a
  couple practice + LP URLs, Article+Breadcrumb on a couple blog URLs.

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

## Standing rules
Recon read-only before edits. One change at a time, explicit filenames, no `git add .`,
git status before+after, build before push, push every commit.
