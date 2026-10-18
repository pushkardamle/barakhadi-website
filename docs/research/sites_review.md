# Barakhadi: current-state review of the two websites

Audit date: 2026-10-17. Method: raw HTML fetched with curl (desktop UA), WordPress REST API (`/wp-json/`), the sitemaps, asset size checks, and read-only probes of the Cloudflare Worker and TalentLMS links. No forms were submitted and no checkout sessions were created.

---

## 1. Live site: https://www.barakhadi.com/ (WordPress + Elementor on Cloudways)

### 1.1 URL inventory (from the sitemap, REST API and nav)

`robots.txt` disallows `/wp-admin/` and points to `https://www.barakhadi.com/wp-sitemap.xml` (the WordPress core sitemap). `/sitemap.xml` redirects to it. `/sitemap_index.xml` returns 404, so no Yoast or RankMath sitemap exists.

| URL | Status | Last modified | Purpose / notes |
|---|---|---|---|
| `/` (page id 27, slug `home-barakhadi`, template `elementor_header_footer`) | 200 | 2025-12-15 | Home / landing page |
| `/faq/` | 200 | 2020-07-24 | FAQ (13 Q&As, accordion) |
| `/contact-us/` | 200 | 2023-02-07 | Contact form (Elementor Pro) |
| `/videos/` | 200 | 2021-02-02 | Two Wistia videos: Demo + Teacher Tutorial. **Not linked from the nav**, but listed in the sitemap |
| `/test/` | 200 | 2023-02-05 | Leftover page that says "Test Page". Indexable, listed in the sitemap |
| `/sample-page/` | 200 | 2020-06-24 | WordPress default "Sample Page" placeholder. Indexable |
| `/hello-world/` | 200 | 2020-06-24 | WordPress default "Hello world!" post. **Shows the author byline as `pushkard@gmail.com`** (personal email made public) |
| `/category/uncategorized/` | 200 | n/a | Default category archive (lists Hello world) |
| `/feed/`, `/comments/feed/` | 200 | n/a | RSS feeds |
| `/about/`, `/pricing/`, `/subscribe/`, `/privacy-policy/`, `/terms/`, `/blog/` | **404** | n/a | These pages do not exist. **No privacy policy or terms page anywhere** |
| `/login/` and `/wp-login.php` | 200 | n/a | WordPress admin login (`/login/` redirects to wp-login.php) |
| http/non-www | 301 | n/a | `http://barakhadi.com` → `https://barakhadi.com` → `https://www.barakhadi.com/` (two hops) |

Header nav: Home, FAQ, Contact Us, Login (→ `https://marathi.talentlms.com`). The footer nav repeats Home / FAQ / Contact Us. Footer text: "© 2026 Barakhadi LLC. All rights reserved." There are no social links and no blog.

### 1.2 Home page (`/`)

Title: `Barkhadi – Learn Marathi made Fun and Easy!`. The WordPress site name is misspelled as **"Barkhadi"**, and that typo appears in every page title and in the RSS feed. Sections in order:

1. **Header**: logo `wp-content/uploads/2020/06/barakhadi-logo.png` plus the nav.
2. **Hero**: full-width image `barakhadi_home_hero_image.jpg` (alt is empty).
3. **H1** "A Web based Marathi language learning program", followed by the images `product_name.png` and `gappa_goshti.png`. The product was originally branded "Gappa Goshti".
4. **Three feature columns** (icons `icon_01-stepwise.png`, `icon_04-anywhere.png`, `icon_06-interactive.png`):
   - **Stepwise Learning**: "Fosters speaking skills through 30 kid friendly conversational topics." "Created by teachers with several years of Marathi teaching experience and IT experts with several years of technical and product development experience."
   - **Learn Anywhere**: "Dual use – in class and home. Effectively bridges teacher-student-parent inter phase." "Learning management system (LMS) hosted program enables tracking individual progress."
   - **Interactive & Live**: "Fun, interactive, audio-visual Marathi learning web program – 100 activities." "Dynamic, current and relevant content."
