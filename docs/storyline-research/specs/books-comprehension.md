# Engine spec: books-comprehension (picture books, listening and reading comprehension)

The family has 7 live projects, which come down to 6 distinct activities: Conversation Module 2 is the Lion book again. Sources were read from the `.story` XML (read-only, in memory), and the preview sheets for dff6feb00d, 1941861186, c66af019dd, 8fad77193a and 21b450293f were checked. The Lion page-flip MP4s were extracted to `_work/scratch/books-comprehension/lion_mp4/` and their frames were captured with headless Chrome.

## 1. What these activities are

### Typical: Lion book "सिंह" (dff6feb00d, unit "Lion - सिंह"), seen by a child
1. **Title** (green chalkboard): "चला वाचायला शिकू या / सिंह", Start, and a sticker teaser.
2. **Cover** ("Main Page"): a closed book (`5xZaPdy6dSU.mp4`), "Click on the Start button to begin reading."
3. **Pages 1–7** (slide3–slide9). Each page plays a 2-second page-turn video (734×468 MP4). The video *is* the page art: a lion photo on the right and a page number on the left. The sentence sits under a green ▶. Tapping ▶ opens layer `Text1`, which plays the narration (`Screen Book Text 1.mp3`, …). Each word is its own text box with a timed **wipe**, so the words light up in sync with the voice (karaoke). Sentences: सिंह रानटी प्राणी आहे. / सिंह आफ्रिकेच्या जंगलात राहतात. / सिंह गुहेत राहतो. / सिंहाच्या मानेवर आयाळ असते. / सिंहाचे दात व पंज्यांची नखे तीक्ष्ण असतात. / सिंह इतर प्राण्यांची शिकार करतो. / म्हणून सिंहाला जंगलाचा राजा म्हणतात.
4. **Glossary** (Page 8): 6 words, each with ▶ and audio: गुहा-cave (`Guha.mp3`), तीक्ष्ण-sharp, प्राणी-animal, राजा-king, रानटी-wild, शिकार-hunt. Then "Read Again" or "Quiz".
5. **Listening puzzle ×4** (slide13–16): "बटणावर क्लिक करून वाक्य ऐका आणि योग्य पर्याय निवडा." The child hears a word (Wild/रानटी, Sharp/तीक्ष्ण, King/राजा, Lion/सिंह), then drags one of 3 picture puzzle pieces, each with its own ▶, onto the slot. The tasks are opposites (पाळीव, बोथट) and gender pairs (राणी, सिंहीण).
6. **True/false ×5** ("सिंह - आकलन"): a statement is read aloud ("सिंहाला दात नसतात."), the child picks बरोबर or चूक and presses Check. A correct/wrong chime layer plays, and the running count shows in `%correctAttempt%`.
7. **Final page**: a 0–5 star layer based on the true/false count, then a sticker (`Stk_Lion_*`, `Lion_gif_anim.gif`).

The `Reverse` scene (slides 11–18) duplicates the 7 pages with backward-flip videos for "Previous".

