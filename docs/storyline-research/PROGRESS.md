# Storyline research progress

Last update: Sun 18 Oct, 11:07 PM

## Steps

1. [x] Inventory: files, hashes, duplicates, TalentLMS courses & units — Newgen 6,213 files (13.5 GB) + rest of Marathi Shala 82,889 files (34 GB) hashed; TalentLMS 525 courses / 1,193 units fetched (GET only)
2. [x] Catalogue: parse every .story, previews — 1,145 projects parsed in memory (no extraction): slides, layers, interactions, triggers, animations, media origins, fonts, Marathi text
3. [x] Matching: projects ↔ TalentLMS courses/units — 325 live SCORM/xAPI units (tests and f-copies excluded) → 269 distinct source projects; 310 high-confidence, 12 medium, 3 low
4. [x] Grouping: activity families → candidate engines — 8 families: vocab-letter 62, trace-write 58, letter-trace 51, conversation 43, numbers-time 27, grammar-translation 15, books 7, word-games 6; 37 preview sheets rendered
5. [x] Deep dives: engine specs (agent workflow) + web-content review — 8 agents finished; 9 specs in specs/ (engines, data models, extraction, rights, effort)
6. [x] Report: report.html, published privately for phone reading — report.html written and published privately: https://claude.ai/artifact/9Bap5bS8WLmYVRPpRCzD1d

## Numbers

- Storyline projects (.story) found: 1,145
- Unique by content: 838
- In Newgen folder: 492
- Elsewhere in Marathi Shala: 647 (+5 only inside zips)
- Old Storyline 1 files (2014): 166
- TalentLMS courses: 525 (411 created in 2020)
- TalentLMS SCORM/xAPI units: 339
- TalentLMS Content units: 239 (+3 Web content)
- Live units matched to a source: 325 / 325
- Distinct source projects behind live units: 269
- Engines proposed: about 12 (incl. shared runtime)
- Estimated build: about 48 AI-assisted days (±30%); wave 1 = 65% of units

## Next

Owner reviews the report; decide on the क pilot

## Findings

- Scope widened (read-only): 'Republished Activities' (Level 0/1/2) and 'TreeTo Working' hold ~306 unique projects not in the Newgen folder; their folders mirror the 2020 TalentLMS categories, so they are likely the source of the live 2020 courses.
- 166 .story files are Storyline 1 (2014) in an old binary format; mostly early experiments/versions, catalogued at file level only.
- Deepti's 2020 lesson pages are 'Content' units (239), not 'Web content' (3).
- The 2020 courses (Level 0/1/2) were republished as SCORM 1.2 from 'Republished Activities'; the 2016-17 Gappa Goshti courses are Tin Can (xAPI) from the Newgen 'Semester' folders. Several Gappa Goshti units share content with Level 0/1 activities (same letter modules).
- Tracing in the letter activities is an embedded web object: William Malone's open-source canvas drawing app (Apache 2.0) over a 'trace_pattern <letter>.png' outline. It is free drawing with no stroke checking, so a new engine can teach stroke order properly; the outline images are reusable.
- TalentLMS unit content (Deepti's pages) cannot be read through the API key (login page returned), so the review is structural: names, sequencing, unit mix.
- Asset origins across the 269 live projects (19,320 media references, 3.5 GB): Newgen machines (E:\Marathi School, E:\Sudarshan) ~6,900; TreeTo/2020 (D:\Barakhadi) ~1,100; voice recorded in Storyline ~3,000; owner's own folders (Pictures, Stock Photos, Stock Sounds/Audioblocks) ~2,500; a few files traced to another client's project folder (D:\Projects\Caveo_PPD, 60 refs), which needs a rights check.
- Fonts: Mangal (Unicode Devanagari) in 267/269 projects, so Marathi text extracts cleanly; only 1 project uses a legacy CDAC font.

## Log

- Sun 18 Oct, 10:17 PM Step 1 running: Hashing Newgen files and fetching TalentLMS courses (GET only)
- Sun 18 Oct, 10:17 PM Job started; keep-awake helper on
- Sun 18 Oct, 10:23 PM Step 1 done: Newgen 6,213 files (13.5 GB) + rest of Marathi Shala 82,889 files (34 GB) hashed; TalentLMS 525 courses / 1,193 units fetched (GET only)
- Sun 18 Oct, 10:23 PM Step 2 done: 1,145 projects parsed in memory (no extraction): slides, layers, interactions, triggers, animations, media origins, fonts, Marathi text
- Sun 18 Oct, 10:23 PM Step 3 running: Picking the final version of each project, then matching to TalentLMS units
- Sun 18 Oct, 10:44 PM Step 3 done: 325 live SCORM/xAPI units (tests and f-copies excluded) → 269 distinct source projects; 310 high-confidence, 12 medium, 3 low
- Sun 18 Oct, 10:44 PM Step 4 running: Fingerprinting the 269 live projects (interactions, triggers, animations, media) into activity families
- Sun 18 Oct, 10:49 PM Step 4 done: 8 families: vocab-letter 62, trace-write 58, letter-trace 51, conversation 43, numbers-time 27, grammar-translation 15, books 7, word-games 6; 37 preview sheets rendered
- Sun 18 Oct, 10:49 PM Step 5 running: 8 agents in parallel: 7 activity families + Deepti's content units. Watch in /workflows
- Sun 18 Oct, 11:07 PM Step 5 done: 8 agents finished; 9 specs in specs/ (engines, data models, extraction, rights, effort)
- Sun 18 Oct, 11:07 PM Step 6 done: report.html written and published privately: https://claude.ai/artifact/9Bap5bS8WLmYVRPpRCzD1d
- Sun 18 Oct, 11:07 PM Job complete
