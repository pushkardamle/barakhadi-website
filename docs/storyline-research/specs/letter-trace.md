# Engine spec: letter-trace ("Learn and Trace" letter lessons)

**Scope.** 51 Storyline 3 projects, all SCORM 1.2 (dossier `_work/families/letter-trace.json`), behind 67 TalentLMS units. 16 projects also sit in Gappa Goshti "Week NN - Learn and Trace X" / "Sem. N - Week N - Writing" courses, for example L1-101 K = Week 09 क.

**Checked:** preview sheets for L1-101 K (78c972b469), L1-012-Am (847ae87ddf), L1-103 Ga (b86f4d81f6), L1-105-Gna (200f1d52a1) and L1-132-S (bd5bebedac). I also unpacked every trace web object into `_work/scratch/letter-trace/` (contact sheets `sheet_main.png` and `sheet_bk.png`).

## 1. What these activities are

**A walk through one lesson, as a child sees it: L1-101 K "Learn and Trace - व्यंजन क"**
1. **Title.** A chalkboard shows "चला शिकू या अक्षरे", a big क and a greyed sticker teaser. Start.
2. **"क"चे शब्द.** Three cartoons, each missing a jigsaw piece. Dropping the piece in completes the picture and plays its sentence: कावळा कुंपणावर बसला आहे. / कपडे कपाटात कोंबले. / कुलपाची किल्ली कुठे विसरली?
3. **चला शिकू या - क.** A stroke-order video (`Trace K_final.mp4`), with Watch Again.
4. **चला गिरवू या - क.** A web object shows a 4-panel sheet (`trace_pattern k.png`):
   - a dark outline with numbered arrows (१ down, २ curve, ३ headline last)
   - a lighter outline
   - a faint outline
   - a blank panel between guide lines ("इथे दोन रेषांमध्ये क लिहून बघा")

   The child scribbles with crayons or markers. **Nothing is checked.**
5. **Word Hunt.** Six pictures (कमळ, चाक, कागद, कात्री, झाड, घर). Tap a picture to hear its word, press the yellow button under each क-word, then Check. A Correct or Incorrect layer follows, then Reveal All. A timer with 3 cue points drives the Star1–3 variables.
6. **"क"ची बाराखडी.** The song plays (`Recorded.mp3`, 951 KB) while a second web object cycles `trace_pattern-k1/k2/k3.png`: 12 outline forms (का…कः) with no arrows.
7. **बाराखडी वाचन.** Four words: कीटक, कैरी, कौतुक, कुलूप. Listen, pick 1 of 3 matra tiles (`04_deergha_velanti.png`…) to fill "क _टक", then Check.
8. **अभिनंदन.** The sticker reveal (कासव, `stk_turtle_80.png`), plus hard-coded "Go to course 102 ख?" jumpToFileUrl lightboxes.

A ①–⑥ page bar allows free jumping between screens. LMS completion is "slides viewed" (`slidesviewed="-1"`), and no score is sent.

**How the lessons differ** (slide-type classifier run over all 51 parses):

| Sub-variant | Count | Flow | Examples |
|---|---|---|---|
| Swar | 13 + 2 Level-2 "Learn and Practice" (ॲ ऑ) | title → word reveal (tap a grey object, it colours in and its word plays; 3 words) → video → trace → word hunt → sticker | L1-004 ee, L1-012-Am, L1-014-Aya |
| Vyanjan, full | 33 | the 8 slides above | L1-101 K … L1-136 Dnya |
| Vyanjan, rare | 2 | title → "Anka_Intro_Animation" video + image-click words → video → trace → sticker | L1-105-Gna ङ, L1-110-Yna ञ |
| Vyanjan, reordered | 1 | trace is slide8.xml (last in the scene), reached via the nav bar | L1-134-L ळ |

The vyanjan slide 2 always holds 3 picture+sentence+audio items, wrapped in one of **5 rotating gimmicks**:
- jigsaw (8): K, Cha, T, t, P, Y, Sha, Dnya
- crystal ball `cbal_1-3` (7): Kha, Chha, Tha, th, Pha, R, S
- film-strip lamp (7): Ga, Ja, D, d, B, l, H
- spin wheel `Spin1-3` (7): Gha, Z, Dha, dha, Bha, V, L
- balloon burst `Brust 1-4` (5): N, n, M, Sh, Ksha

