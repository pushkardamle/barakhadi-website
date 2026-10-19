# Grammar & translation: engine spec

The family covers 15 projects in the dossier, plus 2 that the matcher missed (see §5). All are live in TalentLMS: 16 real units with 27 to 44 learners each, plus 2 "NCS" test units. Every claim below comes from the XML of the `.story` files, read in memory, and from preview sheets for daf3a0cfbb, b4bf675beb, b510effbc2, 216a8e9fb1, 00b3b1c685, 155d8f4374 and eea6086790.

## 1. What these activities are

**A typical one, as a kid sees it: *Nouns - Vegetables* (538a49825c, TreeTo, 5 slides)**
1. **Title**: chalkboard doodles and "Nouns - Vegetables / नामे - भाज्या", with opening music and a voice intro (`Bhaji1,2.mp3`). There is a sticker preview, then **Start**.
2. **Learn 1**: five vegetable pictures. Tapping one plays a sentence such as `ha fulkobi.mp3` and shows "हा फुलकोबी आहे." with "Cauliflower".
3. **Learn 2**: five more pictures with sentences: हा बटाटा / हा भोपळा / हे वांगे / ही मिरची / हा पानकोबी.
4. **Sort**: "Drag the vegetable pictures based on the correct gender". There are three columns headed **हा / ही / हे** and ten pictures. Tapping a picture says its name (`bhopla.mp3`). The child drags each picture into a column and presses **Check**. If any are wrong, a Try Again layer appears with "Attempts Left: %att_1%" (3 attempts). After the last attempt a **Reveal** layer shows the right answer, and a Correct layer appears once everything is right.
5. **Congratulations** and the sticker.

**How much the family varies (17 projects, 16 unique)**

| Sub-variant | Mechanic | Projects |
|---|---|---|
| A. Sort into buckets (many to one) | drag pictures into 3 labelled columns | Nouns - Animals 155d8f4374 (रानटी / सरपटणारे / पाण्यातील प्राणी, 10 items); Birds 8127a8b68d and Vegetables 538a49825c (हा / ही / हे gender, 10 items each) |
| B. Match one to one (slots) | drag a Marathi word under its tile | Nouns-Color daf3a0cfbb (10 colour names onto colour tiles); Days of week 3b398dbc2c (रविवार…शनिवार onto Sunday…Saturday) |
| C. Sentence to picture | drag a sentence onto the matching picture | ProNouns-1 6d3c786375 (मी / आम्ही, 3 items), ProNouns-2 80f06e2b3f (तू / तुम्ही, 3), ProNouns-3 b4bf675beb (तो / ती / ते, 2 rounds of 3) |
| D. Sentence to place in a scene | drop zones are areas of one scene picture | Pronouns-4 eea6086790 (हा / ही / हे, 2 rounds of 3), Pronouns-5 085661a93c (तो / ती / ते, park scene: बाक, कारंजे, घसरगुंडी) |
| E. Picture multiple choice (translation) | read a sentence, look at the picture, tap 1 of 3 options; each option has a 🔊 button | English to Marathi: Translation - 1 b510effbc2 (6 items, "I woke up." → मी उठलो / उठले / उठला) and 13 Translation 2 c5af7fe8e2 (6). Marathi to English: Translation - 2 cccecf6a42 (8, चेंडू → Bat / **Ball** / Glove) and 14 Translation 2 M→E 9ba322c0bf (8) |
| F. Listening multiple choice | hear a Marathi sentence (nothing written), pick the English | Vocabulary Module 4 216a8e9fb1 (4 items, Newgen, Gappa Goshti Sem 2); Trasnlation - 3 598ef79472 is a copy of it |
| G. Tap the right picture (prepositions) | hear and read a sentence, tap 1 of 3 pictures; each right answer adds to a pond scene | 15 Prepositional 00b3b1c685 (10 items: "दूर डोंगराजवळ एक घर आहे." …) |

Sub-variants A to D (all by TreeTo, 2020) also have **learn screens** before the game:
- Tap-to-hear picture cards in all of them.
- In Pronouns 1 to 3, a "Teacher Tip" voice-over (`Slide 2.mp3`).
- In Pronouns 4 and 5, short dialogue scenes. A 🔊 button opens callout 1 ("हे काय आहे?" / "ही पेन्सिल आहे.") and then callout 2 (plural: "ह्या पेन्सिली आहेत."). The characters are GIFs (`Aunt-Pose-1.gif`, `Girl-Pose-2.gif`) and the speaker has a `Speaking-wave-2.gif`.

