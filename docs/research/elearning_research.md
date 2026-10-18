# E-learning research: Storyline/SCORM Marathi activities on TalentLMS (as of Oct 2026)

Context: kids' Marathi activities built 10+ years ago in Articulate Storyline (likely Storyline 1 or 2), exported as SCORM (possibly Tin Can/xAPI), running on marathi.talentlms.com (Grow plan).

Method note: help.talentlms.com blocks direct page fetches (HTTP 403). Its articles were read through the public Zendesk Help Center API (`/api/v2/help_center/en-us/articles/<id>.json`). The source links below are the normal article URLs. **[UNVERIFIED]** marks points I could not confirm from a primary source.

---

## 1. TalentLMS display options for SCORM / xAPI / cmi5 units

**New interface (current default)**
- To add one: Course > Add > Learning Activities > "SCORM | xAPI | cmi5", then upload the ZIP. Under **More options > Unit options** you get:
  - **"Show as": Embedded or Pop-up.**
  - **"Size": Width and Height in pixels.** (Source [1]. This article does not say whether the size applies to embedded mode, pop-up mode, or both. **[UNVERIFIED]**: test both.)
  - "When failed retain the failed status upon retries."
- The article does not list a "new browser tab/window" option for SCORM units, or an admin "fullscreen" toggle. The pop-up is a TalentLMS dialog/window, and the May 2024 release notes say "The SCORM pop-up window has been redesigned" [2].
- The learner help article says content "may open embedded in the page or in a pop-up window". For pop-ups, learners click "Start/Resume unit" and must keep the window open. Some packages only send completion when the window closes [3][4].
- **iFrame units** (for any web page) can be shown **embedded or in a new window** [5][6]. The admin must allow framing ("Allow the application to be loaded in a frame"), and URLs must be https [7]. "Iframe unit options have been added" (Dec 2023 release notes) [8].
- **LTI 1.3 units** also offer pop-up (the default) or embedded [9].
- **Learner full-screen/maximize button:** I found no current help article that documents it. The April 2020 release notes mention "the full-screen button on SCORM content" (a fix for Firefox/IE) [10], so a full-screen control existed, at least in the legacy player. Its exact location and behaviour in the new UI are **[UNVERIFIED]**. Check by logging in as a learner. The browser's own F11 full screen always works.
- The help center has no "Embed" unit type. Embedding is done with Content units (HTML/embed code), Web content units ("embed content from external web sources"), or iFrame units [5]. The legacy code editor strips `iframe`, `script` and `form` tags [11].

**Legacy interface**
- Unit types: Content, Web Content, Video, Audio, Presentation|Document, SCORM|Tin Can|cmi5, iFrame, Test, Survey, Assignment, ILT [6]. iFrame units are "viewed as embedded or in a new window" [6]. The legacy SCORM add screen offered Embedded/Popup (the iSpring guide refers to the "Add SCORM | TinCan | CMI 5" page and recommends popup) [12]. Whether legacy also had width/height fields is **[UNVERIFIED]**.
- The two interfaces still coexist. The new one is the default, and admins can disable legacy under Account & Settings > Portal. I found no announced retirement date [13][14]. LTI 1.3 setup works only in the new interface [9].

**Guest "shared" public links (/shared/start/key:...)**
- Public URL sharing is available on paid plans only. Logged-in users are auto-enrolled. "Non-registered users ... are allowed to complete the course anonymously". "If they do not register, the progress is not tracked." Priced courses cannot be shared publicly [15][16].
- ILT registration is not possible anonymously [16]. I found no documented difference in SCORM display (embedded vs pop-up) for guest sessions **[UNVERIFIED]**. Expect the same unit options. Because progress is not stored, SCORM resume/suspend data for anonymous guests probably does not persist **[UNVERIFIED, inference]**.

**Mobile app:** SCORM works offline only if it is HTML5 and self-contained. SCORM uploaded before 5 Jan 2018 must be re-uploaded. **xAPI and cmi5 are not supported in the app** (they work in a mobile browser). H5P and third-party iFrames are online-only. Pop-up units (SCORM, iFrame) cannot use "compatibility mode" [17][18][19].

## 2. Supported content formats today