5. **H2 "Available for subscription"**: a heading only, with **no button, price or link**.
6. **H2 "See it in action"**: Wistia video embed, media id `ktanuvwk0f`.
7. **H2 "Try it yourself" / "Try these free activites"** (typo in the original). Three cards with sticker images, each linked to a TalentLMS shared-course key:
   - Conversation Activity → `https://marathi.talentlms.com/shared/start/key:EOSNHRKM` (the image links to `/plus/courses/shared/start/EOSNHRKM`)
   - Vocabulary Activity - ड → `.../shared/start/key:EQLNHRKM` (image → `/plus/courses/shared/start/EQLNHRKM`)
   - Writing Activity - ग → `.../shared/start/key:EGBNHRKM` (image → `/plus/courses/shared/start/EGBNHRKM`)
   - Verified: with cookies enabled, the `key:` links start a guest session (302 → `/learner/course/id:305` → `/unit/view/id:1969`, "Week 01 - Greetings (s01_w01_c1) | Sem. 1 - Week 1 - Conversation"). That unit is an Articulate Storyline package with a signup form below it. Without cookies they bounce to the TalentLMS login page.
8. Buttons: FAQ (`/faq`) and Contact Us (`/contact-us`).
9. **H2 "Already have an account?"** with a "Login Here" link to `https://marathi.talentlms.com`.

There are **no links to Stripe, PayPal, a signup page or a pricing page** anywhere on the live site. The FAQ is the only place that states the price.

### 1.3 FAQ (`/faq/`)

H1 "FREQUENTLY ASKED QUESTIONS", then H2 "FAQs" with an accordion of 13 questions:

1. What is Gappa Goshti program?
2. What are the benefits of Gappa Goshti Web program?
3. Who can use this program and how? ("Anyone who wants to learn Marathi!" Works in class and at home.)
4. What are the benefits for students of this program?
5. How does it help students who are already in BMM Shala? (BMM = Brihan Maharashtra Mandal Marathi Shala)
6. I'm a Marathi Shala teacher. How is the program useful for me? (weekly lesson plans, assign homework, track progress)
7. As a Marathi Shala teacher, is teacher preparation required? ("designed for 30 classes … Each class has three activities – a conversation topic, vocabulary game and writing practice.")
8. How is it different from other Marathi learning apps? ("promotes learning through conversation")
9. How does the program work? (cloud hosted, unique login ID and password)
10. Does it work on mobile devices? (iPad, Android tablet, Chromebook)
11. **How much does it cost?** "The program costs **$5 per month per student** and comes with subscription for a year. As part of the subscription you will get immediate access to **100 interactive activities**. We can customize the package for Marathi shala groups based on the student – teacher ratio."
12. Is there trial for the web program? ("three trial activities" plus the video)
13. How do I subscribe? (points back to the home page trial activities and `/contact-us`; there is no actual way to subscribe)

Closing H2: "Don't see your question?" with a Contact Us button.

### 1.4 Contact (`/contact-us/`)

H1 "CONTACT US". H2 "Got questions? Need more info?" H2 "Send an email to **info@barakhadi.com** or simply fill out the form below:"

The form is an **Elementor Pro Form widget** that posts via admin-ajax and is protected by **Google reCAPTCHA**. Fields: Name, Email, Phone, City/Country, Message. Submit button: "Send". Email delivery is most likely handled by the **FluentSMTP** plugin (its REST namespace is present). Submissions may also be stored in Elementor's Form Submissions.

### 1.5 Videos (`/videos/`)

H2 "Videos", then "Barakhadi Demo" (Wistia `pde62e1mhu`) and "Barakhadi Teacher Tutorial" (Wistia `mkwnt2h471`). The home page uses a third Wistia video, `ktanuvwk0f`.

### 1.6 Brand assets (live)

- Logo: `/wp-content/uploads/2020/06/barakhadi-logo.png` (4.5 KB). Favicon: `cropped-barakhadi_favicon-{32,180,192}.png`.
- Images: `barakhadi_home_hero_image.jpg` (62 KB), `product_name.png`, `gappa_goshti.png`, three icon PNGs, and three activity stickers `2020/07/{conv_1,vocab_d,writing_g}_sticker.png`.
- Colors (Kadence global palette and Elementor CSS): green **#119B49 / #129B49**, orange **#F7941D**, blue **#1B75BC / #1C75BC**, red #D44235, dark green #13612E, black #000, grey #555, white.
- Font: **Open Sans** (regular, 700) from Google Fonts.

### 1.7 SEO basics (live)