## 2. Proposed engines

The family needs one **lesson engine with screen modules** plus one **shared tracing engine**. The tracer is shared because `trace-write` (58 projects) and "Trace Numbers 1-10" (`numbers-time`) need it too.

### Engine A: `tracer` (stroke-aware tracing)

**What it replaces.** Trace_main.js is William Malone's 2010 canvas drawing app (Apache-2.0) plus excanvas.js.
- The canvas is a fixed 705×469 (`multTx = 0.705`), with separate touch and desktop copies of the code.
- Touch position is `pageX - offsetLeft`, which breaks when the frame is scaled.
- The eraser paints white, and a hidden "next" hotspot cycles the 3 barakhadi sheets.
- There is no stroke model, no checking and no signal back to Storyline.
- Every outline is named `trace_pattern k.png` whatever the letter, but all 85 images differ (md5).

**Steps**, mirroring the old 4 panels:
1. **Watch.** Strokes animate in order with number badges and direction arrows. This replaces the 51 videos.
2. **Guided.** A light band, a pulsing start dot, then trace.
3. **Faint.** The band at 30%, and the start dot only for stroke 1.
4. **Write.** Blank guide lines, with a lenient check: at least 60% of checkpoints covered, in any order.

**Validation:**
- Each authored polyline is resampled to checkpoints every ~4% of the box.
- The pen must start within R_start of point 1 (12% of box height on easy, 8% on normal).
- It must pass the checkpoints in order, within R (10% or 7%). Following the order is what checks direction.
- The stroke is accepted at 85% coverage once the end is reached.
- If the pen strays past 1.6R for 150 ms or starts at the wrong end, the ink fades, a soft boop plays and the start arrow pulses.
- Dots (ं ः, the dot of ङ) are taps within R.
- An accepted stroke snaps to clean ink, and the next number appears.
- When the letter is done, a chime plays and a star appears.

**Input:** Pointer Events, `touch-action: none` on the trace surface only, `setPointerCapture`, primary pointer only (iPad palm). Coordinates come from `getBoundingClientRect()` mapped to the viewBox, so `fit.js` zoom and iframe scaling are harmless. The canvas is sized by devicePixelRatio.

**Rendering:** the guide is drawn **from the stroke data** as a fat rounded SVG path, not from a font or PNG. What the child sees therefore always matches what is checked, and Marathi forms (अ झ ण ल श) don't depend on the font. The colour pickers and eraser are dropped; one Clear button and a random crayon colour stay.

### Engine B: `letter-lesson` (screen sequencer)

The data lists the screens, a step-dot bar replaces the ①–⑥ bar, and audio uses `shared/sound.js`.

| Screen | Mechanic | Keep / drop |
|---|---|---|
| `title` | letter, intro audio, Start | keep the sticker teaser |
| `words` | 3 cards; tap one → it colours in, the audio plays and the text highlights | **one** treatment replaces reveal, jigsaw, crystal ball, film strip, spin and balloons (decorative); optional `skin:"jigsaw"` later |
| `demo` | tracer in watch mode | old mp4 kept as `video` fallback until strokes are authored |
| `trace` | tracer steps 2–4 | gates completion |
| `wordhunt` | tap to hear, toggle "has क", Check; 2 tries, then Reveal | drop the timer and time stars |
| `barakhadi` | song play/pause + tracer over the 12 forms (lenient) | optional cue-timed highlight |
| `matra-choice` | listen, tap 1 of 3 matras rendered as text, the word fills in, Check; 2 tries | — |
| `reward` | sticker pop, 1–3 stars, "Score saved" | drop the "Go to course 10x" links |

Animations worth keeping: stroke animation, the reveal, correct/wrong feedback and the sticker pop. Animations to drop: swivel and fly entrances, the spinning lamp or wheel, and the timer bar.

## 3. Content data model

L1-101 K, abridged, with real strings and file names from `_work/projects/78c972b469.json`:

