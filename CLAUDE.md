# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Rebuild of **ericblanklaw.com** — the website for **Eric Blank Injury Attorneys**, a Las Vegas personal injury law firm.

The current production site runs on WordPress / GreenGeeks (slow, dated). This repo is the replacement: a faster, better-looking site. **Hard requirement: ZERO loss of SEO rankings or content** during the migration.

Currently a freshly scaffolded Astro "minimal" starter — `src/pages/index.astro` is still placeholder boilerplate, so most real pages, layouts, and components have yet to be built.

## Stack

- **Astro** — site framework (already installed)
- **Tailwind CSS** — styling. NOT installed yet; add it when styling work begins (`npm run astro -- add tailwind`).
- **Cloudflare Pages** — hosting/deploy target. No adapter configured yet.

## Commands

- `npm run dev` — start the dev server at `localhost:4321`
- `npm run build` — build the production site to `./dist/`
- `npm run preview` — preview the production build locally
- `npm run astro -- --help` — run Astro CLI commands (e.g. `astro add`, `astro check`)

There is no test or lint script. Type checking comes from `astro check` (run via `npm run astro -- check`).

Requires Node >= 22.12.0.

## Architecture

Standard Astro file-based routing: files in `src/pages/` become routes by filename. Static assets (including the firm logos in `public/`) are served from `public/` at the site root.

TypeScript is configured in strict mode (`tsconfig.json` extends `astro/tsconfigs/strict`).

`astro.config.mjs` is currently empty (`defineConfig({})`) — no integrations, adapter, or output mode set yet.

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