| Item | Status |
|---|---|
| `<title>` | Present, but uses the "Barkhadi" typo on every page |
| Meta description | **Missing** on all pages |
| Canonical | Present (WordPress core) |
| Open Graph / Twitter tags | **Missing** |
| JSON-LD schema | **Missing** (only a Kadence microdata `itemtype=WebPage` on `<html>`) |
| hreflang | Missing |
| `lang` | `en-US` |
| H1 | Home has an H1. FAQ and Contact use uppercase H1s. The Videos page has no H1 |
| Image alt text | Mostly empty. Only the logo has alt text |
| Sitemap | WP core sitemap, which includes junk URLs (`/test/`, `/sample-page/`, `/hello-world/`, `/category/uncategorized/`) |
| SEO plugin | None |
| Legal pages | None (no privacy policy or terms), a problem for a children's product (COPPA) |
| Analytics | **None found**: no GA4, GTM, Meta pixel, Clarity or Hotjar |

### 1.8 Tech fingerprint (live)

- **Server**: nginx on Cloudways with the **Breeze** cache plugin 2.6.1 (headers `X-Breeze-Cache-Write: SUCCESS`, `Cache-Provider: CLOUDWAYS-CACHE-DC`, `X-Cache: HIT`) and gzip. No Cloudflare (no `cf-ray`). No security headers (no HSTS, CSP or X-Frame-Options).
- **Generator**: WordPress 7.1.3 and Elementor 4.3.4 (`css_print_method-external, google_font-enabled`). **Elementor Pro 4.3.1**.
- **Theme**: **Kadence** 1.5.2.
- **Plugins** seen in the HTML and REST namespaces: Elementor, Elementor Pro, Elementor AI, `elementor-one`, `elementor-mcp-composer` (v1.0.19), WordPress `mcp` adapter and `wp-abilities`, Breeze, **Wordfence** + Wordfence Login Security, **FluentSMTP**, **All-in-One WP Migration** (`ai1wm`).
- **Third-party scripts**: Wistia (`fast.wistia.com` E-v1.js and a jsonp file), Google Fonts, Google reCAPTCHA (contact page). jQuery 3.7.1, jQuery Migrate and jQuery UI core are loaded.
- **Page weight (home)**: HTML 77 KB uncompressed (13.8 KB gzipped). 25 `<script>` tags (14 external) and 10 stylesheets (Breeze-minified Kadence and Elementor CSS). About **1.06 MB** uncompressed of first-party CSS, JS and images, before Wistia. The single largest file is Elementor Pro `elements-handlers.min.js` at 292 KB. TTFB is about 0.2 s (cached).
- The REST user listing is blocked (401), which is good. The author email still leaks through the Hello world post byline.

---

## 2. WIP redesign: https://phpstack-1560311-6053934.cloudwaysapps.com/ (static HTML)

Server: nginx (Cloudways), with the response header `X-Robots-Tag: noindex, nofollow` (good for staging). Files were last modified on 2025-12-13 (home, index-v2, DESIGN_SYSTEM) and 2025-12-16 (subscribe, thank-you). There is no `robots.txt`, no `sitemap.xml` and no custom 404 page (it serves the default nginx 404).

### 2.1 Page status

| URL | Status | Notes |
|---|---|---|
| `/` = `/index.html` (identical) | 200 | Main redesign home, uses `css/styles.css` |
| `/index-v2.html` | 200 | Older variant with inline CSS. **Shows a visible developer note** ("✅ HERO SECTION - Final Updates Applied: … 📸 Hero Image: Replace with transparent PNG/AVIF in production"). Broken image and favicon paths (`hero_image.png`, `mainbarakhadilogo.png`, `barakhadi_favicon.png` at the root all return 404). Footer email is a baked-in Cloudflare `/cdn-cgi/l/email-protection` link, which is broken on Cloudways (decodes to info@barakhadi.com) |
| `/subscribe.html` | 200 | Signup + Stripe checkout page (works as a page; logo and favicon paths are broken) |
| `/thank-you.html` | 200 | Post-payment page. Redirects to `/` if `?session_id` is missing |
| `/DESIGN_SYSTEM.html` | 200 | Internal design-system documentation (publicly reachable) |
| `/about.html`, `/faq.html`, `/contact.html`, `/who-its-for.html`, `/index-with-outfit-font.html` | **404** | Not deployed |
| Linked from the nav/footer but missing: `for-parents.html`, `for-teachers.html`, `for-learners.html`, `activities.html`, `how-it-works.html`, `pricing.html`, `privacy.html`, `terms.html` | **404** | Every nav link except Home is broken |
| `css/styles.css` (27.8 KB) and `assets/images/*` | 200 | Logo `mainbarakhadilogo.png` (4.4 KB), `barakhadi_favicon.png`, six activity screenshots in AVIF (39–152 KB each) |

