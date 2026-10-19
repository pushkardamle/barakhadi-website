# Deepti's Content / Assignment units: structural review

**Scope.** These are the TalentLMS units that are not Storyline: Content, Web content, Assignment, Test, Audio and Video. The source is the GET-only download in `_work/tlms/` (525 courses). The API returns unit **names and types only**, not their bodies, so this review covers structure and naming, not teaching quality. No learner names are reproduced here. The owner has said these units stay as they are for now. This file is a map for later work, not a build plan.

## 1. Inventory

**Totals across all 525 courses:** Assignment 582, SCORM/xAPI 339, Content 239, Audio 12, Test 10, Presentation/Document 3, **Web content 3**, Video 2, Section 2, Survey 1.

Live categories only (the `test` category and one course with no category are left out):

| Level / category | Courses | SL + Assignment | SL only | Content-led (no SL) | Assignment-only | SL + Content | Empty | Content units | Assignment units | Other units |
|---|---|---|---|---|---|---|---|---|---|---|
| Gappa Goshti (2016–18) | 93 | 13 | 78 | – | – | – | 2 | 0 | 15 | 1 Test |
| Level 0 Shishu Varga + Ind | 107 | 94 | 7 | – | 6 | – | – | 0 | 124 | 1 Audio |
| Level 1 | 142 | 70 | 21 | 33 | 16 | 2 | – | 68 | 218 | 3 Audio |
| Level 2 | 148 | 11 | 20 | 72 | 37 | 8 | – | 158 | 210 | 2 Audio, 1 Test |
| Level 3 (2021–22) | 7 | – | – | 2 | – | – | 5 | 2 | 4 | – |
| Level 4 | 5 | – | – | – | 1 | – | 4 | 0 | 1 | – |

(SL = Storyline.)

- **Web content (3), Video (2), Survey (1) and Presentation units appear only in test courses.** Raigad Fort and Chan Chan Goshti 1 are in courses 398 and 438. No live course uses them.
- **Courses with no Storyline: 167** in the live levels. Of these, 107 are Content-led and 60 are Assignment-only. Content-led courses cluster in five places:
  - **L2-01** Learn to Read and Write: 31 courses on Jodakshare, Anuswar and Visarg.
  - **L2-06** Grammar: 20 courses.
  - **L1-05** Grammar: 15 courses on verbs, singular/plural and gender.
  - **L1-02 / L2-02** Writing words and sentences: 14 courses.
  - **Creative writing and comprehension:** L1-09, L2-10, L2-11 and L2-12, 24 courses.
- **Assignment-only courses:**
  - Reading Readiness: 36 courses (L1-06 and L2-07).
  - L0-03 Picture words and actions: 6 courses, 5 recordings each.
  - L2-13 Recite: 5 courses.
  - L2-08 Vocabulary lists: 4 courses.
  - L2-09 Simple Crossword: 3 courses.
- **Mixed Storyline + Content: 10 courses.** These are the Numbers-in-words courses (L1 791–792, L2 511–513, 519), the स्वर ॲ/ऑ courses (440–441) and Write Letter and Words 1–2 (477–478). In each one the Storyline unit comes first and Deepti's mini-lesson and assignment follow.
- **Content units by role:**
  - 142 are answer sheets.
  - 35 are named "Mini-lesson".
  - 51 are other lesson pages.
  - 11 more answer sheets are typed as Assignment, in courses 465–469 and 573/574/595.
- **When:**
  - Course shells were created in bulk: Level 2 on 19–20 Sep 2020, Level 0 on 21 Sep and Level 1 on 22 Sep.
  - The `last_update` dates of the no-Storyline courses are 2020: 49, **2021: 94**, 2022: 18 and 2025: 17. Content was being filled in through 2021.
  - Level 3 was started in Aug 2021 – Mar 2022 and has stalled: 5 of its 7 courses are empty.
  - **Authorship check:** the API lists the admin account (creator_id 1) as the creator of 377 of these 379 courses. It does not record that Deepti wrote them; that comes from the owner's account.