### Sub-variants (7 projects, 6 distinct)
| Variant | Count | Projects | What the child does |
|---|---|---|---|
| A. Read-along picture book + glossary + quiz | 2 (1 distinct) | Lion book dff6feb00d; Conversation Module 2 4088424ad4 (Newgen source; units "Week 02 - Book - Lion", "Sem. 2 - Week 2 - Conversation") | as above. Conv. 2 only changes the instruction ("बटनावर क्लीक करून शब्द ऐका") and the finale ("reveal the mystery phrase" instead of stars/sticker) |
| B. Photo book with audio hotspots | 1 | Farm "चला जाऊ या शेतावर" c66af019dd (TinCan, 720×540) | 11 photo-collage pages, each with one narrated sentence ("शेतकरी शेतामध्ये धान्य पिकवतात.") and 3–7 Storyline **markers** on photos (tap to hear `01-1-tractor.mp3`, `03-2-padval.mp3` …, 40 clips). A 1–10 tab strip for page jumping. No questions. |
| C. Listening comprehension game | 2 | LC Game 1 "Action Words" 1941861186 (2 units); LC Game 2 "Vocabulary" f00e6c9b71 | 5 items. Hear a sentence ("मला भूक लागली आहे.", "मला हत्तीपेक्षा वाघ बघायला आवडतील"), drag the right picture piece (pizza; tiger) next to the scene. One attempt, a Cor/InCor voice clip, Next. |
| D. Reading-comprehension lesson hub | 1 | Parts of body "शरीराचे अवयव" 8fad77193a | Name entry, then a hub (Learn / Activity / Quiz, gated). **Learn**: front/back body with 15 audio markers (हात, डोळे, गुडघा, पोटरी, मनगट…). **Info cards**: 7 parts with a paragraph each ("नाक - आपण नाकाने श्वास घेतो…"). **Activity 1**: drag 9 word labels onto the body, Check / Reveal All. **Activity 2**: 10-piece jigsaw on a timer. **Quiz**: 5 read-aloud MCQs ("चवी कोणत्या अवयवाने कळतात?" छाती/डोळे/नाक/जीभ). |
| E. Picture description (crystal ball) | 1 | Picture Description 1 21b450293f (player title "Vocabulary Module (Crystal ball)") | 3 buttons on a crystal ball, each revealing a picture and a spoken sentence: मी पटकन पोहायला शिकलो. / कपडे कपाटात कोंबले. / लाकूडतोड्या लाकडे तोडतो. Then a sticker. It is the same template as the vocab-letter crystal-ball teaser. |

## 2. Proposed engines

There are **two engines and one shared lesson shell**, all on `activities/shared` (`lms.js`, `fit.js`, `sound.js`, `barakhadi.css`, Baloo 2 fonts). Book and quiz sections are chained inside one SCORM package, because Lion and Body mix them.

### Shell: `lesson` (S)
Runs an ordered list of `sections` (book, glossary, quiz, hub). It also handles the title card, a progress dots bar, and the finale (stars plus sticker, with CSS pop, no GIF). The Body hub becomes a simple 3-tile menu with an "unlock next" rule. Drop the Restart lightboxes, the `%Name%` text entry (TalentLMS already knows the learner), and the Reverse scene: one page array runs both directions.

### Engine 1: `storybook` (M)
- **Page model:** image(s) + sentence + narration + optional hotspots. Layouts are `spread` (Lion: illustration right, text left; stacked on phones) and `collage` (Farm: 2–6 photos in a CSS grid).
- **Page turn:** a CSS 3D flip on a tap of ‹ › or a horizontal swipe. It replaces the 34 MP4 flip videos, which are decorative.
- **Read-along (pedagogical, keep):** ▶ plays the narration and highlights each word from its `t` (ms) timing. **Tap a word** to hear only that word, by playing the narration from `t[i]` to `t[i+1]`. This needs no new recordings. If a glossary clip exists for that word, play it instead.
- **Hotspots** (Farm markers, Body Learn labels): pulsing dots on the picture. A tap shows the caption chip (Marathi + optional English) and plays the clip. Hover-to-play becomes tap, because phones have no hover.
- **Reveal mode** (variant E): N covered cards (skin `ball`). A tap reveals the picture and sentence and plays the audio. It is the same as vocab-letter's `sentences` mode, so share that code.
- **Glossary page:** a word list, each with ▶, Marathi – English.
- **Drop:** fly/fade/swivel entrance animations, the 180 decorative stars, hover states, and the GIF crystal-ball animation (`cbal_anim4.gif`, 1.8 MB). Use a CSS glow instead.

### Engine 2: `comprehension-quiz` (M)
One item runner with typed items. Each item has a prompt (text and/or audio, with an auto "read aloud" option), feedback chime plus optional voice praise, and a configurable number of attempts (default 1, matching Storyline `attempts="one"`).
| Item type | Used by | Interaction |
|---|---|---|
| `listen-pick-picture` | LC1, LC2 | Play the sentence. Tap one of 3 picture tiles; on success it snaps into the scene's puzzle slot as the reward animation. Drag stays optional on desktop, tap is the primary input. |
| `listen-pick-word` | Lion opposites/gender | Same as above, but each option has its own ▶ audio. |
| `true-false` | Lion | Statement read aloud, then बरोबर / चूक. |
| `mcq` | Body | Question and 4 options. The question and the options are read in sequence; Storyline timed them on the timeline, and the engine plays them as a queue. |
| `label-picture` | Body Activity 1 | Drag (or tap-word-then-tap-spot) 9 labels onto dots. Check, then after 2 tries "Show answers" (the original Reveal All). |

