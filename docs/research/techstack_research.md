# Barakhadi.com rebuild: tech-stack research (October 2026)

Research date: 2026-10-17. I checked every version number, price and policy below against a live source this month (see the source list at the end). Where sources disagreed, or only third-party sources were available, the text says so.

---

## 1. TL;DR recommendation

**Use Option A: Astro 7 on Cloudflare Workers (with static assets), plus Stripe Checkout and the Customer Portal, plus a webhook pipeline built on D1 and Queues (or Workflows) that calls TalentLMS.**

Why:

- **Fits the job.** Barakhadi is a content and marketing site with a small amount of server logic (checkout, webhook, later auth). Astro is built for exactly that. Pages ship as plain HTML with zero JS by default, and server endpoints, Actions, sessions and middleware cover the dynamic parts.
- **Cheapest and lowest maintenance.** Hosting is $0, or $5/month on Workers Paid. There is no PHP, no plugins, no server patching and no database server. Static asset requests on Workers are free and unlimited.
- **Same platform as the existing prototype.** The Stripe-to-TalentLMS Cloudflare Worker logic ports directly into an Astro API route, or stays as a sibling Worker.
- **Strategic alignment.** Cloudflare acquired the Astro team in January 2026. Astro stays MIT-licensed and multi-cloud, but the Cloudflare adapter is now first-party and runs workerd in dev, prerender and production.
- **AI-agent friendly.** It is file-based (`src/pages`, `src/content`) and the `.astro` syntax is close to HTML. There is an official Astro Docs MCP server, and `astro dev --background` was added explicitly for AI agents in Astro 7. Everything lives in Git, and every branch gets a preview URL through Workers Builds.
- **Clear path to the future features.** Better Auth (D1-native since v1.5) can run on Workers for accounts. Its OAuth 2.1/OIDC provider plugin can make barakhadi.com the identity provider for TalentLMS SSO, which TalentLMS supports through OpenID Connect. Teacher dashboards can be React or Svelte islands calling the TalentLMS API from server endpoints.

The runner-up is Next.js, either on Vercel or on Cloudflare via OpenNext. It is more powerful for app-heavy dashboards but costs more, churns more, and needs frequent security patching: two critical RCEs were patched on 14 Oct 2026 alone. Staying on WordPress (Bricks or headless) is not recommended, because it fails the "no plugin and security updates" and "edited via AI and Git" requirements.

---

## 2. Current state of the key technologies (verified October 2026)

### 2.1 Cloudflare acquired the Astro team (January 2026)

- On **16 Jan 2026**, Cloudflare announced it was acquiring The Astro Technology Company. All full-time Astro employees joined Cloudflare. Terms were not disclosed. [Cloudflare blog; BusinessWire]
- **Commitments:**
  - Astro stays **MIT-licensed** and open to outside contributions, with a public roadmap and open governance.
  - It stays deployable on any cloud. The Astro Ecosystem Fund continues with Webflow, Netlify, Wix, Sentry and Stainless.
- **What it means for Barakhadi:**
  - (a) The Cloudflare adapter is now effectively first-party and gets priority. Astro 6 rebuilt it so dev, prerender and production all run in **workerd**, and bindings (D1, KV, R2, Queues) are available locally through `import { env } from "cloudflare:workers"`.
  - (b) There is vendor concentration risk: framework and host now belong to the same company. This is mitigated by the MIT license and by the Node, Netlify and Vercel adapters, which continue to exist.
  - (c) Astro's **Cloudflare adapter no longer supports Cloudflare Pages**. You deploy to **Workers**. [Astro Cloudflare adapter docs]

### 2.2 Astro: current version and features

- **The current major is Astro 7.** 7.0 shipped 22 Jun 2026, and the latest is **7.4 (15 Oct 2026)**. 6.0 shipped around March 2026. [astro.build/blog]
- **Astro 7 highlights:**
  - Vite 8 with the Rolldown bundler (15–61% faster builds).
  - A new **Rust `.astro` compiler**, which is stricter: unclosed tags and invalid nesting now produce errors.
  - A Rust Markdown processor (Sätteri) by default.
  - Queued rendering by default.
  - **Advanced Routing** through a `src/fetch.ts` entrypoint, with Hono middleware compatibility.
  - **Stable route caching** (`Astro.cache`, `routeRules`, `cache.invalidate()`, with an experimental Cloudflare CDN provider).
  - `astro dev --background` (a managed dev-server process for AI agents) and JSON logging.
  - `@astrojs/db` was removed: use Drizzle, `node:sqlite`, or D1 directly.
- **Astro 7.4:** separate build and runtime image services, a `--timings` build flag, experimental parallel prerendering, and **Node 22.22.0+** required.
- **Features relevant to Barakhadi:**
  - **Content collections and the Content Layer.** Typed Markdown/MDX blog posts and landing pages, with Zod 4 schemas. **Live content collections** are stable since Astro 6, useful for pulling course data at request time from the TalentLMS API.
  - **Server islands** (`server:defer`). Keep pages static and cacheable while injecting a personalized fragment, such as "Hi Priya, continue your course".
  - **Actions.** Type-safe server functions for forms (newsletter, contact, school enquiry) with Zod validation.
  - **Sessions** (added in 5.7). The Cloudflare adapter auto-configures **Workers KV** as the session store (binding `SESSION`). KV is eventually consistent, with up to 60 s global propagation, so don't use it for payment state.
  - **i18n routing.** Built-in locale routing (`/` for English, `/mr/` for Marathi), with fallback and helper functions.
  - **Fonts API** (Astro 6+). Self-hosts Google Fonts with subsets, which matters for Devanagari: Noto Sans Devanagari, Mukta, Baloo 2 and so on.
  - **CSP API** (Astro 6+).
  - **Image service.** On Cloudflare the default is `cloudflare-binding` (Cloudflare Images), with `compile`, `passthrough` and `custom` also available. Since 7.4 you can use `compile` (sharp at build) for prerendered pages and the binding at runtime.
