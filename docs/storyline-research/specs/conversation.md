# Conversation family (Gappa Goshti): engine spec

Sources: dossier `_work/families/conversation.json` (43 projects, 46 TalentLMS units), project parses in `_work/projects/`, preview sheets for 2951c57190, f5b0af201e, 7bc9d896b9, 70734acc07, 00f680950c and 5a96d9df4d, and direct read-only XML reads of the Diwali, Me and My Things, Hobbies, Fall Color, Class Party, My Jobs (Sem 3), Summer Break and Barakhadi (Sem 2 M8) .story files.

## 1. What these activities are

**A typical module, Diwali (2951c57190, same content as Newgen Sem 1 M3 271edc9ab4), as a kid sees it:**

1. **Title.** A cloud of coloured speech bubbles, "गप्पा गोष्टी / Gappa Goshti", "Conversation Module / Diwali", and a goal line ("Conversation Goal: Celebrating Diwali.", read aloud from `Page 1Conversation Goal.wav`). Start button.
2. **Scenes 1–4** (slides 2–5). A full-screen illustrated scene (`BG2.png`) with 2–5 characters (`Girl4.png`, `Father.png`, `Mother_1.gif`, `Boy5_1.gif`) and a pulsing play icon by one of them. On tap, a red speech bubble (`Callout.png`) fades in above the speaker with the **English** line ("Hi Anjali! what are you getting ready for?"). The **Marathi** line plays as audio, and a "speak-wave" GIF sits at the speaker's mouth. Then the next play icon appears by the other speaker. Tapping the bubble replays the line. The Next button only appears in the last line's layer, so the kid has to hear the whole dialogue. Diwali has 7+2+3+3 = 15 lines.
3. **Independent Practice** (slide 6). "Click on the question and select the answer." There is a play button for the question and three play buttons with radio buttons for the answers. **No text at all: question and answers are audio only.** Check shows a tick or a cross plus a praise or "try again" clip.
4. **Speak** (slide 7). A green "?" bubble and a red bubble with a Marathi question, "तुम्ही दिवाळीला काय काय केलत सांगा बरं?", read aloud. The kid answers out loud. Nothing is recorded.
5. **Completed / mystery phrase** (slide 8). Bubbles grow in. "Click here to reveal the mystery phrase" shows a picture with an audio phrase. The picture teases **next week's topic**: Diwali shows a pumpkin (Thanksgiving is Sem 1 M4), and Hobbies (7bc9d896b9, Sem 3 M5) shows a mailbox (Sem 3 M6 is "A Letter in the Mail").

Storyline tracks completion only: `quizMgr trackMode="slide" slidesViewedNumber="100"`. No score reaches the LMS.

**Variation (43 files, 26 distinct topics).** I classified every slide (88 quiz slides, 50 dialogue scenes, 36 speak prompts, 37 reveals):

| Sub-variant | Files | Examples |
|---|---|---|
| **A. Callout scenes + audio quiz** (2016 Newgen, Sem 1/2 style): characters in a scene, "Callout N" or "Dialogue N" layers, 3-option quiz with audio answers. 16 of these files embed a "Scene" **video** that replays the conversation beside each quiz item | 20 | Diwali 2951c57190, Fall Colors 70734acc07, New Year 897c702287 (14-line scene), Snow Day 8b19966ffc, Sem 1 M1–M10 |
| **B. Narrator panels + Marathi-text quiz or drag** (2017, Sem 3 style): one narrator avatar (`Call 1.gif`, "Talking" state) moves along a motion path across 2–3 slanted scene panels that light up from grey to colour, "Audio N"/"Click N" layers. Quiz answers are printed in Devanagari | 20 | Me and My Things f5b0af201e, Hobbies 7bc9d896b9, Class Party 5a96d9df4d (adds tap-the-paper-chits), Play Date bd475d6b72 (adds a "Teacher tip" layer), A Letter in the Mail afc40d66f4 ("Letter Drop") |
| **C. Alphabet/song modules** | 3 | Swaramala song 00f680950c (13 flowers on a string, letters light up with the song), Vyanjanmala 4afe9fa937 (consonant song plus a "which sound does your name start with? स्, र्" dialogue), Barakhadi 808a1ce91e (23 MB `Akshar_Video.mp4` "How are Marathi letters formed?") |