**Recommendation:** drop the Body **jigsaw** (Activity 2: 10 pieces on a timer, picture of children). It is fiddly at small sizes and teaches no Marathi. If the word-games family builds a jigsaw, it can plug in later.

**Sounds:** the narration and voice clips are the content. UI chimes come from `sound.js chime.*`, which replaces Storyline's copied "correct/incorrect" clips.

## 3. Content data model

Example: Lion (real text, clips and timings from slide3/slide4/slidea/slide13/slide17).
```json
{
  "type": "lesson", "id": "L2-14-lion", "title": "Lion", "titleMarathi": "सिंह",
  "source": "Republished Activities\\Level 2\\14 Books\\01 Lion Book.story",
  "sections": [
    { "type": "storybook", "layout": "spread",
      "cover": { "image": "media/lion-cover.jpg", "title": "जंगलाचा राजा" },
      "pages": [
        { "image": "media/lion-p1.jpg", "text": "सिंह रानटी प्राणी आहे.",
          "audio": "media/screen-book-text-1.mp3",
          "words": [ {"w":"सिंह","t":229}, {"w":"रानटी","t":1125,"gloss":"ranati"},
                     {"w":"प्राणी","t":2125,"gloss":"prani"}, {"w":"आहे.","t":2875} ] },
        { "image": "media/lion-p2.jpg", "text": "सिंह आफ्रिकेच्या जंगलात राहतात.",
          "audio": "media/screen-book-text-2.mp3",
          "words": [ {"w":"सिंह","t":292}, {"w":"आफ्रिकेच्या","t":1271},
                     {"w":"जंगलात","t":2750}, {"w":"राहतात.","t":3750} ] }
      ],
      "glossary": [ {"id":"guha","mr":"गुहा","en":"cave","audio":"media/Guha.mp3"},
                    {"id":"ranati","mr":"रानटी","en":"wild","audio":"media/Ranati.mp3"} ] },
    { "type": "quiz", "attempts": 1,
      "instructions": "बटणावर क्लिक करून वाक्य ऐका आणि योग्य पर्याय निवडा.",
      "items": [
        { "id": "opp-wild", "kind": "listen-pick-word", "label": "Opposite Words",
          "prompt": {"text":"Wild / रानटी","image":"media/Wild_Puzzle_Piece.png","audio":"media/q1.mp3"},
          "options": [ {"image":"media/puzzle_right_Correct-option.png","audio":"media/q1-a.mp3","correct":true},
                       {"image":"media/puzzle_right_Incorrect1-option.png","audio":"media/q1-b.mp3"},
                       {"image":"media/puzzle_right_Incorrect-option2.png","audio":"media/q1-c.mp3"} ] },
        { "id": "tf-pet", "kind": "true-false", "text": "सिंह पाळीव प्राणी आहे.",
          "audio": "media/tf1.mp3", "answer": false }
      ] }
  ],
  "finale": { "stars": "quiz", "sticker": "media/Stk_Lion_80.png", "stickerName": "सिंह" }
}
```
LC item: `{ "kind":"listen-pick-picture", "text":"मला झोप आली आहे.", "audio":"media/3-zop.mp3", "scene":"media/03_zop_boy.png", "options":[{"image":"media/03_bed.png","correct":true},{"image":"media/03_baseball.png"},{"image":"media/03_brushes.png"}] }`.
Farm hotspot: `{ "x":0.45, "y":0.13, "label":"ट्रॅक्टर", "audio":"media/01-1-tractor.mp3" }`. Coordinates are fractions of the image, taken from the marker `loc`.

**Varies per activity:** sections and their order, pages (image, text, audio, word timings, hotspots), glossary, quiz items and answers, attempts, finale type (stars / sticker / mystery phrase). **Fixed in the engine:** layout, chrome strings, chimes, page-turn, star thresholds.

