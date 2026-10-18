# TalentLMS research for the Barakhadi website rebuild

Researched 17 October 2026. Portal: `marathi.talentlms.com`, on a grandfathered "Basic" annual plan.

Sources were TalentLMS's official pricing page, the help center (articles updated through Oct 2026), the official V1 API PDF, the V2 Postman collection, and the new Developer Hub (developers.talentlms.io). I also sent unauthenticated HTTP requests to `marathi.talentlms.com`. Tags used below:
- **[observed]** means I saw it in live HTTP responses.
- **[unverified]** means I could not confirm it from an official source.

---

## TL;DR: the facts that change the architecture

1. **API V1 is officially deprecated.** The Developer Hub says V1 is "deprecated and no longer maintained… Security updates and bug fixes are not applied to the legacy API". Build on **API V2**: `https://{domain}.talentlms.com/api/v2/...`, with headers `X-API-Key` and `X-API-Version: YYYY-MM-DD`. V2 adds pagination, batch upserts, rate-limit headers and structured errors.
2. **On the API, the legacy "Basic" plan is not like Grow.** Both the V1 PDF and the V2 docs list **Basic at 2,000 API calls per hour**, the same as Core. Grow, Pro, Plus and Premium get 10,000 per hour. Every plan is also capped at 200 calls per 5 seconds.
3. **There are no real webhooks.** The only push mechanism is the automation "On course X completion, call URL Z", a plain GET with `?user=…&course=…`. Automations are Pro/Enterprise only (current plans), so on Basic you will almost certainly have to **poll the timeline endpoint**.
4. **Clicking through from the website without a second login works on any paid plan, without SSO.** Your server calls the API for a one-time autologin URL (`login_key` / `goto_url`) and redirects the user's browser to it. SSO (SAML 2.0, OIDC, LDAP) is also on all current paid plans. It is SP-initiated only, and it auto-creates any authenticated user, which consumes active-user seats.
5. **A custom domain (`learn.barakhadi.com`) via CNAME, with a free Let's Encrypt SSL certificate, is available on all current paid plans.** "Remove TalentLMS branding" is **Pro and Enterprise only**. In the new interface there is **no custom CSS or JS**: you only get theme colours, logo, favicon and a custom homepage. CSS and JS customisation survives only in the Legacy interface.
6. **There is no headless or player API.** The API gives you metadata, enrolment and progress, but it cannot render units outside TalentLMS. The realistic "all under the Barakhadi domain" setup is `learn.barakhadi.com` (CNAME), optionally framed from `barakhadi.com`. Framing needs the admin setting "Allow application to be loaded in a frame".

---

## 1. API basics

