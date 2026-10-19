# Trace & write family — engine spec

Family dossier: `_work/families/trace-write.json` (58 projects). Preview sheets reviewed: 0d25549705, 6d55370194, edd7d264b2, cfd97b0c22, c7be121642. The renderer does not draw web objects, so I unpacked them in memory and wrote copies of the guide images to `_work/scratch/trace-write/` (folders `<pid>/<bin>/images/` and `patterns/NN_<pid>.png`).

**Bottom line:** every activity in this family runs on the same embedded web object, William Malone's canvas drawing app (Apache-2.0), shown over a raster "guide" PNG. It is free drawing with no checking. One engine, **`trace`**, shared with letter-trace, covers all 58 projects. Level-0 "Trace and Write" units reuse the exact same media files as the Level-1 letter lessons (same `R5aU1rzU59bF.bin` and same `.mpeg` hashes in 0d25549705 and 77ad2f13b2 L1-01-01 a). So one content record per letter can serve both families.

---

## 1. What these activities are

**Typical: "Trace and Write Swar अ" (0d25549705, `Optional writing Module 1 a.story`, 4 slides)**

1. **Title.** Corkboard background, four pinned cards showing traced letters, "Writing Module 1" and a Start button. Background music plays (`CopiedAudio_68FLZIHykXH`).
2. **चला शिकू या - अ ("let's learn").** A big अ with direction arrows (`trace_dirn_poster_a.png`) and "Click to see how to write the letter". The child taps play and a 12.4 s stroke-order video plays (`vid_trace`, `Trace a.mp4`, 1.2 MB). Two clips play: the letter sound (`snd_Letter`, source `L1-001-01-A.mp3`) and an instruction (`snd_Instr_shiku`, `L1-001-20-Intro.mp3`). Buttons: Watch Again, Previous, Next.
3. **चला गिरवू या - अ ("let's trace").** The web object: a drawing canvas with a crayon/marker picker, six colours, an eraser, size buttons and a "रंग" (colour) / "साहित्य" (tools) frame (`just_canvas.png`). The guide image `trace_pattern k.png` holds four panels: dark outline with numbered stroke arrows ("इथे अ गिरवा"), mid-grey outline, light-grey outline, and blank ruled lines ("इथे अ लिहा"). The child scribbles anywhere and nothing is checked. Instruction audio: `L1-001-30-Intro.mp3`. Button: Finish.
4. **Congratulations!** Same corkboard. A stale leftover "अ" text box appears in every module (2d1c151fe0, c7be121642, 64a4a49fcd…).

Completion today is by slides viewed (`trackMode="slide"`). There is no score.

**Sub-variants (58 projects)**

| Variant | n | Examples | Notes |
|---|---|---|---|
| A. Single-letter "Trace and Write" (Republished, Level 0) | 43 | 0d25549705 अ, 5b51aa0825 क, edd7d264b2 त, 05a872bbe6 "क्ष" | 11 swar + 32 vyanjan. Modules 7, 17 and 42 are absent from Republished. 4 slides, identical template. |
| B. Same template, Newgen Sem-1 "Week N – Learn and Trace" | 9 | 74367df458 अ, 6d55370194 ऋ, df357a5811 | SL 2.11. 8 are byte-identical to A (same guide-image hash). Only ऋ (6d55370194) is unique. |
| C. Word writing with blank/hint/stencil | 4 | cfd97b0c22 "Write Letter and Words - 1", 4d978fba85 "- 2", c7be121642 "Writing Simple Words", 6d0cc061ce "Bonus Writing Activity 2" | 1 web object per slide, each holding 3 stages (akshara 1, akshara 2, whole word) × 3 guides (blank, hint, stencil) plus a "listen" button. |
| D. Join the dots | 1 | 2d1c151fe0 | "Join the dots in order from अ to अः, with black color, then color the picture". The dots and labels are baked into the PNG. |
| E. Colour the letter series | 1 | 64036b3ffb | "Color the flowers": 7 garlands of vyanjan flowers to colour. It sits in a `Swar` folder but the content is vyanjan. |