### 2.2 Home (`/index.html`)

`<html lang="mr">` (wrong: the page content is English). Title "Barakhadi - Learn Marathi the Fun Way". Has a meta description ("Learn Marathi the fun way with Barakhadi - Interactive activities for conversation, reading, and writing designed for kids, loved by families") and meta keywords. **No canonical, no OG/Twitter tags, no JSON-LD.** No `<script>` at all, so the level tabs are not interactive.

Nav: Home, For Parents, For Teachers, For Learners, Activities, Pricing, About, FAQ, **Login (`#`, not linked)**.

Sections:
1. **Hero**: H1 "Learn Marathi the Fun Way", Marathi tagline "**चला शिकू या मराठी**", "An interactive way to learn to read, write, and speak Marathi." CTAs: "Try Free Activities" (`#activities-preview`) and "See How It Works" (`how-it-works.html`, 404). An animated photo strip of six activity screenshots (clock, number tracing, word search, crossword, join the dots, prepositions).
2. **What is Barakhadi?**: H2 "The modern way to learn and practice Marathi". "**Over 300 online interactive activities** designed to make language learning feel like play, not study." Badges: 300+ Activities · 3 Skill Levels · Any Device · Self Paced.
3. **H2 "Master Marathi Through Three Core Skills"**: Conversation ("30 kid-friendly topics"), Reading, Writing (Devanagari tracing). Each links to `activities.html#…` (404).
4. **H2 "Why Families Choose Barakhadi"**: Effortless Learning / Learn Anywhere / Reinforced Learning.
5. **H2 "Try It Yourself—Free!"**: "No signup required. Start learning in 30 seconds." Level tabs: Level 0 - शिशु वर्ग / Level 1 - पहिली / Level 2 - दुसरी. Three cards (Conversation "Family Introductions", Vocabulary - ड, Writing - ग) whose "Start Activity →" links are **all `#`**: the TalentLMS trial links from the live site are not wired in. "Want full access to 100+ activities across all levels? Get Started →" links to `contact.html` (404).
6. **About teaser**: placeholder text "Team Photo" (no image). Deepti Pandit, "Elementary Teacher (15 yrs) / Marathi Teacher (20+ yrs)". Pushkar Damle, "Product & Analytics (22 yrs)". H2 "Created by Teachers Who Care". Copy: "Barakhadi was born from a simple goal: help families keep their Marathi heritage alive." "…preparing for a biliteracy exam…" "More than just an app, Barakhadi is a bridge between generations." The "Read Our Full Story" link goes to `about.html` (404).
7. **Final CTA**: H2 "Ready to Start Your Marathi Journey?" with "Try Free Activities" and "Contact Us to Get Started" (contact.html, 404), plus "View FAQ" (404).
8. **Footer**: columns Product / Resources / Company / Legal / Connect. Email **hello@barakhadi.com**. "© 2024 Barakhadi … Made with ❤️ for Marathi learners everywhere."

`index-v2.html` has the same structure but replaces "What is Barakhadi" with **"Who Is This For?"** persona cards: For Parents ("I want my kids to speak Marathi with their grandparents"), For Teachers, For Adult Learners.

### 2.3 Subscribe flow (`/subscribe.html` → Stripe → `/thank-you.html`)

**Subscribe page**: H1 "Start Your Marathi Learning Journey". "One year of unlimited access to interactive Marathi lessons designed for all ages". Benefits: 300+ activities, 3 skill levels, any device, "**No Auto-Renewal - Simple one-time payment for full year**". Price card: "**$60** · 365-Day Access · All levels included · Immediate access · Email support included". This header and footer copy the live WordPress site: nav links to `/`, `/faq`, `/contact-us` (WordPress-style URLs that 404 on the staging host), and Login goes to **`https://indml-marathi.talentlms.com`**, a different TalentLMS portal from the live site's `marathi.talentlms.com`. Footer: "© 2025 Barakhadi LLC".