## 4. Scoring & SCORM tracking (SCORM 1.2)

Today these projects track by slides viewed (`quizMgr trackMode="slide"` in Lion, Body and Picture Description; `def` in LC and Farm), with `reporting="PassedIncomplete"`. No quiz score reaches the LMS.

- **Completion:** reaching the finale. For books: every page shown, with no requirement to press ▶; Farm and Picture Description are completion-only. For quizzes: every item answered. Status `completed`; `passed` when the score is ≥ 80.
- **Score:** % of quiz items right on the first attempt (Lion 9 items, LC 5, Body 5 MCQ + 9 labels counted as 1 item). Stars: Lion's 0–5 stars can map to this score.
- **Interactions worth recording** (needs the small `lms.interaction()` addition also proposed in the vocab-letter spec; one record per item, not per tap):
  1. `q-<id>` (`choice`): the first option chosen and correct/wrong. The meaningful signal is the **distractor picked on the tricky items**: LC2 "मला हत्तीपेक्षा वाघ बघायला आवडतील" (हत्ती is named but is wrong) and "आमचा ससा गाजर खात नाही…" (गाजर is named but is wrong), plus Lion's true/false negatives ("सिंहाला दात नसतात.").
  2. `label-body` (`matching`): the wrong pairs at first Check, plus the number of Checks.
  3. Book sections, optional: `read-along` as the count of pages where ▶ was pressed. It is a cheap engagement signal. Skip it if the owner wants scores only.

## 5. Extraction plan (`tools/extract_books.py`, built on `activities/tools/parse_story.py`)

1. **Media map:** in `story/story.xml`, `<media>`, `<audio>` and `<video>` all carry `g`, `displayName` and `origFile`. Read all three: the audio is in `<audio>`, not `<media>`. Slide shapes point at them through `assetG` (pictures, sounds, markers) and `video@srcG`. In the slide XML, sounds are named by hash (`5nPt1CIECiV.mp3`), so always go through `assetG`.
2. **Book pages (Lion):** use slides of scene "Main Activity" whose `sld@name` is "Page N". `sentence` = the base text box next to the ▶. Read-along = layer `Text1`/`Text 1`: the word text boxes in z-order, `txtTmCtx@start` as `t` (verified: page 1 starts 229/1125/2125/2875 ms against a 3 787 ms clip), and the layer's `<sound>` gives the narration. Glossary = the layers named Cave/Sharp/… on Page 8, each holding one sound; the caption text box "गुहा - cave" is split on " - ".
3. **Page images:** they exist only inside the flip MP4s (`video@srcG`). Grab the **last frame** of each forward video in headless Chrome (proven on `66d0pl9K1Ci`, `5rplMZc0ITR` …) and crop the right page. Re-shoot or source the originals at higher resolution if the owner has them (the frames are 734×468).
4. **Farm:** the sentence is the long text box. Hotspots = `<marker>` elements: `assetG` gives the clip and `loc` the position. **The captions are not in the XML** (`desc` is empty), so write the Marathi labels by hand from the clip names (`02-1-kobi` → कोबी, `07-2-papaichezad` → पपईचे झाड). Each page's photos are the `pic`s, excluding `tab_*` and `book_header3`.
5. **Quiz answers:**
   - LC drag-drop: in `dragDropIntr/choices/intrFreeChoice`, the **one choice with a non-null `matchShpG`** is correct. `shpG` points at a `group` whose `childLst` holds `<g>` references to the piece and the picture. This was verified on all LC1/LC2 slides (pizza, bed, sled; घसरगुंडी, tiger, lettuce).
   - Lion puzzles: every piece matches the slot, so the key lives in variables. Use the option whose hover state image is named `*Correct-option*`, cross-checked against the `OnDrop>adjustVar` trigger.
   - True/false and MCQ (`multiChoiceIntr` with no `scoringData`): the Check button's `showSubSlide` triggers have `shapeState … name="Selected"` conditions. The correct option is the one whose layer plays the **"correct" chime asset** (Lion/Body `6gv5qxBv3nG.mp3`; the wrong-answer layers use `6MgO9dhKgYD.mp3`).
   - Body labels: the `PartNDrag`→`PartNDrop` pairs come from the drag-drop choices.