| Item | V1 (legacy, deprecated) | V2 (current) |
|---|---|---|
| Base URL | `https://{domain}.talentlms.com/api/v1/...` (e.g. `/v1/users/email:{email}`) | `https://{domain}.talentlms.com/api/v2/...` |
| Auth | API key sent as **HTTP Basic** credentials. The server answers `WWW-Authenticate: Basic realm="TalentLMS-API"` [observed]. Conventionally the key is the username with an empty password, which is what the PHP library does [third-party: Stitchflow]. | Header `X-API-Key: <key>`, plus mandatory `X-API-Version: YYYY-MM-DD` (example `2025-01-01`) and `Accept: application/json`. |
| Style | Mixed. Args go in the path (`/v1/gotocourse/user_id:1,course_id:2`) or as POST form fields. | REST: GET/POST/PATCH/DELETE with JSON bodies. Responses are wrapped in `_data`; errors come back in `_errors`. |
| Pagination | Only `/v1/users/page_size:N,page_number:M` | `page[number]`, `page[size]`, at most 100 per page |
| Rate-limit visibility | `GET /v1/ratelimit` (does not count against the limit) | `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers, and HTTP 429 |
| Batch | none | `POST /api/v2/batch/users`, `/batch/courses`, `/batch/enrollments` (up to 100 items, async; poll with `GET /api/v2/tasks/:id`) |
| Spec | PDF | Postman collection, Developer Hub, and a downloadable OpenAPI spec (added in v7.0, May 2026) |

**Availability:** the API is on all paid plans. It is not on Free or the free trial. Enable it at Account & Settings → Integrations → API. Only a SuperAdmin can enable it and see the key.

**Rate limits per hour, from the official V1 PDF and the V2 docs:**

| Plan | Calls per hour |
|---|---|
| Core | 2,000 |
| Grow | 10,000 |
| Pro | 10,000 |
| Starter / Small (legacy) | 2,000 |
| **Basic (legacy)** | **2,000** |
| Plus (legacy) | 10,000 |
| Premium (legacy) | 10,000 |
| Custom / Enterprise | negotiated |

Every plan is additionally capped at **200 calls per 5 seconds**. To confirm your real limit, call `GET /v1/ratelimit` or read the V2 headers.

**V2 timeline:**
- Jan 2026 (v6.13): V2 launched.
- Mar 2026 (v6.14): Developer Hub, plus endpoints to remove a course from a group or branch.
- May 2026 (v7.0): OpenAPI spec; batch user upsert can update custom fields and status.
- Jul 2026 (v7.1): REST sub-resources under `/v2/users/{id}`.
- Sep 2026 (v7.2): endpoints to register and unregister users for ILT sessions, plus Skills CRUD.

## 2. Endpoints for selling courses from an external site

The V1 parameter names come from the official PDF. The V2 paths come from the Postman collection and the Developer Hub.

| Need | V1 (legacy) | V2 (current) |
|---|---|---|
| Create user | `POST /v1/usersignup`: `first_name`, `last_name`, `email`, `login`, `password`. Optional: `branch_id`, `group_id`, `user_type`, `language`, `restrict_email` (`on`/`off`), `custom_field_1..20`. | `POST /api/v2/users` JSON. Required: `name`, `surname`, `login`, `email`, `password`. Optional: `timezone`, `locale`, `email_notifications`, `user_type_id`, `status`, `description`, `credits`, `deactivation_date`. |
| Get user by email | `GET /v1/users/email:{email}` (also `username:{login}` and `id:{id}`). The response includes `login_key`, `courses[]` with completion data, `groups`, `branches`, `certifications` and `badges`. | `GET /api/v2/users?filter[email][eq]=x@y.com`. Other filters: login, keyword, status, last_updated, branch_id, group_id, custom_field_value. `GET /api/v2/users/:id?resources=courses,groups,branches` (or `resources=all`). |
| Edit user | `POST /v1/edituser`: `user_id`, plus any of `first_name`, `last_name`, `email`, `login`, `password`, `bio`, `timezone`, `credits`, `deactivation_date` (dd/mm/yyyy), `restrict_email`, `custom_field_X` | `PATCH /api/v2/users/:id` (includes `status`, `deactivation_date` as YYYY-MM-DD, `credits`, etc.). Returns 204. |
| Activate / deactivate | `GET /v1/usersetstatus/user_id:{id},status:{active\|inactive}` | `PATCH /api/v2/users/:id` with the status field. The docs are inconsistent: the body example shows `status`, the parameter table shows `active` (boolean). Test both. |
| Delete user | `POST /v1/deleteuser`: `user_id`, optional `deleted_by_user_id`, `permanent` (`yes`/`no`) | `DELETE /api/v2/users/:id` |
| Enrol in course | `POST /v1/addusertocourse`: `user_id` **or** `user_email`, `course_id` **or** `course_name`, optional `role` (`learner`/`instructor`). V1 accepts arrays for bulk. | `POST /api/v2/enrollments` `{course_id, user_id}`. Bulk: `POST /api/v2/batch/enrollments` `{enrollments:[…]}` |
| Unenrol | `GET /v1/removeuserfromcourse/user_id:{id},course_id:{id}` | `DELETE /api/v2/enrollments` `{course_id, user_id}` |
| Add to group | `GET /v1/addusertogroup/user_id:{id},group_key:{groupKey}`. This uses the group's **key** (e.g. `MLdDOnOBn`, shown in group objects), not its id. Joining a group auto-enrols the user in the group's courses. | `POST /api/v2/group-memberships/` `{group_id, user_id}`. This uses the id. |
| Remove from group | `/v1/removeuserfromgroup/user_id:{id},group_id:{id}` | `DELETE /api/v2/group-memberships/` |
| Add to branch | `GET /v1/addusertobranch/user_id:{id},branch_id:{id}` | `POST /api/v2/branch-users` `{branch_id, user_id}` |
| One-click login | Two ways. (a) `login_key` from any user GET. (b) `POST /v1/userlogin` with `login`, `password`, optional `logout_redirect`; this needs the password, so it is not useful with external auth. The PDF says "The login_key URL changes every time it is used, so don't store it… make a fresh request for each and every login." | `GET /api/v2/users/:id/login` returns `_data:[{name, url:".../index/autologin/key:…", is_branch}]`, one URL per portal or branch the user belongs to. No password needed. |
| Go straight to a course | `GET /v1/gotocourse/user_id:{id},course_id:{id}`. Optional `logout_redirect`, `course_completed_redirect` (both **base64-encoded** URLs), and `header_hidden_options` (semicolon list of `courseName;units;sharedFiles;moreOptions;certificationIcon`). Returns `goto_url`. | `GET /api/v2/courses/:course_id/users/:user_id/goto?logout_redirect=<b64>&course_completed_redirect=<b64>` returns `goto_url`. The user must already be enrolled. |
| Logout | `/v1/userlogout`: `user_id`, `next` | `POST /api/v2/users/:id/logout` `{next}` returns `redirect_url` |
| Course list / one course | `GET /v1/courses`, `/v1/courses/id:{id}`. Price is a string like `"$0"`; the single-course response includes `units[]` (with a `url` such as `…/unit/apiview/id:1`), rules and prerequisites. | `GET /api/v2/courses` (filterable by custom field). `GET /api/v2/courses/:id`, where price is `{amount, currency}`. `GET /api/v2/courses/:id/units`. |
| Categories | `GET /v1/categories`, `/v1/categories/id:{id}` (price plus courses), `/v1/categoryleafsandcourses/id:{id}` | `GET /api/v2/categories` (a tree, with optional `price`), `/api/v2/categories/:id` |
| Buy course / category | **Not in the current V1 PDF.** `buycourse` and `buycategory` existed in older V1 versions and are no longer documented [unverified]. | `POST /api/v2/courses/:id/purchase` and `POST /api/v2/categories/:id/purchase`, body `{user_id, cancel_path, return_path, coupon}`. Payment goes through **the portal's own Stripe or PayPal**, or account credits. The response gives a `redirect_url` to checkout. |
| Progress | `GET /v1/getuserstatusincourse/course_id:{id},user_id:{id}` returns role, completion_status, completion_percentage, completed_on, total_time, and per-unit status and score. `GET /v1/getusersprogressinunits/unit_id:{id}[,user_id:{id}]` | `GET /api/v2/course-progress?user_id=&course_id=`, `GET /api/v2/unit-progress?user_id=&unit_id=`, `GET /api/v2/results?unit_id=&user_id=` (test or survey answers), `DELETE /api/v2/course-progress` (reset) |
| Timeline | `GET /v1/gettimeline` with `event_type` and optional `user_id` / `course_id` / `branch_id` / `group_id` / `unit_id`. **Returns only the latest 200 entries.** | `GET /api/v2/timeline?filter[event_type]=course_completion&filter[created_from][gte]=…&filter[created_to][lte]=…` (paginated) |
| Portal info | `/v1/siteinfo` (totals, `monthly_active_users`, `domain_map`, branch limit) | `GET /api/v2/statistics` |

Useful timeline event types: `user_register_user`, `user_self_register`, `user_create_payment`, `course_add_user`, `course_completion`, `course_failure`, `certification_issue_certification`, `unitprogress_test_completion`, `unitprogress_assignment_answered`, `unitprogress_assignment_graded`, `unitprogress_ilt_graded`.

**Not verified:** how long an unused autologin key stays valid. TalentLMS documents only that it changes on each use. Generate it just-in-time on click and never email or cache it.

## 3. Webhooks and event notifications

- **TalentLMS has no general webhook system.** I found no webhook feature in the help center, the Developer Hub or any 2026 release notes.
- **Automation "On course X completion, call URL Z"** (or "Any course"): TalentLMS calls your URL with GET parameters, e.g. `https://site/hook?user=123&course=50`. It sends no signature, and no retry behaviour is documented, so treat the call only as a trigger. Re-check it with `GET /users/:id` or `/course-progress` before acting on it. **Automations are on Pro and Enterprise only** (current pricing page and help center). Legacy Basic most likely has no automations, because older guides show "Triggered Actions" only on Basic *Unlimited*, Plus and Premium [unverified for your specific account].
- **Alternatives:**
  - Poll `GET /api/v2/timeline` with `filter[event_type]` and `filter[created_from]` every few minutes (cheap at 2,000 calls per hour).
  - Zapier's TalentLMS app has a "Course Completed" trigger. It polls the API, so it should work on any paid plan [unverified].
  - The in-app Notifications system (emails, e.g. on user payment or course completion) is for people, not systems.