| Format | Status in TalentLMS | Source |
|---|---|---|
| SCORM 1.2 | Supported (single-SCO) | [20][21] |
| SCORM 2004 | **Not supported**. "supports SCORM 1.2 files only and does not currently support SCORM 2004 or Multi-SCO packages" | [21] |
| AICC | Not supported | [1] |
| xAPI / Tin Can | Supported. Must be enabled under Account & Settings > Integrations > xAPI. Has a **built-in "TalentLMS LRS"**: statements show on Reports > Timeline as [TC] events, and can optionally be pushed to an external LRS (endpoint/key/secret) | [22][23][24] |
| cmi5 | Supported (same upload path, xAPI must be enabled) | [24] |
| LTI 1.3 | Supported as a tool consumer (launches external tools as units). Grow/Pro/Enterprise only, new UI only, no Deep Linking | [9] |
| H5P | **No native H5P unit**. Use an iFrame/embed of H5P.com or another host, or export H5P as SCORM (see section 5). The app lists H5P as online-only | [17][25] |
| iFrame / Web content | Native unit types | [5] |
| TalentCraft (AI authoring) | Built-in authoring for text, media, flashcards, tabs, labeled graphics, with AI generation. Document import came out of beta in March 2026. **Grow includes "TalentCraft premium" with 10,000 AI credits/month** per the pricing page. Some marketing pages say Pro/Enterprise, so this is a conflicting source. Not a games/drag-drop engine | [26][27][28] |

**Size limits (paid plans):** general limit of 600 MB/file. "SCORM, xAPI: 600MB". A generic "zip" file is 200 MB. cmi5 is not listed separately (presumably 600 MB, **[UNVERIFIED]**). The Free plan is 100 MB/file. Max 1,000 units+sections per course [29][30][5].

**Pricing context (Oct 2026):** Core $119/mo, **Grow $229/mo (up to 500 users per the page header)**, Pro $449/mo, about 20% off annually. "SCORM 1.2/Tin Can/cmi5" are listed for all plans. LTI 1.3 and custom domain are on Grow [28].

## 3. Completion and scoring

**SCORM units**
- TalentLMS reads `cmi.core.lesson_status`. The unit completes when the package sets **"completed" or "passed"** and calls `LMSCommit()`. If it only ever sends "incomplete", the unit stays incomplete [21][31].
- The score comes from `cmi.core.score.raw`. The unit has no admin-side passing/mastery threshold: pass/fail and the passing score are decided inside the package (for example the Storyline quiz/reporting settings) [32].
- A SCORM unit's score is not automatically the course score. Fix: Course options > Completion > "Score calculation: Calculate score by: Units I choose", then select the SCORM unit. Learners must re-complete to update [32].
- Suspend data and bookmarks are stored. After re-uploading a changed package, reset suspend data or learners may see blank or wrong slides [20][33].
- Common causes of non-completion: the completion trigger is never reached; the package only posts on pop-up close; a dispatch package loses its connection [21].

**xAPI / cmi5 units:** completion depends on the statements sent (completed/failed, etc.). Results appear on the Timeline, not in the SCORM reports. Learners can "Check your status with this unit" [34].

**Course completion rules** (Course options > Completion): "All units are completed" (default) / "A percentage of units is completed" / "Selected units are completed" / "Selected test is passed" [35].

**Why the owner sees 50% / 66% with an assignment unit**
- An assignment has two completion modes: **"When the Instructor accepts the answer"** (complete only after grading; until then "Pending") or **"When uploading an answer"** (completed/passed immediately on upload) [36][37].
- Course progress counts completed units out of total units. One SCORM completed plus one pending assignment gives 1/2 = 50%. Two of three gives 66%. The assignment stays incomplete until an instructor grades it, or forever if nobody does. **[Mechanism inferred; the help center does not spell out the progress formula.]**
- Fixes: (a) switch the assignment to "When uploading an answer"; (b) grade or accept submissions in the Grading Hub; (c) use "Selected units are completed" or "A percentage..." so the ungraded unit does not block completion. Whether the progress bar then shows 100% or still shows the unit ratio is **[UNVERIFIED]**. (d) Remove assignments from guest/shared courses. Anonymous guests cannot meaningfully submit or receive grades **[inference]**.