6. **Audio order:** map clips per slide, never by file number. LC1 slide3 uses `3-zop.mp3` and slide4 uses `2-tahan.mp3`.
7. **Gotchas**
   - **Stale titles and strings:** Body slide 5 says "चला गिरवू या - अंक" and slide 6 says "\"अ\"चा खेळ"; Body's final page shows "डॉक्टर / १-१० / आ इ ई"; Picture Description has `coursename = "Level 1 - Learn and Trace 121"` and a kite sticker (पतंग); `lms_title` is "Trial_1"/"Trans1"; Lion's `project_title_prop` is "L1-001 a". Take titles from the TalentLMS unit names.
   - **Reverse scene is buggy:** Lion slides 14–16 `Text1` show the *next* page's sentence. Extract from Main Activity only.
   - **Text mismatch:** Lion page 5 base text is "…दात **व** पंज्यांची…" but the read-along says "…दात **आणि** पंज्याची…" (while the word boxes say "व"). Check against the audio.
   - **Duplicates:** older versions exist outside the family: Newgen originals 203a7b07e1 (Body), 1edaf6a183 / 3e55ac43fe (LC), 5a36ea928b (Conv. 2), 530f6be6b2 (crystal ball), and "old sl backup" SL2 copies 06ad604fd7 / 3e7046a97c. Use the `Republished Activities` SL3 files.
   - **Junk data:** `.bin` files in `media` (3.5 MB gzip "RecorderEdition", i.e. `6fs2K5V4yN3.fbr`) are a leftover screen recording; ignore them.
   - **WAV inside the .story:** the Lion narration is stored as `.wav` (7 files). This machine has no ffmpeg, so install it or take the MP3s from the published `L1-09-001 Sinha.zip`.

**Expected automation:** about **65 %**. Text, word timings, answer keys and audio mapping come out automatically for Lion, LC and Body. Done by hand: Farm captions (40), page-image crops, Body info-card layout, and the stale-text QA.

## 6. Reusable assets & rights flags

- **Reusable as-is:** all Marathi narration and word clips: Lion `Screen Book Text 1–7`, glossary clips, LC sentence clips, 40 Farm clips (`user:pushkar`, Sounds\farm), and Body word clips (`Haat.mp3`, `Dole.mp3` … from `path:E:\Marathi School` = Newgen). LC clip-art (`01_pizza.png`, `3-1-tiger.png`, `user:pushkar`, Pictures\Trans). Body figure art (`Front_View.png`, `Boy.png`, `PartNDrag/Drop.png`). Crystal-ball photos `Oval_Image*.png`.
- **Vendor-made (Newgen):** `path:E:\Marathi School` (43 assets in Lion, most of Body and Picture Description), `path:E:\101615` (puzzle pieces, audio buttons), `user:sudarshan.jadhav` (4) and `path:E:\Sudarshan` (3) in Conv. 2, `D:\projects\StoryLineAssignment\HumanBodyParts`, and `user:user` (the vendor PC: `C:\Users\User\Desktop\Play.png`, `Potari.mp3`, and all 17 flip MP4s via `C:\Users\User\AppData\Local\Temp`). **Confirm work-for-hire ownership.** No TreeTo assets in this family.
- **Stock / third-party:**
  - Farm slide 11 carries "Photo credit: Ailisa / Shutterstock.com" (editorial stock, credit required).
  - The other ~40 Farm photos (`Pictures\Farm\*.jpg`) and the **Lion photos inside the MP4s** have unknown origin, probably stock. **Flag both sets.**
  - `stock-folder`: `green_board 2.png`, `the-background-352166.png` (the number suggests Pixabay), `cert_4_main.png`, `sticker_banner_3.png`, `Stickers\star_1.png`.
  - `intro_act.mp3` (Stock Sounds\Audioblocks, subscription licence).
  - `Parchment.jpeg` (Articulate texture; drop it).