Variant C content, read from the guide images: LW-1 = **आज, काच, काजू, ऐक**. LW-2 = **जग, एक, झोका, झाक**. Writing Simple Words and Bonus-2 = **एक, काजू, आज** (a subset). Each word image carries an English caption, e.g. "(cashew)". The stages go by akshara, not by letter: काजू → का, जू, काजू (`trace_pattern-k1..k9`, `cfd97b0c22/R65gF7F1UU66`).

## 2. Proposed engine: `trace` (one engine, step-based)

**Decision: share one engine named `trace` with letter-trace.** Our Level-0 module is literally slides 2–3 of the Level-1 lesson. Join-dots and colouring are the same canvas with a different guide and no checking, so they become modes, not engines.

An activity is a list of **steps**:

- **`watch`**: stroke video, letter sound and instruction audio. "Play" is a large button, the video uses `playsinline`, and "Watch again" stays available. Next unlocks when the video ends, or after 1 replay-free view.
- **`trace`**: the drawing canvas over a **scaffold sequence** of guide frames. The child gets a crayon in 4–6 colours, an eraser, "clear" and "listen" (plays the step audio). Frame order is **stencil → hint → blank**, the fading scaffold Level 0 already uses (dark → mid → light → blank). The old word tool defaulted to *blank* first (`curBackg = "backg1"`), which is backwards. One frame is shown at a time, which is what makes it fit a phone. Level-0 panels are cropped out of the 4-up PNG.
- **`paint`** (variants D/E): one large line-art image with crayons and a **tap-to-fill bucket**. Small fingers cannot colour flowers by scribbling. In dots mode, an optional overlay of tappable dots draws the joining lines in order. That needs hand-entered dot coordinates for 1 activity, so make it optional.
- **`done`**: stars plus "Save my picture" (downloads a canvas PNG). TalentLMS courses already pair these units with paper Assignments ("Assignment 1" in "Trace and Write Vyanjan क"; "Swar Practice 2. Written Practice" in Join the Dots), so a saved image gives the child something to upload.

**Feedback that matters pedagogically:**

- **Coverage check.** At runtime, build a mask of the letter's interior: draw the guide to an offscreen canvas, flood-fill from the outside, and keep the region that stays unfilled. When the child taps "Done", compute *recall* (share of the mask that is inked) and *precision* (share of ink inside a dilated mask). The result is 1–3 stars and a soft chime. Never block progress: show "Try once more?" below 1 star.
- **Blank frame.** Coverage is measured against the stencil mask shown faintly *after* Done, as a "compare" reveal.
- **Stroke-order arrows** on the first frame and the video. Both are pedagogical, so keep them.

**Drop:**
- the corkboard title and congratulations slides (one title card instead)
- `entr:fade` entrance animations (15 per module)
- crayon/marker textures and styles
- 3 brush sizes (keep one, scaled to the frame)
- the Restart-confirm layers
- the sticker tease/reveal in cfd97b0c22 (use the shared stars page)
- the empty `dragDropIntr` on word slides (no drag items, unscored)

**Sounds:** `shared/sound.js` chimes for done and stars; content audio for the letter, instruction and akshara/word "listen".

## 3. Content data model

Example 1, variant A, built from 0d25549705 (real names; `R…` are the stored `story/media` files):