## 4. Articulate Storyline player sizing and migration

**Modern vs Classic player (Storyline 360):** The Modern player (introduced around 2018) "scales smoothly to fill learners' browsers" and is consistent across desktop and mobile. Some features are modern-only. Classic is the older look with finer colour control and is not fully responsive on phones [38][39].

**Player size (Home > Player > Other > Player size)** [40][41]:
- **"Scale player to fill browser"** (default): fills the browser/frame with no white space, on desktop and mobile.
- **"Lock player size"**: fixed at slide size plus player chrome, desktop only. The old label was "Lock player at optimal size".
- **"Lock player size to fit browser"**: scales while keeping the aspect ratio (letterboxing), desktop only.
- "Launch player in new window (creates launch page)" offers browser size options ("Allow learners to resize browser", slide size vs full screen). Articulate notes "many LMSs automatically open courses in new windows" [41].

**Why old output shows scrollbars or fixed frames in an LMS iframe:** Storyline 1/2 output was Flash-first with an HTML5 version (story_html5.html). Flash is now dead, so only the HTML5 path runs, and that early HTML5 player has limited responsive scaling. When an old course was published with a fixed/locked size (for example 720x540 plus chrome) or "Scale player" disabled, and TalentLMS's embedded frame is smaller, the browser shows scrollbars or cuts content off. On iPad, iframed content often fails to scale [42][43][44]. Workarounds without republishing: use TalentLMS pop-up mode, or set the unit Width/Height to the course's native size. The real fix is to republish from the .story file with "Scale player to fill browser" (HTML5 only).

**Can old .story files be republished in Storyline 360?**
- **Storyline 2 and 3:** yes. They open and auto-upgrade, and a backup copy is created. Upgraded projects cannot be reopened in older versions. Engage interactions need "Edit in Engage" for HTML5. YouTube embeds behave differently. Check translated/custom player text labels [45].
- **Storyline 1: as of the 4 Aug 2026 update (build 3.123), Storyline 360 no longer opens Storyline 1 project files.** If you never opened a project before, you must contact Articulate Support to have it upgraded. Workaround: install an older Storyline 360 build, or open the file in Storyline 2/3 if you have a licence **[workaround UNVERIFIED]** [46].
- **Devanagari risk:** Storyline 360 has had Hindi matra (vowel sign) misplacement bugs. The fix advice is to enable **Modern Text** (Design > Fonts > Use Modern Text). Upgraded projects may still use legacy text rendering, so check Marathi rendering in Chrome, Safari and Firefox after upgrading. A Hindi export-to-Word fix shipped in build 3.79 [47].

**Articulate 360 cost (official page, Oct 2026):** Articulate 360 AI **Personal $1,449/seat/yr**, **Teams $1,749/seat/yr** (Storyline + Rise + AI), with a 14-day free trial. Third-party sites also cite "Standard" tiers at $1,199 and $1,499, which the official page did not show **[conflicting]**. Academic pricing is by enquiry [48][49]. One-off Storyline 3 licences appear to be no longer sold **[UNVERIFIED]** [50].

## 5. Modern alternatives for rebuilding kids' activities

**Custom HTML5/JS packaged as SCORM 1.2 (best fit for TalentLMS)**
- TalentLMS needs **SCORM 1.2** (not 2004), or xAPI/cmi5 (no mobile-app support). The minimum package is an `imsmanifest.xml` at the ZIP root plus the HTML/JS/assets. Avoid special or non-Latin characters in **file names** [20].
- **pipwerks SCORM API wrapper** (MIT): a content-side wrapper that finds the LMS API and handles init, get/set, commit and quit. It works with SCORM 1.2 and 2004 but is old (2008) and lightly maintained, which is fine for its small scope [51].
- **scorm-again** (MIT, v3): an **LMS-side** SCORM 1.2/2004 runtime, not a content wrapper. It is useful for local testing, or for a remote launcher's cross-frame bridge (`CrossFrameLMS`/`CrossFrameAPI` over postMessage). It has no cmi5 support [52].
- Validate packages in SCORM Cloud before uploading [20].
- Unicode/Devanagari: HTML5 with web fonts (Noto Sans Devanagari, Mukta, etc.) renders Marathi properly. Crossword and word-search grids must split words into **orthographic syllables (aksharas)**, not code points or grapheme clusters. Unicode grapheme clusters do not keep conjuncts together. Use a custom akshara segmenter, or `Intl.Segmenter` with post-processing **[implementation note]** [53][54].

