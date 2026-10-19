# Word games: engine spec

Family dossier: `_work/families/word-games.json` (6 pids). Checked against `match.json`, the parses and the `.story` XML, which I read in memory and never wrote to.

**Correction to the dossier.** In both levels, TalentLMS units "Word Search Game - 1" (3166 L1, 3172 L2) tied on match score (margin 0.0). They were attached to Activity 2 (L1, `4a03da2daf`) and Activity 1 (L2, `215bd365dd`). Two live packages are missing from the dossier: **Word Search Activity 1 Level 1 (`1cdd9789da`)** and **Word Search Acticity 2 Level 2 (`7f590d6113`)**. Both have published zips in `published.csv` ("RePublished\Word Search Activity 1 Level 1.zip", 2020-12-01). Most likely Game-N = Activity N. **Real scope: 8 live packages, 8 units.**

| Sub-variant | Live projects (pid) | Units / learners |
|---|---|---|
| Word search, Level 1: 6×6 grid, 6 words × 3 puzzles | Activity 1 `1cdd9789da`, Activity 2 `4a03da2daf`, Activity 3 `b429e8b4f4` | L1 Game 1–3 (3166–3168), 44 |
| Word search, Level 2: 8×8 grid, 8 words × 3 puzzles | Activity 1 `215bd365dd`, Activity 2 `7f590d6113`, Activity 3 `78c2f30289` | L2 Game 1–3 (3172, 3173, 3169), 27 |
| Crossword lesson (2 crosswords + 2 alphabetical-order games) | "01 Crossword" `a38f40ce5f`; slide for slide the same as the Newgen source `acc6b740ad` | Crossword (2291), 25 |
| Chitra-Shabda Jodya (picture–word set, "Sea shore") | `e650f04f88` (+ SL2 backup `8214ee277e`, Newgen source `2fbdff7b9f`) | 3174, 27 |
| Treasure Hunt | `35307618ae`, Newgen source only, **not live** | none |

Treasure Hunt is a riddle-and-clock game ("झाडाखाली किती नारळ पडले आहेत?" → set the clock), which belongs with numbers-time. Out of scope here.