```json
{
  "type": "letter-lesson", "id": "L1-101-ka", "letter": "क", "kind": "vyanjan", "lang": "mr",
  "title": "Learn and Trace - व्यंजन क",
  "source": "Republished Activities/Level 1/01 Learn to read and write/Vyanjane/L1-101 K.story",
  "screens": [
    { "type": "title", "heading": "चला शिकू या अक्षरे", "audio": ["media/L1-031-00-Intro.mp3", "media/L1-031-01-K.mp3"] },
    { "type": "words", "heading": "\"क\"चे शब्द", "instructionsAudio": "media/L1-031-10-Intro.mp3", "items": [
        { "text": "कावळा कुंपणावर बसला आहे.", "picture": "media/031-k-pz_1-solved.png", "audio": "media/L1-031-11-Kavla.mp3" },
        { "text": "कपडे कपाटात कोंबले.", "picture": "media/031-k-pz_2-solved.png", "audio": "media/L1-031-12-KapadeC.mp3" },
        { "text": "कुलपाची किल्ली कुठे विसरली?", "picture": "media/031-k-pz_3-solved.png", "audio": "media/L1-031-13-KulupC.mp3" } ] },
    { "type": "demo", "heading": "चला शिकू या - क", "strokes": "strokes/ka.json", "audio": "media/L1-031-21-K.mp3", "video": "media/trace-k.mp4" },
    { "type": "trace", "heading": "चला गिरवू या - क", "strokes": "strokes/ka.json", "instructionsAudio": "media/L1-031-30-Intro.mp3",
      "steps": ["guided", "faint", "write"], "tolerance": "easy" },
    { "type": "wordhunt", "heading": "\"क\"चा खेळ - \"क\" Word Hunt", "instructionsAudio": "media/L1-031-40-Intro.mp3", "attempts": 2, "items": [
        { "word": "कमळ", "gloss": "Lotus", "picture": "media/lotus_2.png", "audio": "media/wh-kamal.mp3", "hasLetter": true },
        { "word": "चाक", "gloss": "Wheel", "picture": "media/wheel.png", "audio": "media/L1-031-43-Chaak.mp3", "hasLetter": true },
        { "word": "कागद", "gloss": "Paper", "picture": "media/paper.png", "audio": "media/L1-031-42-Kagad.mp3", "hasLetter": true },
        { "word": "कात्री", "gloss": "Scissors", "picture": "media/scissors.png", "audio": "media/L1-031-46-Katri.mp3", "hasLetter": true },
        { "word": "झाड", "gloss": "Tree", "picture": "media/tree.png", "audio": "media/L1-031-44-zaad.mp3", "hasLetter": false },
        { "word": "घर", "gloss": "Home", "picture": "media/house.png", "audio": "media/L1-031-41-Ghar.mp3", "hasLetter": false } ] },
    { "type": "barakhadi", "heading": "चला गिरवू या - “क”ची बाराखडी", "song": "media/ka-barakhadi-song.mp3",
      "forms": ["का","कि","की","कु","कू","के","कै","को","कौ","कं","कः"], "strokes": "strokes/ka.json" },
    { "type": "matra-choice", "heading": "क - बाराखडी वाचन", "attempts": 2,
      "instructions": "बटणावर क्लिक करून शब्द ऐका आणि योग्य तो पर्याय निवडून शब्द पूर्ण करा.", "items": [
        { "answer": "कीटक", "stem": ["क","_","टक"], "options": ["ी","े","ि"], "gloss": "Insect", "audio": "media/L1-031-62-Kitak.mp3" },
        { "answer": "कैरी", "stem": ["क","_","री"], "options": ["ौ","े","ै"], "gloss": "Raw Mango", "audio": "media/L1-031-61-Kairi.mp3" },
        { "answer": "कौतुक", "stem": ["क","_","तुक"], "options": ["ो","ा","ौ"], "gloss": "Praise", "audio": "media/L1-031-63-Kautauk.mp3" },
        { "answer": "कुलूप", "stem": ["क","_","लूप"], "options": ["ि","ू","ु"], "gloss": "Lock", "audio": "media/L1-031-64-Kulup.mp3" } ] },
    { "type": "reward", "sticker": "media/stk_turtle_80.png", "stickerAnim": "media/turtule_gif.gif", "stickerWord": "कासव", "audio": "media/L1-031-71-Kasav.mp3" }
  ]
}
```

Notes on this example:
- `wh-kamal.mp3` and `ka-barakhadi-song.mp3` stand in for `Recorded`/`CopiedAudio_*` clips that the extractor maps through the triggers.
- The distractors are the source's Inc1/Inc2 state texts (केटक, किटक, कौरी, केरी, …).

