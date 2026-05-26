# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Rebuild of **ericblanklaw.com** — the website for **Eric Blank Injury Attorneys**, a Las Vegas personal injury law firm. Replaces the firm's old WordPress / GreenGeeks site with a faster, modern build. **Hard requirement: ZERO loss of SEO rankings or content** during the migration.

The v1 site is built and deployed. Current routes (8): `/` (home), `/about`, `/practice-areas`, `/results`, `/reviews`, `/contact`, `/thank-you` (form-success page, `noindex`), and `/practice-areas/car-accidents` (first practice-area detail page — see the Practice Area Page Template below; 11 more to build).

## Stack

- **Astro v6.3.6** — static site framework.
- **Tailwind CSS v4** — installed via the `@tailwindcss/vite` plugin (no `tailwind.config.js`; theme tokens live in `src/styles/global.css` via `@theme`).
- **@astrojs/sitemap** — generates `sitemap-index.xml` / `sitemap-0.xml` at build (`/thank-you` filtered out).
- **lucide-static** — icons, imported as inline SVG via `lucide-static/icons/*.svg?raw`.
- **Cloudflare Pages** — hosting. Auto-deploys on every push to `main` (`github.com/7022222115/ericblanklaw`).

## Commands

- `npm run dev` — start the dev server at `localhost:4321`
- `npm run build` — build the production site to `./dist/`
- `npm run preview` — preview the production build locally
- `npm run astro -- --help` — run Astro CLI commands (e.g. `astro add`, `astro check`)

There is no test or lint script. Type checking comes from `astro check` (run via `npm run astro -- check`).

Requires Node >= 22.12.0.

## Architecture

Standard Astro file-based routing — files in `src/pages/` become routes. Each page composes the `<html>/<head>/<body>` shell directly and imports shared components; there is no `Layout.astro`.

**Shared components** (`src/components/`): `BaseHead` (all `<head>` meta — title/description/canonical/OG/Twitter/robots, with a `noindex` prop), `Header` (sticky nav + mobile menu), `Footer`, `ContactForm` (Formspree-wired call-back form), `Contact` (homepage contact section, wraps `ContactForm`), `PracticeAreaGrid` (12-area card grid), `Badges`, `Testimonials` — plus the homepage sections (`Hero`, `BetterValues`, `PracticeAreas`, `AboutEric`, `Results`, `MidPageCTA`).

The contact form posts to **Formspree** (`https://formspree.io/f/xjgzyjvz`) and redirects to `/thank-you`. Static assets (logos, badges, photos, map, `robots.txt`) live in `public/`. TypeScript is in strict mode (`tsconfig.json` extends `astro/tsconfigs/strict`).

## Brand (v1 — current launch)

- **Firm name:** Eric Blank Injury Attorneys
- **Tagline:** "Better Representation. Better Recovery. It's Better With Blank."
- **Primary color:** `#0F1E3D` (deep navy)
- **Accent color:** `#E8B842` (warm gold) — use sparingly
- **Phone:** (702) 222-2115
- **Address:** 7860 W Sahara Ave Ste. 110, Las Vegas, NV 89117
- **Hours:** Open 24/7
- **Logo — header:** `/public/Eric_Blank_Injury_Attorneys_Logo.png` (black text — for light backgrounds)
- **Logo — footer:** `/public/Eric_Blank_Injury_Attorneys_Logo_White.png` (white text — for the dark navy footer)

## Roadmap

- **v1 (now):** Fast, clean launch using the current brand. Astro + Tailwind. Deploy to Cloudflare Pages at a **temporary URL**. Do NOT touch the live domain — GreenGeeks stays in production until cutover.
- **v2 (later):** Full redesign coming from Claude Design. Same Astro framework, new visual treatment.

## Migration notes (SEO-critical)

- All blog/article URLs from the old WordPress site MUST be preserved **exactly** when content is migrated.
- Build a **redirect map** before going live.
- All copy gets a rewrite/improvement pass — the user provides ideas, Claude writes.

## Working preferences (CRITICAL)

- Take the **simplest path**. No over-engineering, don't complicate things.
- **Present options before recommending** one.
- **Don't assume anything is installed** — ask first.
- Be clear, precise, and step-by-step.

