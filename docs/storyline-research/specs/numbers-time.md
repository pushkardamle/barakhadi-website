# Numbers & time: engine spec

Family dossier: `_work/families/numbers-time.json` (27 pids). Preview sheets checked: 6f6263cb48, 0b9f07587c, d349e8ae28, 4411a5a333, f53e18ca73, 91f7e17561, 3196b73a72, 9fdef7acc6, a98d019e62, c9130e72cb, a649679f82, d9cd131b70, 861b3490c8, aa08ee57bd. Web-object zips were unpacked to `_work/scratch/numbers-time/`.

**The dossier has errors. Fix them before extracting anything:**
- **3 pids are not numbers activities.** TalentLMS matching attached them to Sem-2 numbers units by mistake. 861b3490c8 is "उ" vocabulary. aa08ee57bd is "उ" letter tracing and f4d640908d is "ऊ" letter tracing. The real sources are 6a3e7c84d8 (Sem 2 "Vocabulary Module (Ank Activity)"), Sem 2 `Writing Module SCORM 1.2\Optional Writing Module 1` (its sha matches `Level 1\04 Numbers\orig source files\Trace Numbers.story`) and 787f745afa/5b85b37b7d (Clock).
- **Final sources missing from the dossier:** 3fbabc169a `Final Numbers\Numbers 11 to 20.story`, 64399da25e `Ordinal_Numbers_Activity 1 PD.story`, dabda93b06 `Ordinal_Numbers_Actvity 2 PD.story` and 08adebd284 `Ordinal_Numbers_11 to 20 PD Final.story`. All four were published on 2020-12-24 according to published.csv.
- **The ordinal pids in the dossier are drafts.** 9fdef7acc6 sits in `Ordinal\` with player title "Numbers 91-100" and stale draggables ९२–१००. 3196b73a72 sits in `working\` and still has "Instruction for पुल्लिंगी will go here". Both spell नऊवा, and the published finals correct it to नववा.

## 1. What these activities are

**A typical one, seen by a kid: "Numbers 31-40" (6f6263cb48, 7 slides).**
1. **Title card** ("Numbers ३१-४०", stock `intro_act1.mp3`) with a sticker tease. The kid taps Start.
2. **Order the numbers (truck).** A truck trailer has 10 empty slots, and 10 shuffled tiles ३१…४० sit below it. Tapping a tile plays its number (`31.mp3`…`40.mp3`). The kid drags each tile into its slot and taps Check. Feedback is correct or incorrect, with "Attempts Left: %att%" counting down from 3. After that, the Reveal layer shows the answer.
3. **Make the number.** Six rows read "३० + [picture of loose pencils] = [ ]". The kid counts the pencils (`pencil_box2.png` plus `pencil1..9.png`) and drags the total (३२, ३३ …) into the box. The bank holds 6 tiles, and Check, 3 attempts and Reveal work as before.
4. **चला गिरवू या - अंक.** A web object (the Malone canvas app) shows 5 pages. Each page has 2 numerals as outline, then faded copy, then blank lines (`trace_pattern-k1..k5.png`). The kid colours freely with crayon, marker or eraser. Nothing is checked.
5. **चला गिरवू या - अंकांचे शब्द.** The same app traces the number words (एकतीस, बत्तीस …). Only sets 11–50 have this slide.
6. **Join the dots.** The same app shows one page, a ३१→४० dot-to-dot (flamingo) beside writing lines. Nothing is checked.
7. **Congratulations** and a sticker reveal.

**Sub-variants (distinct activities, then dossier pids, then live units):**

| # | Variant | Example / pids | Mechanics | Live units |
|---|---|---|---|---|
| A | Numerals 11–100 "Practising in words / Learn and Write". 9 sets, one per decade | 3fbabc169a (11-20, missing), c123a01fc7 (21-30; its player title "Numbers 31-40" is stale), 6f6263cb48, 4492540631, 0b9f07587c, e85dc31406, 478c3d2658, b2564225e1, 14069bd014. c9130e72cb is a 1-slide TreeTo working fragment (ducklings) | order-the-numbers, make-the-number, trace numerals, trace words (11–50 only), join dots | 12 (L1 11–50, L2 21–100) |
| B | Numbers 1–10, count and reveal | d349e8ae28 (L0 = L1, same sha). Sem 2 original 6a3e7c84d8 | tap objects to reveal colour and hear "३ - तीन पक्षी"; then "अंकांचा खेळ", tap ovals १→१० in order to draw a fish | 3 |
| C | Trace Numbers 1–10 | 4411a5a333 = d1028e0a97 (same sha) | web object only: 5 numeral pages and 1 join-dots page | 4 |
| D | Number Song (अंकांचे गाणे) | f53e18ca73 = 61300b7d48, f98d859972 (2018 Newgen) | 5 conversation callouts (१–२०); a sing-along slide where numeral images fade in with the song (`Recorded 2.mp3`, 1.5 MB); a mystery-phrase reveal | 3 |
| E | Book: Story of Numbers | 91f7e17561 = 6477cbe85b, 902c8de0fe | 6-page read-aloud with Marathi text, an "E" English layer and page-flip MP4s; 3 listening MCQs (Marathi audio → pick the English sentence) | 3 |
| F | Ordinals (क्रमवाचक) | finals 64399da25e, dabda93b06, 08adebd284. Drafts 9fdef7acc6, 3196b73a72, a98d019e62 | drag ordinal word ↔ numeral, one screen per gender (पहिला/पहिली/पहिले). The 11-20 set has a story audio page, then picks the gendered form for a noun (ते घुबड → अकरावे, तो ससा → बारावा, ती कोंबडी → तेरावी) from 9 words, 6 of them distractors | 3 |
| G | Show the Time | a649679f82, 787f745afa | web object: free drawing of hands on 4 clock faces (२:००, ९:३०, ५:००, ४:४५). Nothing is checked | 2–3 |
| H | Clock conversation | d9cd131b70 (Sem 2 wk 6) | dialogue callouts (7:00 … 8:00, circus 1:00 … 2:00); drag 3 picture cards into time order; 2 spoken questions | 1–2 |

That makes **18 distinct activities behind about 32 live units.** Variants A, B, C and F (13 activities) are the core of this family. D, E and H are conversation and book formats.

## 2. Proposed engines

The family needs **one new engine with modes**. It reuses three engines from other families.

**E1 `number-practice` (new, M).** It takes a list of screens, each of a different type. Every screen follows the same loop: tap a tile to hear it, drag or tap, Check, feedback, retry, reveal.
- `count-reveal`: tap a grey picture (`Truck-g.png`); it swaps to colour (`Truck.png`), plays "दोन ट्रक" and shows the caption "२ - दोन ट्रक (2 Trucks)". The screen is done when all items are revealed.
- `dot-order`: tap numbered dots in order 1→N. A line segment draws on each tap, and the finished picture fades in at the end. A wrong tap gives a gentle buzz and the dot shakes; nothing resets.
- `sequence`: tiles go into ordered slots on an illustration (truck, bus, train, worm, ducklings, puppies). Tiles are tap-to-hear. The kid places them by drag **or** by tap-tile-then-tap-slot, which is easier on phones.
- `make-number`: shows "base + N counted objects = ?" and a bank of totals. The pictures come from data; the engine lays out N copies, so no fixed artwork is needed.
- `match`: N targets and a bank that includes distractors. Each target can carry a noun/gender cue ("ती कोंबडी"). This mode covers ordinals and could later cover numeral ↔ word.

Every screen allows 3 attempts, matching Storyline's `att=3`. After a wrong Check, correct tiles lock and only the wrong ones bounce back. After 3 misses, "Show answer" appears.

**E2 `trace-pad` (shared with the letter-trace family; config only here).** It replaces the Malone app with pages of outline images and pointer-events drawing. Numbers need only multi-page support (the old k1..k5 pages) and per-page images for numerals, words, dots and clock faces. The old app does no validation. Stroke checking would be optional; doing it for Devanagari numerals is expensive.

**E3 `clock-set` (optional upgrade, S).** It turns "Show the Time" from free drawing into a real exercise. The kid drags the hour and minute hands, which snap to 5 minutes, to the shown time (२:००, ९:३०, ५:००, ४:४५), and the engine checks the answer. A second mode reads a clock and picks the digital time. This is the only place in the family where a better mechanic is cheap and teaches more.

**Reused engines.**
- Number Song uses the conversation engine plus a `sing-along` mode: an audio track and a cue list (time → numeral) that lights each numeral as it is sung. This sync matters for learning and must be kept.
- Story of Numbers uses the books engine (text + narration + EN toggle + MCQ).
- The Clock conversation uses the conversation engine. Its card sequencing reuses E1 `sequence` with picture tiles.

**Keep:** tile feedback, slot glow, the number spoken on every tap, the completed fish/flamingo picture, the sing-along highlight and the end sticker (shared reward screen). **Drop:** entrance fades and flies (57 in d349e8ae28, 64 in 6f6263cb48), the blink GIFs, the book's 13 page-flip MP4s (use a CSS page turn), the crayon/marker tool art (use 4 swatches and an eraser) and the hover sticker tease.

## 3. Content data model

Example: **Numbers 31–40** (6f6263cb48), shortened. The text and file names are real; pencil counts are derived as total − 30.

```json
{
  "type": "number-practice",
  "id": "L2-numbers-31-40",
  "title": "Numbers ३१-४०",
  "source": "Republished Activities/Level 2/04 Numbers/Final Numbers/Numbers 31 to 40.story",
  "numerals": "deva",
  "attempts": 3,
  "screens": [
    { "kind": "sequence",
      "instructions": "Click on the numbers to listen to the audio and arrange the numbers in the correct order from 31 to 40",
      "instructionsAudio": "media/slide-2.mp3",
      "scene": "media/order_numbers_truck_18_wheeler.png",
      "items": [
        { "label": "३१", "audio": "media/31.mp3" }, { "label": "३२", "audio": "media/32.mp3" },
        { "label": "३३", "audio": "media/33.mp3" }, "… to ४० / 40.mp3"
      ] },
    { "kind": "make-number",
      "instructions": "Drag the numbers in the dashed boxes to show the total",
      "instructionsAudio": "media/slide-3.mp3",
      "base": { "label": "३०", "picture": "media/pencil_box2.png" },
      "unitPicture": "media/pencil1.png",
      "rows": [ { "add": 3, "answer": "३३" }, { "add": 2, "answer": "३२" }, { "add": 9, "answer": "३९" },
                { "add": 5, "answer": "३५" }, { "add": 4, "answer": "३४" }, { "add": 6, "answer": "३६" } ] },
    { "kind": "trace", "engine": "trace-pad", "title": "चला गिरवू या - अंक",
      "pages": ["media/trace-num-1.png", "media/trace-num-2.png", "…5"] },
    { "kind": "trace", "engine": "trace-pad", "title": "चला गिरवू या - अंकांचे शब्द",
      "pages": ["media/trace-word-1.png", "…5"], "words": ["एकतीस", "बत्तीस", "…"] },
    { "kind": "trace", "engine": "trace-pad",
      "instructions": "Join the Dots to draw the picture and then color the picture.",
      "pages": ["media/dots-31-40.png"] }
  ],
  "reward": { "sticker": "media/Stk_Butterfly_80.png" }
}
```

Ordinal `match` screen, from 08adebd284 slide 3:

```json
{ "kind": "match",
  "instructions": "Select the appropriate ordinal numbers word to match the Marathi numbers",
  "targets": [ { "cue": "११", "noun": "ते घुबड", "answer": "अकरावे" },
               { "cue": "१२", "noun": "तो ससा",  "answer": "बारावा" },
               { "cue": "१३", "noun": "ती कोंबडी", "answer": "तेरावी" } ],
  "bank": ["अकरावी","अकरावे","अकरावा","बारावा","बारावी","बारावे","तेरावा","तेरावी","तेरावे"] }