```json
{
  "type": "trace",
  "id": "L0-trace-swar-a",
  "title": "Trace and Write Swar अ",
  "source": "Optional writing Module 1 a.story (0d25549705)",
  "letter": "अ",
  "steps": [
    { "kind": "watch",
      "heading": "चला शिकू या - अ",
      "prompt": "Click to see how to write the letter",
      "video": "media/trace-a.mp4",
      "poster": "media/trace_dirn_poster_a.png",
      "sound": "media/L1-001-01-A.mp3",
      "instruction": "media/L1-001-20-Intro.mp3",
      "_from": "R5uFquNVPhHs.mpeg (vid_trace), R6HJxgNkGDUJ.wav (snd_Letter), R5onlIfLzIAO.wav (snd_Instr_shiku)" },
    { "kind": "trace",
      "heading": "चला गिरवू या - अ",
      "instruction": "media/L1-001-30-Intro.mp3",
      "frames": [
        { "guide": "media/a-panel1.png", "label": "इथे अ गिरवा", "level": "arrows" },
        { "guide": "media/a-panel2.png", "label": "इथे अ गिरवा", "level": "stencil" },
        { "guide": "media/a-panel3.png", "label": "इथे अ गिरवा", "level": "faint" },
        { "guide": "lines",              "label": "इथे अ लिहा",  "level": "blank", "compareWith": 1 }
      ],
      "_from": "R5aU1rzU59bF.bin :: images/trace_pattern k.png, cropped into 4 quadrants" },
    { "kind": "done", "text": "Congratulations!" }
  ]
}
```

Example 2, variant C, one item from cfd97b0c22 (web object `R65gF7F1UU66.bin`):

```json
{ "kind": "trace", "heading": "बटणावर क्लिक करून अक्षरे ऐका व लिहा.",
  "picture": "media/kaju.png", "caption": "(cashew)",
  "stages": [
    { "text": "का",   "audio": "media/lw1-kaju-1.mp3", "frames": ["k3.png", "k2.png", "k1.png"] },
    { "text": "जू",   "audio": "media/lw1-kaju-2.mp3", "frames": ["k6.png", "k5.png", "k4.png"] },
    { "text": "काजू", "audio": "media/lw1-kaju-3.mp3", "frames": ["k9.png", "k8.png", "k7.png"] } ] }
```

Audio comes from `sounds/Zo.mp3`, `Ka.mp3` and `Zoka.mp3` respectively (the JS maps backg1-3 → audio1 and so on). **The names are a template leftover from झोका**, so a human must listen to confirm each clip.

**Varies per activity:** letter/akshara text, headings, labels, video, letter sound, instruction clips, guide images, picture and caption, and mode (watch/trace/paint). **Constant (lives in the engine):** palette, tools, the done page and the scaffold order.

## 4. Scoring & SCORM tracking

- **Completion:** reach `done`, meaning every trace frame was visited and has some ink, or the paint image was touched. SCORM `completed`. A finished practice is never `failed`, which matches the existing `lms.js` logic.
- **Score (0–100):** the mean coverage-stars across scored frames (stencil, faint and blank). `passed` when every blank frame earns ≥ 2 stars. Paint and dots modes report 100 on completion and are unscored.
- **Interactions** (SCORM 1.2 `cmi.interactions.n.*`, type `performance`). Record only these 3:
  1. `blank-<akshara>`: recall/precision on the *write-from-memory* frame. This is the real handwriting signal (e.g. weak on क्ष, ज्ञ, झ).
  2. `retries-<akshara>`: count of Clear/"Try once more" per step. This shows which aksharas frustrate.
  3. `video-<letter>`: watched to end (y/n) and replays.

`shared/lms.js` has no interaction call yet. Add a small `record(id, type, result, latency)`: about 20 lines, plus an xAPI `answered` statement with an extension.

## 5. Extraction plan (`tools/extract_trace.py`, extends `tools/parse_story.py`)