## 2. Proposed engines

Use **two engines and one shared intro module**. Picture multiple choice and tap-a-picture are the same "pick one" loop, so they share one engine with two modes.

### Engine 1: `choice` (sub-variants E, F, G)
- **Flow**: title → N item screens with a progress counter → result.
- **Item screen**:
  - A prompt: text (Marathi or English), an optional picture and an optional prompt-audio button. Mode F shows audio only.
  - 3 options as large buttons, each with an optional 🔊 button.
  - In `mode: "hotspot"` (G), the options are instead 3 tappable areas on one question picture.
- **Interaction**: tap. No separate Check button: on phones, tap then Check is two targets for one decision. Storyline used radio buttons plus Check.
- **Feedback**:
  - Right: green tick, chime, then the option or answer audio. In mode G, show the answer picture (`01_a_house.jpg`) with the sentence and its audio (`temp12.mp3`).
  - Wrong: shake, a red ✗ on that option, the wrong-answer sound, and the option is disabled. The child keeps trying until right. This is how the Storyline Translation files behave: Check only becomes Disabled `if [radio:मी उठले.].state eq Selected`, and a `correctAttempt` variable counts first-try answers. Vocabulary Module 4 instead allowed one try and then Continue; standardise on retry-until-correct.
- **Keep**: per-option read-aloud (b510effbc2 has 3 play buttons per slide), the picture, and the build-up of the pond scene in G. The build-up costs nothing because each `*_a_*.jpg` answer picture already contains the earlier additions.
- **Drop**: radio styling, page-turn transitions, the "Play/Pause/Down" picture states, and the Storyline 2 textures (`Parchment.jpeg`, `Stationery.jpeg`).

### Engine 2: `sort` (sub-variants A, B, C, D)
- **Flow**: title → (intro) → 1 or more rounds → result. ProNouns-3, Pronouns-4 and Pronouns-5 each have 2 rounds of 3.
- **Board**: a tray of cards (picture cards or Marathi text cards), plus targets of three kinds:
  - `bucket`: a labelled column that holds many cards (A).
  - `slot`: holds one card, sitting under a tile, word or picture (B, C).
  - `zone`: a rectangle in % of a scene picture (D). The XML gives the coordinates, e.g. Pronouns-5 `Ans 3` at 434,261 of 960x640.
- **Interaction**: drag with Pointer Events, plus tap a card then tap a target. Tap-to-place is required for phones and small iframes. Tapping a card plays its audio (`kanda.mp3`), as Storyline did. Cards can be moved freely until Check.
- **Check**: wrong cards bounce back to the tray with a red flash and right cards lock. There are 3 attempts: the Storyline variables `att`/`att_1` start at 3, even though `intrProps attempts="four"`. After that, **Show answers** animates the remaining cards into place (the Reveal layer).
- **Drop**: per-object fade-ins (Nouns-Color has 120 `entr:fade`), the chalkboard backgrounds (stock, see §6), and the 10 to 17 MB habitat photos, which should be kept but resized.

### Shared module: `intro` (learn screens, used by `sort`, optional for `choice`)
- `cards`: a grid of picture + Marathi sentence + English gloss + audio. Children tap each card, and **Next** unlocks after every card has been tapped. Storyline tracked this with `pg2pic1…` variables.
- `dialog`: a scene with 1 to n callouts, played in order with a speaking indicator (CSS pulse instead of a GIF) and replay.
- `tip`: one "Teacher Tip" audio with play, pause and stop. Pronouns use three buttons; collapse them into one play/pause toggle.

**Rewards and sounds (both engines)**: reuse `shared/sound.js` chimes for place, right and wrong. Keep 1 to 3 stars like the crossword. Show the activity's sticker on the result card: `Stk_Phone_80.png` / `Airawat_Phone_anim.gif` (Translation - 1), `Stk_fish_80.png` (Prepositional), `Stk_Heron`, `Stk_Saapshidi`. This should become a shared reward component across families, not part of either engine.

## 3. Content data model