- **Reach (unique learners enrolled):** L1 37, L2 21, L0 19, Gappa Goshti 8. Almost every course in a level has the same roster, which points to whole-level group enrolment.

## 2. Patterns

**Typical lesson shapes (live courses):**

| Shape | Count | Example |
|---|---|---|
| Storyline → Assignment(s) | 185 | L1 "Learn and Trace – स्वर अ": SL, Assignment 1, Assignment 2 |
| Storyline only | 126 | Gappa Goshti weeks |
| Assignment(s) only | 59 | Reading Readiness – Jodakshare 1–10 |
| Assignment → Answers (repeated) | 39 | L1 "Gender – Sort by Gender": (A1, Answers 1) ×3 |
| Content → (Assignment → Answers)+ | ~40 | L2 "Pronouns – सर्वनामे": Mini-lesson, (A, Answers) ×3–4 |
| Content → Assignment(s) | 16 | L2 Clock "15 minutes time – सव्वा" |

Deepti's standard lesson is **mini-lesson Content → Assignment n → "Answers for Assignment n" Content**. This shape is very regular in L2 Grammar (the pratyay चा/ची/चे/ला/त/शी/ने/नी series 529–536) and in L1 Grammar.

**Completion rules.** Every course has the rule "All units must be completed" and none has prerequisites. Answer units therefore count toward completion and can be opened whenever the learner likes. The download does not show whether unit order is set to sequential.

**Naming consistency.** The names vary in format but are understandable.

- **101 generic unit names.** Examples are "Assignment 1" and "Answers- Assignment 2". The prefix pattern also varies across `Answers-`, `Answers:`, `Answers for…`, `…-Answers` and `Sample-Answers`.
- **231 names with stray spaces** (leading, trailing or doubled).
- **Typos:** Narative ×2 (course names), Numberes, Jodakhsare, Comnonly ×3, Assignement, Couse, plus doubled "))" in two course names.
- **Likely mistakes in live courses:**
  - Course 342 (अः) contains "**Assignment 2 for अ (clone)**". This looks like a clone of the wrong letter.
  - Course 467 (ड, ढ) is titled "अर्धा दंड" but its lesson unit says "शेवटी उभा दंड".
  - Course 476 (Visarg) has a lesson unit titled "Anuswar- ह्कार…".
  - Course 566 has two units both named "Assignment 1 – Sight Words – 5".
  - Course 488's answer unit lacks the "Answers" prefix.
  - Course 808 places the assignment before the Storyline.
  - In 465–469 and in the crossword courses, the answer sheets are typed as **Assignment**. Learners may have to "submit" just to see the answers.
- **Cross-level duplicates.** These lessons appear in both L1 and L2:
  - Writing Sentences (Word Order, Question Words, आणि, वाक्यरचना)
  - Picture Description 1–3
  - Practicing Numbers 21–30
  - Write Letter and Words – 1
  - Word Search Game 1–3
  - Introduction to Vyanjanmala
  - Verbs, Gender and Singular/Plural mini-lessons

  The bodies are not available, so we cannot tell whether these are copies or level-adjusted versions.

**Test and placeholder courses.**

- **Test category:** 22 courses, 4 of them inactive (the "\*\*\* Coming in December \*\*\*" ×3 and "Course 1").
- **11 active test courses still have `hide_from_catalog = 0`:** temp_wk2, test qa, temp_app1–3, Deepti Test Course, सर्वनाम – १, 010 Passages, 09, test word search, Temp 99.
- **Test courses outside the test category:**
  - "Test – Level 3 – Category 2" (868)
  - "Test_New" (872, Level 4)
  - "Test New 5" (873, no category; Oct 2025). This one is the only course with Sections, and it has a "Welcome to जोडाक्षरे" Content unit and a "my_html_unit" Content unit, which suggests someone was already trying HTML content.