## 4. Built-in e-commerce vs Stripe plus the API

**Built-in features** (help center). No plan restriction is stated, so it appears to be on all paid plans [unverified; the pricing page does not list e-commerce at all].

- **Gateways:**
  - Stripe, through Stripe Connect and Stripe Checkout.
  - PayPal. Note: you must re-enable and reconnect PayPal **by 31 Dec 2026** because PayPal is retiring its old API.
  - All branches using Stripe must share one Stripe account; PayPal can differ per branch.
- **Prices:** set per course, per group (a "bundle") or per category (a "bundle"). Currency is set per portal or branch, and INR is supported.
- **Subscriptions:**
  - Stripe only, monthly or annual, for "Access to all paid courses", with an optional first month free.
  - Turning subscriptions on **disables individual course purchases** (it is one or the other).
  - You can't change the subscription price or turn subscriptions off while anyone has an active subscription.
  - Learners who cancel **lose access immediately**.
- **Discounts:** coupons (fixed or %, a validity window, a redemption count, scoped to courses, groups or categories) and a global percentage discount.
- **Credits:** an off-site payment mechanism. Admins give users credits, 1 credit = 1 currency unit. Credits buy single courses only, not subscriptions.
- **Other:** invoices to learners, payment tracking via Reports → Timeline → "User payment", and the "user has not made a purchase" notification and automation.
- **Branches** can each have their own e-commerce settings.