`TreeTo Working\Word Search Working\` holds about 30 old or working copies (e.g. `89d8074f82` "Word Search Pushkar Template", `699e7d997b` "…Nov 11"). Some carry stale titles like "Learn and Trace - व्यंजन क" (`12cc45f652`). Never extract from them.

## 1. What these activities are

**Word search (kid's view, L1 Activity 2 `4a03da2daf`, preview sheet looked at):**
1. **Title.** A "Word Search / शब्द शोध" splash with narration (`First Slide.mp3`), then Start.
2. **Puzzle 1, "Read the clues".** A 6×6 grid of akshara tiles sits on the left. A Clues panel lists पांढरा हिरवा काळा पिवळा केशरी जांभळा. The kid taps tiles. When every tile of a word is selected, the tiles turn "Correct", a capsule outline appears around the word, the clue gets a tick and a generic `Correct Audio.mp3` plays. A stopwatch (`watch1.png` × 9, wipe animations) runs. After 60 s (the "Timer" layer, 59.75 s) the **Reveal All** button unlocks with `Ding-31.mp3`. Next stays disabled until all 6 words are found or the answers are revealed.
3. **Puzzle 2, "Listen to the audio clues".** Six play buttons. Each plays one word: झाला होता कारण आणि किंवा सगळे.
4. **Puzzle 3, "Look at the picture clues".** Six bird pictures: पोपट चिमणी कावळा घुबड बदक कबुतर.
5. **End screen.** "Word Search Completed" (`Last Slide.mp3`).

Every word search project has the same three clue modes: text, audio, picture. Words run only left→right or top→bottom, with one akshara per tile. Level 2 grids are 8×8 with 8 words and much heavier conjuncts (महाराष्ट्र, प्राणीसंग्रहालय across 7 tiles, उत्सुकता). Across the family that is 18 puzzles and 126 words.

**Crossword lesson (`a38f40ce5f`, sheet looked at):** title (chalkboard) → crossword 1 → "Help the hungry bunny": drag कागद गणपती [गलबत pre-placed] तबला पतंग onto steps labelled with consonant rows (क ख ग घ ङ … त थ द ध न, प फ ब भ म). Each correct drop plays the word and moves the bunny up a step, until it reaches the carrot → crossword 2 → "Help the bird get to the nest" (करकोचा चाळीस तास बदक साबण onto signposts labelled क/च/त/प/श rows) → sticker page ("फुलपाखरू", 0–5 star layers). **The engine in `activities/` covers only slides 2 and 4.** Its own README says the alphabetical-order game, the title screen and the sticker page are still to do.

**Chitra-Shabda Jodya (`e650f04f88`, sheets looked at):** one theme with 6 words (छत्री लाटा वाळू बॉल शिडाची बोट सतरंजी), played as 4 mini-games:
- (a) "Guess the word": 6 face-down cards. Each has an audio riddle; tap a card to flip it and see the picture with the Marathi + English word.
- (b) Drag the 6 word labels onto a beach scene, then tap the magic wand (glitter + beach audio).
- (c) Complete 4 sentences with picture clues by dragging words into the blanks, e.g. "छत्री जवळ सतरंजी आहे.", "लाटा दगडावर आपटत आहेत.", with Check after each.
- (d) Read 3 sentences and choose 1 of 2 words: "मला पोहायचे आहे." → लाटा / सतरंजी.
- Then a sticker ("वाळूचा किल्ला").

## 2. Proposed engines

**Engine A: `wordsearch` (new; this is the bulk of the family).**
- **Data:** 1 package = 1–3 puzzles in sequence. Each puzzle is a grid plus words, and each word has a clue of kind `text`, `audio` or `picture`.
- **Interaction:** press on the first akshara and drag to the last, snapping to a straight line (pointer events). A tap-first/tap-last fallback covers small fingers.
- **Not the Storyline toggle.** Storyline only checks that a word's tiles are all "Selected". Ignoring extra tiles means **a kid can select all 36 tiles and solve everything**.
- **Directions:** across and down only, which is what all 18 puzzles use. Reversed and diagonal can be data flags, off by default.
- **Shared cells are required.** Seven puzzles overlap words, e.g. पिसे/पिसारा share (5,2) in `215bd365dd`; ग्रहण/ग्रह, आम्हाला/आपल्याला and सफरचंद/जास्वंद do too.
- **On success:** tile colour + capsule, clue tick, a chime (`shared/sound.js`), plus the word's audio where one exists.
- **On a wrong line:** a gentle shake and a counter. Keep this signal.
- **Show answers:** appears after `revealAfterSec` (default 60), as in the original. Revealed words are drawn in a different colour and don't count.
- **Drop:** the 9-frame stopwatch, the opening/closing JPG splashes (replace with a CSS title card) and the wipe entrances.
- **Layout:** grid on top and clues below (phone); side by side in landscape. With 8×8 tiles at 34 px the grid fits a 320 px phone with 16 px gutters. Use `fit.js` for the TalentLMS frame.

**Engine B: `wordorder` (new, small; the missing L1-003 game).**
- **Task:** drag words from a bank into N ordered slots. Each slot shows its varga-row hint, and one slot can be pre-filled.
- **Feedback:** a correct drop snaps, plays the word audio and moves a character one step (CSS transform; theme `bunny` or `bird`, art reused). A wrong drop springs back.
- **Kept on purpose:** the character's climb is the progress bar, so it stays. Motion paths and the "Pause" layers are decorative and go.
- **Words come from the crossword:** both games use exactly that crossword's 5 words, so the data can reference the crossword file.

**Lesson runner (shared, small).**
- **Why:** each live unit is a whole `.story`. The Crossword unit is title → crossword → wordorder → crossword → wordorder → sticker. The rebuild should be **one SCORM package per unit**, so `package.py` needs a `sequence` manifest that mounts engines one after another and reports once.
- **Shell:** the title and sticker/stars screens are the same Newgen shell used across Release 2 (`star_1.png`, `sticker_banner_3.png`). Build them once, and share them if another family already has.

**Engine C: Jodya.** It is a one-off with 4 modes. Don't build a dedicated engine. Assemble it in the runner from generic pieces: flip-card reveal, drag-label-to-scene hotspots, sentence-blank drag, and 2-option choice. Reuse those from the vocab and grammar families if they exist. The estimate below assumes a standalone build in case they don't.

## 3. Content data model

Real data from `4a03da2daf`, extracted automatically (grids abbreviated to the first 2 rows in puzzle 2):

```json
{
  "type": "wordsearch",
  "id": "L1-WS-2",
  "title": "Word Search Game - 2",
  "titleMarathi": "शब्द शोध",
  "source": "Republished Activities\\Level 1\\02 Listen and trace\\Word Search Activity 2.story",
  "introAudio": "media/first-slide.mp3",
  "revealAfterSec": 60,
  "puzzles": [
    {
      "clueKind": "text",
      "instructions": "Read the clues. Click on the letter tiles to find the words.",
      "instructionsAudio": "media/slide-1.mp3",
      "grid": [["जां","भ","के","श","हि","र"],["पां","का","ळा","वा","र","पि"],["ढ","ना","पो","ला","वा","नि"],
               ["रा","पि","प","के","श","री"],["ना","व","रा","ल","हि","पां"],["ला","ळा","रा","जां","भ","ळा"]],
      "words": [
        {"text":"पांढरा","row":1,"col":0,"dir":"down","len":3},
        {"text":"हिरवा","row":0,"col":4,"dir":"down","len":3},
        {"text":"काळा","row":1,"col":1,"dir":"across","len":2},
        {"text":"पिवळा","row":3,"col":1,"dir":"down","len":3},
        {"text":"केशरी","row":3,"col":3,"dir":"across","len":3},
        {"text":"जांभळा","row":5,"col":3,"dir":"across","len":3}
      ]
    },
    {
      "clueKind": "audio",
      "grid": [["झा","ला","या","जा","हो","हा"],["क","ण","का","र","ता","टी"]],
      "words": [{"text":"झाला","row":0,"col":0,"dir":"across","len":2,"clue":{"audio":"media/ws2-p2-w1.mp3"}}]
    },
    {
      "clueKind": "picture",
      "words": [
        {"text":"पोपट","row":0,"col":1,"dir":"across","len":3,"clue":{"picture":"media/level_1_png.png"}},
        {"text":"कबुतर","row":5,"col":1,"dir":"across","len":4,"clue":{"picture":"media/level_6_bird.png"}}
      ]
    }
  ]
}
```

- **Fields that vary per activity:** grid, words (text, row, col, dir, len), clue audio or picture, instructions text and audio, title, `revealAfterSec`.
- **Fixed in the engine:** sounds, colours, behaviour.
- **`len` counts aksharas, not code points.** The grid is an array of strings, so "ष्ट्र" is one cell.

The `wordorder` example comes from crossword-1 in `a38f40ce5f`:

```json
{"type":"wordorder","id":"L1-003-order-1","theme":"bunny","instructions":"Arrange the words in alphabetical order by dragging them in the correct boxes.",
 "slots":[{"hint":"क ख ग घ ङ","word":"कागद"},{"hint":"क ख ग घ ङ","word":"गणपती"},{"hint":"क ख ग घ ङ","word":"गलबत","prefilled":true},
          {"hint":"त थ द ध न","word":"तबला"},{"hint":"प फ ब भ म","word":"पतंग"}],
 "wordAudio":{"कागद":"media/w-kagad.mp3"}}