Embedded mini-games across the family:
- **Choice:** audio-only answers in 54 items, Devanagari text answers in 53, and picture answers in Summer Break 044c175e8b (`freePickOneIntr`, 4 items).
- **Drag word into blank:** f5b0af201e and e4fb7375ef. The learner drags माझा/माझे/माझी into a dotted box under a picture.
- **Order cards by audio:** Word Game 2727395287/37a629c07b (word chain गाडी, डबा, मुलगी) and Field Trip 760d008fd1, with a "Reveal All" layer.
- **"Barakhadi Song" sub-screen:** in 12 Newgen Sem 2/3 files. One consonant's 12 forms pop up in time with a song (घ घा घि … घः), then 3 example words with pictures (घर (Home), घसर (Slide), घे (Take)).
- **Speak prompt:** 36 files. **Mystery reveal:** 37 files.

**Duplication:** 17 "Republished Activities" files are later edits of Newgen files on the same topic (e.g. Republished Hobbies 7bc9d896b9 = Sem 3 M5 7fd0cc45ae, with the Barakhadi Song slide removed). That leaves **26 distinct topics**. Both copies are live: Newgen files in the "Sem. N – Week N – Conversation" units, Republished files in the "Practicing Conversation – X" units.

## 2. Proposed engine

**One engine, `conversation` (a scene player), with a list of typed screens.** Variants A, B and C are screen types inside it, so they don't need separate engines. The quiz components should live in `shared/` because the books-comprehension family needs the same audio and text choice items.

| Screen `kind` | Mechanic | Keep / simplify |
|---|---|---|
| `title` | Topic, Marathi heading, goal line with audio, Start | Replace the 14 growing bubble PNGs with one CSS bubble cluster |
| `scene` | **Stage + transcript.** The background and characters are drawn on a 3:2 stage, with characters placed in % coordinates taken from the XML boxes. Each line: the speaker gets a glow (or their talking GIF if one exists), the Marathi audio plays, and a bubble shows the English text (with Marathi text if a transcript exists). On wide frames the bubble sits over the stage near the speaker. On phones and in the small TalentLMS iframe the lines stack below the stage as a chat log, which is easy to read at 360 px. Tap the play icon to advance; tap any earlier bubble to replay it. Next unlocks once every line has been heard (same as Storyline) | Keep: speaker highlight, audio and text in step, gating. Keep grey-to-colour panel reveal for variant B as a crossfade (it shows where to look). Drop: the narrator's motion path, fly-ins, wipe entrances |
| `quiz` | Modes: `choice` (each option can be audio, Devanagari text or a picture, each with a replay button), `blank` (drag or tap a word tile into a slot), `order` (drag or tap cards into slots 1–3). Tap-to-select plus a Check button, so it works on touch without fine dragging | Keep: tick/cross, praise and "try again" clips, one retry, then show the answer. Replace the question video with a "Hear the conversation again" button that replays that scene's lines from data (the video is a recording of the same dialogue; to confirm with the owner) |
| `song` | Song audio with timed cues. Each akshara grows and highlights at its cue time (karaoke), then example words with pictures. Tap any akshara to replay from its cue | Keep the timing (it is the teaching). Drop the 12 per-letter motion paths |
| `video` | Plain `<video>` with a poster (`Akshar_Video_Slate.png`), for 808a1ce91e only | Re-encode |
| `chits` | Tap items to reveal a picture and audio (Class Party paper chits) | Same reveal component as `reveal` |
| `speak` | Marathi question with audio and the English instruction; "I said it!" button | No recording in v1. A record-and-playback option is an open question |
| `reveal` | Completion card, tap to reveal the teaser picture and phrase audio, stars | Keep |

