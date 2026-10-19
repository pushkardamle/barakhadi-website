# Storyline activities research: plan and rules

Approved plan for researching Barakhadi's Storyline activities, ahead of converting them to HTML5 engines.
**Read this first after any context reset.** Status is kept in `progress.html` and `PROGRESS.md`.

## Hard rules (from the owner, 2026-10-18)

1. **Never write to `B:\My Documents\Marathi Shala\Source Files from Newgen`.** It is the only copy. Read only.
   Unpack `.story` files (they are zips) into the scratchpad or `docs/storyline-research/_work/` (git-ignored), never next to the source.
2. **TalentLMS API: GET only.** Courses are live with paid students. Use `tools/tlms_readonly.py` (no code path for POST/PUT/DELETE).
   The key is in `barakhadi-web/.env` (git-ignored). Never print it.
3. All outputs go under `A:\Barakhadi AI Website\barakhadi-web\docs\storyline-research\`.
   Commit the report and catalogue (small files) to the private repo. Never commit previews or raw extracts (`_work/`, `previews/`).

## Owner decisions

- Free-trial courses ending in `f` (e.g. `L1-04-003f`) are copies: skip them, **unless no non-f course with the same code exists**, in which case keep the f course.
- Shutterstock images were paid licences; the licence type is unknown. The report should point to Shutterstock account → licence history to confirm Standard or Enhanced.
- Agents: Claude decides how many (about 6–8), run as a workflow so the owner can watch in `/workflows`.
- Deepti's TalentLMS "web content" units stay as they are, but get a light review.

## Scope (measured 2026-10-18)

- Newgen folder: 6,213 files, 13 GB. **492 `.story` files (6.6 GB).**
  - Layout: `Release 1/` (01 Learn and trace … 09 Learn and Read), `Release 2/`, `Semester 1–3` (Conversation / Vocabulary / Writing modules, plus SCORM 1.2 variants), `Sem1 New`, `Sem 2 New`, `Trial Storyline 360`.
  - Course list exports: `marathi-courses.csv` (247 courses), `marathi-courses_assessment.xlsx`.
- TalentLMS: 525 courses (521 active). Course names carry codes like `Crossword (L1-04-003)`.
- Other local published outputs: 195 under `B:\My Documents\Marathi Shala\` (see the storyline-fix notes in memory).

## Steps

1. **Inventory (script):** all files with hashes. Find duplicates across folders and zips, and pick the final version of each project. From TalentLMS (GET only), every course and its units with unit type (SCORM/xAPI/web content).
2. **Catalogue (script):** parse each `.story` (extend `activities/tools/parse_story.py`). Capture title and code, slides and layers, interaction types, media counts, animations, triggers and variables, Marathi text, and slide size. Render a slide preview sheet per project.
3. **Matching (script, then review):** project ↔ course/unit by code, title and activity id. Flag projects with no course and courses with no source.
4. **Grouping (script, then review):** structural fingerprint → activity families, giving a candidate engine list (about 10–15).
5. **Deep dives (workflow, 6–8 agents):** one per family, each writing an engine spec (mechanics, data model, scoring, animations, edge cases, S/M/L complexity, reusable assets, rights flags). Plus one agent reviewing Deepti's web-content units.
6. **Report:** `docs/storyline-research/report.html`, in the same style as `barakhadi-rebuild-assessment.html`. Covers the catalogue in numbers, the engines and build order, effort (calibrated on the crossword engine in `activities/`), the asset and rights audit (Shutterstock, developer artwork, audio, Flash/SWF), and recommendations.

## Progress visibility

- `progress.html` auto-refreshes every 30 s. Update it at each milestone: step, counts, findings, next step.
- Short chat updates; `/workflows` during step 5.
- Keep the machine awake. The owner either uses PowerToys Awake, or Claude runs a keep-awake helper (SetThreadExecutionState) and stops it at the end.