**Comparison:**

| | TalentLMS built-in | External Stripe + API |
|---|---|---|
| Checkout UX | Inside the TalentLMS catalog, with TalentLMS styling | Fully custom on barakhadi.com |
| Pricing models | Per course, bundles, a single all-catalog subscription, coupons | Anything: per-level subscriptions, family plans, sibling discounts, regional pricing, trials, Stripe Billing portal |
| Who must exist first | User must register in TalentLMS before buying | You create the TalentLMS user only after payment, which saves active-user seats |
| Access revocation | Automatic on cancel (immediate) | Your webhook handler calls unenrol or deactivate (you control grace periods) |
| Effort | Configuration only | You build the Stripe webhook, user provisioning, enrolment and SSO/autologin |
| Plan dependency | None beyond paid | API is on all paid plans; Basic's 2,000 calls per hour is ample for this |
| Hybrid | `POST /api/v2/courses/:id/purchase` starts a TalentLMS-native Stripe checkout for a given user from your site | |

**Recommendation for a kids' subscription product:** use external Stripe (Billing plus Customer Portal) as the source of truth. On `checkout.session.completed` or `invoice.paid`:
1. Upsert the TalentLMS user.
2. Add them to a group per product tier (the group auto-enrols them in its courses).
3. Activate them.

On `customer.subscription.deleted`, remove them from the group or deactivate them.

## 5. SSO

- **Protocols:** SAML 2.0, OpenID Connect and LDAP, plus preset guides for Okta, Entra ID, OneLogin, Google, miniOrange, ADFS and Salesforce. SCIM v2 provisioning works with Okta and Entra. SSO can be configured per branch, with a different IdP per branch.
- **Plans:** "Single Sign On (SAML2.0, LDAP & OpenID Connect)" is ticked on **Core, Grow, Pro and Enterprise** on the current pricing page. Legacy Basic included SSO according to older guides (elearningindustry, b2breviews).
- **How it works:**
  - TalentLMS acts as the service provider. It supports **SP-initiated login only**.
  - For IdP-initiated or "deep link" entry, send users to `https://{portal}/index/ssologin/service:saml` or `…/service:oidc`.
  - Required attributes: username (the unique key), first name, last name and email.
  - Optional attributes: groups (auto-assigns users to same-named groups, which auto-enrols them) and custom fields.
  - The OIDC redirect URI is `https://{domain}.talentlms.com/simplesaml/module.php/openidconnect/resume.php`. OIDC claims must come from the **userinfo endpoint**; claims carried only in the access token are not mapped.
- **Gotchas:**
  - Accounts are matched **by username**. A mismatch creates a duplicate account, or an `idp_email_already_exists` error.
  - SSO users **bypass sign-up restrictions**: any user who authenticates at your IdP gets an account, and that **consumes an active-user seat**.
  - SSO works on *either* the custom domain *or* the talentlms.com domain, not both.
  - Deleted (archived) users with the same email block login until they are permanently deleted or restored.

**Can a custom website login (Clerk, Auth0 or a custom IdP) give users a seamless click-through?**
- **Option A, no SSO (recommended, simplest):** the user is logged into barakhadi.com and clicks "Open lesson". Your backend:
  1. Looks up or creates the TalentLMS user.
  2. Calls `GET /api/v2/users/:id/login` or `/courses/:cid/users/:uid/goto`.
  3. Sends a 302 redirect to the returned URL.
  
  The user lands logged in. This works on any paid plan. You control exactly who gets provisioned, and `logout_redirect` / `course_completed_redirect` bring the user back to your site.