Both engines use the crossword's top-level keys: `type`, `id`, `title`, `titleMarathi`, `instructions`, `instructionsAudio`, `source`, `sticker`.

**`sort`: Nouns - Vegetables (538a49825c), shortened**
```json
{
  "type": "sort", "id": "L1-05-nouns-vegetables",
  "title": "Nouns - Vegetables", "titleMarathi": "नामे - भाज्या",
  "source": "Nouns - Vegetables.story, slides 2-4",
  "instructions": "Drag the vegetable pictures based on the correct gender",
  "instructionsAudio": "media/bhaji-dnd-instr.mp3",
  "intro": [
    { "kind": "cards", "audio": "media/slide-2.mp3", "cards": [
      { "picture": "media/fulkobi.png", "text": "हा फुलकोबी आहे.", "gloss": "Cauliflower", "audio": "media/ha-fulkobi.mp3" },
      { "picture": "media/gajar.png",   "text": "हे गाजर आहे.",   "gloss": "Carrot",      "audio": "media/he-gajar.mp3" },
      { "picture": "media/kakdi.png",   "text": "ही काकडी आहे.",  "gloss": "Cucumber",    "audio": "media/hi-kakdi.mp3" } ] }
  ],
  "attempts": 3,
  "rounds": [ {
    "layout": "buckets",
    "targets": [ { "id": "ha", "label": "हा" }, { "id": "hi", "label": "ही" }, { "id": "he", "label": "हे" } ],
    "cards": [
      { "id": "bhopla", "picture": "media/bhopla.png", "alt": "भोपळा", "audio": "media/bhopla.mp3", "target": "ha" },
      { "id": "batata", "picture": "media/batata.png", "alt": "बटाटा", "audio": "media/batata.mp3", "target": "ha" },
      { "id": "kakdi",  "picture": "media/kakdi.png",  "alt": "काकडी", "audio": "media/kakdi.mp3",  "target": "hi" },
      { "id": "mirchi", "picture": "media/mirchi.png", "alt": "मिरची", "audio": "media/mirchi.mp3", "target": "hi" },
      { "id": "gajar",  "picture": "media/gajar.png",  "alt": "गाजर",  "audio": "media/gajar.mp3",  "target": "he" },
      { "id": "vaange", "picture": "media/vaang.png",  "alt": "वांगे",  "audio": "media/vaange.mp3", "target": "he" } ] } ]
}
```
- In `slots` layout, each target has a `picture`, `text` or `color`, and holds 1 card. For example, Days uses `{ "id": "sun", "text": "Sunday" }` and the card `{ "text": "रविवार", "audio": "media/ravi.mp3", "target": "sun" }`.
- In `scene` layout, the round has a `scene` picture and each target has `zone: {x, y, w, h}` in %.

**`choice`: Translation - 1 (b510effbc2), item 1**
```json
{ "type": "choice", "id": "L1-05-translation-en-mr-1", "mode": "options",
  "title": "Translation from English to Marathi", "titleMarathi": "चला करू या भाषांतर",
  "instructions": "Listen to the audio and choose the correct option based on the picture.",
  "items": [ {
    "id": "q1", "prompt": "I woke up.", "promptLang": "en", "picture": "media/question1.png",
    "options": [
      { "text": "मी उठलो.", "audio": "media/q1-a.mp3" },
      { "text": "मी उठले.", "audio": "media/q1-b.mp3", "correct": true },
      { "text": "मी उठला.", "audio": "media/q1-c.mp3" } ] } ] }
```
- Mode G uses item `{ "picture": "media/01-q-house.jpg", "text": "दूर डोंगराजवळ एक घर आहे.", "audio": "media/temp10.mp3", "zones": [{ "x":…, "y":…, "w":…, "h":…, "correct": true }, …], "answerPicture": "media/01-a-house.jpg", "answerAudio": "media/temp12.mp3" }`.
- Mode F simply has `promptAudio` and no `prompt` text.

**Fields that change per activity**: everything under `intro`, `rounds` and `items`, plus the titles, the instruction text and audio, and the sticker. The `layout` and `mode` flags are the only switches in the engine.

## 4. Scoring & SCORM tracking