## Practice Area Page Template

`src/pages/practice-areas/car-accidents.astro` is the template for all 12 practice-area pages.
URL pattern: `/practice-areas/[slug]` (file: `src/pages/practice-areas/[slug].astro` — note the
`practice-areas/` directory coexists with the `practice-areas.astro` index page).

### 9-section structure (in order)

1. **Hero** — navy. Eyebrow, `<h1>`, lead paragraph, two CTAs (gold "Free Case Review" → `#contact`, outlined phone CTA), small trust strip.
2. **Trust strip** — white, `border-b`, compact (~`py-10`). 4 stats — big gold value, navy label.
3. **First Steps** — white. "What to do after a [X] in Las Vegas" — 6 numbered steps (`<ol>`), each icon + title + 2-3 sentences.
4. **How We Help** — gray-50. 4 cards (Investigate / Build medical record / Negotiate / Try the case) — largely reusable across all areas.
5. **Damages** — white. "What [X] victims can recover in Nevada" — 2 cards (Economic / Non-Economic icon-bullet lists) + caps note.
6. **Nevada Law** — gray-50. 3 cards (Statute of Limitations, Comparative Negligence, Insurance Minimums) + disclaimer. SOL = 2 yrs (NRS 11.190) and the 51% comparative-negligence rule are constant for all auto/PI cases.
7. **FAQ** — white, `max-w-3xl`. 6 Q&A pairs, all expanded (`<h3>` question + `<p>` answer). Must match the FAQPage JSON-LD.
8. **Featured testimonial** — gray-50. One large centered quote + "Read more client reviews →" → `/reviews`.
9. **Final CTA + form** — navy, `id="contact"`, `scroll-mt-24`. "Why Call Now" 3 bullets + `<ContactForm />`; lead references the practice area.

### Shared components reused

`BaseHead`, `Header`, `Footer`, `ContactForm`. The page composes the `<html>/<head>/<body>` shell directly (no `Layout.astro`). Lucide icons imported via `lucide-static/icons/*.svg?raw`.

### Per-page data to fill in (checklist for each new page)

- [ ] Slug + file `src/pages/practice-areas/[slug].astro`
- [ ] Source WordPress URL — WebFetch it first for any substantive content
- [ ] BaseHead — title, description, canonical (`https://ericblanklaw.com/practice-areas/[slug]`)
- [ ] Hero — eyebrow, `<h1>`, lead paragraph (confident, Vegas-specific, no invented statistics)
- [ ] Section 2 stats — adjust labels to the practice area
- [ ] Section 3 — adapt the 6 steps to the accident type
- [ ] Section 5 — damages lists (usually reusable; tweak if the area differs)
- [ ] Section 6 — SOL / comparative negligence stay constant; swap in area-specific law where relevant (e.g. dog-bite strict liability, premises liability)
- [ ] Section 7 — 6 FAQ Q&A pairs
- [ ] Section 8 — pick a relevant existing client testimonial
- [ ] Section 9 — one lead sentence referencing the practice area
- [ ] JSON-LD — `serviceType` string + FAQPage built from the FAQ array

### Rules

- All body links are **internal** (`/contact`, `/reviews`, `/practice-areas`, `#contact`) — never old WordPress URLs.
- Include 2-3 contextual internal links in the body copy.
- Don't invent statistics — keep claims qualitative unless verified.
- FAQ JSON-LD answer text must match the visible on-page answers (required for rich results).

### Practice-area grid link switchover

The `PracticeAreaGrid` component (`src/components/PracticeAreaGrid.astro`) is the single source of truth for the 12-area card grid (rendered on the homepage via `PracticeAreas.astro` and on `/practice-areas`). All 12 cards now link to internal `/practice-areas/[slug]` pages — no WordPress URLs remain in the grid.

- [x] Rideshare (Uber/Lyft) → `/practice-areas/rideshare-accidents` ✓ (Batch 2B)
- [x] Workers' Compensation → `/practice-areas/workers-compensation` ✓ (Batch 2B)
- [x] Wrongful Death → `/practice-areas/wrongful-death` ✓ (Batch 2B)

No card should be left pointing at a WordPress URL once its internal page is live — that's a redirect-leak that costs SEO equity and breaks the migration plan.