**H5P**
- Relevant content types: Crossword, Find the Words (word search), Drag and Drop, Drag the Words, Mark the Words, Image hotspots, Dialog Cards, Memory Game, Speak the Words, Audio, Interactive Video, Course Presentation [55].
- **Known problems with Indic and complex scripts:** a Tamil user reported Find the Words rendering broken (2021 feature request, no response). Crossword has no RTL support (2025 maintainer reply). Expect Devanagari grid issues in Crossword and Find the Words; other H5P types handle Unicode text fine [56][57].
- To get H5P into TalentLMS: (a) iFrame-embed from H5P.com (paid; content deleted 30 days after cancellation) or from a self-hosted WordPress/Drupal H5P, where the host must allow framing [25]; tracking does not come back to TalentLMS this way. (b) **Lumi desktop** (free) exports H5P to SCORM. After the v1.0.0 rebuild (May 2025), the University of Alberta reported that the SCORM export was broken. Latest is v1.0.3 (May 2026) and I could not confirm a fix **[UNVERIFIED]**. The SCORM version Lumi exports is also unconfirmed [58][59].

**Authoring tools**
- **iSpring Suite**: $970/author/yr, Suite AI $1,290/yr, with academic/nonprofit discounts. PowerPoint-based, with drag-and-drop and quiz interactions. Exports SCORM 1.2/2004, xAPI, cmi5 [60] (the export list is from general knowledge; the pricing page did not list it).
- **Adobe Captivate**: the "new" Captivate is still missing features vs Classic. Classic is planned to sunset in 2027, conditional on feature parity. A risky platform choice right now [61].
- **Rise 360**: block/form-based. Its only custom interactivity is Storyline blocks and the newer sandboxed Custom Code Block. Exports SCORM 1.2/2004/AICC. Poor fit for kids' games [62].
- **Elucidat**: enterprise, quote-priced, responsive authoring. Overkill for this use case **[not researched in depth]**.
- **Storyline 360 itself**: still the strongest no-code tool for drag-drop, states and triggers, but costs $1,449+/yr.

## 6. "Remote launcher" / dispatch pattern