- **Completion**: `completed` when the child reaches the result screen, whether or not "Show answers" was used. `passed` is added only when everything is right on the first try. This matches the crossword policy, so a practice unit never shows as failed.
- **Score** (0 to 100):
  - `choice`: the share of items answered right on the first tap. This is Storyline's `correctAttempt`.
  - `sort`: the share of cards placed right at the first Check, averaged over rounds. Stars are 3 for a first-Check solve, 2 before reveal, and 1 after reveal.
- **Interactions** (SCORM 1.2 `cmi.interactions.n`). There are only 2 per attempt, written once on completion. `shared/lms.js` needs a small `record()` addition.
  1. `first_try_misses` (type `choice`): item and chosen-wrong pairs, e.g. `q1:मी उठला|q4:ताई उठले`, or for sort `vaange>ha|mirchi>ha`. This is the signal that matters here: it shows which gender/agreement or pronoun confusions a child has. Keep it within 255 characters by using item ids and the Marathi answer text.
  2. `checks_used` (type `numeric`): the number of Check presses (sort) or total wrong taps (choice), plus `revealed=true/false`.
- Do not log taps, audio plays or timing beyond `session_time`.

## 5. Extraction plan

Write one script, `tools/extract_grammar.py`. It reads the `.story` with `zipfile` in memory, handles " :: " nested zips, and writes JSON + media only under `activities/content/<id>/`.

1. **Assets**: take every `story.xml` element with `displayName` (audio/image) and match it to `story/media/*` by **MD5**. The `<md5Checksum><stream>` value equals the zip member's MD5: 71/71 matched in b510effbc2. This is more reliable than the crossword's size matching. Display names repeat (`Recorded.mp3` ×22, `CopiedAudio_*`), so always go through the slide's `sound@assetG` and never by name.
2. **Slide order** comes from `story/_rels/story.xml.rels`.
3. **Choice (E/F)**:
   - Options are `radio` elements. Their own `<text>` is empty; the real label is in `stateLst/state[@name='Normal']//text` (Span `Text=` attributes). The prompt is the `textBox name="&Title"`. The picture is the plain `pic` (`Question1.png`, `Q1.png`, `Img2.png`).
   - **Correct answer**: in E it is `radio/scoreData@correct="true"`. In F (`freePickManyIntr`) the `scoringData correct` flags are wrong (several are "true"). Use the Check button's triggers instead: the `showSubSlide` whose condition is `[radio X].state eq Selected` and whose target is the correct feedback layer (named `''`, or containing `snd_Cor`; wrong layers are `Incorrect 1/2`). `multiChoiceIntr@ansG` is shared by every slide and means nothing.
   - **Option audio**: each `pic tn="Play 1"` has `OnClick>playMedia(audio@playG)` → `sound@assetG` → asset. Pair it with an option by nearest `loc@t`.
4. **Hotspot (G)**: three `clkAreaRect` with `typeName` `Hs_Cor` / `Hs_Incor1` / `Hs_Incor2`. Their `loc` l, t, r and b become % zones. Also read `pic tn="pic_Q"`, layer `Cor` → `pic tn="pic_A"`, `textBox tn="txt_Sentence"`, and `sound tn="snd_Obj"`.
5. **Sort (A–D)**:
   - Pairs come from `dragDropIntr/choices/intrFreeChoice@shpG → @matchShpG`. Skip choices whose GUIDs do not resolve: Nouns-Color has one dangling choice, and the learn slides contain empty `dragDropIntr` left over from the template.
   - Drag-card label: the Normal-state text, or its picture asset. **The shape's own `<text>` is a placeholder "७१/७४/७८"** that would otherwise be extracted as content. `typeName` repeats the label with a stray number ("हा हत्ती ७").
   - Drop targets are invisible rects named `Ans n`. Their bucket label, tile, picture or colour must be found by **geometry**: the nearest text rect or picture above or overlapping the slot. This includes the column headers हा/ही/हे, "रानटी प्राणी&#xA;" and the English labels. This step needs hand QA.
   - Card audio comes from the card's `OnClick>playMedia`.
6. **Intro**:
   - Learn slides: pics with an `OnClick>playMedia` trigger and Normal-state texts (sentence + English gloss).
   - Teacher tip: `sound tn="Insta 2"` (`Teacher Tip Hi.mp3`).
   - Dialogs: layers `Callout 1/2`, each with question + answer textBoxes and `OnStart>playMedia` (`Callout 3.mp3`).