- **Recorded voice:** `recorded-in-storyline` clips (LC feedback, Lion quiz prompts `temp*.mp3`, Body MCQ readings). Speaker unknown. Confirm consent and reuse rights.
- **Fonts:** Mangal, Arial Unicode MS, CDAC-GISTYogesh (only the Farm title; Unicode text, no legacy encoding), Articulate (player icon glyphs), Segoe Print. All are replaced by the bundled Baloo 2.
- **Conversion:** 34 `.mpeg` page-flip MP4s across Lion and Conv. 2 become still JPGs plus a CSS flip. GIFs (`cbal_anim4.gif` 1.8 MB, sticker GIFs) are replaced by CSS. 7+6 WAVs go to MP3. No Flash/SWF and no third-party code or web objects in this family.

## 7. Effort (calibrated on crossword: about 1 session for engine + 2 activities + packaging + tests)

| Item | Size | AI-assisted days |
|---|---|---|
| `storybook` engine (spread/collage, CSS flip + swipe, read-along highlight, tap-word slice, hotspots, reveal, glossary) | M | 1.5 |
| `comprehension-quiz` engine (5 item types, read-aloud queue, attempts, `lms.interaction`) | M | 1.75 |
| `lesson` shell (sections, hub with unlock, finale stars/sticker) | S | 0.5 |
| Extractor (trigger/answer-key rules, word timings, MP4 last-frame grab, WAV→MP3) | M | 0.75 |
| Packaging + TalentLMS/iPad test (reuse `package.py`, `test-packages.mjs`) | S | 0.5 |

**Per-activity data + QA:**

| Activity | Minutes |
|---|---|
| LC1 | 45 |
| LC2 | 45 |
| Picture Description | 30 |
| Lion (crops, the mismatches, 9 quiz items) | 180 |
| Conversation Module 2 (diff vs Lion, finale) | 30 |
| Farm (40 hand captions, 11 collages) | 180 |
| Body (15 hotspots, 7 cards, labels, 5 MCQ) | 240 |
| **Total** | **750 (≈ 107 min average)** |

**Family total: about 6.5 AI-assisted days**: 5.0 for engines and tooling, plus 1.6 for data and QA. Owner time for the rights answers and any re-recording comes on top.

## 8. Risks, edge cases, open questions

- **Devanagari:**
  - Highlight whole words only, never split inside an akshara. Conjuncts (प्राण्यांची, तीक्ष्ण, आफ्रिकेच्या) must stay inside one `<span>`; use `Intl.Segmenter` grapheme fallback if per-akshara highlighting is wanted later.
  - The word chips use `white-space: nowrap`. Watch line-break placement on 320 px phones: Storyline forced a manual "\n" in "सिंह आफ्रिकेच्या\nजंगलात राहतात."
- **Audio sync:** the timings are Storyline timeline values, so expect ±100 ms. Use `audio.currentTime` polling (rAF), not `setTimeout`. iOS needs a user tap before the first `play()`; the Start button provides it. Make sure only one clip plays at a time (`sound.js stop()`), and that auto-read queues (MCQ question then options) cancel when the child taps.
- **Touch and small frame:**
  - Hover-only interactions (Farm `OnMouseHover>stopMedia`, Body `OnMouseHover>playMedia` on 15 labels) do nothing on iPad today. Everything becomes tap.
  - Drag on phones: tap-to-select is the primary input.
  - The book spread stacks vertically under 700 px. Hotspot dots need a 44 px minimum hit area, and their positions must be relative to the image (stored as fractions).
  - Lion and Conv. 2 report size "0x0" in the parse; the slides are 960×640.
- **Page art quality:** the 734×468 video frames are soft once enlarged. Original photos may be better, if they can be found and licensed.
- **Open questions for the owner:**
  1. May we drop the Body jigsaw and the Body name entry?
  2. Should Conversation Module 2 be the *same* package as Lion with a different finale, or one package used in both courses?
  3. Who recorded the `recorded-in-storyline` voices and the Newgen narrations, and do you hold the rights to the Lion and Farm photos?
  4. Should books report a score at all, or completion only? Lion's star count currently never reaches the LMS.
  5. Is "Picture Description 1" meant to grow into a describing exercise (record or type a description), or stay a listen-only reveal? Its folder is "10 Creative Writing", but there is no writing task.
  6. Farm captions: OK to show the Marathi labels written from the clip names, given that Storyline showed no text?