```

**Varies per activity:** title, number range (it generates labels and audio names for A and C), `scene`, `make-number` rows, trace pages, instruction audio and sticker. Ordinals add targets, nouns and bank; 1–10 adds reveal items and dot coordinates. **Fixed:** attempts (3), feedback sounds and screen order.

## 4. Scoring and SCORM tracking

- **Completion:** reach the end screen. Every check screen must be finished (correct, or answer revealed), and trace pages only need to be visited, as in Storyline, where trace was free play.
- **Score:** the share of check items (sequence slots, make-number rows, match targets, dots) right on the **first** Check, from 0 to 100. Stars use the crossword rule: 3 if all right on the first try, 2 on the second, 1 after reveal. Tracing does not count towards the score.
- **Interactions worth recording (SCORM 1.2 `cmi.interactions`, at most 3 per activity):**
  1. `make-number` / `sequence`: a per-screen `result` and `latency`, plus the attempts used. This shows who struggles with place value.
  2. `match` (ordinals): the **wrong word chosen per target**, e.g. `बारावी` for "तो ससा". This catches gender-agreement errors, the most useful signal in the family.
  3. `clock-set` (if built): the target time and the time the kid set, e.g. `9:30 → 6:45`, which catches hour/minute hand swaps.

## 5. Extraction plan

Use the crossword's `tools/parse_story.py` approach and read the zip in memory.

1. **Sequence and match:** `dragDropIntr` → `intrFreeChoice shpG` (drag tile) → `matchShpG` (drop target).
   - Tile text comes from the tile's **base** `<plain>`. Do not take text from states. State text is stale template text: ordinal tiles carry "७१/७४/७८" from the 71-80 template, and the 31-40 states show ५१…५५ from 51-60.
   - Slot order is the drop target `loc.l`, then `loc.t`.
   - A tile with no `matchShpG` target is a distractor (a98d019e62/08adebd284).
   - `intrProps attempts="four" shuffle="true"`. The custom var `att=3` drives "Attempts Left".
2. **Audio ↔ item:** each tile's `OnClick>playMedia` points to a `<sound>`.
   - The sound's `typeName` is the English number ("Fifty-Two", "Sixty" in 0b9f07587c).
   - Its media `orig` is `…\Number 31-40\Audio\31.mp3` (6f6263cb48).
   - Either field maps directly to the number; check both.
3. **Make-number:** the answer is the dragged tile's base text. Rows come from the drop-target `loc.t`. Count the `pencilN.png` pictures in each row's bounding box and check that count = answer − base.
4. **Trace pages:** inside the `.bin` web object (a zip), take `images/trace_pattern-k1..k5.png` (or `trace_pattern k.png` for single-page objects). Then check the page order in `Trace_main.js` (`outlineImageN.src`).
5. **Count-reveal (1–10):** for each group: the grey/colour picture pair (`Truck-g.png`/`Truck.png`), the caption text and the audio orig ("Screen 2_Don_Don truck.mp3").
   - Dot-order: oval `loc` plus text १–१० gives coordinates.
6. **Sing-along cue times:** the `txtTmCtx start` (ms) of each numeral picture on the song slide's Audio layer.
7. **Book:** layer `Text1` holds the Marathi text and `English Text` the English, with narration from `recorded-in-storyline`. Import with the books-family extractor.

**Gotchas:**
- **Metadata is stale everywhere.** `lms_title="Trial_1"`, `project_title_prop="L1-001 a"`, `coursename="Level 1 - Learn and Trace 201"`, and player titles are wrong in c123a01fc7, 9fdef7acc6, c9130e72cb and a649679f82 ("Bonus Writing Module (Clock)"). Name activities from the folder and TalentLMS course instead.
- **Instruction audio is reused.** 31-40, 21-30 and 11-20 play `Numbers 51-60-Trace Instr..mp3` and an 11-20 `Slide 5.mp3`, so check that each says the right range.
- **One audio may be duplicated.** In d349e8ae28, `Screen 3_Daha_Daha Zende.mp3` and `Screen 3_Aath_Aath Phulpakhre.mp3` are both 80,375 bytes, so one may play the wrong number.
- **Stale text in hidden layers.** The book has Lion-book sentences ("सिंह रानटी प्राणी आहे") left in hidden layers, and the whole book appears twice (slides 3–8 and 10–14). Take one copy.
- **Exact duplicates.** L0 and L1 copies are byte-identical (same sha1), so extract once and package per unit.

**Automatic vs by hand:** about **70% automatic** (sequence, match, audio mapping, trace pages, make-number answers). By hand: listening QA (about 10 clips per set), the 1–10 dot coordinates and picture, sing-along cue timing, choosing the final ordinal versions, and Marathi instructions (today English only).

## 6. Reusable assets and rights flags

- **Reuse as-is:** number audio `11.mp3`…`100.mp3` and slide instructions (`path:D:\Barakhadi`, 346 files, the owner's recordings); 151 Storyline-recorded narration clips; 1–10 object pictures (`E:\Marathi School\Anka Activity\…`, 551 Newgen files); TreeTo-era illustrations (`order_numbers_*.png`, `pencil*.png`, `user:pushkar` under `TreeTo Working`).
- **Vendor-owned art; check the contracts:** Newgen (`path:E:\Marathi School`, `path:E:\Sudarshan` stickers `Stk_Butterfly_*` and blink GIFs, `user:sudarshan.jadhav` `watch1.png`, `numbers_marathi_activity.jpg`); TreeTo (`user:tdt-05` `Correct Audio.mp3`, `Incorrect audio.mp3`, `L SL.mp3`).
- **Stock-folder files (58):**
  - `intro_act1.mp3` comes from `Stock Sounds\Audioblocks`. It needs a live Audioblocks licence; otherwise replace it with a shared chime.
  - `the-background-352166.png` and `green_board 2.png` have no recorded source.
  - `order_numbers_truck_18_wheeler.png` looks like a stock photo; verify it.
  - The book's lion photos are likely stock as well.
- **Text-to-speech:** c9130e72cb uses Storyline TTS (`Text to Speech 12–21.vtt`). Do not reuse it; record a human voice.
- **Third-party code:** William Malone's drawing app (Apache-2.0, © 2010) and `excanvas.js` (Apache-2.0). Both get replaced; if any code is kept, keep the NOTICE.
- **Articulate files:** `Parchment.jpeg` is an Articulate Storyline 2 texture under Articulate's licence. Drop it.
- **Fonts:** Mangal (Microsoft, not redistributable) is used in every project, plus the "Articulate" font and Open Sans. Switch to the shared Baloo 2 Devanagari (OFL) already in `activities/shared/fonts`.
- **Video and Flash:** 41 MP4s, all book page flips from `storyline-temp`; drop them. There is no SWF/Flash. 25 EMF images in the ordinal files need converting to SVG or PNG, or rebuilding as CSS tiles.

## 7. Effort

Calibrated against the crossword, where engine, extraction, packaging and tests took about 1 working day.

| Item | Size | AI-assisted days |
|---|---|---|
| E1 `number-practice` (5 screen kinds, tap-to-place on phones, retry/reveal, scoring) | M | 3.0 |
| E2 `trace-pad` number pages (if the letter-trace family builds the engine; otherwise +1.5) | S | 0.5 |
| E3 `clock-set` (optional) | S | 1.0 |
| `sing-along` mode on the conversation engine | S | 0.5 |
| Data + QA for 18 activities at about 60 min each (numeral sets 45, ordinals 60, 1–10 75, song 90, book 60) | — | 2.25 |
| Packaging and TalentLMS checks for about 32 units | — | 0.5 |
| **Family total** | | **about 7.75 days** (9.25 if the trace engine is not shared) |

## 8. Risks, edge cases, open questions

**Risks and edge cases:**
- **Devanagari numerals and words.** ३१–१०० must render as Devanagari digits from data (`"numerals":"deva"`), never through `toLocaleString`. Number words have conjuncts (एक्याण्णव, त्र्याहत्तर, सत्त्याऐंशी), so tiles need font fallback testing and no per-letter splitting.
- **Ordinal spelling.** The finals use नववा/नववी/नववे; the drafts use नऊवा. Confirm which form is correct.
- **Audio sync.** Sing-along cues rely on Storyline timeline offsets, so check them by ear. Don't play a tile's audio again during a drag; play it on tap only. iOS needs a tap before the first sound plays.
- **Touch and small frames.** 10 sequence slots on a 360 px phone need 2 rows of 5. Drag-and-drop must have a tap-to-place fallback. Drawing must use `touch-action:none` on the canvas only, so the page still scrolls. The crossword's `fit.js` scale-down (minWidth 700) is too small for tracing on phones, so use a reflow layout instead.
- **Make-number artwork.** Showing 9 pencils plus a box of 10 must stay legible at phone width, so render the pencils in a grid rather than at absolute positions.

**Questions for the owner:**
1. **Gappa Goshti 2017 units.** Rebuild the Sem-2 units (2–3 learners each: wk 4 Number Song, wk 5 Numbers 1-10 / Trace Numbers / Book, wk 6 Clock / Show the Time), or retire them in favour of the Level 0–2 courses?
2. **Level 2 "Clock" unit (2286).** It matched a649679f82 with low confidence. Is it the conversation module (d9cd131b70) or a duplicate of Show the Time?
3. **Show the Time.** Upgrade to the checked `clock-set` engine, or keep free drawing?
4. **Tracing.** Keep it free-form, or add simple stroke checking later (shared decision with the letter-trace family)?
5. **Instructions.** Should they become Marathi with English subtitles? Today they are English text plus Marathi audio.
6. **Ordinals 1-10.** Activity 1 and Activity 2 are near-identical (gender screens in a different order). Merge them into one unit?