## Pre-Launch Legal Review Checklist

**A firm attorney must review and sign off on every Nevada Law section and every FAQ section across every practice-area page before DNS cutover to the live domain.** This is a law firm; the published statutory and procedural claims need a Nevada-licensed attorney's eyes before they go live.

Open items flagged during page builds (verify the current statute text and apply firm preference for citation style):

- [ ] **Motorcycle / Pedestrian — additional-penalty cross-references.** Pedestrian page references "additional penalties apply when a driver causes a pedestrian collision" (NRS 484B.283, with the penalty mechanism in NRS 484B.653 subsec. 4). If the firm wants the cross-reference cited on-page, confirm both statute numbers and subsection numbers are current. Same review applies to any future motorcycle-page reference to driver-duty statutes.
- [ ] **Pedestrian — UM/UIM applicability when struck as a pedestrian.** The pedestrian FAQ states UM/UIM on the injured person's own auto policy "can apply even though you weren't in a car." This is generally true in Nevada but is fact- and policy-specific. Confirm the firm is comfortable with the wording as marketing language.
- [ ] **Bicycle — helmet-law phrasing.** Page deliberately avoids a positive claim that "Nevada does not require adult cyclists to wear helmets." Decide whether to (a) leave the cautious phrasing as-is or (b) add an explicit confirmation that there is no statewide adult bicycle helmet law (noting any Clark County / municipal ordinances if applicable).
- [ ] **Truck — FMCSA insurance minimums.** Page cites federal minimums of $750,000 (general freight), $1,000,000 (oil), and $5,000,000 (certain hazmat) under 49 CFR §387. Confirm these dollar figures are current and that the firm is comfortable citing them as marketing copy.
- [ ] **NRS 11.190 SoL exceptions.** All four new pages cite "2 years from the date of the accident" as the personal-injury statute of limitations. Confirm the firm is comfortable with the exceptions currently flagged in FAQ copy (claims against government entities have shorter notice periods under NRS 41.036; minors get tolling; wrongful-death is a separate statutory scheme) and decide whether any additional exception language should be added page-by-page.

### Batch 2A items (slip-and-fall, dog-bites, casino-injuries, brain-and-spine-injury)

- [ ] **Dog bites — Nevada negligence framework (HIGHEST RISK in this batch).** Page positions Nevada as "not a strict-liability state" for dog bites and frames liability around (a) the owner's knowledge of dangerous propensity (one-bite), (b) negligence, and (c) violations of local leash/animal-control ordinances. References NRS 202.500 for dangerous/vicious-dog classifications and Clark County Title 10 for the local animal code. Confirm the firm is comfortable with each of these characterizations as marketing copy — including specifically the "one-bite" framing, the negligence-per-se theory built on leash-law violations, and the statement that Nevada has no broad strict-liability dog-bite statute. Verify the cited statute and code references are current and apply to the geographies the firm serves.
- [ ] **Dog bites — Clark County Title 10 reference.** Page mentions "Clark County's Title 10 animal code" generally without citing a specific section. If the firm prefers a more specific citation (e.g., 10.36.040 leash provision or 10.16 dangerous-animal ordinance), update accordingly and confirm those section numbers are current.
- [ ] **Slip and fall — duty of care by visitor status (invitee / licensee / trespasser).** Page summarizes Nevada's traditional premises-liability framework around invitee/licensee/trespasser categories and notice (actual + constructive). Confirm this framing matches the firm's preferred Nevada case-law citations and the current state of Nevada premises liability doctrine.
- [ ] **Casino injuries — "highest duty of care to business invitees" language.** Page asserts that Nevada casinos/resorts owe their "highest duty of care" to invitees. This tracks standard premises-liability articulation, but the precise duty owed by Nevada casinos/hotels under controlling case law should be confirmed (the firm may prefer a more measured phrasing).
- [ ] **Casino injuries — over-service / dram-shop framing.** FAQ touches on casinos and bars having "duties around serving guests." Nevada has historically been a limited-dram-shop state (NRS 41.1305 generally limits liability for furnishing alcohol to adults), so the firm should confirm the on-page wording is acceptable or have it tightened.
- [ ] **Brain & spine — "cause determines the framework" language.** Page tells visitors that the liability framework depends on how the injury occurred (crash, fall, premises, assault, workplace). Confirm the firm is comfortable with this as general marketing language and with the workers' comp / third-party coordination FAQ answer in particular.
- [ ] **Brain & spine — Nevada damages caps note.** Page repeats the standard "Nevada caps damages in medical malpractice cases but not in general personal injury claims" line that's used on every practice-area page. For catastrophic-injury cases that originate from a med-mal event, the caps DO apply. Decide whether this page should carry a more nuanced caps note.