7. **Normalise**:
   - Strip `&#xA;`, `&#xD;`, trailing spaces and double spaces ("आम्ही  सॉकर खेळतो.").
   - NFC-normalise and keep the Devanagari as-is.
   - Rename media to ASCII slugs. `tools/package.py` only bundles references that match `^[\w./-]+\.(…)$`, and `लाल.mp3`, `Prani 1,2.mp3` and `two_boys_house_2 [Converted].png` all fail that test, so they would be silently left out.
   - Resize the photos: `dnd_jungle_bg.jpg` is 17 MB, `dnd_baron_land.jpg` 9.8 MB and `dnd_waterhole.jpg` 7.6 MB.
   - Convert the `.wav` files (`Page Intro.wav`) to mp3.
   - Drop the `.fbr` (a 3.5 MB Storyline font cache that appears as `Unknown`/`.bin`).

**Gotchas: which file is live**
- **Unit 2495 "Translation - Marathi to English 1"** is matched to b510effbc2, which is English to Marathi. The real source is almost certainly **598ef79472 `Trasnlation - 3.story`**: its player title is "Translation - Marathi to English", and an output with that title was published at 11:52 on 2020-10-12.
- **Unit 2289 "मराठी -> इंग्रजी Translation - 2"** is matched to c5af7fe8e2 (English to Marathi) with a match margin of 0.0. The likely source is **9ba322c0bf `14 Translation 2 Marathi to English.story`**.
- Both projects are missing from the dossier, and the extractor should use them.
- TreeTo Working holds about 40 WIP/"Dec 11"/"Chaitanya"/"Pushkar" versions of the same nouns and pronouns. Use only the `Final\` files.
- Some titles are wrong or misspelled: "Pronous", "Opning Slide", `lms_title`="Trial_1", and `coursename` = "Level 1 - Learn and Trace 201". Take titles from the dossier, not from the XML.

**Expected automation**:
- About 95% for choice: text, correct answer, picture and audio all come out of the XML.
- About 90% for hotspot.
- About 75% for sort: pairs and labels are reliable, but target-to-picture/label association by geometry and zone sizes need checking.
- **About 85% overall.**

## 6. Reusable assets & rights flags

- **TreeTo (2020)**: about 360 items, `path:D:\Barakhadi` + `user:tdt-05`. This covers all the noun and pronoun pictures (`noun_*.png`, `bhopla.png`), the Marathi word and sentence audio (`hatti.mp3`, `Teacher Tip He.mp3`, `Callout 3.mp3`) and `Correct Audio.mp3` / `Incorrect audio.mp3`. These are good and reusable as-is, **if TreeTo's contract assigned the rights**: please confirm.
- **Newgen**: 135 items from `path:E:\Marathi School`, 34 from `E:\Sudarshan`, 4 from `user:sudarshan.jadhav`, and the play buttons from `E:\101615`. This covers the Translation question pictures (`counting-*.png`, `Q1.png`, `06-01-EngtoMar1.png`), `Board1.png` and the sticker art (`Stk_Butterfly_80.png`). The same rights question applies; the play buttons are replaced by CSS anyway.
- **Owner's own** (`user:pushkar`): the Prepositions scene pictures (`Pictures\Prepositional Words\01_q_house.jpg …`) and the grammar backgrounds (`grammar_doodles.png`, `noun_light_green_bg.jpg`).
- **Stock folder** (`stock-folder`, `C:\Users\Pushkar\Documents\Marathi Shala\Stock Photos\`): `the-background-352166.png` (in all 17 projects), `green_board 2.png`, `sticker_banner_3.png`, `cert_4_main.png`, `Stickers\star_1.png`, `round_1.png`. Their licence is unknown; the numeric name looks like a stock-site download. These are decorative, so **drop them** rather than clearing them.
- **Articulate Storyline 2 textures** (`Parchment.jpeg`, `Stationery.jpeg`, `path:C:\Program Files (x86)`): licensed only for use inside Storyline output, so drop them.
- **Unknown machine** (`user:user`): `Page Intro.wav`, `Pause.png`, `congo.png`. Re-record or drop.
- **Recorded in Storyline**: 86 clips, mostly the option read-alouds in the Translation files (`Recorded.mp3`, `temp13.mp3`). Whose voice is it? Confirm it is Barakhadi's.
- **GIFs**: 15. The animated stickers (`Airawat_Phone_anim.gif`, `Heron_gif_anim.gif`, `Fish_gif_anim.gif`, `Parrot_gif_anim.gif`, `Saapshidi_gif_anim.gif`) and the character poses (`Aunt-Pose-1/2.gif`, `Girl-Pose-1/2.gif`) can be kept, ideally as WebP. Replace `Play-button-GIF1.gif` and `Speaking-wave-2.gif` with CSS.
- **Fonts**: Mangal (810 uses; Microsoft's, cannot be redistributed), Segoe Print, MV Boli and Articulate. Replace them with the shared Baloo 2 / Nunito (OFL).
- There is **no third-party code, video, SWF or web object** in this family: `codes` is empty, and the only `.bin` is the font cache.

## 7. Effort

The calibration point: the crossword took one AI-assisted session for engine, extraction, packaging and tests, and packaging, LMS code, fit and sound are now reusable.

| Piece | Size | Build days |
|---|---|---|
| `choice` engine (options + hotspot modes) | M | 0.75 |
| `sort` engine (buckets / slots / scene zones, rounds, tap-to-place, reveal) | M | 1.25 |
| `intro` module (cards / dialog / tip) | S | 0.5 |
| Extractor (§5) | — | 0.75 |
| `lms.js` interactions + TalentLMS smoke test | — | 0.25 |

**Per-activity data + QA**, averaging about 50 minutes over 16 unique activities:
- Choice files: about 30 minutes each, listening to every option clip.
- Prepositions: 45 minutes, checking zones.
- Nouns: 45 to 60 minutes each, for geometry, labels and photo resizing.
- Pronouns 1 to 3: 60 minutes each.
- Pronouns 4 and 5: 90 minutes each, for scene zones and the dialog intro.

This comes to about 13.5 hours, roughly 1.7 days. **Family total is about 5.25 AI-assisted days.**

## 8. Risks, edge cases, open questions

- **Devanagari**:
  - Card text must never break inside an akshara. Use `word-break: keep-all` and no per-letter spans.
  - Watch conjuncts and nukta forms in the content (`ह्या`, `त्या`, `खाल्ल्या`, `मुंगूस`) and test them with Baloo 2 on iOS Safari.
  - The 255-character SCORM response field must count UTF-16 code units, not letters.
- **Audio**:
  - Phones require a tap before any audio plays, so autoplay instructions (`OnStart>playMedia` on every slide) must wait for Start.
  - Stop the previous clip when a new card is tapped; `sound.js` already does this.
  - The Pronouns teacher tips are 1 to 1.5 MB each, so preload lazily.
- **Touch and small frames**:
  - Drag must work with Pointer Events and `touch-action: none` on cards only, so the page can still scroll. Tap-to-place is the main input on phones.
  - Ten picture cards plus three columns will not fit 360 px wide in landscape layout. Use a vertical stack: columns as horizontal drop bands, with the card tray scrolling sideways.
  - Scene zones (D) at phone width can be about 40 px; enlarge the hit areas beyond the drawn zone.
- **Content errors to fix while extracting**:
  - Vegetables glosses पानकोबी as "Lettuce", but it means cabbage.
  - Marathi options contain double spaces, for example "मला  खूप गोळ्या…" in c5af7fe8e2 and "मी  सॉकर खेळतो." in 6d3c786375.
  - Nouns-Color has a dangling drag choice.
- **Questions for the owner**:
  1. Are units 2495 and 2289 really fed by `Trasnlation - 3.story` and `14 Translation 2 Marathi to English.story`? See §5; the published zips in TalentLMS would settle it.
  2. Do the TreeTo and Newgen contracts give Barakhadi the pictures and voice recordings? Whose voice is in the 86 Storyline recordings?
  3. Retry-until-correct for all multiple-choice items (Storyline Translation) or one try (Vocabulary Module 4)?
  4. Is Vocabulary Module 4 (Gappa Goshti, 2 learners) still worth rebuilding, given that it is a duplicate?
  5. Should the per-activity stickers carry over into a shared sticker-book across activities?