- **Adapter:** `@astrojs/cloudflare` v14.x (v13+ required for Astro 6+). Prerendered pages run in workerd by default (`prerenderEnvironment: 'node'` if needed). Bindings come through `cloudflare:workers`, and `Astro.locals.runtime` was removed.
- **AI tooling:**
  - Official **Astro Docs MCP server** at `https://mcp.docs.astro.build/mcp` (streamable HTTP; works with Claude Code).
  - A "Building Astro sites with AI tools" guide.
- **Security:** Astro is not maintenance-free. Several 2026 advisories hit on-demand features:
  - server-island encryption replay leading to XSS (fixed 6.1.10)
  - `astro/hono` checkOrigin bypass (fixed 7.0.6)
  - an AVIF image-optimization RCE (critical)
  - a server-actions body-size DoS in `@astrojs/node`

  A mostly static site has a tiny attack surface. Still, enable Dependabot or Renovate and take a minor update roughly monthly. [corgea, Tenable, GitLab advisory DB]

### 2.3 Cloudflare: Workers with static assets vs Pages

- **Cloudflare's direction:** Workers now serves static assets. New full-stack projects are steered to Workers, and the Pages-to-Workers migration guide says Workers has "a distinctly broader set of features". Pages is **not** being shut down, and no official forced migration has been announced.
- **Workers-only features** (from Cloudflare's compatibility matrix): Cron Triggers, Queue consumers, Workers Logs, Logpush, Tail Workers, Source Maps, Gradual Deployments, the Cloudflare Vite plugin, Rate Limiting, Image Resizing, Email Workers, non-root routes. Durable Objects are fully supported only on Workers.
- **Pages-only:** custom domains outside Cloudflare zones. That doesn't matter here, because DNS will move to Cloudflare.
- **Preview deployments on Workers:** enable "Builds for non-production branches" in Workers Builds (Git integration). Every branch gets `<branch>-<worker>.<subdomain>.workers.dev` and a commit URL, posted as a PR comment. Previews can sit on custom domains and be protected with Cloudflare Access. Previews are **not** generated for Workers that define a Durable Object, which is another reason to avoid Durable Objects here.
- **Redirects:** a `_redirects` file in the static assets supports up to **2,000 static and 100 dynamic** redirects with 301/302/303/307/308. Beyond that, use Bulk Redirects. Astro's own `redirects` config also works.
- **Decision: use Workers with static assets. Do not start new on Pages.** The Astro adapter only supports Workers anyway.

### 2.4 Cloudflare platform pieces and limits

Figures come from the official Workers pricing page, October 2026.

| Product | Free plan | Workers Paid ($5/mo minimum) | Use at Barakhadi |
|---|---|---|---|
| Workers requests | 100,000/day | 10M/mo included, then $0.30/M | API routes, webhook, SSR pages |
| Workers CPU | 10 ms per invocation | 30M CPU-ms/mo included; up to 5 min per invocation (default 30 s) | Stripe signature verification and JSON work fit easily on Paid |
| Static asset requests | Free and unlimited | Free and unlimited | All marketing pages and blog |
| D1 (SQLite) | 5M rows read/day, 100k rows written/day, 5 GB | 25B reads/mo, 50M writes/mo, 5 GB included | Customers, entitlements, processed webhook events, schools and seats, auth tables |
| KV | 100k reads/day, 1k writes/day, 1 GB | 10M reads, 1M writes/mo | Astro sessions, feature flags, cache |
| R2 | 10 GB-month, 1M Class A, 10M Class B, free egress | $0.015/GB-month | Worksheets/PDFs, media, D1 backups |
| Queues | 10,000 ops/day; 24 h retention (fixed) | 1M ops/mo, then $0.40/M; retention 4 days default, up to 14 | Webhook → TalentLMS jobs with retries and a DLQ |
| Workflows | Included; 3,000 steps/day; 1 GB-month state; billing for steps started 10 Aug 2026 | Higher | Durable multi-step provisioning, as an alternative to Queues |
| Cron Triggers | Workers-only feature (Pages lacks it) | Yes | Nightly Stripe ↔ D1 ↔ TalentLMS reconciliation |
| Turnstile | Free: up to 20 widgets, unlimited challenges, 10 hostnames per widget | n/a | Bot protection on forms, sign-up and free-trial start |
| Web Analytics | Free, "privacy-first", no visitor personal data | n/a | Baseline traffic and Core Web Vitals |
| Images (transformations) | 5,000 unique transformations/mo; new ones beyond that error (no charge) | 5,000 included, then $0.50 per 1,000 | Astro `<Image>` at runtime (prefer build-time `compile` for static pages) |
| Email Service | Routing (inbound) free; **sending to arbitrary recipients is Beta and needs Workers Paid** | Paid | Possible future replacement for Resend; still Beta |

**Practical advice:** start on the free plan for the MVP, then move to **Workers Paid ($5/mo)** before taking real payments. That buys the CPU headroom, longer queue retention and Email Sending, and avoids daily caps.

---

## 3. Option comparison

### Option A: Astro 7 on Cloudflare Workers (recommended)

**Architecture:**

```
barakhadi.com (Cloudflare DNS + CDN)
└── Worker "barakhadi-web" (Astro 7 + @astrojs/cloudflare)
    ├── static assets: /, /pricing, /schools, /blog/**, /mr/** (prerendered HTML)
    ├── POST /api/checkout          -> creates Stripe Checkout Session (subscription | payment)
    ├── POST /api/portal            -> creates Stripe Customer Portal session
    ├── POST /api/stripe/webhook    -> verify, dedupe in D1, enqueue, 200
    ├── Actions: contact / school enquiry / newsletter (Turnstile + D1 + Resend)
    ├── (later) /api/auth/*         -> Better Auth (D1), OIDC provider for TalentLMS SSO
    └── (later) /dashboard/**       -> on-demand pages + React islands, data from TalentLMS API
Queue "provisioning" -> consumer (same Worker or a separate one) -> TalentLMS REST API
Cron (nightly) -> reconciliation job
D1 "barakhadi" | KV "SESSION" | R2 "assets" | DLQ "provisioning-dlq"
```

| Criterion | Assessment |
|---|---|
| **Hosting cost** | **$0** on Workers Free, or **$5/mo** on Workers Paid (recommended once live). Optional extras: Plausible about $9/mo, Resend free up to 3,000 emails/mo. |
| **Performance (CWV)** | The best of the three. Static HTML from Cloudflare's edge, zero JS by default, and islands only where needed. Astro's own CrUX analysis (2023, vendor-published) found it the only framework with more than 50% of sites passing CWV. For comparison, about 30% of WordPress sites fail LCP on phones (corewebvitals.io, Oct 2026). Devanagari fonts need care: subset and self-host them through the Fonts API, with `font-display: swap`. |
| **SEO** | Full control of `<head>`, canonical, hreflang and JSON-LD (Course, Product, FAQ, Organization). `@astrojs/sitemap` and RSS integrations are available. Clean URLs, with `trailingSlash` configurable to match WordPress's existing URLs. Redirects go in `_redirects` or Astro config. Landing pages are just files or content-collection entries. |
| **Claude Code fit** | **Excellent.** File-based routing, HTML-like `.astro` files, Markdown content and a small API surface. Training-data familiarity is good, though Astro 7 changes (Rust compiler strictness, `src/fetch.ts`, Sätteri) are newer than most training data. Mitigate with the Astro Docs MCP server and a `CLAUDE.md` that pins conventions. Use `astro dev --background` and `wrangler dev` locally. Cloudflare docs publish llms.txt and agent prompts. |
| **Stripe** | Redirect to Stripe Checkout from an API route. The webhook lives in the same Worker. The Customer Portal link comes from an API route. The Stripe Node SDK works on Workers with `Stripe.createFetchHttpClient()` and `constructEventAsync(..., Stripe.createSubtleCryptoProvider())`. |
| **Auth (future)** | **Better Auth** (open source; D1 native since v1.5, Feb 2026; Astro integration documented; joined Vercel in Jul 2026 but remains framework and host agnostic). Its **OAuth 2.1/OIDC provider plugin** (`@better-auth/oauth-provider`) lets barakhadi.com be the IdP for TalentLMS SSO. Alternatives: **Clerk** (hosted; free up to 50,000 monthly retained users since Feb 2026; Pro about $25/mo) or **Supabase Auth** (free 50k MAU, but free projects pause after 7 idle days). **Cloudflare Access** is for staff and admin areas and preview protection, not customer accounts. |
| **Database** | **D1** (SQLite; use Drizzle ORM for schema and migrations). KV for sessions and cache, R2 for files. |
| **i18n** | Built-in Astro i18n routing; content collections per locale; hreflang in the layout. |
| **Email** | **Resend** (free 3,000/mo with a 100/day cap; Pro $20/mo for 50k). Later, Cloudflare Email Service once it leaves Beta. Stripe sends receipts, invoices and trial reminders itself. |
| **Forms** | Astro Actions + Turnstile + a D1 insert + an email notification. No third-party form SaaS needed. |
| **Analytics** | Cloudflare Web Analytics (free) for baseline and CWV. Add GA4 (free; needs a consent banner for UK/EU visitors) for ads attribution, or Plausible ($9/mo, cookieless) for simple privacy-friendly marketing analytics. Use Stripe as the revenue source of truth. |
| **Images** | Astro `<Image>`/`<Picture>`. Prefer build-time optimization for static pages (no runtime cost). Use the Cloudflare Images binding for runtime (5k transformations/mo free). |
| **Preview deploys** | Workers Builds: per-branch preview URLs and PR comments; can be protected with Access. |
| **Lock-in** | Low to moderate. Astro is portable through adapters, and content is Markdown in Git. Lock-in sits in Cloudflare bindings (D1, Queues). Mitigate with Drizzle (D1 is SQLite) and a thin `provisioning` module. |
| **Long-term maintenance** | Low. `npm update` about monthly through Renovate or Dependabot PRs. A framework major roughly yearly (Astro 6 in Mar 2026, 7 in Jun 2026, so expect breaking changes). There is no server or OS to patch. |

**Risks and cons:**

- Astro is younger and less "app-like" than Next.js for rich dashboards. React or Svelte islands mitigate this, and dashboards are a later phase.
- Astro 7 is only four months old, and its stricter compiler may reject sloppy HTML that AI agents sometimes write. In practice that is a feature.
- Framework and host are now the same company.

### Option B: Next.js (App Router) on Vercel, or on Cloudflare via OpenNext

**Current state:**

- **Version.** The latest is **Next.js 16.4** (6 Oct 2026), patched to **16.4.1** on 14 Oct 2026. 16.2 (Mar 2026) introduced a **stable Adapter API**, built with OpenNext, Netlify, Cloudflare, AWS Amplify and Google Cloud, plus AGENTS.md in create-next-app. 16.3 added "Instant Navigations" and agent tooling (first-party Skills).
- **Security churn is substantial:**
  - **14 Oct 2026:** two **critical unauthenticated RCEs** (`use cache` returning typed arrays; Image Optimization with SVG through sharp) and a high-severity Server Actions DoS.
  - **30 Sep 2026:** six more advisories (SSRF in image optimization, several cache-poisoning and cache-leak bugs, and an MCP dev-endpoint info leak).
  - **Dec 2025:** React Server Components RCE (CVE-2025-66478 / CVE-2025-55182, CVSS 10).

  A site on Next.js must be patched promptly, several times a year.
- **Middleware renamed.** Next 16 renamed middleware to "proxy" (a codemod is provided).
- **Vercel pricing.** **Hobby is free but "for personal, non-commercial use"**, so a store doesn't qualify. **Pro is $20/mo per seat** with a $20 usage credit and 1 TB of transfer. Overages: data transfer from $0.15/GB, functions from $0.60/M, image transformations from $0.05 per 1k.
- **OpenNext on Cloudflare** (`@opennextjs/cloudflare`):
  - Supports Next 16 (all minors), the App Router, ISR, PPR, `use cache` and middleware. **Node Middleware is not yet supported.**
  - Worker size limit is **3 MiB compressed on Free and 10 MiB on Paid**, so expect to need Paid.
  - Image optimization needs Cloudflare Images configured.
  - **"Full Windows support is not guaranteed; use WSL"**, a real friction point because the owner develops on Windows 11.
  - Cloudflare also has **vinext**, an experimental Vite-based Next.js re-implementation (Feb 2026). It is not production-ready for all apps.

| Criterion | Assessment |
|---|---|
| Hosting cost | Vercel Pro **$20/mo** minimum (plus metered usage), or Cloudflare Workers Paid **$5/mo** via OpenNext. |
| Performance | Good if built carefully (RSC, static generation), but it ships a React runtime on every page. Real-world CWV is weaker than Astro's on content sites. |
| SEO | Excellent (Metadata API, sitemap and robots route handlers, OG image generation). |
| Claude Code fit | **The most training data of any framework**, plus AGENTS.md and agent skills. But the App Router's caching model has changed repeatedly (fetch cache, then `use cache` and Cache Components), so agents often produce stale or mixed patterns. It also has more concepts (server vs client components, caching, proxy). |
| Stripe | Very well-trodden (route handlers, Server Actions; Vercel and Stripe templates). |
| Auth | Clerk (best Next.js DX), Better Auth, or Auth.js. **Auth.js is now maintained by the Better Auth team, which recommends Better Auth for new projects** (Sep 2025). Supabase Auth also works. |
| DB | Vercel Marketplace Postgres (Neon, Supabase), or D1 via OpenNext. |
| i18n | next-intl or App Router `[locale]` segments. |
| Email/forms/analytics | Same as Option A (Resend, Server Actions + Turnstile, Vercel Analytics is paid per event, GA4/Plausible). |
| Images | `next/image` (metered on Vercel; this is the component behind several of the 2026 CVEs). |
| Preview deploys | Best-in-class on Vercel. Good on Workers Builds. |
| Lock-in | Moderate on Vercel, where ISR, image and cache features are tuned for it. Lower now that the Adapter API is stable. |
| Maintenance | **Highest of the code options.** Frequent security releases, a large dependency tree, and a yearly major with caching or API changes. |

**Verdict:** this is overkill for a 3–4 page marketing site. Pick it only if the product becomes primarily a web app with many interactive dashboards and the team wants React everywhere. Even then, OpenNext on Cloudflare (with WSL) or SvelteKit are cheaper than Vercel.

### Option C: Stay on WordPress, with Bricks Builder (or headless WP) on Cloudways

- **Cloudways:** the official price page lists DigitalOcean Micro at **$11/mo**. Several 2026 third-party guides say $14, so check the live page. The 2 GB plan is about $28/mo.
- **Bricks:** about **$79/yr** (Starter), $149 and $249 tiers, or **$599 lifetime unlimited** (from the official pricing page, which is undated).
- **Security track record:**
  - Bricks had **CVE-2024-25600**, an unauthenticated RCE (CVSS 9.8–10) that was actively exploited, with a public Exploit-DB exploit still circulating in 2026.
  - Patchstack's *State of WordPress Security in 2026* counts **11,334 new WP-ecosystem vulnerabilities in 2025 (+42% YoY)**: 91% in plugins, 9% in themes, about 6 in core.
  - For heavily exploited bugs, the median time from disclosure to mass exploitation was **about 5 hours**.
- **AI-editability:** WordPress 6.9/7.0 has a core **Abilities API**, and the **MCP Adapter** plugin (pre-1.0) can expose it to agents. A bare install exposes only about 3 read-only abilities, so write access depends on plugins. Community Bricks MCP servers exist. Either way, content and layout live in the MySQL database (Bricks stores element JSON in post meta), **not in Git**. AI edits happen against a live production database through Application Passwords, with no diff or PR review. That breaks the "only via AI and Git" workflow.
- **Headless WP** (WordPress as CMS, Astro or Next as frontend) keeps WordPress to patch **and** adds a frontend build. It is the worst of both for a solo owner.
- **Stripe:** needs WooCommerce plus a subscriptions or membership plugin (paid annually; exact prices not verified), or keeps the Cloudflare Worker for checkout and webhooks anyway, at which point WordPress adds little.

| Criterion | Assessment |
|---|---|
| Cost | $11–28/mo hosting, plus Bricks $79/yr (or $599 once), plus paid plugins (SEO, forms, membership/subscriptions, backups/security). |
| Performance | Bricks is much leaner than Elementor, but it's still PHP and MySQL with page caching. About 30% of WP sites fail LCP on phones. |
| SEO | Strong through plugins (Yoast or Rank Math). |
| Claude Code fit | Poor to fair: database-centric, not file and Git-centric. |
| Maintenance | **Highest:** core, theme, builder and plugin updates, PHP version upgrades, malware scanning, backups. |

**Verdict:** reject. It fails the core requirement of no plugin or security updates.

### Others considered (briefly)

- **SvelteKit.** Excellent Cloudflare adapter, small bundles and a nice DX. However, **SvelteKit 3 went to Release Candidate in Aug 2026**, and its headline feature (remote functions) is still experimental. Svelte 5 runes also made much older training data stale. It's a strong choice for an app-heavy future but mid-transition right now, and Astro is the better fit for a content and marketing site. Svelte components can still be used *inside* Astro as islands.
- **Plain static HTML plus a Worker.** Zero dependencies and $0, and fine for literally 3 pages. But you hand-roll layouts, the blog, i18n, sitemaps, image optimization and forms. Astro outputs essentially the same static HTML while adding components, content collections and an image pipeline, so the trade-off favors Astro.
- **Webflow / Framer.**
  - Framer: Basic about $10/mo and Pro about $30/mo per site (yearly).
  - Webflow: Basic $15/mo, and Premium (formerly CMS/Business, simplified May 2026) about $25/mo yearly. Ecommerce plans are about $42–$320/mo; third-party sources conflict, so check the live page.

  Both are visual-editor-first rather than Git or code-agent-first. Native subscription selling is limited (it typically needs third-party membership tools). You would still need a Worker for the Stripe → TalentLMS webhook. Rejected on AI and Git workflow, per-site fees and lock-in.

---

## 4. Stripe design for Barakhadi

### 4.1 Products and pricing model

| Offer | Stripe setup | Checkout mode |
|---|---|---|
| Family monthly/annual subscription with free trial | Product "Barakhadi Family", recurring Prices (month and year) | `mode=subscription`, `subscription_data.trial_period_days=7/14` |
| One-time course purchase | Product per course, one-time Price | `mode=payment` |
| School / bulk seat licence | Product "School licence", **per-seat** recurring Price (`quantity` = seats); optionally **volume tiered** pricing for seat discounts | `mode=subscription` with `line_items[].adjustable_quantity {enabled, minimum, maximum}`, or Stripe **Invoicing / Quotes** for schools that need a PO and bank transfer |
| Quick links for social/WhatsApp campaigns | **Payment Links** (no code; work with the Customer Portal) | n/a |

**Trials.** Stripe now positions the new **Trial Offers API** (API version `2026-09-30.endive`, flexible billing mode) as the recommended approach, and labels `trial_end`/`trial_period_days` "legacy". But:

- Trial Offers with **Checkout are private preview only**, and they don't work with Payment Links or pricing tables.
- The **Customer Portal can't update subscriptions that use trial offers.**

So for the MVP, use the still-documented and fully supported Checkout pattern:

```
mode=subscription
subscription_data[trial_period_days]=14
payment_method_collection=if_required            # "no card needed" trial (optional)
subscription_data[trial_settings][end_behavior][missing_payment_method]=cancel  # or pause
```

- No-card trials invite abuse. Stripe itself recommends requiring an account and a captcha first, so use **Turnstile** and email verification.
- Card-up-front trials convert better and are simpler.
- `customer.subscription.trial_will_end` fires 3 days before the trial ends (configurable). Stripe can also send its own reminder emails, and card-network trial-compliance rules apply.

**Customer Portal:**

- Customers update cards and billing details, view and pay invoices, switch plans (up to 10 products), change quantity, and cancel (with optional retention coupons and cancellation reasons).
- Create sessions server-side from `/api/portal`. Sessions expire after 5 minutes if unused, and the portal **can't be iframed**.
- A **no-code portal login link** is also available, which is useful before barakhadi.com has its own accounts.
- Gotcha 1: by default, changing a `trialing` subscription in the portal ends the trial. Set `features.subscription_update.trial_update_behavior=continue_trial`.
- Gotcha 2: subscriptions billed by `send_invoice` (typical for schools) can be cancelled but not updated in the portal.

### 4.2 Fees, tax and international (US/UK diaspora plus India)

| Item | Cost (stripe.com/pricing, Oct 2026) |
|---|---|
| US domestic card | 2.9% + 30¢ |
| International card | +1.5% |
| Currency conversion | +1% |
| **Stripe Billing** (subscriptions) | **0.7% of Billing volume** (pay-as-you-go) |
| **Stripe Tax** (no-code: Checkout, Billing, Payment Links) | **0.5% per transaction** where you're registered |
| **Managed Payments** (Stripe as merchant of record) | **+3.5%** on top of payment fees |
| **Adaptive Pricing** (show local currency) | **No fee to you** on standard pricing; the customer pays about a 2%+ conversion fee |

- **Multi-currency.** Two ways to charge GBP or INR customers in their own currency:
  - (a) Set explicit per-currency prices (`currency_options` on a Price), which allows psychological and purchasing-power pricing such as ₹ pricing much lower than USD.
  - (b) Turn on **Adaptive Pricing**, which now supports new **subscriptions** in Checkout and Payment Links (GA in the Optimized Checkout Suite around Aug 2026). FX is re-quoted each billing cycle unless you use the gated stability buffer.

  Recommendation: explicit USD, GBP and INR prices for the main plans, and Adaptive Pricing for everyone else.
- **Stripe account location matters.** **Stripe India is invite-only for new accounts**, and existing Indian accounts are still supported. An India-based entity selling abroad also needs extra onboarding (IEC code, RBI purpose codes).
  - If the business entity is US or UK, open the Stripe account there and sell to India in INR.
  - Stripe's portal docs list **UPI (INR) as a payment method for US-based businesses**. Verify eligibility in your Dashboard.
  - If Indian customers are a big segment and the entity is Indian, consider Razorpay for domestic India alongside Stripe for international. This was not researched in depth.
- **Tax.** Selling digital education to consumers in the UK and EU can trigger VAT obligations for non-resident sellers from the first sale, and US states have their own digital-goods rules. Confirm with an accountant. Options:
  - **Stripe Tax** (0.5%) calculates and collects, but **you** still register and file.
  - **Managed Payments** (+3.5%, Stripe as MoR) handles sales tax, VAT and GST in 80+ countries, plus fraud, disputes and transaction-level support.

  Managed Payments limitations: Checkout and Payment Links only, no Elements, and subscriptions must be created through Checkout or Payment Links. For a small founder selling worldwide, the MoR route may be worth the 3.5% until revenue justifies doing tax compliance yourself.

### 4.3 Webhook events to handle

Set these up as **snapshot** events, so the Stripe SDK types match the handler. Stripe now labels "thin" events as recommended for new endpoints. They work too, but each one needs an extra fetch.

| Event | Action |
|---|---|
| `checkout.session.completed` | Main fulfilment trigger. Read `mode`, `client_reference_id`/`metadata` (product → TalentLMS course or branch), customer and email, then enqueue "provision" (create the TalentLMS user and enroll). For one-time purchases, check `payment_status=paid`. |
| `customer.subscription.created` / `.updated` | Sync status (`trialing`, `active`, `past_due`, `canceled`, `unpaid`, `paused`), `current_period_end`, `cancel_at_period_end`, and **quantity** (school seats). Sets the entitlement expiry in D1. |
| `customer.subscription.deleted` | Revoke access: deactivate or unenroll in TalentLMS. |
| `customer.subscription.trial_will_end` | Send your own reminder email, and check that a payment method exists. |
| `customer.subscription.paused` / `.resumed` | Used if no-card trials end with `missing_payment_method=pause`. |
| `invoice.paid` | Extend access on renewals (confirm the subscription `status=active`). |
| `invoice.payment_failed` | Email the customer a portal link. Rely on Smart Retries and keep access until `unpaid` or `canceled` (grace period). |
| `charge.refunded`, `charge.dispute.created` | Revoke access or flag it for review. |

Key Stripe guidance:

- Events are **not delivered in order** and **may be duplicated**, so dedupe on `event.id`.
- Return **2xx quickly** and process asynchronously.
- Use the **raw body** for signature verification.
- Stripe retries in live mode for **up to 3 days** with exponential backoff.

### 4.4 Webhook → TalentLMS on Cloudflare Workers: best-practice pattern

```
POST /api/stripe/webhook
  1. body = await request.text()            // raw body, never JSON-parse first
  2. event = await stripe.webhooks.constructEventAsync(
         body, request.headers.get('stripe-signature'), env.STRIPE_WEBHOOK_SECRET,
         undefined, Stripe.createSubtleCryptoProvider())   // Web Crypto on Workers
  3. INSERT INTO stripe_events(id, type, created, status) VALUES (?, ?, ?, 'queued')
       ON CONFLICT(id) DO NOTHING;           // D1 = durable idempotency ledger
     if no row inserted -> return 200        // duplicate delivery
  4. await env.PROVISION_QUEUE.send({ eventId: event.id, type: event.type })
     (or: env.PROVISION_WORKFLOW.create({ id: event.id, params }) -- instance id = event id)
  5. return new Response('ok', { status: 200 })   // fast ack; Stripe stops retrying

Queue consumer (max_retries ~8, dead_letter_queue = provisioning-dlq)
  for each msg:
    - re-fetch current state from Stripe (session/subscription), don't trust event ordering
    - compute desired entitlement -> upsert D1 (customers, entitlements, seats)
    - TalentLMS, idempotently:
        * look up user by email -> create (usersignup) only if missing
        * enroll (addusertocourse) only if not enrolled; treat "already enrolled" as success
        * for schools: create/assign to a TalentLMS group or branch per school (verify plan features)
    - store talentlms_user_id in D1; mark stripe_events.status='done'
    - msg.ack()
    on transient error (5xx/429/timeout): msg.retry({ delaySeconds: min(3600, 30 * 2**msg.attempts) })
    on permanent error (4xx validation): record error in D1, ack, alert (email via Resend)
DLQ consumer -> write to D1 'failed_jobs' + email the owner
Cron Trigger (nightly) -> reconcile: Stripe active subs vs D1 entitlements vs TalentLMS enrolments; fix drift
```

**Notes:**

- **Why D1 for the ledger, not KV:** D1 is strongly consistent for this use with unique constraints. KV is eventually consistent (up to 60 s), so it can't safely dedupe concurrent duplicates.
- **Delivery semantics:** Queues redeliver on failure (at-least-once in practice) and retry `max_retries` times (default 3) with per-message delays up to 24 h, then send to the DLQ. Every TalentLMS call must therefore be safe to repeat.
- **Workflows alternative:** Cloudflare **Workflows** (`step.do()` with automatic retries and persisted step state) suits multi-step provisioning: create user, then enroll, then send a welcome email. Using `event.id` as the instance ID gives natural idempotency. Free plan: 3,000 steps/day.
- **Outbound Stripe writes:** send an `Idempotency-Key` header, for example `provision-${event.id}`.
- **TalentLMS limits:** TalentLMS documents **200 API calls per 5 seconds** for API v2. Older reports mention much lower limits on free portals. V1 uses an HTTP Basic API key; v2 uses header keys. Keep the key in `wrangler secret`.
- **Map products to courses:** put the mapping in Stripe Product/Price `metadata` (for example `talentlms_course_id=12`) or in a D1 table, so you can add courses without code changes.
- **Testing:** use the Stripe CLI (`stripe listen --forward-to localhost:4321/api/stripe/webhook`, `stripe trigger checkout.session.completed`), test clocks for trials and renewals, and Workers preview URLs.

### 4.5 Future: accounts, SSO into TalentLMS, teacher dashboards

- **Accounts.** Better Auth on Workers + D1: email/password, magic link, Google sign-in. Organizations or teams can model schools.
- **SSO into TalentLMS.** TalentLMS supports **OpenID Connect** and **SAML 2.0** SSO, acting as the service provider. You configure the client ID and secret plus the authorize, token and userinfo endpoints. With Better Auth's **OAuth 2.1 / OIDC provider plugin**, barakhadi.com becomes the IdP: a "Go to my course" button sends the parent or child to TalentLMS, already logged in.
  - Alternative: Clerk can also act as an OAuth/OIDC provider (not verified in detail here).
  - Verify which TalentLMS plan includes SSO.
- **Teacher and school dashboards.** On-demand Astro pages behind auth middleware. Server endpoints call the TalentLMS API (users, courses, progress), cache it briefly in KV, and render charts in React islands. Seat management: the school admin invites students, and the Worker creates TalentLMS users within the purchased `quantity`.

---

## 5. Migrating barakhadi.com from Cloudways to Cloudflare with zero SEO loss

**Phase 0: inventory (before building)**

1. Export every indexed URL from Search Console (Pages report), the WordPress sitemap (`/sitemap_index.xml` or `/wp-sitemap.xml`), and a crawl (for example Screaming Frog's free tier, up to 500 URLs). Include images (`/wp-content/uploads/...`), PDFs, feeds, and category, tag and author archives.
2. Record each page's title, meta description, H1, canonical, OG tags and structured data. Pull page content through the WP REST API (`/wp-json/wp/v2/pages`, `/posts`) so Claude Code can convert it to Astro and Markdown.
3. Note the trailing-slash convention (WordPress default is `/about/`) and set Astro's `trailingSlash: 'always'` to match.

**Phase 1: move DNS to Cloudflare first, with the site still on Cloudways (no visible change)**

1. Add the domain to Cloudflare (Full setup) and let it scan records. **Manually verify every record:** A/CNAME for the apex and www, plus **MX, SPF, DKIM and DMARC TXT** records for email. Email records stay "DNS only".
2. **Disable DNSSEC at the registrar** before changing nameservers, or the domain can go dark. Re-enable it in Cloudflare afterwards.
3. Lower TTLs about a week before the cutover (Google recommends this for host moves).
4. Change nameservers at the registrar to the two Cloudflare nameservers. Propagation takes up to 24 h. The site keeps serving from Cloudways, now proxied by Cloudflare.
5. Optionally transfer the domain to Cloudflare Registrar (at-cost renewals). Keep the Search Console **Domain property** verified through a DNS TXT record so it survives the host change.

**Phase 2: build and stage**

1. Build the Astro site and deploy to `*.workers.dev` or a preview subdomain with `noindex` and/or Cloudflare Access protection.
2. Keep **identical URLs** wherever possible. For anything that changes, add **301s** in `public/_redirects` (or Astro `redirects`). Map one-to-one to the most relevant page, never mass-redirect to the homepage, and avoid redirect chains. Common WordPress leftovers:
   - `/feed/` → `/rss.xml`
   - `/?p=123` → canonical page
   - `/category/...` → `/blog/...`
   - `/wp-content/uploads/...` images, which you either keep at the same path in `public/` or redirect
3. Generate `sitemap.xml` and `robots.txt`, add self-referencing canonicals and hreflang (en/mr), and port JSON-LD.
4. Check the staging build with Lighthouse and the URL Inspection tool (live test) to confirm Googlebot isn't blocked by WAF or bot settings.

**Phase 3: cutover**

1. Remove `noindex`/disallow from production config.
2. Attach `barakhadi.com` and `www` as **Workers Custom Domains**. Cloudflare updates DNS for you, so the switch is near-instant. **Rollback** means pointing the DNS record back to the Cloudways IP.
3. Pick one canonical host (apex or www) and 301 the other with a Cloudflare Redirect Rule.
4. Submit the new sitemap in Search Console. Spot-check the top URLs with URL Inspection, and run a crawl to confirm every old URL returns 200 or 301 (no 404s or soft-404s).

**Phase 4: monitor and decommission**

1. Watch Search Console (Pages, Sitemaps, Core Web Vitals, Performance) and Workers logs for 404s for 2–4 weeks. A temporary crawl dip followed by a rise is normal.
2. Keep Cloudways running until it receives no traffic (Google's advice), then cancel. Keep redirects for **at least a year**, ideally forever, since they cost nothing in `_redirects`.
3. Because the domain doesn't change, **no Change of Address** is needed in Search Console. That tool only applies to domain changes.

---

## 6. Suggested MVP plan (Option A)

1. `npm create astro@latest`, then `astro add cloudflare sitemap mdx react` (React only if needed). Add Tailwind for a colorful, friendly design system. Use the Fonts API for a Devanagari plus Latin pairing.
2. Pages: Home, Pricing (family and school), About or How it works, Blog index and post template, plus `/mr/` versions or Marathi sections. Add legal pages: privacy, terms and refunds, which Stripe requires.
3. `/api/checkout` and `/api/portal`, plus `/api/stripe/webhook` with D1, a Queue and the TalentLMS consumer (port from the prototype Worker).
4. Contact and school-enquiry form through an Astro Action with Turnstile, D1 and Resend.
5. Cloudflare Web Analytics, plus GA4 or Plausible. Workers Builds connected to GitHub with branch previews.
6. DNS migration as described in section 5.
7. Repo hygiene for Claude Code: a `CLAUDE.md` with conventions (Astro 7, adapter v14, D1/Drizzle, never parse the webhook body before verifying), the Astro Docs MCP server configured, Renovate or Dependabot, and `wrangler.jsonc` checked in. Secrets go in `wrangler secret`, never in Git.

Estimated running cost: **$0–5/mo** for hosting, plus Stripe fees (about 2.9% + 30¢, plus 0.7% Billing, plus 0.5% Tax if used), plus about $10/yr for the domain.

---

## 7. Sources

**Astro and Cloudflare acquisition**
- Cloudflare blog, "Astro joins Cloudflare" (16 Jan 2026): https://blog.cloudflare.com/astro-joins-cloudflare/
- BusinessWire press release: https://secure.businesswire.com/news/home/20260116386991/en/Cloudflare-Acquires-Astro-to-Accelerate-the-Future-of-High-Performance-Web-Development
- The New Stack: https://thenewstack.io/cloudflare-acquires-team-behind-open-source-framework-astro/
- InfoQ, Astro v6 beta and Cloudflare: https://www.infoq.com/news/2026/02/astro-v6-beta-cloudflare
- Astro blog index (7.0–7.4 release dates): https://astro.build/blog/
- Astro 7.0 release post: https://astro.build/blog/astro-7/
- Astro 7.4 release post: https://astro.build/blog/astro-740/
- Astro v7 upgrade guide: https://docs.astro.build/en/guides/upgrade-to/v7/
- Astro Cloudflare adapter docs (Pages unsupported, sessions/KV, image service, bindings): https://docs.astro.build/en/guides/integrations-guide/cloudflare/
- Astro sessions: https://docs.astro.build/en/guides/sessions/
- Astro "Building with AI tools" / Docs MCP server: https://docs.astro.build/en/guides/build-with-ai/
- Astro advisories (third-party trackers): https://corgea.com/advisories/packages/npm/astro , https://www.tenable.com/plugins/cloud-security/441793 , https://advisories.gitlab.com/npm/astro/GHSA-8mv7-9c27-98vc/
- Astro 2023 framework performance report: https://astro.build/blog/2023-web-framework-performance-report

**Cloudflare**
- Migrate from Pages to Workers (feature matrix, preview URLs): https://developers.cloudflare.com/workers/static-assets/migrate-from-pages/
- Workers pricing (Workers, D1, KV, R2, Queues): https://developers.cloudflare.com/workers/platform/pricing/
- Workers preview URLs changelog: https://developers.cloudflare.com/changelog/post/2025-07-23-workers-preview-urls/
- Workers Builds branch builds: https://developers.cloudflare.com/workers/ci-cd/builds/build-branches/
- Static assets `_redirects`: https://developers.cloudflare.com/workers/static-assets/redirects/
- Queues batching and retries: https://developers.cloudflare.com/queues/configuration/batching-retries/
- Workflows pricing: https://developers.cloudflare.com/workflows/reference/pricing/
- Turnstile plans: https://developers.cloudflare.com/turnstile/plans/
- Web Analytics: https://developers.cloudflare.com/web-analytics/about/
- Images pricing: https://developers.cloudflare.com/images/pricing/
- Email Service: https://developers.cloudflare.com/email-service/
- DNS full setup: https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/
- Stripe support in Workers: https://blog.cloudflare.com/announcing-stripe-support-in-workers
- vinext: https://blog.cloudflare.com/vinext , https://github.com/cloudflare/vinext , https://infoq.com/news/2026/03/cloudflare-vinext-experimental
- Third-party Pages vs Workers commentary: https://mecanik.dev/en/posts/cloudflare-pages-vs-workers-which-to-use-in-2026/ , https://www.morphllm.com/comparisons/cloudflare-pages-vs-workers

**Next.js / Vercel / OpenNext**
- Next.js blog index (16.2–16.4, security posts): https://nextjs.org/blog
- Next.js Across Platforms / Adapter API: https://www.nextjs.org/blog/nextjs-across-platforms
- Security update 14 Oct 2026: https://nextjs.org/blog/nextjs-security-update-october-14-2026
- September 2026 security release: https://nextjs.org/blog/september-2026-security-release
- CVE-2025-66478 advisory: https://nextjs.org/blog/CVE-2025-66478
- OpenNext Cloudflare: https://opennext.js.org/cloudflare
- Vercel pricing: https://vercel.com/pricing

**WordPress / Bricks / Cloudways**
- Bricks pricing: https://bricksbuilder.io/pricing/
- Bricks CVE-2024-25600: https://www.bleepingcomputer.com/news/security/hackers-exploit-critical-rce-flaw-in-bricks-wordpress-site-builder/ , https://feed.craftedsignal.io/briefs/2026-07-wordpress-bricks-rce/
- Patchstack State of WordPress Security 2026: https://www.patchstack.com/whitepaper/state-of-wordpress-security-in-2026/ (summary: https://patchstack.com/?p=25568)
- Cloudways pricing: https://www.cloudways.com/en/price-plan.php
- WordPress MCP Adapter: https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/ , https://instawp.com/wordpress-mcp-adapter-review/
- Bricks MCP server (community): https://glama.ai/mcp/servers/sabiertas/bricks-mcp-server
- CWV by CMS (Oct 2026, LCP pass rates): https://www.corewebvitals.io/state-of-cwv/explorer/technologies/cms

**Other frameworks and builders**
- SvelteKit 3 RC: https://devclass.com/devops/2026/08/20/sveltekit-3-puts-heat-on-nextjs-with-radical-approach-to-rpcs/5290688
- Svelte blog: https://svelte.dev/blog/whats-new-in-svelte-february-2026
- Framer vs Webflow pricing (third-party, read 2026-09-03): https://siter.io/framer-vs-webflow , https://www.costbench.com/compare/webflow-vs-framer/

**Auth / email / analytics**
- Better Auth 1.5 (D1 support): https://better-auth.com/blog/1-5
- Better Auth joins Vercel (7 Jul 2026): https://better-auth.com/blog/better-auth-joins-vercel
- Auth.js joins Better Auth: https://www.better-auth.com/blog/authjs-joins-better-auth
- Better Auth Astro integration: https://www.better-auth.com/docs/integrations/astro
- Better Auth OAuth 2.1 / OIDC provider: https://www.better-auth.com/docs/plugins/oauth-provider
- Clerk pricing explainer: https://clerk.com/articles/clerk-pricing-explained
- Supabase pricing (third-party): https://makerkit.dev/blog/saas/supabase-pricing , https://www.jetadmin.io/blog/supabase-pricing-2026-guide-to-plans-limits-and-real-world-costs/
- Resend pricing: https://www.resend.com/pricing.md
- Plausible pricing (third-party): https://www.toolpick.dev/pricing/plausible

**Stripe**
- Pricing: https://stripe.com/pricing
- Trial offers: https://docs.stripe.com/billing/subscriptions/trials
- Free trials (legacy `trial_period_days`, Checkout no-card trials): https://docs.stripe.com/billing/subscriptions/trials/free-trials
- Subscription webhooks: https://docs.stripe.com/billing/subscriptions/webhooks
- Webhooks best practices: https://docs.stripe.com/webhooks
- Customer Portal: https://docs.stripe.com/customer-management
- Per-seat pricing: https://docs.stripe.com/subscriptions/pricing-models/per-seat-pricing
- Pricing models (tiered/volume): https://docs.stripe.com/products-prices/pricing-models
- Adjustable quantity: https://docs.stripe.com/payments/checkout/adjustable-quantity
- Adaptive Pricing: https://docs.stripe.com/payments/checkout/localize-prices/adaptive-pricing , https://support.stripe.com/questions/adaptive-pricing-for-subscriptions , https://stripe.com/blog/adaptive-pricing-for-subscriptions
- Stripe Tax pricing: https://support.stripe.com/questions/understanding-stripe-tax-pay-as-you-go-pricing
- Managed Payments: https://docs.stripe.com/payments/managed-payments
- Stripe India invite-only: https://support.stripe.com/questions/stripe-accounts-are-invite-only-in-india , https://docs.stripe.com/india-exports

**TalentLMS**
- API v2 (rate limit 200 calls / 5 s): https://help.talentlms.com/hc/en-us/articles/24874457011356-TalentLMS-API-V2 (returned 403 to automated fetch; figure taken from search snippet)
- API overview (third-party): https://www.stitchflow.com/user-management/talentlms/api
- SSO with OpenID Connect: https://help.talentlms.com/hc/en-us/articles/360014659393-How-to-configure-SSO-with-OpenID-Connect

**SEO migration**
- Google, site move without URL changes: https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes
- Google, site move with URL changes: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes

**Caveats on sources**
- These figures come mostly from third-party sources and should be checked live before committing: Clerk Pro price, Webflow ecommerce tiers, Plausible tiers, Supabase limits, the Cloudways $11 vs $14 entry price, and Cloudflare Email Service per-message pricing.
- The TalentLMS rate limit and the exact v1/v2 endpoint behavior should be confirmed in the TalentLMS developer docs.