- **Pattern:** a thin SCORM package in the LMS loads content hosted elsewhere in an iframe. The two sides relay the SCORM API through `window.postMessage`, because the same-origin policy blocks direct cross-domain API calls (the "3-node problem") [63][64]. Examples: Rustici SCORM Cloud Dispatch / Content Controller [65], and Catalyst's Moodle **SCORM Remote** plugin (a thin wrapper with a scorm-again bridge, content in a sandboxed iframe) [66].
- **TalentLMS's position:** dispatch packages are explicitly acknowledged. They "depend on that server's availability and on your domain being accepted", and a dispatch's broken connection is listed as a cause of non-completion. Support's fallback advice is "upload a non-dispatched SCORM package" [20][21].
- **Reliability and pitfalls:**
  - **Third-party cookies:** if the remote content uses cookie sessions, Safari (ITP) and increasingly Chrome/Edge block them inside an iframe on another domain. SCORM Cloud had to add cookieless "Content Vault" token auth for this reason [67][68].
  - **Storage partitioning:** since Chrome 115 (Safari and Firefox similar), localStorage and IndexedDB in a cross-site iframe are partitioned per top-level site. Remote content cannot rely on its own localStorage to persist progress across contexts. Keep state in SCORM `suspend_data` via the bridge [69].
  - **Framing headers:** the remote host must allow being framed (no `X-Frame-Options: DENY`; set `Content-Security-Policy: frame-ancestors` to include `*.talentlms.com` and any custom domain).
  - **postMessage security:** validate `event.origin` on both sides, use explicit target origins, and handle the async round trip. SCORM 1.2 `LMSGetValue` is synchronous, so the wrapper must preload or cache values (scorm-again's CrossFrameAPI is "cache-first" for this reason) [52].
  - **Unload timing:** the final commit and LMSFinish on tab close are less reliable across frames. Commit on every meaningful event, not only on exit.
  - **Mobile app:** it cannot work offline, and remote content is "online only" [17].
- **Verdict:** workable and widely used commercially, but it adds a failure point. With roughly 600 MB allowed per SCORM package, self-contained packages are simpler and more reliable for small kids' activities. Use a remote launcher only if you need one-source-many-LMS updates.

## 7. AI coding assistants converting or generating e-learning

- I found **no documented case study** of an AI assistant converting Storyline .story/Flash courses to HTML5 automatically. Sources point to *rebuilding* rather than converting [70][71].
- **LXPack migration guide:** uses Claude to draft HTML interactions (drag-drop, hotspots) with human validation. Complex timeline animations need rebuilding [70].
- **LessonKit "vibe coding" guide:** non-coders use Cursor or VS Code + Copilot to describe a course, preview it, and **export a SCORM 1.2 package** [72].
- eLearning Industry piece on "vibe coding in eLearning" (vendor-leaning) [73]. Jan 2026 webinar "Vibe Coding for Storyline" (AI-built HTML5 micro-games as web objects) [74]. DevLearn 2026 (2 Nov) has a vibe-coding workshop for instructional designers [75].
- A practitioner (LinkedIn) notes AI cannot yet reproduce complex Storyline triggers, states and variables [71]. A Jan 2026 Director-to-HTML5 discussion warns that plausible-looking AI code can take as long to debug as a manual rebuild [76].
- Pre-LLM research: SWF2JS semi-automated Flash-to-JS (IIIT Hyderabad, 2017) [77]. Ruffle (Flash emulator) is not a viable route for Storyline Flash output: Storyline output is multi-file, and Ruffle's AS3 support is limited **[UNVERIFIED for Storyline]** [78].
- **Practical takeaway:** the activities are small and self-contained (crossword, word search, drag-drop, colouring, tracing, listen-and-match, dialogues), which is the sweet spot for AI-assisted HTML5/JS generation. Extract assets (audio, images, Marathi text) from the old published output (`story_content/` folder) or the .story, then have an AI assistant generate each activity plus a SCORM 1.2 wrapper, and validate in SCORM Cloud and on TalentLMS.

---

## Sources

1. How to work with the supported eLearning protocols (SCORM 1.2, xAPI, cmi5) in TalentLMS: https://help.talentlms.com/hc/en-us/articles/9651360207132
2. Release Notes May 2024: https://help.talentlms.com/hc/en-us/articles/13954321916828-Release-Notes-May-2024
3. SCORM for Learners: What to Expect: https://help.talentlms.com/hc/en-us/articles/26558408919708-SCORM-for-Learners-What-to-Expect-and-How-It-Works
4. Why your SCORM content may not complete: https://help.talentlms.com/hc/en-us/articles/9651374214428-Why-your-SCORM-content-may-not-complete-in-TalentLMS
5. How to add content to a course in TalentLMS: https://help.talentlms.com/hc/en-us/articles/9651361074460-How-to-add-content-to-a-course-in-TalentLMS
6. How to add content to a course in the Legacy interface: https://help.talentlms.com/hc/en-us/articles/360017465634
7. How to use discussions as course units (iFrame requirements): https://help.talentlms.com/hc/en-us/articles/9651351788316
8. Release Notes December 2023: https://help.talentlms.com/hc/en-us/articles/11807853023388-Release-Notes-December-2023
9. How to enable LTI 1.3 in TalentLMS: https://help.talentlms.com/hc/en-us/articles/18600381592476-How-to-enable-LTI-1-3-in-TalentLMS
10. Release Notes April 2020: https://help.talentlms.com/hc/en-us/articles/360013223440-Release-Notes-April-2020
11. Code editor guide (Legacy): https://help.talentlms.com/hc/en-us/articles/360014658213
12. iSpring: How to add a SCORM course into TalentLMS: https://www.ispringsolutions.com/supported-lms/talentlms/add-e-learning-course-into-talentlms
13. How to disable the Legacy interface: https://help.talentlms.com/hc/en-us/articles/15260910024988-How-to-disable-the-TalentLMS-Legacy-interface
14. Switching between new and legacy interfaces: https://help.talentlms.com/hc/en-us/articles/9652249968284
15. How to share courses with users in TalentLMS: https://help.talentlms.com/hc/en-us/articles/9652335475484
16. "Try it for free" indication: https://help.talentlms.com/hc/en-us/articles/28892008865948
17. Content types supported by the TalentLMS mobile app: https://help.talentlms.com/hc/en-us/articles/9651766450716
18. Unit compatibility mode for the app: https://help.talentlms.com/hc/en-us/articles/360015305900
19. Release Notes May 2021: https://help.talentlms.com/hc/en-us/articles/360021543059-Release-Notes-May-2021
20. SCORM in TalentLMS: Overview, Setup, and Best Practices: https://help.talentlms.com/hc/en-us/articles/26499696329756
21. Why your SCORM content may not complete (SCORM 1.2 only): https://help.talentlms.com/hc/en-us/articles/9651374214428
22. Integrate with an external LRS: https://help.talentlms.com/hc/en-us/articles/9651511869724
23. Release Notes March 2026 V6.14: https://help.talentlms.com/hc/en-us/articles/25894133905692
24. How to import and track cmi5 content: https://help.talentlms.com/hc/en-us/articles/9651373731356
25. H5P forum: embedding H5P.com in TalentLMS: https://h5p.org/node/1063563
26. TalentCraft page: https://www.talentlms.com/talentcraft
27. TalentLMS March 2026 product updates: https://www.talentlms.com/blog/talentlms-march-2026-release/
28. TalentLMS pricing: https://www.talentlms.com/prices
29. Upload limits in TalentLMS: https://help.talentlms.com/hc/en-us/articles/9651468986268-Upload-limits-in-TalentLMS
30. Upload limits (Legacy): https://help.talentlms.com/hc/en-us/articles/360014572694
31. Common issues with SCORM progress: https://help.talentlms.com/hc/en-us/articles/27011524694556
32. SCORM scoring and reporting issues: https://help.talentlms.com/hc/en-us/articles/28365179031580
33. Reset SCORM suspend data: https://help.talentlms.com/hc/en-us/articles/9651383888156
34. Completion and reporting issues with xAPI/cmi5: https://help.talentlms.com/hc/en-us/articles/29993214574108
35. How to set completion rules for courses: https://help.talentlms.com/hc/en-us/articles/9651377683100
36. How to work with assignments in TalentLMS: https://help.talentlms.com/hc/en-us/articles/9651387967004
37. How to work with assignments (Legacy): https://help.talentlms.com/hc/en-us/articles/360014657293
38. Storyline 360: The Modern Player: https://access.articulate.com/support/article/Storyline-360-Modern-Player
39. IconLogic: Modern and Legacy players: https://blog.iconlogic.com/2018/10/articulate-storyline-360-modern-and-legacy-players.html
40. Storyline 360: Modern Player Size Control: https://www.articulatesupport.com/article/Storyline-360-Modern-Player-Size-Control
41. Storyline 360: Changing the Browser Settings and Player Size: https://www.articulatesupport.com/article/Storyline-360-Changing-the-Browser-Settings-and-Player-Size
42. Articulate community: SCORM content hard coded (SL2 cut off in LMS): https://community.articulate.com/discussions/articulate-storyline/scorm-content-hard-coded
43. Articulate community: html5 player too large for iPad: https://community.articulate.com/discussions/html5-player-too-large-for-ipad
44. Articulate community: HTML still requires Flash?: https://community.articulate.com/discussions/articulate-storyline/html-still-requires-flash
45. How to Upgrade a Course to Storyline 360: https://www.articulatesupport.com/article/How-to-Upgrade-a-Course-to-Articulate-Storyline-360
46. Storyline 360: Ending Support for Storyline 1 Project Files (4 Aug 2026): https://www.articulatesupport.com/article/Storyline-360-Ending-Support-for-Storyline-1-Project-Files
47. Articulate community: Hindi font issue: https://community.articulate.com/discussions/articulate-storyline/hindi-font-issue
48. Articulate 360 pricing: https://www.articulate.com/360/pricing/
49. Knowlify: Articulate 360 pricing: https://knowlify.com/articles/articulate-360-pricing
50. Articulate community: Storyline 3 vs 360: https://community.articulate.com/discussions/articulate-storyline/storyline-3-vs-360
51. pipwerks SCORM API wrapper: https://github.com/pipwerks/scorm-api-wrapper
52. scorm-again: https://github.com/jcputney/scorm-again
53. W3C Devanagari layout requirements: https://www.w3.org/International/ilreq/devanagari/
54. W3C i18n: grapheme clusters vs Indic conjuncts: https://lists.w3.org/Archives/Public/public-i18n-archive/2020JanMar/0291.html
55. H5P Find the Words example (UBC): https://h5p.open.ubc.ca/h5p-examples/find-the-words/
56. H5P: Unicode support for Tamil (Find the Words): https://h5p.org/node/1119551
57. H5P: RTL problem in Crossword: https://h5p.org/node/1520746
58. U Alberta: exporting H5P as SCORM (Lumi 1.0.0 export broken): https://support.eclass.ualberta.ca/Knowledgebase/Article/View/592/55/exporting-h5p-content-from-eclass-to-use-as-scorm-content-in-canvas
59. Lumi releases: https://github.com/Lumieducation/Lumi/releases
60. iSpring Suite pricing: https://www.ispringsolutions.com/ispring-suite/pricing
61. IconLogic: "Adobe: It's Time to Deliver on the Captivate Promise" (Aug 2026): https://blog.iconlogic.com/2026/08/adobe-its-time-to-deliver-on-the-captivate-promise.html, and the Adobe roadmap: https://elearning.adobe.com/2024/07/new-captivate-roadmap/
62. Articulate community: Rise custom code block vs Storyline: https://community.articulate.com/discussions/code-block-forum/rise-360%E2%80%99s-new-custom-code-block-%E2%80%94-how-far-can-it-go-to-replace-the-need-for-sto/1240510
63. Rustici Driver "Other Notes" (cross-domain problem): https://docs.rusticisoftware.com/driver/Other-Notes.html
64. scorm.com: Bypass SCORM cross-domain restrictions: https://scorm.com/?p=22081
65. scorm.com: SCORM cross domain: https://scorm.com/scorm-cross-domain/
66. Moodle SCORM Remote plugin: https://moodle.org/plugins/mod_scormremote
67. SCORM Cloud Content Protection (3rd-party cookies, Safari bug): https://support.scorm.com/hc/en-us/articles/206163636-SCORM-Cloud-Content-Protection
68. SCORM Cloud: Launch in an iFrame / Content Vault: https://support.scorm.com/hc/en-us/articles/46727466405787 and https://support.scorm.com/hc/en-us/articles/360042728333
69. Chrome Storage Partitioning: https://developer.chrome.com/docs/privacy-sandbox/storage-partitioning
70. LXPack: Migrating from legacy tools: https://lxpack.readthedocs.io/en/latest/guides/migrating-from-legacy-tools/
71. LinkedIn practitioner post (via search): https://eg.linkedin.com/in/abdullah-mohamed07/ar
72. LessonKit: Vibe coding guide: https://lessonkit.readthedocs.io/en/latest/guides/vibe-coding/index.html
73. eLearning Industry: Vibe coding in eLearning: https://elearningindustry.com/vibe-coding-in-elearning-how-ai-is-transforming-interactive-course-creation
74. Vibe Coding for Storyline webinar: https://addcal.io/e/htmcbup9fz4p
75. DevLearn 2026 session: https://devlearn.com/learning-technology-conference-overview/session-details/0994863d-a0cf-482e-91ce-20bb810dd066/
76. Director-to-HTML5 AI caution (Jan 2026): https://vispo.com/pipermail/hopperxx_vispo.com/2026-February/000215.html
77. IIIT Hyderabad SWF2JS: https://web2py.iiit.ac.in/research_centres/publications/view_publication/inproceedings/1345
78. Articulate community: single swf output: https://community.articulate.com/discussions/articulate-storyline/single-swf-output