### Batch 2B items (rideshare, workers-compensation, wrongful-death)

- [ ] **Workers' compensation — every line of statutory framework (HIGHEST RISK in this batch).** The page departs further from the auto-PI template than any other and asserts: (a) no-fault — no proof of employer negligence required; (b) Form C-1 (Notice of Injury / Occupational Disease) within 7 days; (c) Form C-4 (Employee's Claim for Compensation) within 90 days; (d) benefits limited to medical, TTD, TPD, PPD, PTD, vocational rehab, death benefits; (e) NO pain-and-suffering recovery under comp alone; (f) third-party PI claims may exist alongside comp; (g) multi-step appeal (hearings officer → appeals officer → district court). Confirm every one of these statements against the current text of NRS 616A–616D and 617 — these deadlines and forms can be amended by the Legislature, and a misstatement on a comp page is professionally dangerous.
- [ ] **Workers' compensation — authorized-provider rule wording.** Page tells injured workers that treatment "generally has to be from an authorized provider — your employer's or insurer's panel." Confirm the firm is comfortable with this characterization (it's accurate as a general rule but the precise mechanics are nuanced).
- [ ] **Workers' compensation — TTD "two-thirds of wage" reference.** Page says TTD "generally replaces about two-thirds of wage" (the 66 2/3% figure widely reported). Confirm this remains accurate for the relevant wage base and reflects any 2025–2026 changes.
- [ ] **Rideshare — Uber/Lyft coverage tier figures.** Page cites "$50,000 per person / $100,000 per accident / $25,000 property damage" in Period 2 (app on, waiting) and "$1,000,000" in Period 3 (ride accepted through drop-off). Confirm these dollar figures are current and that the page's parenthetical reference to "Nevada law currently sets the rideshare company's per-incident liability at $1,000,000" reflects the post–Oct 1, 2025 AB 523 regime correctly.
- [ ] **Rideshare — "the same general structure applies to Lyft" wording.** Page repeatedly states Uber and Lyft tier structures are comparable. Confirm the firm is comfortable with this generalization for marketing purposes, or have it tightened.
- [ ] **Wrongful death — NRS 41.085 damages split (HIGHEST RISK — sensitive content).** Page divides recovery between heirs (grief, sorrow, loss of probable support, companionship, consortium, decedent's pre-death pain/suffering/disfigurement) and the estate / personal representative (medical expenses, funeral/burial, other special damages, lost earnings). Confirm this split tracks the current text of NRS 41.085. Particularly verify the heirs vs. personal-representative pain-and-suffering allocation, since wrongful-death and survival-action damages are easy to mix up and this is the most sensitive page on the site.
- [ ] **Wrongful death — definition of "heir."** Page describes "heirs" as "the people who would inherit the decedent's separate property under Nevada intestate succession law — most often a spouse and children, and in some cases parents or other family members." Confirm this lay summary is acceptable to the firm, since the precise category list under NRS 41.085 / intestate succession can be more nuanced than "spouse and children."
- [ ] **Wrongful death — 2 years from date of death.** Page cites the SoL as "generally 2 years from the date of death" under NRS 11.190. Confirm this remains correct (the wrongful-death SoL has historically run from death, but the firm should verify against the current statute and any 2025–2026 amendments).
- [ ] **Wrongful death — tone and CTAs.** Page deliberately softens the standard hero CTA ("Speak With Our Team" instead of "Free Case Review") and the final-section heading ("When You're Ready To Talk, We're Here"). Confirm the softened tone is acceptable to the firm — including the trust strip ("No Fees Unless We Recover") and the "What To Expect / A Conversation, Not A Sales Pitch" framing.
