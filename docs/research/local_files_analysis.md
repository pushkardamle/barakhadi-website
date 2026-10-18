# Barakhadi website rebuild: analysis of local files

Folder analysed: `A:\Barakhadi AI Website` (read only; nothing was modified). Skipped: `stripe.exe` (Stripe CLI, 31.6 MB, Dec 13 2025) and the empty `barakhadi-web/`.
Analysis date: 2026-10-17. All secret values below are masked to their first 4 characters.

---

## 0. Executive summary

- The work ran in four bursts: **Dec 6–10 2025** (home page in Claude Code, design system), **Dec 12–15 2025** (subscribe and thank-you pages with Stripe, reCAPTCHA and a TalentLMS-integrated Cloudflare Worker, iterated in Claude Desktop and committed to git), **Dec 16 2025** (Claude Desktop wireframes plus draft About/FAQ/Contact/Who-it's-for pages, never committed), and **Jan 10 2026** (CSS refresh: Outfit headings, green hero, darker orange). Nothing has changed since Jan 11 2026, except `.vscode/settings.json`, which was touched today.
- **The most mature asset is the payment flow** (`Barakhadi-New/subscribe.html` + `thank-you.html`, commit `25f76a1`, Dec 15). The Worker that backs it (`barakhadi-subscription.pushkard.workers.dev`) is **not in the folder**. Its source, `wrangler.toml` and secrets exist only on Cloudflare or on another machine.
- The **home page is split across incompatible versions**. Committed `index.html` (Quicksand, 7 sections, real screenshots) is now styled by an **uncommitted** `css/styles.css` that expects the **Outfit** font, which `index.html` does not load. Claude Desktop's `Dec 16/index.html` follows the wireframe more closely, but it uses a different CSS system and has placeholder images.
- **Plaintext secrets** (Stripe test secret key, Stripe webhook secret, reCAPTCHA secret keys and two passwords) sit in `Misc Barakhadi website with Claude code.txt`, and one password is also in `shell_commands.txt`. **None of these were committed to git.** Git holds only public keys (Stripe `pk_test`, reCAPTCHA site keys). The GitHub repo **is public**: `api.github.com/repos/pushkardamle/barakhadi-new` returns HTTP 200 without auth.
- The draft content contradicts itself on facts: 100+ vs 300+ activities, auto-renewal vs no auto-renewal, manual 1–2 day setup vs instant account creation, "Pushkar Deshpande" vs "Pushkar Damle", `marathi.talentlms.com` vs `indml-marathi.talentlms.com`, and "Hindi" with बरखड़ी vs Marathi बाराखडी.

---

## 1. File-by-file inventory

Status key: **CANONICAL** = latest or best version to build from; **SUPERSEDED** = an older iteration; **DUPLICATE** = byte-identical (or identical apart from line endings) to another file; **REFERENCE** = supporting material.

### 1.1 Git timeline (`Barakhadi-New`, branch `main`, up to date with `origin/main`)

| Commit | Date | Message | What changed |
|---|---|---|---|
| 2ae1f7e | 2025-12-06 | Initial Barakhadi landing page | `index` placeholder ("Coming soon") |
| 6c292cc | 2025-12-06 | Initial Barakhadi Landing Page with Claude | first `index.html` |
| b18e0b6 | 2025-12-07 | Initial wireframe from Claude | `index.html`, `index-v2.html`, `css/styles.css` (1071 lines), README, logo/favicon/hero_image.png, `.claude/settings.local.json` |
| 1ffe74b | 2025-12-12 | Added subscription pages | DESIGN_SYSTEM.html, concept_1, section_2, AVIF screenshots, hero_image.png deleted, **subscribe.html + thank-you.html** first version (old reCAPTCHA site key) |
| 32c4daf / dd01369 / c11b20f | 12-12 → 12-13 | Added subscription pages v3 | new reCAPTCHA site key, title tweaks, "- Test" subtitle |
| ea3f1a3 | 2025-12-13 | Added validation for subscription form | email-availability check (`/api/check-email`); thank-you gains verify-enrollment polling and error state |
| 31f49a1 | 2025-12-13 | fixed subscription page | = `subscribe-corrected.html` |
| d4971e5 | 2025-12-13 | subscription page validation fixed | = `subscribe-with-email-blocking.html` |
| 8bb85cc | 2025-12-13 | visual improvements validations | = `subscribe-final-with-icons.html` |
| 8ce7fae | 2025-12-13 | (same msg) | thank-you = `thank-you-with-retry.html` |
| a69e972 | 2025-12-13 | (same msg) | thank-you = `thank-you-bulletproof.html` |
| e7d1a7d | 2025-12-13 | (same msg) | thank-you ≈ `thank-you-branded-final.html` + confetti |
| **25f76a1** | **2025-12-15** | (same msg) | **subscribe = `subscribe-redesigned.html`, thank-you = `thank-you-redesigned.html` (current HEAD)** |

Working tree: `css/styles.css` **modified, not committed** (Jan 10 Outfit/green refresh). Untracked: `css/old_styles.css`, `css/old_2_styles.css`, `styles-updated.css`, `index-with-outfit-font.html`. There is no `.gitignore` and no CI or deploy config.

### 1.2 `Barakhadi-New/`

| File | Date | Size | What it is | Status |
|---|---|---|---|---|
| `subscribe.html` | 2025-12-15 | 42,566 | Signup + Stripe Checkout page (inline CSS/JS, Quicksand/Nunito) | **CANONICAL** subscribe page (= `Claude desktop files/subscribe-redesigned.html`, = files.zip) |
| `thank-you.html` | 2025-12-15 | 24,275 | Post-payment page; polls Worker; confetti | **CANONICAL** thank-you (= `thank-you-redesigned.html`) |
| `index.html` | 2025-12-10 | 19,560 | Home page, 7 sections, `lang="mr"`, uses `css/styles.css`, loads Quicksand | **Best committed home page**, but font-mismatched with the current CSS (see §2.4) |
| `css/styles.css` | 2026-01-10 20:58 | 27,865 | Main mobile-first stylesheet (1479 lines), Jan 10 version **plus manual tweaks** (hover `#CC7A00`, hero h1 weight 700) | **CANONICAL CSS** (uncommitted) |
| `styles-updated.css` | 2026-01-10 20:27 | 27,877 | Claude Desktop Jan 10 output | DUPLICATE of `css/old_2_styles.css` and `Claude desktop files/Jan 10/styles.css`; superseded by `css/styles.css` |
| `css/old_2_styles.css` | 2026-01-10 20:28 | 27,877 | Backup | DUPLICATE (as above) |
| `css/old_styles.css` | 2025-12-10 | 27,814 | Backup | DUPLICATE of committed HEAD `css/styles.css` (purple hero, Quicksand) |
| `index-with-outfit-font.html` | 2026-01-10 20:58 | 4,966 | **Header + hero only** sample with Outfit font link (600;700) and new nav (Who Barakhadi is for / Activities / Pricing / About / Contact / FAQ) | Partial; newest nav and font link. Superset of the Jan 10 desktop version, but with weight 800 dropped from the font URL |
| `index-v2.html` | 2025-12-07 | 36,183 | Early home page with inline CSS, hero_image.png, audience cards; broken image paths (`mainbarakhadilogo.png` at root) | SUPERSEDED |
| `concept_1_final_refined.html` | 2025-12-07 | 9,896 | Prototype of the polaroid "photo strip" hero; says "Interactive **Hindi** learning", title बरखड़ी | SUPERSEDED (concept demo) |
| `section_2_with_fonts_2.html` | 2025-12-09 | 19,417 | Demo of section 2 ("What is Barakhadi") with Quicksand + Nunito rationale | SUPERSEDED (folded into index.html) |
| `DESIGN_SYSTEM.html` | 2025-12-09 | 42,624 | Design system doc (colors, type, spacing, components, SEO, a11y, breakpoints, animation) | REFERENCE; partly outdated (purple hero, Quicksand) |
| `README.md` | 2025-12-07 | 2,146 | Project readme (structure, palette, breakpoints) | Outdated (lists hero_image.png, system fonts, blue `#1CB0F6`) |
| `.claude/settings.local.json` | 2025-12-07 | 100 | Claude Code permission `Bash(tree:*)` | Harmless; committed |
| `assets/images/mainbarakhadilogo.png` | 12-07 | 4,427 | Logo "बाराखडी" with flower mark. **Actually a JPEG** with a .png extension (no transparency) | Reusable, but re-export as SVG/PNG |
| `assets/images/product_name.png` | 12-07 | 11,688 | "चला शिकू या मराठी" orange outlined tagline. **JPEG** with a .png extension | Reusable |
| `assets/images/barakhadi_favicon.png` | 2020-06-25 | 10,782 | 520×520 favicon | Reusable |
| `assets/images/barakhadi_hero_image.avif` | 12-07 | 49,592 | Hero image | Unused by any page |
| `assets/images/ss_*_result.avif` (9 files) | 12-07 | 39–152 KB | Activity screenshots (clock, clock_2, crossword, numbers_51_60, join-the-dots, numbers_trace, prepositions, snow, word_search) | Reusable. 6 are used in the hero photo strip; `ss_clock_2`, `ss_snow` and `ss_numbers_51_60` are unused |

### 1.3 `Claude desktop files/`

| File | Date | Size | What it is | Status |
|---|---|---|---|---|
| `BARAKHADI_WEBSITE_WIREFRAMES.md` | 2025-12-16 23:27 | 53,285 | Full wireframes + copy for Home, Who We Serve, Pricing, About, FAQ, Contact, global components | **CANONICAL content plan** (see §3) |
| `subscribe.html` | 2025-12-12 22:34 | 30,054 | Subscribe v1 (= git 32c4daf) | SUPERSEDED |
| `subscribe-corrected.html` | 12-13 18:54 | 32,916 | = git 31f49a1 | SUPERSEDED |
| `subscribe-with-email-blocking.html` | 12-13 19:08 | 34,418 | = git d4971e5; blocks submit until email is checked | SUPERSEDED |
| `subscribe-final-with-icons.html` | 12-13 19:13 | 37,353 | = git 8bb85cc | SUPERSEDED |
| `subscribe-redesigned.html` | 12-15 23:34 | 42,566 | = `Barakhadi-New/subscribe.html` | DUPLICATE of canonical |
| `thank-you.html` / `old-thank-you.html` | 12-12 21:09 | 9,428 each | Static v1 (no JS); points to `marathi.talentlms.com` | DUPLICATES of each other; SUPERSEDED |
| `thank-you-enhanced.html` | 12-13 18:37 | 16,087 | = git ea3f1a3; single verify call after 3 s; error state | SUPERSEDED |
| `thank-you-with-retry.html` | 12-13 21:17 | 17,240 | = git 8ce7fae; 3 attempts. **Contains Cloudflare email-obfuscation markup** (`/cdn-cgi/l/email-protection`, `email-decode.min.js`), so it was saved from a Cloudflare-proxied page | SUPERSEDED |
| `thank-you-bulletproof.html` | 12-13 21:34 | 18,989 | = git a69e972; 15 s global timeout; error state | SUPERSEDED |
| `thank-you-branded-final.html` | 12-13 21:45 | 18,113 | Per-attempt 10 s AbortSignal; always shows success; still has unused error-state markup; no confetti | SUPERSEDED (git e7d1a7d = this + confetti) |
| `thank-you-redesigned.html` | 12-15 23:34 | 24,275 | = `Barakhadi-New/thank-you.html` | DUPLICATE of canonical |
| `files.zip` | 12-15 23:34 | 13,038 | subscribe-redesigned.html + thank-you-redesigned.html | DUPLICATE (contents identical) |
| `files3.zip` | 12-16 23:40 | 12,684 | `Dec 16/index.html`, `Dec 16/who-we-serve.html`, **`WEBSITE_BUILD_STATUS.md` (only copy; not extracted anywhere in the project)** | Contains one unique file |
| `files4.zip` | 12-16 23:54 | 26,383 | Everything in `Dec 16 - 2/` | DUPLICATE (contents identical) |
| `Dec 16/index.html` | 12-16 23:40 | 32,989 | Home page built to the wireframe (subscribe-page styling, inline CSS, working skills tabs JS, email-capture form with no backend, placeholder founder photos, "Pushkar Deshpande", hero बराखडी without photo strip) | Alternative home; closest to the wireframe |
| `Dec 16/who-we-serve.html` | 12-16 23:40 | 19,947 | Persona deep-dive with comparison table; references `/hero_image.png`, `/lms_platform.jpg` (missing) | SUPERSEDED by who-its-for.html in naming, but has the comparison table |
| `Dec 16 - 2/index-complete.html` | 12-16 23:55 | 33,023 | Another home page (index-v2 lineage: hero_image.png, audience cards, non-functional level tabs, no JS, tiny base64 placeholder logos, links to `marathi.talentlms.com`) | SUPERSEDED / inferior to `Barakhadi-New/index.html` |
| `Dec 16 - 2/who-its-for.html` | 12-16 23:55 | 19,041 | Parents / Teachers / Adult learners + Seal of Biliteracy callout; strong copy | **Most advanced who-its-for page** |
| `Dec 16 - 2/about.html` | 12-16 23:55 | 12,157 | Story, team (Deepti Pandit, Pushkar Damle), values | **Most advanced about page** |
| `Dec 16 - 2/faq.html` | 12-16 23:55 | 21,024 | 15-question accordion with JS | **Most advanced FAQ** (content contradicts the subscribe flow) |
| `Dec 16 - 2/contact.html` | 12-16 23:55 | 12,695 | Contact info + form (`action="#"`, no backend, no captcha) | **Most advanced contact page** |
| `Dec 16 - 2/WIREFRAME_SUMMARY.md` | 12-16 23:54 | 8,941 | Summary of the Dec 16-2 pages, design tokens, TODOs | CANONICAL summary |
| `Jan 10/CSS_UPDATES_SUMMARY.md` | 2026-01-11 | 5,255 | Changelog for the Outfit/green-hero CSS refresh (dated "Dec 17, 2024" inside, which is wrong) | REFERENCE |
| `Jan 10/styles.css` | 2026-01-10 | 27,877 | = `styles-updated.css` | DUPLICATE |
| `Jan 10/index-with-outfit-font.html` | 2026-01-10 | 4,974 | Header/hero sample with Outfit 600;700;800 | SUPERSEDED by Barakhadi-New copy (only difference is the font weights) |
| `course_default.jpg` | 12-13 | 530,349 | 1451×967 TalentLMS course cover "मराठी" on green-blue gradient | Reusable (LMS) |
| `course_bg.jpg` | 12-13 | 51,351 | 480×320 gradient background | Reusable (LMS) |
| `course_bg.if` | 12-13 | 70,367 | Fabric.js v3.2.0 canvas JSON (TalentLMS image editor): bg image + text "maraOaI" in legacy **AMS Saral** font (= मराठी) | Source for course_default |
| `barakhadi_course_image.jpg` | 12-13 | 1,904 | 640×427 **blank white** image | Throw away |

`WEBSITE_BUILD_STATUS.md` (in files3.zip only, Dec 16): Home and Who-We-Serve marked done; Pricing, About, FAQ and Contact "in progress". It defines the header nav `Home | Who We Serve | Pricing | About | FAQ | Contact | [Login]`, a 3-column footer, breakpoints 1024/768, and says a hamburger menu is still to be implemented.

### 1.4 `Current Site Screeshots/` (Dec 6 2025)

| File | Size | Content |
|---|---|---|
| `Barakhadi_Home_Page.jpg` | 797 KB | Live WordPress/Elementor home page: hero photo (tablet with ख tracing), "A Web based Marathi language learning program", "चला शिकू या मराठी", "गप्पा गोष्टी", 3 feature columns (Stepwise Learning / Learn Anywhere / Interactive & Live, "100 activities", "30 conversational topics"), green "Available for subscription" band, Wistia video, blue "Try it yourself" band, 3 free activity stickers, FAQ/Contact buttons, "Already have an account? Login Here" |
| `Barakhadi_FAQ_Page.jpg` | 376 KB | 13-question accordion about the **"Gappa Goshti"** program (BMM Shala, Marathi Shala teachers, cost, trial, mobile) |
| `Barakhadi_Contact_Page.jpg` | 178 KB | Contact form: Name, Email, Phone, City/Country, Message, invisible reCAPTCHA, Send; "info@barakhadi.com" |

### 1.5 `Firecrawl data/` (scrape of www.barakhadi.com, 2025-12-07T02:27Z)

- `….json` and `… (1).json` (68,683 bytes each) are **duplicates** (same md5).
- `….md`, `(1).md`, `(2).md`, `(3).md` (3,271 bytes each) are **duplicates**.
- Facts captured: WordPress 6.8.3 + Elementor 3.33.2; title "**Barkhadi** – Learn Marathi made Fun and Easy!" (typo); fonts Open Sans; colors primary `#F7941D`, accent `#119B49`, text `#555555`; no og:image; Login → `https://marathi.talentlms.com/`; free activity shared links `…/shared/start/key:EOSNHRKM` (Conversation), `key:EQLNHRKM` (Vocabulary ड), `key:EGBNHRKM` (Writing ग); Wistia video id `ktanuvwk0f` (3:07).

### 1.6 Top level

| File | Date | Size | What it is |
|---|---|---|---|
| `HOME_PAGE_STRUCTURE.md` | 2025-12-08 | 4,763 | "Final approved" 7-section home structure (dated "2024" inside, which is wrong; says "बरखड़ी" and "Hindi") |
| `Misc Barakhadi website with Claude code.txt` | 2026-01-06 | 1,130 | Ops notes: Cloudways account and URL, git/wrangler commands, **passwords and keys** (see §6) |
| `shell_commands.txt` | 2025-12-14 | 251 | Git push and `wrangler tail` commands + a **password** |
| `.vscode/settings.json` | 2026-10-17 (today) | 1,441 | Peacock theme colors (`#c97603`); no secrets |

### 1.7 Most advanced version of each page

| Page | Most advanced | Notes |
|---|---|---|
| Home | `Barakhadi-New/index.html` + current `css/styles.css` (structure, real screenshots, a11y attributes, meta description). Take the header/nav and Outfit font link from `index-with-outfit-font.html` | `Claude desktop files/Dec 16/index.html` is the closest match to the wireframe (personas, tabs with JS, email capture, founders). Merge its sections into the index.html/CSS system |
| Subscribe | `Barakhadi-New/subscribe.html` (HEAD 25f76a1) | Functional against the live Worker |
| Thank-you | `Barakhadi-New/thank-you.html` (HEAD 25f76a1) | Consider restoring the error state from `thank-you-bulletproof.html` |
| About | `Claude desktop files/Dec 16 - 2/about.html` | |
| FAQ | `Claude desktop files/Dec 16 - 2/faq.html` | Answers must be corrected (§8) |
| Contact | `Claude desktop files/Dec 16 - 2/contact.html` | Form has no backend |
| Who it's for | `Claude desktop files/Dec 16 - 2/who-its-for.html` | Pull the comparison table from `Dec 16/who-we-serve.html` |
| Pricing, Activities, Terms, Privacy, How it works | **Do not exist** | Linked from many pages |

---

## 2. Design system

### 2.1 Colors

| Token | Value | Source / use |
|---|---|---|
| Brand orange | `#FF9500` | All docs, subscribe/thank-you, DESIGN_SYSTEM. Primary CTA |
| Orange (Jan 10 CSS) | `#E68600` (`--orange-primary` in current `css/styles.css`) | Darkened "for WCAG contrast"; hover `#CC7A00` (manual tweak), `--orange-light #FFB84D` |
| Orange hover (subscribe) | `#e68600` | subscribe/thank-you `.btn-login:hover`, gradient end |
| Live-site / logo orange | `#F7941D` | Firecrawl branding; Jan 10 Marathi tagline color |
| Brand green | `#119B49` | Everywhere (success, checkmarks, accents) |
| Green dark | `#0D7A37` (CSS) / `#0D7A38` (DESIGN_SYSTEM) / `#0F8A40` (DS hover) | Secondary outline button (Jan 10) |
| Green light | `#E8F5E9`; hero gradient `#66BB6A → #81C784 → #C8E6C9` (Jan 10) | |
| Blue accent | `#1976D2` (DESIGN_SYSTEM "recommended" label/link color, `--blue-accent`) vs `#1CB0F6` (README) | |
| Red | `#D32F2F` (DS) vs error red `#E63946` (subscribe) | |
| Purple | `#CE82FF` (README, CSS); hero `#667eea → #764ba2` (DS "approved", replaced Jan 10); CTA `#5B3A9E → #1976D2` | |
| Yellow | `#FFC800` (CSS), `#FFD700` (confetti), warm gradient `#FF6F00 → #FDD835` | |
| Text | `#1a1a1a` / `#4a4a4a` (DS, CSS) vs `#3d3d3d` / `#333333` / `#6B7280` (subscribe, wireframes) vs `#2B2B2B` / `#666666` (WIREFRAME_SUMMARY) | |
| Backgrounds | `#FFFFFF`, `#fafafa` (DS), `#f8f9fa` (DS, subscribe), `#F7F9FA` (CSS), cream `#FFF8E1`, subscribe hero `#f0fdf4` | |
| Borders | `#E5E7EB` | |
| Tagline border | dark brown `#4A2C0A` | |

### 2.2 Fonts

- **Headings:** Quicksand 700 (DESIGN_SYSTEM, README-era CSS, subscribe/thank-you, all Dec 16 pages, wireframes) → **Outfit 600/700/800** (Jan 10 decision, `css/styles.css` h1–h4 and `.hero-tagline-marathi`). The current CSS still has leftover `'Quicksand'` declarations at lines 587 and 734.
- **Body:** Nunito 400/600/700(/800) everywhere. The README claims system fonts. DESIGN_SYSTEM's performance checklist says "use system fonts (no external font loading)", which contradicts its own Google Fonts import.
- **Devanagari:** no Devanagari web font is loaded anywhere. DESIGN_SYSTEM wrongly says Quicksand/Nunito "render Devanagari beautifully". Neither has Devanagari glyphs; the browser falls back to a system font. WIREFRAME_SUMMARY flags "TODO: Noto Sans Devanagari or Mukta". The live site uses Open Sans plus images for Marathi text. The TalentLMS course art uses the legacy AMS Saral (non-Unicode) font.

### 2.3 Spacing, radius, layout, motion

- CSS scale (`css/styles.css`, "+15%"): `xs 8 / sm 16 / md 24 / lg 35 / xl 55 / 2xl 70 / 3xl 90 / 4xl 115 px`. Radius `8 / 16 / 20 / 24 px`, buttons pill `28px` (DS: `50px`).
- DESIGN_SYSTEM section padding: 115/90 px desktop, 80/60 tablet, 70/35 mobile. Containers 1400 / 900 / 700 px. Margins: label 20, headline 30, subheadline 60, paragraph 20.
- Subscribe and Dec 16 pages: 1200 px max-width, `4rem 2rem` section padding, 8 px button radius, 12–16 px card radius.
- Type scale: DS H1 3.5rem / H2 3rem / H3 1.8rem. CSS mobile-first h1 2→2.5rem, h2 1.75→2.25, hero h1 up to 4rem/800 (Jan 10, then hand-reverted to 700). Wireframe H1 2.5–3rem, H2 2rem.
- Motion: 0.26 s badge interactions, 0.3 s buttons/cards, photo-strip float 11–15 s, prefers-reduced-motion snippet in DS (**not present in `css/styles.css`**).

### 2.4 Components

- **Buttons:** `.btn-primary` (orange), `.btn-secondary` (outline; orange in DS, black in Dec CSS, dark green in Jan CSS), `.btn-outline`, `.btn-white`, `.btn-outline-white`, `.btn-login` (orange, 6px radius), green/red variants (DS).
- **Cards:** flip "badge" with hover reveal (section 2), persona card (lift + blue border), wireframe card (`#f8f9fa`, 12px, 4px green left border), activity card, team member, benefit item, pricing card (orange gradient, sticky), detail cards (thank-you).
- **Patterns:** section label overline (uppercase, letter-spacing 1.5–2px; orange in wireframes, blue in DS), polaroid photo strip hero (3 columns, 8° angle, float animation), skills tabs (Dec 16 index has JS; index.html uses alternating blocks), level tabs Level 0 शिशु वर्ग / Level 1 पहिली / Level 2 दुसरी (no JS anywhere), FAQ accordion (faq.html JS), confetti.
- **Header:** sticky; logo + links + orange Login. **Footer:** dark `#3d3d3d`, 3 or 4 columns, "© 2025 Barakhadi LLC" (the Jan 10 sample says "© 2024 Barakhadi").

### 2.5 Breakpoints

- `css/styles.css`: mobile-first `min-width` 640, 768, **968** (nav appears), 1024, 1200, plus one `max-width: 767px`.
- README: <640, 640–968, >968. DESIGN_SYSTEM and WEBSITE_BUILD_STATUS: <768, 768–1024, >1024.
- Subscribe/thank-you/Dec 16 index: desktop-first `max-width` 1024 / 768. Dec 16-2 pages: single `max-width: 968px`.

### 2.6 Inconsistencies to resolve

1. **Heading font:** Outfit (current CSS) vs Quicksand (every other page). `index.html` loads Quicksand but the CSS asks for Outfit, so headings fall back to generic sans-serif.
2. **Primary orange:** `#FF9500` vs `#E68600` vs `#F7941D`. White on `#FF9500` is about 2.1:1 and on `#E68600` about 2.6:1, so **neither passes WCAG AA** for normal text, despite the Jan 10 claim.
3. **Accent:** blue `#1976D2` vs `#1CB0F6`. Section labels are blue in DS and orange in the wireframes.
4. **Hero:** purple (DS "approved") → green gradient (Jan 10) vs light green/gray (subscribe) vs green-gradient page heroes (Dec 16-2).
5. **Text grays:** three different families (`#1a1a1a/#4a4a4a`, `#3d3d3d/#333/#6B7280`, `#2B2B2B/#666`).
6. **Breakpoints:** three systems, and mobile-first vs desktop-first.
7. **Button shape:** pill (28–50px) vs 8px vs 6px.
8. **Image paths:** `assets/images/…` (index.html) vs root `/mainbarakhadilogo.png` (subscribe, thank-you, Dec 16) vs relative `mainbarakhadilogo.png` (Dec 16-2, index-v2).
9. **Copyright and naming:** "Barakhadi LLC" (live and most pages) vs "Barakhadi" 2024.

---

## 3. Site map and content plan

### 3.1 Navigation (three competing versions)

- Wireframes / WEBSITE_BUILD_STATUS: `Home · Who We Serve · Pricing · About · FAQ · Contact · [Login → indml-marathi.talentlms.com]`
- WIREFRAME_SUMMARY / Dec 16-2 pages: `Home · Who It's For (#parents #teachers #learners) · Activities · Pricing · About · FAQ · Contact · Login (→ marathi.talentlms.com)`
- Jan 10 (latest): `Home · Who Barakhadi is for · Activities · Pricing · About · Contact · FAQ · Login`
- Older index.html: separate For Parents / For Teachers / For Learners pages (superseded by a single persona page).
- Subscribe/thank-you headers mirror the **live WordPress** nav (`/`, `/faq`, `/contact-us`, Login).

### 3.2 Pages

| Page | URL | Status | Key content |
|---|---|---|---|
| Home | `/` | Drafted (several versions) | 7 sections, below |
| Who it's for | `/who-its-for` (or `/who-we-serve`) | Drafted | Parents & Kids (diaspora heritage, ages 6–16), Teachers & Schools (weekend schools, lesson plans, bulk licensing), Adult Learners; Seal of Biliteracy callout; comparison table; future testimonials |
| Pricing | `/pricing` | **Wireframe only** | "Simple, Transparent Pricing"; one card **$60/year**; 300+ activities, all 3 levels, devices, progress tracking, email support, **no auto-renewal**; FAQ (Stripe cards, free trial = 3 activities, **30-day money-back**, school discounts); school pricing for 10+ students |
| About | `/about` | Drafted | Story (challenge → solution), founders Deepti Pandit (15 yrs elementary, 20+ yrs Marathi teaching) and Pushkar Damle (22 yrs product/analytics), values, "By the numbers" (300+ / 3 / 10,000+ practice hours) |
| FAQ | `/faq` | Drafted | Categories: Getting Started, Subscription & Pricing, Learning & Content, Technical, For Teachers (15 Q&As built) |
| Contact | `/contact` | Drafted (no backend) | Form (name, email, category, message); info@ / support@ / schools; "Virginia, USA"; response within 24 h; quick links; school inquiries |
| Activities | `/activities` | **Not started** | Activity types, level breakdown, free TalentLMS shared links, AVIF screenshots |
| Subscribe | `/subscribe` | **Built and wired** | §4 |
| Thank-you | `/thank-you` | **Built and wired** | §4 |
| Free activities landing | n/a | Not started | Email-gated in HOME_PAGE_STRUCTURE; "no signup required" in index.html (contradiction) |
| Terms, Privacy, How it works | `/terms`, `/privacy`, `how-it-works.html` | **Missing** | Linked from subscribe (terms checkbox) and footers |

### 3.3 Home page sections (HOME_PAGE_STRUCTURE + wireframes)

1. **Hero.** Approved headline was "बरखड़ी – Learn & Play" (wrong spelling; built pages use "Learn Marathi the Fun Way" + "चला शिकू या मराठी" + "An interactive way to learn to read, write, and speak Marathi"). CTAs: Try Free Activities / See How It Works. Polaroid photo strip of 6 screenshots.
2. **What is Barakhadi** (label "WHAT WE OFFER"): "Learn Marathi Through Play & Practice" or "The modern way to learn and practice Marathi". 300+ activities, 3 levels, any device, self-paced; video below the text.
3. **Who it's for:** 3 equal persona cards with 4 benefits each and one "Learn more" CTA.
4. **3 core skills** (Conversation, Reading, Writing): tabs with screenshot and bullet list.
5. **Try 3 free activities:** gated with email (wireframe) using the existing TalentLMS shared links.
6. **About us:** two founders, link to full story.
7. **Final CTA:** "Ready to Start Your Marathi Journey?" Primary "Choose Your Plan" → /pricing, secondary Contact.

Out of scope for now: testimonials, pricing on the home page, urgency, user counts.

### 3.4 Messaging and voice

- Pillars: Effortless learning → Learn anywhere → Reinforced learning → Heritage (supporting, not leading).
- Tone: friendly, confident, accessible, playful but not childish. Parents empathetic, teachers practical. Duolingo-inspired minimalism.
- CSS_UPDATES_SUMMARY: Outfit headings, green hero gradient, taller header (logo 55/65px, nav 1.05rem), darker orange, dark-green outline button, hero h1 4rem/800, Marathi tagline orange `#F7941D` with brown border.

---

## 4. Payment / subscription flow

### 4.1 Plan and price

- **One plan: $60, one-time payment for 12 months ("One year of unlimited access", "No Auto-Renewal", "365-Day Access")**. Features: all levels, immediate access, email support, 300+ activities, 3 skill levels, any device. There are no other tiers. Contact-form categories hint at future Individual / Family / School plans.
- The price is **only displayed client-side**. The amount actually charged is decided by the Worker (Stripe Price ID or `price_data`), which can't be verified from here.

### 4.2 `subscribe.html` (canonical, Dec 15)

**External scripts:** `https://js.stripe.com/v3/`, `https://www.google.com/recaptcha/api.js` (reCAPTCHA **v2 checkbox**, `div.g-recaptcha` with site key `6Lck…`).
**Config constants:** `STRIPE_PUBLISHABLE_KEY = 'pk_t…'` (test mode), `RECAPTCHA_SITE_KEY = '6Lck…'` (declared but unused; the div carries the key).

**Form fields (id → payload key):**

| Field | Type | Required | Validation |
|---|---|---|---|
| `email` | email | yes | regex `^[^\s@]+@[^\s@]+\.[^\s@]+$` + server availability check. Help text "Parent email if account is for a minor under 18" |
| `password` | password (show/hide toggle) | yes | ≥8 chars, at least one uppercase, lowercase and digit |
| `student-first-name` → `studentFirstName` | text | yes | non-empty |
| `student-last-name` → `studentLastName` | text | yes | non-empty |
| `age-group` → `ageGroup` | select: `under-5`, `5-10`, `11-18`, `18-plus` | yes | non-empty |
| `level` → `level` | select: `0` Beginner, `1` Intermediate, `2` Advanced | yes | non-empty ("Not sure? Start with Beginner") |
| `parent-name` → `parentName` | text, shown only when age < 18 | conditional | non-empty if minor; sent as `null` otherwise |
| reCAPTCHA → `recaptchaToken` | `grecaptcha.getResponse()` | yes | non-empty |
| `terms-agreement` | checkbox (links `/terms`, `/privacy`, which don't exist) | yes | **not sent to the server** |

**Email blocking (duplicate-account prevention):**
- On `blur` (debounced 500 ms): `POST https://barakhadi-subscription.pushkard.workers.dev/api/check-email`, body `{"email": "<email>"}` → expected response `{"available": true|false}`.
- The field shows a spinner, then a green ✓ or red ✗ (CSS background SVGs) and sets `setCustomValidity`.
- `emailIsAvailable` is tri-state. Submit is **blocked while `null`** (not yet checked; the check is triggered) and while `false` ("This email address is already registered… contact support"). Typing resets the state to `null`.
- **Fail-open:** a network error returns `{available: true}`, so a Worker outage lets submissions through.

**Submit:**
1. `validateForm()`; on failure, inline errors.
2. Button disabled with spinner.
3. `POST …/api/create-checkout-session`, `Content-Type: application/json`, body:
   ```json
   {"email":"…","password":"…","studentFirstName":"…","studentLastName":"…",
    "ageGroup":"5-10","parentName":"…"|null,"level":"0","recaptchaToken":"…"}
   ```
4. Expected response `{"sessionId":"cs_test_…"}` or `{"error":"…"}`.
5. `stripe.redirectToCheckout({ sessionId })` (Stripe-hosted Checkout).
6. On error: `alert('An error occurred…')`, button re-enabled, `grecaptcha.reset()`.

**Problems found:**
- `console.log('Sending form data:', formData)` **logs the plaintext password** to the browser console.
- The password travels to the Worker and, from there, almost certainly into Stripe session metadata or Worker storage (see §4.4).
- `stripe.redirectToCheckout` is deprecated in current Stripe.js. New builds should redirect to `session.url` returned by the server.
- There is no CSRF/origin check visible client-side, and the email-availability endpoint enables **account enumeration** against TalentLMS.
- Header and footer links (`/faq`, `/contact-us`) and root image paths assume the page is deployed **next to the live WordPress site**.

### 4.3 `thank-you.html` (canonical, Dec 15)

- Reads `session_id` from the query string (Stripe `success_url` must be `…/thank-you(.html)?session_id={CHECKOUT_SESSION_ID}`). If it's missing, the page redirects to `/`.
- Shows "Verifying Your Enrollment…", waits **5 s** (for the webhook), then up to **3 attempts** of `GET …/api/verify-enrollment?session_id=<id>` with `AbortSignal.timeout(10000)` per attempt.
  - Expected response `{"enrolled": true|false, "email": "…"}`.
  - On non-200 it waits 2 s and retries. On a 200 with `enrolled:false` it retries **immediately, with no delay** (bug: the 2 s wait only applies on exceptions).
- **Regardless of the outcome, the page always shows the success state** ("Payment Successful! Your Account Has Been Created!") and fills in the email. Earlier variants had an error state ("Payment Received – Account Setup Issue… we'll manually set up your account within 24 hours", showing the Payment ID). That was removed in the Dec 15 redesign.
- Copy promises a confirmation email "with your login credentials" within 5 minutes, support at `support@barakhadi.com`, and a portal at `https://indml-marathi.talentlms.com`.
- `session_id` is interpolated into the URL without `encodeURIComponent` (minor).

**Evolution of thank-you logic:** static page (v1, `marathi.talentlms.com`) → single check after 3 s with error state (enhanced) → 3 tries with 2 s gaps (with-retry) → 15 s global race timeout (bulletproof) → per-attempt 10 s abort, always success (branded-final) → + confetti and redesign (canonical).

### 4.4 Reconstructed Cloudflare Worker `barakhadi-subscription`

Source isn't in the folder. The reconstruction below comes from the client contract, the notes (Stripe secret key, **webhook signing secret**, reCAPTCHA secret, `wrangler tail barakhadi-subscription`), the presence of `stripe.exe` (Stripe CLI, Dec 13, consistent with `stripe listen --forward-to` webhook testing) and page copy.

**Host:** `https://barakhadi-subscription.pushkard.workers.dev/` (preview `*-barakhadi-subscription.pushkard.workers.dev`).
**Likely secrets (wrangler secrets/vars):** `STRIPE_SECRET_KEY` (sk_test), `STRIPE_WEBHOOK_SECRET` (whsec), `RECAPTCHA_SECRET`, `TALENTLMS_API_KEY`, `TALENTLMS_DOMAIN` (`indml-marathi.talentlms.com`), probably a Stripe Price ID and course IDs per level, and possibly a KV namespace binding.

| Endpoint | Method | Request | Response | What it must do |
|---|---|---|---|---|
| `/api/check-email` | POST | `{email}` | `{available: bool}` | CORS preflight (OPTIONS) + `Access-Control-Allow-Origin`. Call TalentLMS `GET https://<domain>/api/v1/users/email:<email>` with HTTP Basic auth (API key as username, empty password). 200 → `available:false`; 404/"user does not exist" → `available:true` |
| `/api/create-checkout-session` | POST | form payload (§4.2) | `{sessionId}` or `{error}` | (1) Verify reCAPTCHA: `POST https://www.google.com/recaptcha/api/siteverify` (`secret`, `response`, optional `remoteip` from `CF-Connecting-IP`). (2) Server-side re-validation and possibly a re-check of the email. (3) `POST https://api.stripe.com/v1/checkout/sessions` with `mode=payment`, one line item of $60 USD (Price ID or `price_data`), `customer_email`, `success_url=<site>/thank-you.html?session_id={CHECKOUT_SESSION_ID}`, `cancel_url=<site>/subscribe.html`, and **`metadata`** carrying studentFirstName/LastName, ageGroup, parentName, level, and (to create the LMS account later) **the password**, either directly in metadata (bad: visible in the Stripe Dashboard and events) or stored in KV keyed by session id. (4) Return `session.id` |
| Stripe webhook (likely `/api/webhook` or `/webhook`) | POST | Stripe event | 200 | Verify `Stripe-Signature` with the whsec (in Workers: `stripe.webhooks.constructEventAsync` + `SubtleCryptoProvider`, or manual HMAC-SHA256). On `checkout.session.completed` with `payment_status=paid`: (a) TalentLMS `POST /api/v1/usersignup` (`first_name`, `last_name`, `email`, `login` (probably the email), `password`, maybe custom fields for age group / parent name); (b) `POST /api/v1/addusertocourse` (`user_id`, `course_id` mapped from level 0/1/2, `role=learner`), or add to a group; (c) record status (KV `session_id → {enrolled, email, userId}`) or rely on a later lookup. 12-month expiry: TalentLMS user `deactivation_date` / course expiration would have to be set; there is no evidence it was |
| `/api/verify-enrollment` | GET | `?session_id=` | `{enrolled: bool, email}` | Either read KV, or `GET https://api.stripe.com/v1/checkout/sessions/<id>` → `customer_email`, then look up the TalentLMS user (`users/email:`) and check course membership |

**Emails:** the "login credentials" email is most likely TalentLMS's built-in welcome notification triggered by `usersignup`. No transactional email provider appears anywhere.

**To recover:** `wrangler whoami` → `wrangler deployments list --name barakhadi-subscription`, download the script from the Cloudflare dashboard (Workers → barakhadi-subscription → Edit code / Download), `wrangler secret list --name barakhadi-subscription`. Check the Stripe Dashboard (test mode) → Developers → Webhooks for the registered endpoint URL and event types, plus Checkout Sessions metadata to see exactly what was stored.

---

## 5. Deployment setup (evidence)

| Piece | Evidence | Notes |
|---|---|---|
| GitHub | `origin = https://github.com/pushkardamle/barakhadi-new.git`, branch `main`, author `pushkard@gmail.com`. **Repo is public** (unauthenticated GitHub API returns 200). Standard command in notes: `git add . && git commit -m "visual improvements validations" && git push -u origin main` (explains the repeated identical commit messages) | No CI (`.github/` absent), no `.gitignore` |
| Cloudways | Notes: Cloudways account (email `falt…`), app URL `phpstack-1560311-6053934.cloudwaysapps.com` (PHP stack) | Likely Cloudways "Deployment via Git" pulling `main` into `public_html` (manual "Pull" or webhook). Not confirmed: no deploy script or webhook config in the repo. Pages use root-absolute assets (`/mainbarakhadilogo.png`, `/barakhadi_favicon.png`) while the repo stores them under `assets/images/`, so either files were copied to the web root by hand or images were broken on the server |
| Cloudflare Worker | `wrangler tail barakhadi-subscription` (notes, shell_commands.txt); workers.dev URL and preview URL pattern in notes | No `wrangler.toml` or Worker source locally. Deployed from elsewhere or via the dashboard |
| Stripe | Test-mode keys; webhook signing secret noted; `stripe.exe` present (CLI for `stripe login` / `listen` / `trigger`) | No live keys anywhere, so **never launched in live mode** |
| reCAPTCHA | v2 checkbox. Old key pair replaced Dec 12–13 by a new pair (site key changed in commit 32c4daf/dd01369) | Site key must list the Cloudways and/or production domains |
| Cloudflare proxy | `thank-you-with-retry.html` contains Cloudflare email-obfuscation injection, so at some point the page was served through a Cloudflare-proxied host | Consistent with Cloudways + Cloudflare or barakhadi.com on Cloudflare |
| Production | www.barakhadi.com is still the **WordPress 6.8.3 / Elementor** site (Dec 2025 scrape); Login → `marathi.talentlms.com` | The new site was never cut over |

---

## 6. Security concerns

### 6.1 Plaintext secrets and credentials (values masked to their first 4 characters)

| # | File | Line | Label in file | Masked value | Sensitivity | In git? |
|---|---|---|---|---|---|---|
| 1 | `Misc Barakhadi website with Claude code.txt` | 3 | Cloudways account (email) | `falt…` | Account identifier (PII) | No |
| 2 | same | 25 | "PW" | `Doma…` | **Password** (probably Cloudways or similar) | No |
| 3 | same | 31 | (unlabelled) | `8H46…` | **Likely a password / credential** | No |
| 4 | same | 36 | Google reCAPTCHA Key | `6Lck…` | Public site key | Yes (public by design) |
| 5 | same | 42 | Stripe Publishable Key | `pk_t…` | Public (test) | Yes (public by design) |
| 6 | same | 46 | **Stripe Secret Key** | `sk_t…` | **Secret** (test mode: can create charges/refunds and read customer data in the test account) | No |
| 7 | same | 50 | Sitekey OLD | `6Leh…` | Public | Yes (commit 1ffe74b, 32c4daf) |
| 8 | same | 51 | Sitekey NEW | `6Lck…` | Public | Yes |
| 9 | same | 55 | **reCAPTCHA Secretkey OLD** | `6Leh…` | **Secret** | No |
| 10 | same | 56 | **reCAPTCHA Secretkey NEW** | `6Lck…` | **Secret** | No |
| 11 | same | 73 | **Stripe signing secret** | `whse…` | **Secret** (webhook forgery) | No |
| 12 | `shell_commands.txt` | 15 | "PW" | `Doma…` | **Password** (same as #2) | No |
| 13 | `Barakhadi-New/subscribe.html` | 721, 761, 762 | site key, pk_test | `6Lck…`, `pk_t…` | Public | Yes |
| 14 | `Claude desktop files/subscribe*.html` (5 files) | ~605–761 | pk_test, site key | `pk_t…`, `6Lck…` | Public | 3 of the 5 versions are in git history |

**Git scan:** `git log -p | grep -iE "sk_test|sk_live|whsec|secret|password"` turns up only `password` form-field markup and `pk_test`/site-key lines. Targeted pickaxe searches (`git log --all -S`) for the Stripe secret, webhook secret, both reCAPTCHA secrets and both passwords return **no commits**. **No secret has been committed.** The top-level folder is not a git repo. Note that the repo is public, so the committed public keys and the Worker URL are world-visible. That is acceptable for publishable/site keys, but it exposes the Worker endpoints to abuse.

### 6.2 Other security issues

1. **Rotate** the Stripe test secret key, webhook secret and both reCAPTCHA secrets, and change both passwords. Do this even though none are in git, because they sit in plaintext in a synced or shared work folder and the notes file was pasted into AI chats. Move them into a password manager and into `wrangler secret`.
2. **Password handling:** the user's chosen TalentLMS password is logged to the console (`subscribe.html:1057`), sent to the Worker, and very likely stored in Stripe metadata or KV until the webhook runs. A rebuild should not collect a password at checkout. Instead, let TalentLMS send a set-password / welcome link, or generate a random password, or use TalentLMS SSO.
3. **Account enumeration:** `/api/check-email` reveals whether any email has a TalentLMS account, with no rate limit visible. Add Turnstile/reCAPTCHA or rate limiting, or remove the pre-check and handle duplicates after payment.
4. **Fail-open** email check on network error. The thank-you page **always reports success**, even when enrollment failed, so a failed webhook leaves a paying customer with no account and no warning.
5. **PII of minors** (student name, age group, parent name) flows to Stripe metadata and TalentLMS. The privacy policy and terms pages linked from the form don't exist (COPPA implications for under-13 users).
6. `stripe.exe` (31.6 MB binary) lives in the project folder. It's harmless, but keep it out of any repo.
7. The `session_id` query parameter is not URI-encoded; the `verify-enrollment` response leaks the purchaser's email to anyone holding a session id (low risk).

---

## 7. Quality assessment

### 7.1 Code quality

- **subscribe/thank-you:** single-file pages, about 500 lines of inline CSS each, duplicated header/footer/tokens, verbose `console.log`s, `alert()` for errors, 13 near-identical copies across folders. The logic is readable and the validation thorough. Built against a deprecated Stripe API.
- **index.html + css/styles.css:** the cleanest code. Semantic HTML (`header/nav/main/section/article/footer`), mobile-first CSS with custom properties and a spacing scale. It has inline `style=""` leftovers, emoji placeholders instead of images, `href="#"` activity links, a Login link of `#`, non-functional level tabs (`role="tab"` without JS), and "300+" vs "100+" contradicting each other on the same page.
- **Dec 16 Claude Desktop pages:** each page has its own inline CSS (no shared stylesheet), root vs relative path inconsistencies, missing images (`/placeholder-deepti.jpg`, `/lms_platform.jpg`, `hero_image.png`), and forms with no backend.
- **Doc dates** say 2024 though the work is from 2025/2026; the git messages are uninformative.

### 7.2 Accessibility

- Good: `lang="mr"` on index (though most content is English, so `lang="en"` with `lang="mr"` spans would be more accurate), `aria-hidden` on decorative emoji, label/`for` pairs on subscribe and contact forms, alt text on most images, one h1 per page in the canonical files.
- Problems:
  - Orange buttons with white text fail contrast (~2.1–2.6:1).
  - Password toggle has no `aria-label` or `aria-pressed`.
  - Form errors are not tied to inputs (`aria-describedby`/`aria-invalid`) and are not announced (`aria-live`).
  - The loading state on the thank-you page is not announced.
  - Focus is removed (`outline:none`), replaced only by a faint box-shadow.
  - No `:focus-visible` styles in `css/styles.css`.
  - No `prefers-reduced-motion` handling in the CSS even though DS prescribes it (photo strip floats forever, confetti).
  - Old thank-you variants had three h1 elements.
  - Emoji used inside headings ("🎓 Your Account…").
  - Mobile nav simply disappears (`display:none` below 968/768 px) with **no hamburger menu**, so mobile users can't navigate.

### 7.3 Mobile responsiveness

Layouts do collapse properly: grids stack and the pricing card un-sticks. The issues are the missing mobile nav (all versions), the photo strip, which needs a mobile treatment ("adapt/hide" noted but not verified), and the reCAPTCHA v2 widget (304 px), which can overflow narrow screens.

### 7.4 SEO

- Only `index.html`, `index-with-outfit-font.html`, `Dec 16/index.html` and `who-we-serve.html` have meta descriptions.
- **No page has Open Graph tags, canonical URLs or JSON-LD.** DESIGN_SYSTEM provides templates for all three.
- No sitemap, robots.txt or favicon set beyond one PNG. Subscribe and thank-you lack `noindex`.
- Titles are reasonable. The live site's title typo "Barkhadi" should be fixed in the rebuild.
- All Marathi text is either rendered with fallback fonts or locked in images (product_name.png), so it isn't indexable as styled text.

### 7.5 Reuse vs throw away

**Reuse**
- **Copy:** wireframe doc (all page copy), who-its-for.html personas and pain-point quotes, about.html story and bios, FAQ question set, home section copy from index.html ("The modern way to learn and practice Marathi", skills, benefits), subscribe benefits list. Check facts before reuse (§8).
- **Design tokens:** brand orange/green, Nunito body, one heading font (pick Outfit or Quicksand), the CSS spacing scale and radius, the section-label pattern, the components list in WIREFRAME_SUMMARY.
- **Images:** 9 AVIF activity screenshots, logo, tagline, favicon (re-export logo and tagline as true PNG/SVG), TalentLMS course cover, live-site assets (hero tablet photo, sticker thumbnails, Wistia video `ktanuvwk0f`), free-activity shared links.
- **Components:** polaroid photo-strip hero, flip badges, persona cards, tabs JS (Dec 16 index), accordion JS (faq.html), pricing card, form field/error styling, email-availability UI states, confetti (with reduced-motion guard).
- **Flow logic:** field set and validation rules, conditional parent-name field, reCAPTCHA gating, the Worker endpoint contract (check-email / create-checkout-session / webhook / verify-enrollment), retry-with-timeout polling, the error-state copy from thank-you-bulletproof (restore it).

**Throw away**
- All superseded subscribe/thank-you variants (8 files), duplicate zips, duplicate Firecrawl copies, `css/old_*.css`, `styles-updated.css`, `index-v2.html`, `Dec 16 - 2/index-complete.html`, `concept_1_final_refined.html` and `section_2_with_fonts_2.html` (keep only as visual reference), blank `barakhadi_course_image.jpg`, the purple-gradient and "system fonts" guidance in DESIGN_SYSTEM/README.
- Collecting a password on the payment form, `console.log` of form data, `alert()` errors, `redirectToCheckout`, the always-success thank-you behaviour, and unsubstantiated claims ("helping thousands", "hundreds of adult learners", "research-backed", "10,000+ practice hours").

---

## 8. Gaps and open items

1. **Worker source not in the folder.** Recover it from Cloudflare (plus `wrangler.toml`, secrets list, KV bindings) and document the Stripe webhook endpoint and events.
2. **Never went live.** Stripe is test-mode only. No live keys, no live webhook, no Stripe product/price confirmation, no tax/receipt settings, no refund policy implementation (the wireframe promises 30-day money-back).
3. **Pages never built:** Pricing, Activities, Terms of Service, Privacy Policy (both required by the subscribe checkbox), How it works, free-activities landing / email capture.
4. **No backends** for the contact form (`action="#"`) or the home-page "Get Free Access" email capture (no ESP chosen).
5. **No mobile navigation** (hamburger) anywhere.
6. **Home page not consolidated:** committed index.html vs uncommitted Outfit CSS vs Dec 16 wireframe version. The `index.html` font link was never updated to Outfit (font mismatch). The Jan 10 CSS was never committed.
7. **Content contradictions to settle:**
   - Activity count: 100 (live) / 100+ (FAQ, who-its-for, index CTA) / 300+ (subscribe, index, wireframes).
   - Renewal: FAQ says "annual and renew automatically… cancel anytime"; subscribe says "No Auto-Renewal, one-time payment".
   - Onboarding: FAQ says "account setup is done manually… 1–2 business days"; subscribe/thank-you say "Immediate access… account has been created".
   - Free trial: "gated with email" (structure doc) vs "No signup required" (index, FAQ).
   - Founder name: "Pushkar Deshpande" (wireframes, Dec 16 index) vs "Pushkar Damle" (index.html, about.html, WIREFRAME_SUMMARY, git remote).
   - LMS domain: `marathi.talentlms.com` (live site, Dec 16-2 pages, Jan 10 header) vs `indml-marathi.talentlms.com` (subscribe/thank-you/wireframes). Confirm which portal the Worker writes to.
   - Spelling: "बरखड़ी" and "Hindi" (HOME_PAGE_STRUCTURE, concept_1, DESIGN_SYSTEM) and "बराखडी" (Dec 16 index) vs the correct Marathi "बाराखडी" (logo, index.html).
   - Product naming: live site is built around the "Gappa Goshti" program; the new site never mentions it.
   - Contact email: info@ (live) vs support@ (new pages).
   - Teacher features: "lesson plans", "class management dashboard" and "homework assignments" are promised but unverified against what TalentLMS provides.
8. **Subscription lifecycle:** no handling of the 12-month expiry in TalentLMS, renewal reminders, multiple children per parent email (the email-uniqueness rule blocks a second child), school/bulk purchases, coupons, or receipts.
9. **Thank-you error path removed.** Failed enrollments are invisible to the customer, and there is no admin alerting (e.g. email or Slack on webhook failure).
10. **Assets:** real founder photos, persona images, skill screenshots per tab, demo video embed, OG image, Devanagari web font, logo as SVG.
11. **SEO and analytics:** OG/JSON-LD/canonical/sitemap/robots, analytics integration, redirects from WordPress URLs (`/faq/`, `/contact-us/`) at cutover.
12. **Deployment hygiene:** add `.gitignore`, move the site's assets path convention to one scheme, decide on the Cloudways git-deploy vs an alternative, add a staging/production split for Stripe keys and reCAPTCHA domains, and remove secrets from the notes files (after rotating them).
13. **Accessibility pass** (contrast, focus, aria-live, reduced motion) and **cross-device testing**: listed in every TODO and never done.