1. **Slide order:** read it from `story/story.xml` → `sldIdLst` → `story/_rels/story.xml.rels`, never from file names. In 5301b247ed, `slide2.xml` is the *Congratulations* slide.
2. **Watch step:** in the slide containing a `<video … typeName="vid_trace">`, follow its `assetG` to the `.mpeg` (it is an MP4 with `ftypmp42`/`isom` header, so rename it `.mp4`). Each lesson stores **two** `.mpeg` files (in 0d25549705 they are 1.2 MB and 283 KB). Pick the one referenced by `vid_trace` and take the duration from `<movie dur=…>`. Sounds come from `typeName` `snd_Letter*` and `snd_Instr*`. The slide-3 instruction is the slide's only `<sound>`. The heading text matches `चला शिकू या - X` / `चला गिरवू या - X`, which gives the letter.
3. **Trace step:** the `.bin` member that opens as a zip and holds `Trace_main.js`. Regex `(outlineImage\d*|audio\d)\.src = "…"` gives the frame and audio list. A 907-line JS means a single 4-panel PNG (crop it into quadrants of 380×290 at 760×580). A 1426-line JS means 9 overlays plus 3 sounds, with group *g* = images 3g-2..3g and audio *g*.
4. **Word text:** it is raster only. Have an AI vision pass read `k3`/`k6`/`k9`, then a human confirms it (8 unique words).
5. **Dedupe** by MD5 of the guide PNG and video. This collapses the 8 Newgen copies and 6d0cc061ce = c7be121642, and c7be121642's three items reuse cfd97b0c22 and 4d978fba85.
6. **Cross-check the letter** from slide text, the unit name and the guide image against each other, and stop if they disagree.

**Gotchas found:**