- **Option B, OIDC SSO:**
  - **Auth0** works as a standard OIDC provider.
  - **Clerk** can act as an OAuth/OIDC provider through its "OAuth applications" feature [unverified for TalentLMS specifically; check that Clerk's userinfo returns username, given_name, family_name and email].
  - Link to `…/index/ssologin/service:oidc`. If the user already has an IdP session, the round trip is silent.
  - Downsides: the seat consumption and username-matching rules above.

## 6. Custom domain and white-labelling

- **Custom domain:**
  - Account & Settings → Portal → Custom domain, then add `CNAME learn.barakhadi.com → marathi.talentlms.com`.
  - Branches map automatically to `{branch}.learn.barakhadi.com`; add the wildcard `*.learn` CNAME.
  - Root domains need A records, which is discouraged.
- **SSL:** a Let's Encrypt certificate is issued automatically within 24 hours, "enabled by default for all plans", covering up to about 100 hostnames. You can also upload your own certificate, which must be a wildcard if you use branches.
- **Plan:** "Custom domain + SSL" is ticked on all current paid plans. Older guides say Basic included custom domain and SSL [unverified for your account; check Account & Settings → Portal].
- **Custom sending domain** for notification emails: help articles dated Sep 2026.
- **Remove "Powered by TalentLMS" branding:** **Pro and Enterprise only** (pricing page, plus the help article updated Sep 2026). It also lets you exclude admins and instructors from TalentLMS marketing communications. Basic will almost certainly keep the footer.
- **Themes:**
  - The new interface offers theme colours, logo, favicon, a custom homepage builder, CMS pages, a unit font and certificates.
  - **Custom CSS and JavaScript exist only in the Legacy interface.** The help center says "CSS/JavaScript customization options are not available in the new interface". The Legacy interface can still be enabled but is clearly being phased out.
  - A white-label Android app costs extra and is limited to Pro Annual and Enterprise.

## 7. Embedding

- **Framing:**
  - TalentLMS has an admin setting, **Account & Settings → Security → Other → "Allow application to be loaded in a frame"**. The Salesforce Embedded app guide requires it, which implies framing is blocked by default.
  - [observed] On 17 Oct 2026, the unauthenticated pages of `marathi.talentlms.com` sent no `X-Frame-Options` and no CSP `frame-ancestors`. `www.talentlms.com` does send `X-Frame-Options: SAMEORIGIN`.
  - Session cookies are `Secure; SameSite=None`. Framing `marathi.talentlms.com` from `barakhadi.com` is therefore a **third-party-cookie** scenario, which Safari and Firefox block or partition and which would break login inside the frame.
  - Framing **`learn.barakhadi.com` from `barakhadi.com` is same-site**, so cookies work. That is a strong reason to set up the custom domain first.
  - Test logged-in course and unit pages with the frame setting on.
- **Headless / player API:** **none.** The V2 API covers users, courses, units *metadata*, enrolments, progress and results, but there is no endpoint to render units, launch SCORM, or write progress. The V1 unit `url` (`/unit/apiview/id:N`) is undocumented [unverified what it renders].
- **Realistic options for "everything under the Barakhadi domain":**
  1. **Recommended:** marketing site, catalog and checkout on `barakhadi.com`, built from API data (`/courses`, `/categories`, prices). Lessons run on **`learn.barakhadi.com`** (CNAME plus SSL), reached through API autologin. Use `logout_redirect` and `course_completed_redirect` to send learners back, and `header_hidden_options` to simplify the course header.
  2. Same as 1, but `barakhadi.com/learn/...` pages iframe `learn.barakhadi.com` after you turn on the frame setting. This is a same-site iframe, but expect UX friction on mobile, with full-screen video and with pop-up units.
  3. Public course share links (paid plans, free courses only) or the external course catalog, for marketing previews.
  4. Rebuild the activities natively on your own site and use TalentLMS only for record-keeping. TalentLMS has no write-progress API, so this effectively means leaving TalentLMS.

## 8. Teachers and schools

- **Roles:** the built-in user types are SuperAdmin, Admin-Type, Trainer-Type (Instructor) and Learner-Type. **Custom user types** with fine-grained permissions ("custom user permissions") are listed on all plans. A user can be an *instructor* in some courses and a *learner* in others (`role` on enrolment).
- **Groups:**
  - Available on all plans; a user can belong to many groups.
  - Groups can carry a price (bundle) and a join key (`group_key`).
  - Group reports exist, and reports can be scheduled to recipients.
  - **The Group Supervisor role** (scoped reports and messaging for a group, assignable even to a Learner-based custom type) is **Pro and Enterprise only** and new-interface only. Pro is limited to 10 groups.
- **Branches** (independent sub-portals with their own URL, theme, users, courses, e-commerce and SSO; a branch admin sees only their branch):
  - Core: 1
  - Grow: 3
  - Pro: 15
  - Enterprise: unlimited
  - Free: none
  - Legacy Basic: probably 1 [unverified]. `/v1/siteinfo` returns `limits.maximum_brances`, and `/api/v2/statistics` returns `branch_limit`; check your number there.
- **Teaching features:**
  - Assignments: submission, grading and history.
  - ILT units: classroom or webinar sessions with attendance and grading, plus Zoom, Teams and BigBlueButton. ILT session registration has been possible via the V2 API since Sep 2026.
  - Tests and surveys, certificates, gamification and learning paths. Learning paths: Grow allows 5; Pro and Enterprise unlimited; Core shows the feature greyed out.
- **Reports:**
  - Standard reports and timeline exist on every plan.
  - **Custom reports, Analytics and LTI 1.3 need Grow or above** (greyed out on Core).
  - Reporting APIs: `/course-progress`, `/unit-progress`, `/results`, `/timeline`, `/statistics`, plus Developer Hub sub-resources `get-group-users`, `get-course-users`, `get-user-courses`, `get-user-certificates`, `get-unit-result-attempts`.

**A teacher dashboard for a home-based Marathi school:**
- *Native, cheapest:*
  1. Make each teacher an Instructor, using a custom "Teacher" type.
  2. Create one **group** per class or batch and enrol the teacher as instructor in that class's courses.
  3. Instructors see progress, grade assignments and run ILT sessions for their courses.
  
  The limitations: instructors see everyone in a course, not only their batch, unless the courses are split per batch. Group Supervisor would scope this properly but needs Pro.
- *Branch per school:* a good fit for partner schools that want their own URL and admin, but you are limited by the branch count (likely only 1 on Basic). A branch admin needs an admin-role user type.
- *Custom dashboard on barakhadi.com:*
  - Pull `group users` → per-user `course-progress` / `results` → cache in your own database, refreshed incrementally from `/timeline`.
  - Gives full control over scoping (teacher → students), parent views and a Marathi UI.
  - Budget: about 2,000 calls per hour. 50 students × 10 courses = 500 calls for a full refresh, so cache aggressively and use timeline deltas.
  - Recommended if you want parent and teacher views branded as Barakhadi.

## 9. Plan comparison (current public plans, talentlms.com/prices, Oct 2026)

Prices are the entry tier, billed annually. The annual-plan help article confirms Core at 1–40 users is $119/month and at 41–70 users is $159/month.

| Feature | Core | Grow | Pro | Enterprise |
|---|---|---|---|---|
| Entry price | $119/mo | $229/mo | $449/mo (+$6/extra user) | Quote (from 1,000 users; Flex from 500) |
| Max active users on the plan | up to 100 | up to 500 | up to 1,000 (or Flex add-on) | 1,000+ (or Flex) |
| Courses | Unlimited | Unlimited | Unlimited | Unlimited |
| API | Yes (2,000/hr) | Yes (10,000/hr) | Yes (10,000/hr) | Yes (custom) |
| SSO (SAML 2.0, OIDC, LDAP) | Yes | Yes | Yes | Yes |
| Custom domain + SSL | Yes | Yes | Yes | Yes |
| Custom homepage | Yes | Yes | Yes | Yes |
| Branches | 1 | 3 | 15 | Unlimited |
| Custom reports / Analytics / LTI 1.3 | No | Yes | Yes | Yes |
| Learning paths | No | 5 | Unlimited | Unlimited |
| Group Supervisor | No | No | Yes (10 groups) | Yes |
| Automations (incl. call-URL on completion) | No | No | Yes | Yes |
| Remove TalentLMS branding | No | No | Yes | Yes |
| HubSpot integration | No | No | Yes | Yes |
| E-commerce (Stripe/PayPal, coupons, subscriptions) | Not listed on pricing page. Help articles state no restriction, so likely all paid plans [unverified] | same | same | same |
| Flexible user limit | No | No | Add-on | Add-on |
| Support | Email | Email | Priority email + chat | + phone |

**Grandfathered "Basic" (legacy Starter/Basic/Plus/Premium family). Likely includes:**
- Up to about 100 users.
- Unlimited courses.
- SSO.
- Custom domain + SSL.
- Probably 1 branch.
- The API at **2,000 calls/hour** (official docs).

**Likely excludes:**
- Automations / triggered actions.
- Custom reports.
- Branding removal.
- Group Supervisor.

Older guides put Triggered Actions on "Basic Unlimited", Plus and Premium, and Custom Reporting on Plus and Premium. **Verify in your portal under Home → Subscription**: the plan card greys out features you don't have, and the Usage summary shows active users and branches.

## 10. Gotchas

- **JSON errors are not guaranteed.** V1 and V2 document JSON errors (`{"type":"invalid_request_error|api_error","message":…}` in V1; `{"_errors":[{"id":"bad_request","title":"…"}]}` in V2 examples). However, an unauthenticated request returned **`401` with an HTML body** (`content-type: text/html`) on both `/api/v1` and `/api/v2` [observed]. Always check the status code first and parse JSON defensively.
- **Status codes:** 400 bad parameters, 401 bad key, 403 API disabled or domain inactive, 404 not found, 422 malformed, 429 rate limit, 500 server error.
- **Rate limits:** 2,000 per hour on Basic, a 200 per 5 seconds burst cap, and 429 on excess. Cache course catalogs, use batch endpoints, and back off on 429.
- **V1 quirks:**
  - Deprecated, with no security fixes.
  - Numbers come back as strings.
  - Dates use the portal date format (`dd/mm/yyyy, hh:mm:ss`).
  - Redirect URLs must be **base64-encoded**.
  - The timeline returns only the latest 200 events.
  - `addusertogroup` takes the group **key**, not the id.
- **V2 quirks:** `X-API-Version` is mandatory, `Accept: application/json` is required, there are 100 items per page at most, and batch jobs are asynchronous (poll `/tasks/:id`).
- **Emails must be unique per user, and email is required.** For siblings sharing a parent's email, use plus-addressing or another scheme, and turn off `email_notifications` / `restrict_email` where appropriate.
- **Active-user pricing:**
  - On standard (non-Flex) plans, **only users marked Active count**. Inactive users don't take a seat and keep all their data and progress; they cannot log in, and reactivating them restores access.
  - Flex plans (Pro and Enterprise only) bill on unique monthly logins regardless of status.
  - Strategy: create users only after purchase, deactivate them when a subscription lapses (`usersetstatus` or `PATCH`), and reactivate on renewal. A scheduled `deactivation_date` can be set through the API.
  - Without automations (Basic), the "deactivate after N hours with no purchase or login" rules are not available. Do this from your own backend.
  - What happens exactly when you hit the active cap (blocked activations or sign-ups vs overage) is not documented for standard plans [unverified].
- **Deleting vs deactivating:** a non-permanent delete archives the user and blocks re-use of that email until they are permanently deleted or restored. Prefer deactivation.
- **SSO** auto-creates and activates any IdP-authenticated user. Don't expose SSO to non-paying website users, or you will burn seats.
- **The automation callback is an unauthenticated GET.** Anyone who knows the URL can spoof it, so verify via the API.
- **PayPal:** reconnect it by 31 Dec 2026 if you use it.
- **The Legacy interface is being phased out.** Don't rely on CSS or JS theme hacks.

---

## Sources

**Official, TalentLMS**
- Pricing page (feature ticks per plan, parsed from the page HTML): https://www.talentlms.com/prices
- V1 API documentation PDF (legacy): https://www.talentlms.com/pages/docs/TalentLMS-API-Documentation.pdf (redirects to https://market.talentlms.com/pages/docs/TalentLMS-API-Documentation.pdf)
- V2 Postman collection: https://documenter.getpostman.com/view/31867199/2sAY548Kou
- Developer Hub: https://developers.talentlms.io/intro · https://developers.talentlms.io/errors · https://developers.talentlms.io/legacy-api · https://developers.talentlms.io/openapi · https://developers.talentlms.io/api/get-users · https://developers.talentlms.io/api/login-user · https://developers.talentlms.io/api/purchase-a-course · https://developers.talentlms.io/api/get-course-units · https://developers.talentlms.io/supported-values-currencies
- TalentLMS API V2: https://help.talentlms.com/hc/en-us/articles/24874457011356-TalentLMS-API-V2
- Can I integrate my site / API: https://help.talentlms.com/hc/en-us/articles/9651527213468-Can-I-integrate-my-site-with-TalentLMS-Do-you-offer-an-API
- How subscription plans work (active users, Flex): https://help.talentlms.com/hc/en-us/articles/9652402239516-How-TalentLMS-subscription-plans-work
- Find your plan's price and features: https://help.talentlms.com/hc/en-us/articles/29114817575964-How-to-find-out-your-plan-s-price-and-features-in-TalentLMS
- Moving between annual plans (Core tier prices): https://help.talentlms.com/hc/en-us/articles/9652402694428-What-happens-when-you-move-from-one-annual-plan-to-another
- Call URL on course completion: https://help.talentlms.com/hc/en-us/articles/9651457002908-How-to-trigger-a-custom-action-when-users-complete-a-specific-course-in-TalentLMS
- Automations: https://help.talentlms.com/hc/en-us/articles/9651467215900-How-to-work-with-automations-in-TalentLMS
- SAML 2.0 SSO: https://help.talentlms.com/hc/en-us/articles/9652216640284-How-to-configure-SSO-with-a-SAML-2-0-identity-provider-in-TalentLMS
- OpenID Connect SSO: https://help.talentlms.com/hc/en-us/articles/9652261417628-How-to-configure-SSO-with-OpenID-Connect-in-TalentLMS
- SSO and registration restrictions: https://help.talentlms.com/hc/en-us/articles/9652232201884-SSO-and-registration-restrictions-in-TalentLMS
- Common SSO issues: https://help.talentlms.com/hc/en-us/articles/16419645852700-Common-SSO-issues
- Map a custom domain: https://help.talentlms.com/hc/en-us/articles/9652249770780-How-to-map-a-custom-domain-to-TalentLMS
- SSL for custom domains: https://help.talentlms.com/hc/en-us/articles/9652259336476-How-to-set-up-SSL-for-your-custom-domains
- White label your portal: https://help.talentlms.com/hc/en-us/articles/14872333440028-How-to-white-label-your-TalentLMS-portal
- Customise themes: https://help.talentlms.com/hc/en-us/articles/20571132132124-How-to-customize-your-themes-in-TalentLMS
- New UI vs Legacy (no CSS/JS in new UI): https://help.talentlms.com/hc/en-us/articles/18866853953820
- Stripe gateway: https://help.talentlms.com/hc/en-us/articles/9651801532188-How-to-set-up-your-Stripe-payment-gateway
- PayPal gateway (Dec 2026 deadline): https://help.talentlms.com/hc/en-us/articles/9651769057436-How-to-set-up-your-PayPal-payment-gateway-in-TalentLMS
- Subscriptions: https://help.talentlms.com/hc/en-us/articles/9651815458844-How-to-work-with-subscriptions-in-TalentLMS
- Coupons: https://help.talentlms.com/hc/en-us/articles/9651763696668-How-to-work-with-coupons-in-TalentLMS
- Discounts and bundles: https://help.talentlms.com/hc/en-us/articles/9651785371292-How-to-work-with-discounts-in-TalentLMS
- Credits / off-site payments: https://help.talentlms.com/hc/en-us/articles/9651763633180-How-to-handle-off-site-payments-in-TalentLMS
- How a user purchases: https://help.talentlms.com/hc/en-us/articles/20296373763100-How-can-a-user-purchase-a-course-or-a-subscription-in-TalentLMS
- Users who don't purchase: https://help.talentlms.com/hc/en-us/articles/9651785454364-How-to-deal-with-users-that-don-t-purchase-any-courses
- Track payments: https://help.talentlms.com/hc/en-us/articles/9651763915932-How-to-track-payments-in-TalentLMS
- Branches: https://help.talentlms.com/hc/en-us/articles/10730422769436-How-to-work-with-branches-in-TalentLMS
- Groups vs branches: https://help.talentlms.com/hc/en-us/articles/9651522351260-What-is-the-difference-between-groups-and-branches-in-TalentLMS
- User types: https://help.talentlms.com/hc/en-us/articles/9652280520092-A-guide-to-the-TalentLMS-user-types
- Group Supervisor: https://help.talentlms.com/hc/en-us/articles/27464091325340-What-is-the-Group-Supervisor-role-in-TalentLMS-and-how-it-works
- Deactivate users: https://help.talentlms.com/hc/en-us/articles/9652291013788-How-to-deactivate-users-in-TalentLMS
- Share courses / public URL / external catalog: https://help.talentlms.com/hc/en-us/articles/9652335475484-How-to-share-courses-with-users-in-TalentLMS
- Embed content (iFrame units): https://help.talentlms.com/hc/en-us/articles/9651374849564-How-to-embed-content-in-TalentLMS
- Salesforce Embedded app ("Allow application to be loaded in a frame"): https://help.talentlms.com/hc/en-us/articles/9651494734108-How-to-integrate-the-TalentLMS-Salesforce-Embedded-app
- WordPress / WooCommerce plugin: https://help.talentlms.com/hc/en-us/articles/360014573294
- Release notes, 2026: Jan https://help.talentlms.com/hc/en-us/articles/24927571306012 · Mar https://help.talentlms.com/hc/en-us/articles/25894133905692 · May https://help.talentlms.com/hc/en-us/articles/27610532444828 · Jul https://help.talentlms.com/hc/en-us/articles/28761874377116 · Sep https://help.talentlms.com/hc/en-us/articles/30414725933084

**Third-party (used only for legacy plans and context)**
- eLearning Industry, TalentLMS pricing plans (legacy Small/Basic/Plus/Premium): https://elearningindustry.com/talentlms-pricing-plans
- B2B Reviews (Basic includes SSO, a branch, custom domain + SSL): https://www.b2breviews.com/?p=532
- Stitchflow (V1 HTTP Basic auth): https://www.stitchflow.com/user-management/talentlms/api
- Zapier TalentLMS triggers: https://zapier.com/apps/talentlms/integrations/webhook
- 2026 per-tier pricing roundups: https://lmscost.com/vendors/talentlms · https://www.teachfloor.com/blog/talentlms-pricing

**Direct observation (17 Oct 2026):** unauthenticated `curl` requests to `https://marathi.talentlms.com/`, `/index`, `/catalog`, `/api/v1/siteinfo` and `/api/v2/users` (response headers and status codes only).
