# 🟢 CURRENT STATE — 2026-06-18 (PM)  ·  HEAD `e4b3f02`

> Newest-on-top. Everything below the `---` rule is prior state, preserved
> as historical record. Read this section first.

**Tree clean, all pushed. 4 fixes shipped this session (A/B/C/D), all VERIFIED
LIVE on pages.dev.** Came in for the trailing-slash fix; verify-don't-assume
caught two pre-existing bugs (infinite redirect loop + sitewide soft-404) and
fixed both.

## Commits this session (on top of f18791f)
| Job | Commit | Fix |
| --- | --- | --- |
| A | `21c87d2` | Canonical + og:url → trailing slash, centralized in BaseHead (1-line, file-ext guard). Fixed all 37 hardcoded no-slash literals; no-op for the 36 correct pages. |
| B | `b85b3df` | All 292 `_redirects` targets slashed → killed 2-hop chains (single hop now). Lyft redirect confirmed single-hop live. |
| C | `8af7053` | Removed 5 self-referential redirect rules (`/blog/`, `/contact/`, `/faq/`, `/careers/`, `/privacy-policy/` → each redirected to itself) causing INFINITE LOOPS. `/blog/` + `/contact/` shadowed real built pages → were UNREACHABLE. Un-shadowed; ~65 inbound `/blog/` redirects now resolve. |
| D | `e4b3f02` | Added `src/pages/404.astro` (was missing entirely) → fixed sitewide SOFT-404 (no 404 page meant homepage served at HTTP 200 for every bad URL). noindex=true, on-brand. Real 404 status confirmed live. |

## Patterns established this session (reuse)
- **Canonical is centralized in `BaseHead.astro`** — one place emits the
  canonical + og:url, normalized to trailing slash w/ file-extension guard.
  Pages passing NO canonical prop fall back to pathname (correct slash).
  DO NOT re-add per-page hardcoded canonical literals.
- **`_redirects` edits:** transform to TEMP file → diff old-vs-new to prove
  ONLY the intended change → apply. Preserve column whitespace (perl/sed, NOT
  `awk OFS="\t"` which collapses alignment). Verify dist/_redirects == source
  after build.
- **Verify against pages.dev, NOT apex.** Apex `ericblanklaw.com` still serves
  OLD WordPress (X-Powered-By: PHP). New build is pages.dev-only until cutover.
- **Cloudflare edge propagates mid-probe** — re-run live checks after ~1-2 min
  before concluding (saw 200 then 404 on the same URL seconds apart this session).

## New open item from this session
- **8 missing redirect targets now return clean 404s** (were soft-404
  homepage-200 pre-D): `/attorneys` + 3 bios (`/eric-blank`,
  `/robert-hernandez`, `/fikisha-miller`), `/faq`, `/careers`,
  `/privacy-policy`, `/terms-of-use`. 13 redirect lines feed these. Correct
  behavior, but these legacy URLs hit a 404 until the pages exist.
  **`/privacy-policy` + `/terms-of-use` likely pre-launch must-haves — raise
  with Eric.** Attorney bios gated on the bio-page decision.
- **404 self-canonicalizes to `/404/`** (BaseHead emits canonical
  unconditionally). Benign on a noindex page. Optional future JOB D-2: make
  BaseHead canonical conditional. Low priority.

## Still open (carried, unchanged)
- Attorney bio-page decision (ClickUp `86ba711eu`) — unblocks
  `/our-firm/eric-r-blank/` body links (AboutEric.astro:81, about.astro:29),
  `attorneyNode.url`, and Wave 2 schema rollout.
- Custom-domain cutover — apex still WordPress; handle Cloudflare-side, NEVER
  add noindex/Disallow in-repo (would ship to prod).
- Rich Results validation (pending redeploy).
- criminal-law priceRange call (ClickUp `86bafjx5c`) — Eric's judgment.
- Phase 4 leftovers: Wave 2 `attorneyNode` rollout (~30 pages), title/meta
  verification, OG tags + og-default.jpg recon, blog in nav, Adobe Stock heroes.

## Key IDs (current)
- HEAD `e4b3f02` | session commits `21c87d2`, `b85b3df`, `8af7053`, `e4b3f02`
- Notion parent `36fc0431-1626-8131-9050-ebee84fda8b9`
  | this session log `383c0431-1626-8130-9c0f-eb8005d98cc9`
- ClickUp: Phase 4 `86baf0x59` | Phase 5 Redirect Map `86baf0x9v`
  | Pre-Cutover Gate `86baf0xf1` | criminal-law priceRange `86bafjx5c`
  | bios/broken-link `86ba711eu`