- **Empty shells:** "NCS" (874) was created today with 3 SCORM units, which looks like the pilot upload. The 11 empty live-category courses are:
  - Level 3: 5
  - Level 4: 4 ("Assignment 1" ×4)
  - Gappa Goshti Speak and Practice: 2 ("Assignment 1/2")

## 3. Relation to the HTML5 engine plan

The decisions below are a direction for later. Nothing has to change now.

| Content group | Courses | Recommendation |
|---|---|---|
| L2 Simple Crossword (573, 574, 595) | 3 courses, 6 puzzles | **Quickest reuse.** These are Assignment-based crosswords. If the grids and clues are exported, they fit the existing crossword engine's JSON as-is: no engine work, about 30–45 min per puzzle. |
| Jodakshare (L2-01: intro, सम/विषम, उभी/आडवी जोडणी, 16 "types by दंड" courses) + L2-07 Reading Readiness Jodakshare 1–10 | ~31 | Candidate **conjunct-builder engine**: drag a half-form onto a consonant, then hear and see the conjunct; or sort conjuncts by दंड type. No Storyline covers this today, so it would be new teaching value rather than a migration. Size M (~1.5 days on the crossword calibration). Keep Deepti's mini-lessons as the explanation pages. |
| Anuswar / Visarg rules (L2 471–476) + RR Anuswar 1–5 | 11 | A later fit for a listen-and-choose pronunciation activity. It could share the audio-choice engine planned for the vocab-letter / comprehension families. |
| Grammar sorts: Gender (L1 820–823, L2 544), Singular/Plural (L1 815–818, L2 543), Pratyay series (L2 529–536), Synonyms/Antonyms (L2 545–546) | ~20 | Map to the **grammar-translation** family engines (drag-sort, fill-the-suffix). Deepti's answer sheets already hold the answer keys, which makes them good seed data once exported. |
| Clock सव्वा/दीड/पाऊण/5-min (L2 521–524) | 4 | Fold into the **numbers-time** clock engine, which already has Storyline Clock projects. |
| Reading / Listening comprehension passages (L2-11, L2-12) | 10 | Could become auto-checked questions in the **books-comprehension** engine. Keep the passage as-is. |
| Mini-lessons, creative writing, personal narrative, picture description, recite, conversation follow-ups, L0 picture-word recordings, Reading Readiness read-aloud | ~120 | **Stay as Deepti-authored pages and teacher-graded assignments.** These tasks are open-ended or rely on recordings, and the teacher's feedback is the point. At most, restyle them later with `shared/barakhadi.css` so they look consistent. |

**Quick wins.** All of these are TalentLMS admin work, with no build involved.

1. **Naming convention.** Use `<Lesson> · Mini-lesson`, `<Lesson> · Assignment n – <topic>` and `<Lesson> · Answers n`. Trim spaces and fix the typos listed above. This is about one hour with bulk editing.
2. **Hold back answers until submission.** Turn on sequential unit order, if it is not already on, so each answer sheet unlocks only after its assignment is done. Change the 11 Assignment-typed answer sheets to Content.
3. **Fix the live mistakes:** courses 342, 467, 476, 566, 488 and 808.
4. **Hide or deactivate** the 14 visible test courses. Decide whether the 11 empty shells stay as placeholders.
5. **Decide on the L1/L2 duplicates:** keep them as level-specific versions, or point both levels at one course.

## 4. Questions for the owner

1. Can you export or copy the HTML of **one unit of each kind**? That means a mini-lesson (e.g. 444 सम जोडाक्षरे), an answer sheet, an Assignment, a crossword assignment (573) and the Raigad Fort Web content. This would confirm the format: plain rich text, images, embedded audio, or Google Docs/YouTube links.
2. Should learners see answer sheets before they submit? Is sequential order currently on?
3. Did Deepti author all of these? The API shows only the admin account as creator.
4. Are the L1/L2 duplicate lessons intentional level variants?
5. Is Level 3/4 still planned, or can the empty shells and test courses be archived?
6. Do any Content units embed third-party images, PDFs or videos that we would need to replace before reusing them in engines?