- **Wrong letter in 4 live units.** "Module 43 h" (81b2a20645) is entirely स (text, video and guide). "44 L" (e5d80bc4f7) is ह, "45 ksha" (05a872bbe6) is ळ, and "46 dnya" (5301b247ed) is क्ष. Their media hashes equal L1-132-S, L1-133 H, L1-134-L and L1-135 Ksha. The correct ळ, क्ष and ज्ञ assets exist in 295f05923d, 66baca5a25 and dc68fc141e. TalentLMS also lists "Trace and Write Vyanjan ष" and "स" units with no matched source here.
- **Broken audio in the word variants.** c7be121642 and 6d0cc061ce reference `sounds/Zoka.mp3` or `Ka.mp3` files that are missing (`Zoka_.mp3`, `1.mp3` are shipped instead), so some "listen" buttons are silent. The clips are also scrambled across items (the काजू object contains आज's clip). Take the audio from cfd97b0c22/4d978fba85 instead.
- **Typos baked into the guides:** झ panel 1 says "इथे आ गिरवा" (64a4a49fcd), and the ह guide's last panel says "इथे ब लिहा". Crop the labels away and render them as live text.
- **Stale titles:** player titles read "Writing Module" or "Trace and Write Vyanjan त" inconsistently. `lms_title` is "Trial_1" everywhere. df357a5811 (an `Archive` अ lesson) is mapped to "Sem. 2 – Week 4 – Join the Dots Swar". 64036b3ffb is filed under Swar.
- 64a4a49fcd's video is in the zip as `.mpeg` but is missing from the parsed media list. 61bc4a5f7a carries a duplicate web object.

**Expected automatic:** about 95% for variants A/B (everything except the human listen/watch QA), about 60% for C (the words need vision plus confirmation, and the audio needs relabelling), and 50% for D/E (the paint image is auto, dot coordinates are by hand). **Overall about 88% automatic.**

## 6. Reusable assets & rights flags

- **Reuse as-is:**
  - 44 unique stroke videos (MP4, 0.3–1.2 MB). `Trace a.mp4` etc. carry origin `user:pushkar`. Most others are `storyline-temp` names created on Newgen and Exult machines.
  - Guide PNGs (4-panel letters; 9 per word item).
  - `trace_dirn_poster_*.png`.
  - Letter and instruction recordings: `path:\\gold\projects\Marathi Shala\Exult Working\Audios` (vendor Exult Corp, 2015); `path:E:\Marathi School\…` (Newgen); 67 `recorded-in-storyline` clips (presumably the owner's own recordings).
- **Stock:** `the-background-352166.png` (`stock-folder`, all 58) and the sticker art `stk_*`, `star_1`, `green_board 2` (cfd97b0c22) are decorative, so drop them. There are no `stock:shutterstock` origins. **However, the word pictures** (cashew, calendar, glass, swing, globe, "listen" boy, gold "1", cover) are baked into the `k7–k9` guide PNGs, look like stock vectors, and have **unknown licence**. Ask the owner, or re-source them.
- **Vendor files:** title collage `1.png`–`4.png`, `Bg.png`, `Patch.png` (`path:E:\Marathi School\Gappa Goshti\Optional Writing Module`, Newgen); `008-13-Background.png` (`user:sudarshan.jadhav`, Newgen); the `D:\Projects\Marathi shala\Exult Corp\Graphics` images. All decorative, so drop them.
- **Third-party code:** `Trace_main.js` © 2010 William Malone, Apache-2.0, heavily modified by the vendor. `excanvas.js` (Google, Apache-2.0). Do **not** reuse either: the new canvas code is written fresh. The Malone crayon/marker PNGs come from his tutorial download with unclear licence, so drop them.
- **Fonts:** Mangal (58 projects), "Articulate" (56) and MV Boli (2). Replace with the shared Baloo 2 Devanagari (OFL).
- **No Flash/SWF.** Video needs no conversion. Optionally re-encode to cut 30–50% of the size.

## 7. Effort

| Item | Complexity | AI-assisted days |
|---|---|---|
| `trace` engine core: canvas with pointer events and DPR, scaffold stepper, watch step, coverage stars, done page with save-PNG, `lms.js` `record()` | **M** | **2.0** (crossword was 1 day at ~350 JS lines; this is about 650 lines plus phone/iPad pointer testing) |
| `paint` mode (bucket fill, optional dots) | S | 0.5 |
| Extractor plus dedupe and cross-check | S | 0.5 |
| Data/QA: 44 letter lessons × 10 min (watch video, listen ×3, check crop) plus 3 missing letters (ष, ज्ञ, अः from L1 lessons) × 15; 8 word items × 20; 4 word activities × 10; D/E × 40 | — | ~13 h ≈ 1.6 |
| Packaging and batch build with `tools/package.py` (about 51 unique packages) | — | 0.3 |
| **Family total** | | **≈ 4.9 days** (about 2.4 if letter-trace builds the core engine first) |

That averages about 13 min of data/QA per project, and about 15 min per *unique* activity.

## 8. Risks, edge cases, open questions

- **Devanagari:** conjuncts क्ष and ज्ञ; matras that hang below the lower guide line (जू's ू in `k6` crosses the baseline, so the canvas must not clip it); the अं anusvara dot is tiny, so weight it low in coverage; the shirorekha is a separate stroke. The engine works per *akshara*, never per Unicode code point.
- **Coverage is gameable** by colouring the whole box. Precision (ink outside the dilated mask) caps it. Hollow outlines that touch the frame edge break the flood fill, so pad the image by 2 px.
- **Touch:** set `touch-action:none` on the canvas, use pointer events with coalesced points, support Apple Pencil, and ignore a second simultaneous pointer (palm). **Do not wrap the canvas in `fit.js` CSS `zoom`**: pointer coordinates go wrong under zoom in Safari and Firefox. Size the canvas from a ResizeObserver instead. The old tool hard-coded `multTx = 0.955` and the 960×640 stage.
- **Small frame/phone:** one frame per screen, with the guide area at least 280 px. Toolbar along the bottom in portrait, at the side in landscape.
- **Audio/video:** iOS requires a tap before playing with sound. Start audio on the Play button. Keep one clip at a time (`sound.js`).
- **Open questions for the owner:**
  1. Do you want coverage stars, or keep free practice (complete on Finish)?
  2. Should we fix the four mislabelled ह/ळ/क्ष/ज्ञ units and add ष/अः Level-0 units from the Level-1 assets?
  3. Should the 9 Newgen "Sem. N – Week N – Writing" units point at the same rebuilt package as the Level-0 letter?
  4. Can the stock word pictures be reused?
  5. Is tap-to-fill colouring fine instead of crayon-only?
  6. Interactive dots for Join the Dots, worth about 30 min of manual coordinates?
  7. Keep the MP4 stroke videos, or later replace them with animated SVG stroke paths? That would need path data for about 48 letters and is out of scope here.