---

# HANDOFF — Phase 4 SEO Parity (firmNode rollout + Wave 2 attorney consolidation COMPLETE)

**Last updated:** 2026-06-17, end of session. **HEAD at this write:** c69d30e.

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
- ✅ ALL 20 practice-area pages wired to firmNode. Waves 1–4 (0eb591d, 43f7284,
  85f499c, fb77bf2) covered only 19 — wrongful-death.astro silently slipped through
  ALL four waves and kept shipping duplicated inline NAP. The "20/20" claimed at
  fb77bf2 was actually 19/20. Discovered during Wave 2 (its missing firmNode import
  surfaced when the attorney swap failed); backfilled in 4dbbde3 (firmNode wiring +
  attorney consolidation, body-copy diff verified empty). NOW genuinely 20/20.
- ✅ ALL 10 LP pages wired (canary las-vegas-car-accident 1de1928 + batch of 9 8c3b454).
  LPs were uniform — no FAQPage, standard Lightbox import anchor, priceRange on all 10.
- ✅ homepage (index.astro) wired (e914362). SPECIAL CASE done: replaced its inline
  canonical #legalservice + #attorney nodes with `{ ...firmNode, description }` and
  `{ ...attorneyNode, description: "..." }`. Stale schema Attorney.url 404 dropped.
  index.astro is now the FIRST and ONLY consumer of attorneyNode.

**firmNode rollout = 31/31 pages COMPLETE.** firm.ts is the single source of truth
for the firm NAP. The duplicated inline NAP that started this batch is gone.

## Wave 2 — COMPLETE (30/30)
- ✅ Attorney node consolidated across all 30 remaining pages. Every page now sources
  #attorney from shared attorneyNode (car-accidents canary 603a418, batch of 27 18e1b3a,
  wrongful-death 4dbbde3, criminal-law c69d30e). firm.ts is now single source of truth
  for BOTH firm (#legalservice) AND attorney (#attorney) across all 31 schema pages.
  All inline attorney nodes gone. Each page GAINED worksFor → #legalservice (the inline
  nodes lacked it — lossless + additive).
- criminal-law jobTitle was NOT auto-corrected to "Personal Injury Attorney". DELIBERATE
  DECISION to keep generic "Attorney" via `{ ...attorneyNode, jobTitle: "Attorney" }` —
  "Personal Injury Attorney" is inaccurate schema labeling on a criminal-defense page
  (NRPC 7.1 — every page is a separate advertisement). criminal-law now has TWO
  deliberate per-page overrides: no priceRange + jobTitle "Attorney".

## Still open
- ⬜ BROKEN BODY LINKS (distinct from the schema fix): two live user-facing links to
  /our-firm/eric-r-blank/ still 404 — AboutEric.astro:81 (homepage CTA button) and
  about.astro:29 (bioUrl). GATED on the bio-page decision: when the real
  /attorneys/eric-r-blank page exists (alongside Miller/Hernandez bios), fix both links
  AND add url to attorneyNode in one pass — they all resolve together. Don't guess a
  destination (e.g. /about) before that decision.
- ⬜ VALIDATE in Google Rich Results Test once Cloudflare redeploys: LegalService on a
  couple practice + LP URLs, Article+Breadcrumb on a couple blog URLs.
- ✅ RESOLVED: 2 untracked logos deleted. ERB_Logo_W.png was a byte-identical dup of
  tracked Eric_Blank_Injury_Attorneys_Logo_White.png (still in use); ebl-logo.png was
  a unique unused orphan (no refs, no intent signal). Both removed; tree clean.

## Outlier files (learned during rollout)
- criminal-law.astro + sexual-assault.astro: imports stop at ContactForm (no Lightbox
  import) — firmNode import goes after ContactForm, not Lightbox.
- criminal-law #service node has NO priceRange (correct — criminal defense isn't
  contingency; a contingency claim there is false). Keep it priceRange-free.
- criminal-law Attorney node deliberately keeps jobTitle "Attorney" (NOT the canonical
  "Personal Injury Attorney") via spread override. This is intentional, not drift — do
  not "fix" it to match the shared node.

## Flagged for Eric (logged in ClickUp task 86bafjx5c)
- criminal-law: the shared firm node still renders priceRange "Contingency Fee…" on
  that page (it's the firm-wide node). Service node is clean; firm node isn't.
  Bar-advertising judgment call — Eric to decide if firm-level contingency language is
  OK on the criminal page or if priceRange should leave the shared node entirely.

## Standing rules
Recon read-only before edits. One change at a time, explicit filenames, no `git add .`,
git status before+after, build before push, push every commit.