```

## 4. Scoring & SCORM tracking

- **Word search:**
  - Completion: every puzzle finished, whether all words were found or the rest were revealed.
  - Score: words found without reveal ÷ all words.
  - Interactions (at most 2 per puzzle):
    - `ws-p{n}`, type `fill-in`, `student_response` = the words that had to be revealed. These are the hard words, often conjunct-heavy.
    - A wrong-line count with latency, which tells guessing apart from searching.
- **Crossword lesson:**
  - Keep the existing crossword scoring: 3/2/1 stars by attempt; score = share of blanks correct.
  - Add `wordorder` first-try placements.
  - Interactions:
    - Per crossword, the **wrong tiles placed on each blank**. The bank's decoys are mātrā traps (ति/ती, टं/तं), so these show ि/ी confusion.
    - Per ordering game, the number of wrong drops.
  - Report once at the end of the sequence, not per screen.
- **Jodya:** the score is the 4 sentences in (c) plus the 3 choices in (d). Record each wrong sentence item. Mini-games (a) and (b) count only for completion.
- **Status:** SCORM 1.2 completed/passed with `cmi.core.score.raw`, through the existing `lms.js`. Test in TalentLMS whether Devanagari survives in `student_response`. If it doesn't, send word ids like `w3` plus a romanised label.

## 5. Extraction plan

I have tested this extraction on all 6 word search projects (script in the session scratchpad; port it into `activities/tools/`).

1. **Tiles** are `rect` shapes with a `Selected` state. **The akshara text lives in the `Normal` state's `<plain>`, while the shape's own `<plain>` is empty.** That is why the preview renderer draws slide 2's letters on every slide. Rows and columns come from the distinct `loc` l/t values. Each grid appears twice (base layer plus the "Reveal All" layer), so dedupe by position.
2. **Answers.** Each slide has one `OnStateChange → adjustVar` trigger per word. Its `stateLst` holds the GUIDs of that word's tiles, and it sets `Color1`/`Object1`/`Bird1`… = "word1". Map the GUIDs to cells to get the word, its start and its direction. This is 100% automatic: 126 of 126 words came out.
3. **Clue to word.** `OnVariableValueChange(varChangeG=WordK)` sets a clue object to "Correct". For picture clues that object is the picture (`assetG` → `story.xml <media displayName>`). For audio clues it is the play button, whose `OnClick → playMedia` names the sound. The sound bytes are found by file size in `story/media/`, as `render_preview.py` does.
4. **Text clues** are the clue textBoxes' `Normal` state.
5. **Words in the ordering game.** Correct pairs come from `OnDrop` triggers with a `dropLst`; the order is the drop targets' x positions. A word with no drag trigger is the pre-filled slot (गलबत).

Gotchas:
- **Answer-key note:** an off-slide note ("Cuadro de texto", l=994, e.g. "Color1=Shabd1:पांढरा") gives the answers but uses wrong variable names: slide 3 says `Word1` while its triggers use `Object1`. Use it only as a cross-check.
- **Bug in a live package:** in `215bd365dd` slide 2, the clues कंठ, पंख, चोच and पिसारा have the `Correct` state text "तुरा". A learner who finds कंठ sees the clue change to तुरा. Take clue text from `Normal`.
- **Fake visarga:** स्वत:ला (`7f590d6113`) and दु:ख (`78c2f30289`) are typed with ASCII ":" (U+003A), not visarga ः (U+0903). Normalise them.
- **Filler tiles in Level 2** still carry Level 1 colour syllables (के श, हि र, जां भ ळा) and could accidentally spell words. Run a check that no clue word appears in an unintended place.
- **Trimmed audio clips:** in `4a03da2daf` all 6 audio clues have displayName "L1-Activity 2.mp3" but are different trimmed assets. Map by asset GUID, never by name.
- **Stale metadata:**
  - `coursename` = "Level 1 - Learn and Trace 001" on all word searches, and "Level 1 - Learn and Practice 003" on Jodya.
  - LMS lesson title "Trial_1".
  - Project id L1-09-001 shared by the crossword and Jodya.
  - Player title typo "Acticity".
  - TalentLMS course 768's description says "Writing words - 3".
  - Use the TalentLMS unit names instead.
- **Recorded audio:** Jodya and crossword audio is "Recorded" in Storyline (no file names). Map it through layer names (Chatri, Lata, Valu…) and triggers, and listen to every clip once.

**Expected share extracted automatically:** word search about 90% (grid, answers and clues are automatic; audio-clip mapping still needs a listen); crossword lesson about 85% (crossword JSON done; order data automatic; word audio needs a listen); Jodya about 50% (sentence-blank geometry and card riddles by hand). **About 85% overall.**

## 6. Reusable assets & rights flags

- **Reusable as-is (after optimising):**
  - Word search clue pictures (`level_*_png.png`; L2 `WS_L2_A1_P1_jackfruit.png`, `L2_A2_1_rhino.png`, …).
  - Clue audio clips and instruction narration (`Slide N.mp3`).
  - Crossword pictures (already in `activities/content/L1-003/media`).
  - Jodya pictures `04-004-*.png`, `Bunny.png`.
- **TreeTo (2020 republish, `path:D:\Barakhadi\Words Search\…`):** backgrounds `backg_*.jpg`; `ws_opening_slide.jpg` and `ws_closing_slide.jpg` from a Google Drive download; clue pictures; voice. Ownership should be clear under the TreeTo contract, so confirm it.
- **Level 2 clue pictures** sit under `user:pushkar`, in "TreeTo Working\…\level 2 pics". **Their source is unknown and they look like web clipart. Verify the licence or regenerate them.**
- **Newgen (`path:E:\Marathi School`, `user:sudarshan.jadhav`, `user:user`):** crossword and Jodya art, `watch1.png`, play buttons. These are work-for-hire, presumably owned.
  - `bunny_jump_sequence_00.mp3` came from sudarshan's Downloads folder: a third-party sound effect with no known licence. **Drop it** and use a generated chime.
  - `Ding-31.mp3` and `Correct Audio.mp3` (`user:tdt-05`) are sound effects of unknown origin. Replace them with `sound.js` tones.
- **Stock folder (`Marathi Shala\Stock Photos`):** `the-background-352166.png` (all 6 word searches), `star_1.png`, `round_1.png`, `green_board 2.png`, `sticker_banner_3.png`, `cert_4_main.png`. Need proof of licence before reuse; otherwise redraw them in CSS.
- **Articulate-owned:** `Parchment.jpeg` (Storyline 2 texture, Jodya) and the 3.5 MB `6fs2K5V4yN3.fbr` font bundle in every project. Don't reuse either.
- **Recorded voice:** 30 clips in the crossword and 27 in Jodya, recorded in Storyline, narrator unknown. Confirm consent to reuse.
- **Fonts:** Mangal, MV Boli and the "Articulate" icon font. Replace with the bundled Baloo 2 (OFL).
- **No Flash, SWF, video or web objects** in this family.

## 7. Effort

Calibration: the crossword took about 1 session (≈1 day) for engine, extraction, packaging and tests, and the shared pieces now exist.

| Item | Size | AI-build days |
|---|---|---|
| `wordsearch` engine + extractor + tests | M | 2.0 |
| `wordorder` engine (bunny/bird) | S | 0.75 |
| Lesson runner (`sequence` packaging, title/sticker shell); 0 if another family builds it | S | 0.5 |
| Jodya modes (flip card, label-to-scene, sentence blanks, 2-option choice); about 0.5 if reused | M | 1.5 |
| **Engines subtotal** | | **4.75** |

Per-package data/QA:

| Package | Count | Minutes each | What it covers |
|---|---|---|---|
| Word search | 6 | 45 | 3 puzzles; run extractor, listen to 6 clue clips, check visarga and overlaps, phone test |
| Crossword lesson | 1 | 90 | 2 ordering datasets, word audio, sequence QA |
| Jodya | 1 | 180 | |

That is ≈540 min ≈ 1.25 days, or ≈68 min per package on average.

**Family total ≈ 6 AI-assisted days.** This drops to ≈4.5 if the runner and generic drag/choice pieces come from other families.

## 8. Risks, edge cases, open questions

**Risks and edge cases:**
- **Aksharas.** Tiles hold clusters like ष्ट्र, प्रा, स्वं, ल्ली and र्णि (reph). Store the grid as strings and never split them. Check that Baloo 2 renders every conjunct at 18 px in a 34 px tile. Tap targets must be at least 34 px, so a 9×9 grid would not fit a phone; cap the grid at 8×8.
- **Touch.** Drag-select must use `touch-action: none` on the grid, or iOS scrolls the page instead of selecting. Drag and drop in `wordorder` must use pointer events, as the crossword does, not HTML5 drag-and-drop.
- **Audio.** iOS needs a user gesture before the first sound, so the Start tap unlocks audio. Play one clip at a time (`sound.js`).
- **Overlapping words.** Already-found cells must stay selectable for a second word that crosses them.
- **Small frame.** The clue panel moves under the grid; picture clues become a 3×2 or 4×2 strip.

**Open questions for the owner:**
1. Do Game-1/2/3 map to Activity 1/2/3 in both levels? The matcher tied, but the published zips suggest yes.
2. Should found words speak the word aloud? The originals play only a generic "correct" sound, and no recordings exist for text or picture clues, so this would need new recordings or approved TTS.
3. Keep the 60-second Reveal All timer, or show answers after N wrong lines?
4. One SCORM package per unit (the whole crossword lesson in one unit, as today), or split the crosswords and ordering games into separate units?
5. Fix the तुरा clue bug and the ASCII visarga silently in the rebuild? (Recommended.)
6. Who owns the Level 2 clue pictures, the stock sticker/background images and the Storyline-recorded voice?
7. Treasure Hunt (`35307618ae`) was never published. Leave it unbuilt?