**Stroke file** (one per glyph, shared across families). The viewBox is 0–100, with head line y=25 and baseline y=75; the points are illustrative:

```json
{ "glyph": "क", "guides": { "head": 25, "base": 75 },
  "strokes": [
    { "n": 1, "kind": "line",  "pts": [[60,25],[60,88]] },
    { "n": 2, "kind": "curve", "pts": [[58,42],[40,36],[30,48],[40,58],[58,50],[72,46],[78,58],[70,70]] },
    { "n": 3, "kind": "line",  "pts": [[22,25],[86,25]] } ],
  "matraAnchor": { "stemX": 60, "right": 86 } }
```

**What changes per lesson:** the letter, kind, title, the screen list (6, 8 or 5 screens), the words or sentences, pictures, audio, `hasLetter` flags, matra items, sticker and song. Stroke files depend only on the glyph.

## 4. Scoring & SCORM tracking

- **Completion:** reaching `reward` with `trace` finished (every stroke accepted once). Report `completed`, never `failed`.
- **Score:** first-try accuracy over the 6 word-hunt decisions plus the 4 matra choices. Swar lessons use the word hunt only, and ङ/ञ use the trace result. Stars: 3 for ≥90%, 2 for ≥60%, otherwise 1.
- **Interactions** (`cmi.interactions.n.*`; `shared/lms.js` currently writes only score and status, so this needs a small addition):
  1. `trace-<letter>` (performance): `retries=3;wrongStart=1;wrongOrder=0`. Shows which letters children struggle to form.
  2. `wordhunt-<letter>` (choice): the first-try errors, e.g. `picked:घर|missed:कात्री`.
  3. `matra-<letter>` (choice), wrong first answers only, e.g. `कीटक→केटक`. This exposes ी/े/ि confusion, the most useful teaching signal here.

## 5. Extraction plan

The extractor reads the .story read-only with zipfile, extending `parse_story.py`.

1. **Screen order** comes from the nav-bar `jumpToSlide` targets, not the slide-file order (L1-134-L). Slide types are recognised by signature:
   - a `web` object means trace, or barakhadi when the text has "बाराखडी"
   - a `movie` means demo
   - "Word Hunt" text means wordhunt
   - "वाचन" plus Check means matra-choice
   - a `Sticker Reveal` layer means reward

   This rule set already classified all 51 projects correctly.
2. **Words and sentences.** Pair each text and "(English)" gloss with the picture and sound in its click trigger. **Gotcha:** 27 of the 34 vyanjan files carry stale template sentences from the क or ग projects ("कपडे कपाटात कोंबले.", "गाणे गुणगुणत गुराखी…") on hidden objects (e.g. L1-132-S, L1-120 n). Keep only sentences that contain the lesson's letter and are bound to a played sound.
3. **Word-hunt flags** = whether the word contains the akshara (for swar, the independent vowel). Cross-check against the badges on the `Reveal All` layer.
4. **Matra choice.** Each word textbox has states `Normal/Inc1/Inc2/Cor`: `Cor` is the answer, the Inc states are the distractors and `Normal` is the stem. Fully automatic.
5. **Audio.** Newgen clips are named `L1-<code>-<slide><item>-<Word>`, where 1x = words, 4x = word hunt and 6x = matra. Vyanjan files use the *old* code (L1-031 = क). That covers about 60% of clips. The rest (695 `Recorded` and 300+ `CopiedAudio_*` clips) are mapped through their `playMedia` triggers. WAVs are transcoded to mp3.
6. **Trace assets.** Unzip `story/media/*.bin` in memory and read `outlineImage*.src`. Swar files often hold an unused duplicate .bin. The PNGs become the stroke-authoring reference only.
7. **Ignore:**
   - `lms_title` "Trial_1" (all 51)
   - stale `project_title_prop` ("L1-031 k - with puzzle"; "L1-010 Au" on Ru, Am, Aha, Aya and Ou)
   - the player title on L1-107-Chha, which says च when it is छ
   - the 3.5 MB `.fbr` blob
   - the older "Final Activities\Learn and Trace" copies in published.csv

**Expected split:** about 75% automatic. The manual part is checking the trigger-mapped audio by ear, confirming the song clip, the ङ/ञ intro screens and a QA pass on a phone.