Sounds come from the existing clips (praise and try-again) plus the chimes in `shared/sound.js` (one clip at a time, which also fixes the original's 36 `stopMedia` triggers per quiz slide). Reward: 1–3 stars on the reveal card, from first-try quiz accuracy.

## 3. Content data model

One JSON file per topic. Real data from Diwali 2951c57190, with the drag item from f5b0af201e and the song from Sem 3 M2 0bebc57088:

```json
{
  "type": "conversation",
  "id": "conv-diwali",
  "title": "Diwali",
  "titleMarathi": "गप्पा गोष्टी",
  "goal": "Celebrating Diwali.",
  "goalAudio": "media/goal.mp3",
  "cast": {
    "boy":    { "img": "media/boy5_1.gif" },
    "anjali": { "name": "Anjali", "img": "media/girl4.png" },
    "father": { "img": "media/father.png" },
    "mother": { "img": "media/mother_1.gif" }
  },
  "screens": [
    { "kind": "scene", "layout": "callouts", "bg": "media/bg2.png",
      "actors": [ { "cast": "anjali", "box": [105,376,217,603] }, { "cast": "boy", "box": [235,376,342,599] },
                  { "cast": "father", "box": [285,160,399,468] }, { "cast": "mother", "box": [600,241,680,502] } ],
      "lines": [
        { "who": "boy",    "audio": "media/s1-01.mp3", "en": "Hi Anjali! what are you getting ready for?", "mr": null },
        { "who": "anjali", "audio": "media/s1-02.mp3", "en": "Tomorrow is Diwali, so we are decorating the house.", "mr": null },
        { "who": "anjali", "audio": "media/s1-03.mp3", "en": "We made Rangoli, lit the lamps and put up the lantern too.", "mr": null }
      ] },
    { "kind": "quiz", "mode": "choice", "id": "q1",
      "prompt": { "audio": "media/q1.mp3" },
      "choices": [ { "audio": "media/q1-a.mp3" }, { "audio": "media/q1-b.mp3" }, { "audio": "media/q1-c.mp3" } ],
      "answer": 0, "replayScene": 0 },
    { "kind": "quiz", "mode": "blank", "id": "q2", "img": "media/question1.png", "prompt": { "audio": "media/q2.mp3" },
      "tiles": [ { "mr": "माझा", "audio": "media/q2-t1.mp3" }, { "mr": "माझे", "audio": "media/q2-t2.mp3" }, { "mr": "माझी", "audio": "media/q2-t3.mp3" } ],
      "answer": "माझी" },
    { "kind": "song", "audio": "media/gha-song.mp3",
      "cues": [ { "t": 812, "mr": "घ" }, { "t": 1750, "mr": "घा" }, { "t": 2500, "mr": "घि" } ],
      "words": [ { "t": 27000, "mr": "घर", "en": "Home", "img": "media/house111.png" } ] },
    { "kind": "speak", "mr": "तुम्ही दिवाळीला काय काय केलत सांगा बरं?", "audio": "media/speak.mp3" },
    { "kind": "reveal", "img": "media/teaser.png", "audio": "media/teaser.mp3" }
  ],
  "feedback": { "correct": "media/fb-correct.mp3", "tryAgain": "media/fb-try.mp3" },
  "source": { "story": "Republished Activities/Level 2/03 Conversation Activities/03 Conversational Module - Diwali.story",
              "media": { "s1-01.mp3": "story/media/R6WlVcdfyl6n.wav (Scene1Boy1.wav)", "s1-02.mp3": "R5ib8Jvc8crI.wav (Scene1Girl1.wav)",
                         "q1.mp3": "R6K9XHxem2Wx.mp3", "q1-a.mp3": "R6hEdrHO2xBB.mp3", "speak.mp3": "R5Ye0z7GMAbT.mp3",
                         "teaser.mp3": "R5ar7AnWMACU.mp3", "fb-correct.mp3": "CopiedAudio_6dojYJCg4Ll" } }
}
```

(Real answer keys: Diwali Q1 = top radio. f5b0af201e Q1 = माझी, the tile whose `OnDrop` sets `Drop1=True`. Hobbies Q1 = "त्याला फोटोग्राफीचा छंद आहे.")

**What varies per activity:** cast and images, number of scenes and lines, `layout` (`callouts` or `panels`), `en`/`mr` text, quiz modes and keys, whether there is a song and its cues, the speak prompt, and the teaser. Engine code, feedback chimes and the title and reveal art are shared.

## 4. Scoring & SCORM tracking

- **Completion:** `cmi.core.lesson_status = "completed"` when the reveal screen is reached. Scenes are gated on hearing all lines, so this matches Storyline's "100 % slides viewed". There is no pass/fail, because the originals had no mastery score.
- **Score:** `cmi.core.score.raw` = % of quiz items correct **on the first try**. It is omitted for item-less modules (00f680950c). Stars: 3 at ≥ 90 %, 2 at ≥ 60 %, 1 otherwise.
- **Interactions worth recording (2):**
  1. One per quiz item: `id` = item id (e.g. `diwali-q1`), `type` = `choice` or `sequencing`, `student_response` = the **first** pick (option index, tile text or card order), `result` = correct/wrong. This shows which wrong answers kids pick on tricky items.
  2. Tries-to-correct per item, as a numeric interaction `<id>-tries`.
  
  Optionally, total line replays go in `suspend_data` as a rough "hard to follow" signal. Use `shared/lms.js` unchanged; the xAPI path stays for the 10 TinCan units.

## 5. Extraction plan

Write a `tools/extract_conversation.py`. It reads each .story in memory (zipfile, read-only) and writes a draft JSON plus renamed media. Steps:

1. **Screens:** the slide order comes from `story/_rels/story.xml.rels`. The classifier I used (it covered every slide): text "Gappa Goshti" means title; layers `Callout N`/`Dialogue N`/`Audio N`/numeric/character names mean scene; `Correct`/`Incorrect` layers or `freePickOneIntr`/`dragDropIntr` mean quiz; "Barakhadi Song" or an "Audio" layer with Devanagari letters means song; "answer the following question" means speak; "mystery phrase" means reveal.
2. **Lines:** each dialogue layer holds one `sound` element plus one `textBox`. **Audio file** = `story/media/R` + the sound's `name` (e.g. `6WlVcdfyl6n.wav` maps to `R6WlVcdfyl6n.wav`). The display name comes from `assetG` matched against `<audio g=…>` in `story.xml`. Line order = layer order. Drop the duplicate "Click N", "Delay" and "Pause" layers, which repeat the previous text. My prototype got all 15 Diwali lines and 16 Hobbies lines right.
3. **Speaker:** pick the first rule that applies:
   - The Newgen audio name (`Scene1Boy1.wav`, `Scene4Girl1.wav`).
   - The layer name when it is a character ("Mother", "Mihir 2", "Soha", "Ved").
   - Nearest base-layer character picture to the layer's `Speak-wave` GIF or `Callout.png`.
   
   Proximity alone was right for Diwali scene 1 but wrong for parts of scenes 3–4, so expect hand fixes.
4. **Answer keys:**
   - Radio quizzes: the `Correct` layer's `showSubSlide` trigger condition gives the selected radio (`shapeState … name="Selected"`). Rank radios top-down and pair each with the play button in the same row. Each play button's `playMedia → audio playG` gives that option's clip.
   - Drag into blank: the tile whose `OnDrop>adjustVar` sets `boolVal="True"`.
   - Ordering: the `intrFreeChoice shpG→matchShpG` pairs.
   - Picture choice: `freePickOneIntr` `scoringData correct`.
   
   Verified on Diwali, Hobbies (Q1 = index 0, Q2 = index 2, both match the story) and Fall Colors.
5. **Song cues:** `tmCtx start` (ms) of each textBox in the song layer (घ 812, घा 1750 … घः 10000; words 27000/29000/30500).
6. **Geometry:** `loc l/t/r/b` on a 960×640 canvas, converted to % for actors.

**Gotchas:**
- **Stale titles.** All Newgen titles are "Conversational Module N", and three files share "Conversational Module 1". 3469f8d2bc's file is "My Jobs" but its title is "Talking about Self". `project_id` = "L1-001", `lms_title` "Trial_1" and `coursename` "Level 1 - Learn and Trace 101" were copied from a template. Name topics from the TalentLMS unit name and the goal line.
- **`sndProps/origFile` is stale.** A Diwali scene sound claims `…L1-008-Ae\Audio\008-10-Intro.mp3`. Never use it.
- **91 % of 1,792 audio clips are anonymous** ("Recorded.mp3", "temp25.mp3", "CopiedAudio_*"), so mapping has to come from structure, never from file names.
- Layer names have typos and stray spaces: "Dialouge 1 ", "Shuorya  ".
- Drag feedback layers are unnamed `feedBackLayer`s.
- Videos are stored once per slide (Snow Day carries the same 8.4 MB clip 3 times; New Year is 111 MB). Deduplicate by bytes.
- Pick one source per topic for the 17 Republished/Newgen pairs, then diff them, because the Newgen Sem 3 copies have the extra Barakhadi Song slide.

**Expected automation:** about 90 % automatic for structure, English text, images and the audio-to-line mapping. About 95 % for answer keys. About 65 % for speaker attribution. **0 % for Marathi transcripts**: the dialogue exists only as audio, with no notes and no alt text. Displaying Devanagari needs speech-to-text plus a native speaker's review. **Overall about 75 % automatic.**

## 6. Reusable assets & rights flags

- **Art:**
  - 1,841 files from `E:\Marathi School`, 377 from `E:\Sudarshan`, 66 with origin `user:sudarshan.jadhav`, and 43 from the `\\gold\operations\Projects\MarathiShala` share. All are **Newgen**-made characters, scenes, bubbles and play icons.
  - They can be reused as-is (PNG and GIF, 960×640 scale) **if the Newgen contract gives Barakhadi ownership** (to confirm).
  - The recurring cast (Soha, Ved, Shourya, Roshan, Aakash, Sayali, Mihir, Anjali) should become one shared `cast/` library.
- **Stock:**
  - 86 files from `C:\Users\Pushkar\Documents\Marathi Shala\Stock Photos` (e.g. `the-background-352166.png`, `green_board 2.png`) and 1 `stock:shutterstock`. The licence proof is unknown, so replace them or confirm the licence.
  - `Parchment.jpeg` is a Storyline 2 built-in texture (Articulate licence). Drop it.
- **Voice:**
  - 1,237 clips recorded inside Storyline and 393 copied clips: the owner-side voices. Get consent if child voices are used.
  - The named WAV/MP3 clips (`Scene1Boy1.wav` …) were Newgen recordings.
  - Convert all WAV (100) to mono MP3 and normalise loudness.
- **Video:**
  - Question videos (`Question Video_M5.mp4` 1.3 MB, `Question Video.mov` 22.6 MB in New Year, `Question VideoFinal.mov` in Play Date) appear in 16 files.
  - Also `Fireworks.mp4` (New Year, origin unknown) and `Akshar_Video.mp4` (23 MB, Newgen `\\gold\Projects\Akshar`).
  - Re-encode to H.264 480p, or drop the question videos in favour of scene replay.
  - **No Flash/SWF and no web objects:** the one `.bin` in every file is Storyline's 3.5 MB `.fbr` temp resource, so there is no third-party code licence to track.
- **Fonts:** "Articulate" (Storyline-only), Mangal (Microsoft, not redistributable) and Edwardian Script ITC (New Year). Replace them all with the OFL Baloo 2 Devanagari already in `activities/shared/fonts`.
- **Size:** 1,025 MB of sources across 43 files. The rebuilt packages should be about 3–6 MB each.

## 7. Effort

Calibration: the crossword engine (one engine, one mini-game, extraction, packaging, tests) took about one AI-assisted session/day.

| Item | Estimate |
|---|---|
| Engine complexity | **L**: scene player with 2 layouts, 3 quiz modes, song with cues, video, chits, speak, reveal, responsive stage/transcript |
| Engine build (AI-assisted) | **5 days**: scene player and layouts 1.5, quiz modes 1.5, song/video/reveal/speak 0.5, extractor 1, packaging and tests 0.5 |
| Per distinct topic (26) | **~75 min**: run the extractor, listen-check about 40 clips, fix speakers, verify keys, re-encode media, test in the iframe and on a phone |
| Per duplicate (17) | ~15 min: diff against the twin; publish the same JSON to both units |
| Optional Marathi subtitles | +30 min per topic (speech-to-text plus native review) |
| **Family total** | 5 + (26×75 + 17×15) min ≈ 5 + 4.6 = **about 10 working days**, or about 11.5 with Marathi subtitles |

## 8. Risks, edge cases, open questions

**Risks / edge cases**
- **Devanagari:** half-forms and conjuncts (स्, र्, क्ष, ज्ञ in 4afe9fa937) and visarga/anusvara (घः, घं) have to render with Baloo 2 and never be split across tiles. Tile matching should compare whole strings in NFC form.
- **Audio sync:** the song cues are absolute ms from the layer start, so start the song timeline only on the `audio.playing` event. iOS blocks autoplay, so the first line of every scene must be tap-started; Storyline started it `OnStart`.
- **Touch:** 44 px minimum targets, tap-to-place as an alternative to drag, and no hover states (the originals depend on Hover states).
- **Small frame:** the 960×640 scenes hold 4–7 small characters. Below 600 px wide, use the transcript layout with the stage at full width (≈ 360×240). The bubble text must never sit over the art.
- **Content bugs to carry or fix:** the teaser pictures assume a week order, so a module reused elsewhere teases the wrong topic. The Greetings, My House and A Letter in the Mail units point at files with other titles: f5b0af201e, 7bc9d896b9 and 2951c57190 each match 2 units.

**Open questions for the owner**
1. The callouts show English while the audio is Marathi (inferred from the XML; no transcript exists). Should we add Marathi Devanagari text (needs transcription, about 13 h for 26 topics), a transliteration, or keep English only?
2. For the 17 duplicate topics, which version is canonical: Republished (edited) or Newgen (with the Barakhadi Song slide)? Can one JSON serve both TalentLMS units?
3. Is it OK to replace the question videos with "replay the conversation" from the scene data? Please watch one first, e.g. `Question Video_M5.mp4` in 70734acc07.
4. Does the Newgen contract transfer rights to the art, voices and `Akshar_Video.mp4`? Are the stock-folder images licensed?
5. Should the speak prompt record the child's voice for self-playback? (Mic permission inside the TalentLMS iframe is uncertain.)
6. Which file backs the live "Practicing Conversation – Greetings" and "– My House" units? No Republished Greetings or My House .story exists in the family, apart from a 2020 published "Conversation Module - My House" output.