Form "Create Your Account" (`#signup-form`):
- Fields: Email (with the note "Parent email if account is for a minor under 18"), Password (minimum 8 characters with upper, lower and a number, plus a show/hide toggle), Student first and last name, Age group (Under 5 / 5-10 / 11-18 / 18+), Level (0 Beginner / 1 Intermediate / 2 Advanced), Parent name (required if the learner is a minor), reCAPTCHA v2 (site key `6Lck4iksAAAAACI5c1ghqLwdnDHkWylvla2c_wQu`), and a Terms/Privacy checkbox linking to `/terms` and `/privacy` (neither exists).
- JS endpoints on the **Cloudflare Worker `https://barakhadi-subscription.pushkard.workers.dev`**:
  - `POST /api/check-email` runs when the email field loses focus. It checks whether the email already exists (the comment says "Email exists in TalentLMS"). If the check fails, it treats the email as available.
  - `POST /api/create-checkout-session` sends email, **password**, student names, age group, parent name, level and the reCAPTCHA token. It receives `sessionId`, then calls `stripe.redirectToCheckout({sessionId})`. Stripe.js v3 loads from `js.stripe.com`.
  - Stripe key is **`pk_test_…` (TEST mode)**. Live checkout is not configured.
  - `console.log('Sending form data:', formData)` **logs the plaintext password to the browser console**. Remove this before launch.
  - `redirectToCheckout` is a legacy Stripe.js method. Consider redirecting to the session URL instead.
- Worker probe (read-only): the root returns 404. A CORS preflight returns 204 with `Access-Control-Allow-Origin: *` and allows the `Stripe-Signature` header (so a webhook endpoint exists). `GET /api/verify-enrollment?session_id=bogus` returns `{"enrolled":false,"error":"Session not found"}`, so the Worker is deployed and responding.

**Thank-you page**: reads `session_id` and shows "Verifying Your Enrollment...". After 5 seconds it calls `GET /api/verify-enrollment?session_id=…` up to three times (10 s timeout each, 2 s between attempts). It then **always shows "Payment Successful! 🎓 Your Account Has Been Created!" with confetti, even when verification fails**, using "your email" as a fallback. Copy: confirmation email with login credentials "within the next 5 minutes", next steps, "Email: **support@barakhadi.com**", "Login URL: indml-marathi.talentlms.com", and a "Go to Learning Portal →" button linking to `https://indml-marathi.talentlms.com`.

Inferred architecture: static page → Worker → Stripe Checkout (one-time $60 payment) → Stripe webhook → Worker creates the TalentLMS user (with the password the user chose) and enrolls them in a level → thank-you page polls the Worker.

### 2.4 Design system (`/DESIGN_SYSTEM.html`) and visual style

- Fonts: **Quicksand** (headings, buttons) and **Nunito** (body), from Google Fonts. The doc's own checklist says "Use system fonts (no external font loading)", which contradicts this.
- Colors (`styles.css` tokens): orange `#FF9500` (primary buttons), green `#119B49` / `#0D7A37`, blue accent `#1976D2` (recommended for labels and links), red `#D32F2F`, yellow `#FFC800`, purple `#CE82FF`. Text `#1a1a1a` / `#4a4a4a`. Backgrounds white, `#F7F9FA`, cream `#FFF8E1`. Gradients: hero purple `#667eea → #764ba2` (approved), CTA purple-blue `#5B3A9E → #1976D2`. The green and orange live-site brand colors are kept, but the approved hero and CTA gradients are purple, which is not a brand color.
- Spacing scale from 8 to 115 px, radii from 8 to 24 px, pill buttons (50 px radius), generous padding described as "Duolingo-like". The doc also covers heading hierarchy, semantic HTML, an SEO and meta checklist, WCAG AA notes, breakpoints and animation (including reduced-motion handling).
- Overall style: a modern, playful, emoji-heavy edtech landing page in the Duolingo vein, much more polished than the 2020 Elementor site.

### 2.5 Completeness compared with the live site