## 6. Reusable assets & rights flags

- **Reuse:**
  - voice clips from `path:E:\Marathi School` (1,221 refs) and `path:E:\Project` (both Newgen)
  - `recorded-in-storyline` clips (695, likely the owner's voice)
  - `user:pushkar` pictures (`Pictures\puzzles\031-k-pz_*`, `0 LNT\Barakhadi\*`) and the stickers
- **Stock:** 339 `stock-folder` refs (lotus_2, wheel, scissors, green_board 2…) have unknown licences; confirm them. `shutterstock_134568512.png` (L1-103 Ga) needs a licence check.
- **Foreign client art:** `D:\Projects\Caveo_PPD\…\Splash1-7.png` in L1-135 Ksha. Replace it.
- **Drop:** the `user:sudarshan.jadhav` (Newgen) buttons and ON/OFF sounds, the `user:user` Play/Pause icons, and Ding-3/4.
- **Code:** Malone's app and excanvas.js, both Apache-2.0, and the crayon sprites. All of it is dropped, so nothing reused and no NOTICE needed.
- **Video:** 51 stroke clips (vendor Flash exports such as `Aya_Animation.fla.mov`, stored as mp4 in the .story) are an interim fallback only. L1-109-Z has a movie object with no video in its media list, so check it. ङ and ञ also have ~2 MB intro videos.
- **Fonts:** Mangal (6,881 runs; not redistributable), MV Boli and Articulate. Use Baloo 2 (OFL) from `activities/shared/fonts`. There is no SWF.

## 7. Effort

| Item | Size | AI-assisted days |
|---|---|---|
| `tracer` + `stroke-author.html` tool | L | 3.5 |
| `letter-lesson` (7 screens, scoring, lms.js interactions) + family extractor | M | 4.5 |
| Stroke data: 51 glyphs × ~8 min, 11 matra templates, barakhadi special cases (रु, रू) | – | 1.5 |
| Per lesson: about 30 min swar, 45 min vyanjan, **avg 40 min** × 51 | – | 4.25 |
| **Family total** | | **≈ 14** |

Calibration: the crossword (engine, extraction, packaging and tests) took about one session. The tracer is roughly 3 crosswords, and the lesson shell is about 6 crossword-sized screens, most of them simpler.

**How the stroke paths get authored:** the 51 `trace_pattern` first panels already show each glyph with its numbered order and arrows.
1. Flood-fill the outline and skeletonize it (Zhang-Suen) into a centerline graph.
2. In `stroke-author.html`, click segments in order (or redraw over the image), set the direction and save smoothed polylines. Claude can pre-propose the order from the arrows.
3. Author the matras once against `matraAnchor` and compose them into each letter's 11 forms.
4. Numerals ०–९ and 1–10 go through the same tool at about 5 min each.

## 8. Risks, edge cases, open questions

- **Aksharas:** क्ष and ज्ञ are traced as one unit. The Marathi shapes of झ, ल, श and अ match the patterns (L1-109-Z, L1-128 l), but the text elsewhere must render them too (check Baloo 2 `locl` under `lang="mr"`). अं, अः, ङ, ॲ and ऑ need dot and arc strokes, and ऋ has an unusual order.
- **Small frames:** the trace box is min(width, 70vh), and tolerances are relative to it. A finger covers about 10% of a 300 px box, which is why easy is the default.
- **Touch:** only the trace surface blocks scrolling. iPad palm and Pencil input are covered by the primary-pointer rule.
- **Audio:** WAV transcoding, the autoplay unlock on Start, and song cues if a highlight is wanted.
- **Fixed for free:** text baked into the images goes away. For example, L1-004 ee's panel 4 says "इथे इ लिहा" (wrong vowel); captions now come from JSON.
- **Open questions for the owner:**
  1. Should stroke order follow Balbharati or the vendor arrows, which draw the shirorekha last?
  2. Must the barakhadi forms follow strict order, or is shape enough?
  3. Is it OK to drop the 5 slide-2 gimmicks and the word-hunt timer?
  4. Can the stock-folder and Shutterstock licences be confirmed, and should the Caveo art be replaced?
  5. For the 16 projects used in two units, should one package be uploaded twice, or should the weekly units link to the main course?
  6. Should ङ and ञ stay 5-screen lessons with the अंक intro video?
