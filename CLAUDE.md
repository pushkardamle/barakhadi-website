# CLAUDE.md — Barakhadi website (www.barakhadi.com)

Read this before changing anything. It holds the decisions that aren't obvious from the code.

## What this is

Marketing site for **Barakhadi** (बाराखडी), a Marathi-learning product for kids by **Barakhadi LLC** (Virginia, USA).
The lessons themselves run on **TalentLMS**; this site explains the product, offers free trial activities, and (Phase 2) sells access.
It replaces a WordPress + Elementor site on Cloudways. The owner, **Pushkar Damle**, is the only editor and edits through Claude Code + Git. No CMS.

Background, research and the decision record: `docs/barakhadi-rebuild-assessment.html` and `docs/research/`.

## Stack (decided)

- **Astro 7** (pinned to the 7.3 line) + **Tailwind 4** + `@astrojs/cloudflare` 14.3, deployed as a **Cloudflare Worker with static assets** (not Pages).
- Pages are prerendered (static). Only routes that need a server (contact form now; Stripe checkout/webhook later) opt out with `export const prerender = false`.
- Fonts self-hosted via Astro's Fonts API from Fontsource packages (see `astro.config.mjs`). Nunito for body; Baloo 2 for Devanagari.
- No React or other UI framework yet. Plain `.astro` components and a few lines of vanilla JS where needed (mobile menu, tabs). Add an island only when it earns its weight.
- Images live in `src/assets/` and go through `astro:assets` `<Image>`/`<Picture>`.

## Content rules (owner decisions, 17 Oct 2026)

- Spell it **Barakhadi** in English and **बाराखडी** in Marathi. Never "Barkhadi", never Hindi spellings (बरखड़ी).
- Founder: **Pushkar Damle** (never "Deshpande"). Co-creator: **Deepti Pandit**, Marathi teacher.
- Activity count: **300+**. Three levels: Level 0 शिशु वर्ग, Level 1 पहिली, Level 2 दुसरी. 30 conversation topics.
- Price shown: **$60 per student, per level, per year**. More than one level: discounted price on request ("contact us"). No online checkout until Phase 2, so the CTA is "Contact us to subscribe".
- Only the 3-minute intro video (Wistia `ktanuvwk0f`) is public. The full demo and teacher-training videos were made for one Marathi school: never put them on the site.
- Visual style: flat buttons and badges (no hard drop shadows; the owner doesn't want a Duolingo look). Hover = colour change plus a small lift.
- Activity screenshots don't repeat across the main pages (home hero, home core skills and Who it's for each use different ones); repeats undercut the "300+ activities" claim.
- Colour balance: use the four logo colours roughly equally. Home hero is green; inner page headers are blue or red (`<PageHeader tone>`); orange is reserved for buttons. Accents rotate red / blue / green.
- No small accent labels ("eyebrows") above section headings.
- Contact email: **info@barakhadi.com**. Show it as text; no `mailto:`-only flows.
- Canonical host: **https://www.barakhadi.com** with trailing slashes (`/faq/`, `/contact-us/`), matching the old WordPress URLs.
- Pages are in English with Marathi phrases. `<html lang="en">`; wrap Marathi runs in `lang="mr"`.
- Don't invent claims (user counts, hours practiced, testimonials). Ask the owner.

## TalentLMS facts

- One TalentLMS account: `marathi.talentlms.com`. Schools/classes are **branches** (grandfathered: 255 branches on a Grow plan). Never suggest changing the plan; it would lose the branches.
- Self-learners who sign up on the web go to the **indml** branch: `indml-marathi.talentlms.com`. School students are created manually by the owner.
- Use **API v2** (`/api/v2`, `X-API-Key` + `X-API-Version` headers). API v1 is deprecated.
- Free-trial guest links (live site): `https://marathi.talentlms.com/...` keys `EOSNHRKM`, `EQLNHRKM`, `EGBNHRKM` (see `src/data/site.ts`).

## Security rules

- Secrets go in `wrangler secret put` (prod) and `.dev.vars` (local, git-ignored). Never in code, docs, commits or chat output.
- Stripe webhooks (Phase 2): verify the signature on the raw body before anything else, dedupe on `event.id` in D1, process through a Queue. The old Worker skipped this; see `docs/reference/legacy-barakhadi-subscription.worker.js` for what *not* to do.
- Never collect a learner's password on this site.
- Forms use Cloudflare Turnstile and send through Resend to info@barakhadi.com. Never auto-reply to the address a visitor typed.

## Working conventions

- `npm run dev` for local work, `npm run build` must pass before committing.
- Keep components small and in `src/components/`. Site-wide data (nav, links, contact) in `src/data/site.ts`.
- Colors and fonts come from the tokens in `src/styles/global.css`. Don't hard-code hex values in components.
- Accessibility: visible focus states, AA contrast (white text on bright orange fails; check), alt text on every image, a working mobile menu.
- Old WordPress URLs that change get a 301 in `public/_redirects`; junk WordPress pages return 410.

## Hosting and deploys (live since 2026-10-18)

- Live at https://www.barakhadi.com. The Worker `barakhadi-web` is attached by zone routes `www.barakhadi.com/*` and `barakhadi.com/*` (see `wrangler.jsonc`).
- Cloudflare settings: the DNS records for the apex and www are proxied, Always Use HTTPS is on, and a Redirect Rule sends `barakhadi.com` to `https://www.barakhadi.com` (301).
- Deploy with `npm run build && npx wrangler deploy`. Secrets live in Cloudflare as **Secret** type; `keep_vars` stops deploys from wiping dashboard variables.
- `workers/email-forwarder` is a separate Email Worker: info@ goes to the addresses in `FORWARD_TO`. Deploy it with `npx wrangler deploy --config wrangler.jsonc` from that folder.
- Rollback: set the two DNS records back to "DNS only" while the old Cloudways host still exists.

## Phases

1. **Now:** replace WordPress. Home, Who it's for, Pricing, About, FAQ, Contact, Privacy, Terms. (A "How it works" page was dropped on 2026-10-18; `/videos/` redirects to the home page video.) DNS to Cloudflare.
2. Stripe checkout (subscriptions, one-time, trials, school seats) → TalentLMS v2 provisioning into the indml branch.
3. `learn.barakhadi.com` custom domain for TalentLMS + one-click login links.
4. Accounts / teacher extras, only if branches don't already cover the need.