| Live-site content | In the WIP? |
|---|---|
| Home value proposition | Yes, rewritten and expanded (300+ activities, 3 levels, 3 skills) |
| Free trial activities (TalentLMS shared keys) | Cards exist, **links are `#`** |
| Demo video (Wistia) | **Missing** |
| `/videos/` (Demo + Teacher Tutorial) | **Missing** |
| FAQ (13 Q&As) | **Missing** (`faq.html` 404) |
| Contact form + info@ email | **Missing** (`contact.html` 404). No form handler chosen |
| Login link | Home: `#`. Subscribe/thank-you: `indml-marathi.talentlms.com` |
| Pricing | Only on subscribe.html ($60 one-time). `pricing.html` 404 |
| Teacher / BMM Shala positioning | Only a nav label (For Teachers, 404). The FAQ teacher content has not been carried over |
| Legal pages | Linked but 404 |

Estimate: about 25–30% complete. Two finished marketing pages (home and a variant), a functional but test-mode subscribe/checkout flow, and a design-system doc. Eight or more linked pages are missing.

### 2.6 Inconsistencies to resolve

- **Activity count**: live says 100 activities. WIP says "300+" in the hero and "100+" in the trial section.
- **Price model**: live says "$5 per month per student, subscription for a year". WIP says "$60 one-time, no auto-renewal" (the same $60 per year, framed differently). The live FAQ's school and group pricing has no equivalent.
- **Emails**: info@ (live and index-v2), hello@ (WIP home), support@ (thank-you).
- **TalentLMS portal**: `marathi.talentlms.com` (live) versus `indml-marathi.talentlms.com` (new flow). Confirm which one is canonical.
- **Copyright years**: 2026 (live), 2024 (WIP home), 2025 (subscribe).
- **Product name**: "Gappa Goshti" (live FAQ and images) versus "Barakhadi". Also the "Barkhadi" typo in the WordPress site name.
- **Root-relative paths** in subscribe, thank-you and index-v2 (`/mainbarakhadilogo.png`, `/barakhadi_favicon.png`) 404. The real files are in `assets/images/`.

---

## 3. What must be carried over to the new site

**URLs to preserve or 301-redirect**
- `/` → new home
- `/faq/` → keep the same path, or 301 to the new FAQ (the WIP's `/faq` links already assume it)
- `/contact-us/` → keep the same path, or 301 to the new contact page (subscribe.html already links to `/contact-us`)
- `/videos/` → 301 to a How it works or demo page that includes the videos
- `/feed/` → retire (410) or 301 to home
- Junk URLs `/test/`, `/sample-page/`, `/hello-world/`, `/category/uncategorized/` → 410, or 301 to home. Do not carry them over, and remove the email byline.
- `/wp-admin`, `/wp-login.php`, `/wp-json/*` → these disappear. They need no redirects.
- Keep the www canonical host and https, and collapse the two-hop redirect into one 301.
- New: `robots.txt` and `sitemap.xml` listing only real pages. Remove `noindex` when going live.

**Content**
- All 13 FAQ answers (update the pricing and activity counts), including the BMM Shala and teacher Q&As.
- Contact email(s) and a working contact form with spam protection (replacing Elementor Forms, reCAPTCHA and FluentSMTP).
- The three free-trial TalentLMS links (`key:EOSNHRKM`, `key:EQLNHRKM`, `key:EGBNHRKM`), verified to work as guest sessions.
- Wistia videos `ktanuvwk0f` (home), `pde62e1mhu` (Demo) and `mkwnt2h471` (Teacher Tutorial). Alternatively, migrate them to self-hosted or YouTube.
- Teacher and classroom value proposition ("30 classes, 3 activities each: conversation, vocabulary, writing"; assign homework; track progress) and the school/group pricing note.
- The login link to the correct TalentLMS portal.
- Brand assets: logo, favicon, activity stickers, green #119B49 and orange #F7941D, "Barakhadi LLC" legal name.

**Must add (missing on both sites)**
- Privacy policy and terms of service, especially COPPA-relevant wording for an under-13 audience. The subscribe form already requires agreement to both.
- Meta descriptions, OG/Twitter tags and image, JSON-LD (Organization, Product/Offer, FAQPage), alt text, a correct `lang` (`en` with `lang="mr"` on Marathi spans), and a canonical tag.
- Analytics (GA4 or a privacy-friendly alternative) plus conversion tracking on checkout.
- Before launch: a Stripe live key, removal of the password `console.log`, a thank-you page that does not claim success when verification fails, and a decision on which TalentLMS portal to use.
