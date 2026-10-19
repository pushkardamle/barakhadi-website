# Engine spec: vocab-letter (words with a letter, alphabet intros and songs)

Family dossier: `_work/families/vocab-letter.json` has 62 projects. Preview sheets checked: 4ecda45321 (क), b8efceaafc (ग), 758e839406 (छ), 43334b79e7 (अ), b9a7409306 (Swar Song), 2fcfbb86a2 and 107d7c4888 (Vyanjanmala), 9173247d59 (Akshar Olakh), e58aa13bf1 (Barakhadi Vachan).

## 1. What these activities are

### Typical "Words with Vyanjan छ" (758e839406), seen by a child
1. **Title screen.** A cartoon classroom with "Words with Vyanjan छ" and a round sticker button. Hovering over it shows a faded sticker (`sticker_tease` layer).
2. **"छ"चे शब्द, the sentence teaser.** A crystal ball. Tapping its button plays one of three sentences with a picture inside the ball (`cbal_1..3` layers): छंदामुळे वेळ छान जातो. / छत्रीच्या छोट्या छिद्रातून पाऊस आत आला. / छोले छान लागतात.
3. **"छ"चा खेळ, the Word Hunt.** Six pictures, each with a Marathi + English caption: छावा (Cub), छप्पर (Roof), छकडा (Wagon), छत्रपती, चमचा (Spoon), झुडूप (Bush). Tapping a picture plays the word. A `Timer` layer blocks other taps while the clip plays. A yellow toggle under each picture marks "has छ". **Check** shows `Correct` ("Good job") or `Incorrect` ("Try again"). **Reveal All** puts green छ badges under the four right answers.
4. **Final page.** "Congratulations!", then "Click to see your sticker". A sticker reveals with a GIF (छत्री, `Stk_Umbrella_*.png`, `Umbrella_gif_anim.gif`).

The Swar modules (e.g. अ, 43334b79e7) are the same except screen 2. Swar screen 2 is a **picture reveal**: three greyed objects, and tapping one turns it to colour and speaks it. In अ these are अष्टकोन, अननस, अक्षर, using `octagon g.png` → `octagon.png`.

### Sub-variants (62 projects)

| Variant | Count | Examples |
|---|---|---|
| A. Words with Swar: picture reveal + Word Hunt + sticker | 12 Level 0 + 1 Newgen-only (ऋ, 42aa9d2065) | 43334b79e7 अ … e3532b7c02 अं (in an "old sl backup" folder) |
| A-dup. Newgen copies of A (only the title and one Previous button differ) | 8 | c03dbca1ba, 9def715668, 9dc9b94274, 3de7993977, 11324c4178, 59a98864c4, d4bf405325, 063ad022cb |
| A-stale. Newgen Sem 2 "Vocabulary Module 1" ×3, all अ content but matched to the औ/अं/अः units | 3 | 7c03bf316a, 99e8dbf2a2, 25476510f7 |
| B. Words with Vyanjan: sentence teaser + Word Hunt + sticker | 34 | 4ecda45321 क … 4e4383b738 ज्ञ, incl. TreeTo-reworked त/प (68a9a0f2af, ea80186597) |
| C1. Song chart (timed highlight, tap any letter) | 2 | b9a7409306 Swar Song; 2fcfbb86a2 Intro to Vyanjanmala (L0) |
| C2. Akshar Olakh: video + Swar song + Vyanjan song + sticker | 1 | 9173247d59 |
| C3. Intro to Vyanjanmala L1: song + 2 name-sound dialogues + 3 "pick the letter" MCQs + an open question | 1 | 107d7c4888 |
| C4. Barakhadi Vachan: 12 matra tabs × 36-consonant tap-to-hear grid | 1 | e58aa13bf1 (447 mp3) |

**The B teaser comes in 5 gimmicks.** All 5 do the same job: reveal 3 sentences, each with a picture and audio.
- puzzle (drag pieces): 8 projects (क च ट त प य ष ज्ञ)
- crystal ball `cbal_*`: 7 (ख छ ठ थ फ र स)
- filmstrip/lamp `Center…Right to left`: 7 (ग ज ड द ब ल ह)
- spin wheel `Spin1-3`: 7 (घ झ ढ ध भ व ळ)
- balloon burst `Brust 1-4` + `Lightbox`: 5 (ण न म श क्ष)

**Word Hunt layout:** 6 items. Usually 4 contain the letter and 2 are distractors. ऋ (42aa9d2065) has only 2 correct, and in ओ the key is FFTTTT. "Contains the letter" is not always "starts with it": ई uses पपई/सुरई/कढई/चटई, ळ uses शाळा/कळी/खेळ/माळा, and अं uses कंदील/पतंग.

**Unique units to rebuild: 52.** These are 13 Swar (12 sources, plus अः, which has a published output but no .story), 34 Vyanjan and 5 intros/songs.

## 2. Proposed engines

There are **two engines** on one shared runtime: lms.js, fit.js, sound.js and barakhadi.css from `A:\Barakhadi AI Website\activities\shared`.

### Engine 1: `letter-words` (variants A and B, 47 units, plus the MCQ in C3)
The flow is a list of screens taken from the data. Each screen is optional.

1. **Intro.** Big letter tile and title. The intro clip (e.g. `L1-001-10-Intro.mp3`) plays when the child taps the button, never on load, because iOS needs a gesture. The hover sticker tease is dropped: there is no hover on touch.
2. **Discover**, in one of two modes:
   - `words` (Swar): 3 cards. Tapping a card shows it in colour, then plays the audio and shows the caption. A greyscale CSS filter replaces the separate `… g.png` images.
   - `sentences` (Vyanjan): 3 cards. Tapping a card reveals the picture and sentence and plays the audio. The 5 Storyline gimmicks become one reveal interaction with a cosmetic `skin`: `ball` / `film` / `spin` / `balloon` / `puzzle` (CSS transforms only). I recommend **dropping the drag-the-jigsaw step**. It is fiddly on phones and teaches nothing; the content is the sentence.
   - **Next** unlocks after every card has been opened once. The original tracked this the same way with `pg2pic1..3` / `Pg2Visited`.
3. **Word Hunt** (`hunt`): a 2×3 grid on phones and 3×2 on wide screens. Tapping the picture plays the word (one clip at a time, which replaces the Timer layer). A separate large toggle chip marks "has the letter"; this keeps "listen" and "answer" apart, as the original did. **Check** gives this feedback:
   - All right: chime + "छान!" + stars.
   - Wrong: wrongly chosen cards shake and missed ones stay neutral. The child gets a second try.
   - After 2 failed checks, **Show answers** appears, which is the original Reveal All. Right items get a letter badge.
4. **Sticker**: a tap reveals the module's sticker (e.g. अवकाशयान `stk_spaceship_80.png`) with a CSS pop. The GIF is optional. The result card shows "Score saved to your course" as in the crossword.

Optional screen type `pick` (for C3): show a picture with an audio button and 3 letter choices with audio, e.g. क/ख/ग, then Check. It is the same component as the hunt, in single-select mode.

**What to keep, what to drop.** Keep anything pedagogical: audio on every picture and sentence, the listen/answer split, two tries, then reveal. Drop or simplify the decorative parts: entrance animations (fade/swivel/spinGrow, about 95 per module), the 54 decorative stars, hover states, the Restart lightboxes, and the "Go to course 002 आ?" `jumpToFileUrl` links (the LMS handles navigation). The original's stock sounds (`snd_correct1.mp3`, `Ding-3/4.mp3`, `ON/OFF.mp3`, Audioblocks `intro_act1.mp3`) become generated `chime.*` tones.

### Engine 2: `letter-chart` (variant C, 5 units)
- **Song mode** (C1, C2): a letter grid (Swar 12+ऋ, Vyanjan 36) with play/pause. While the song mp3 plays, the cell whose cue time has passed lights up, driven by `audio.currentTime`. Tapping any cell plays that letter's clip (14 `playMedia` in Swar Song). Cue times come straight from the XML: on the Swar Song `Audio` layer, each letter's text box starts at अ 625 ms, आ 1625, इ 2771 … अः 11688, and the second pass runs from 16292. The song is `SwarSongRU.mp3`, 39.6 s.
- **Tabs mode** (C4 Barakhadi Vachan): 12 tabs (मुळाक्षर, काना, ह्रस्व/दीर्घ वेलांटी, उकार ×2, एक/दोन मात्रा, ओकार, औकार, अनुस्वार, विसर्ग). Each tab shows the 36-consonant grid, and tapping a cell plays its clip. The text is generated: consonant + matra sign, via Unicode composition rather than images.
- **Video screen** (C2): `Akshar_Video.mp4` (23 MB) with native controls.
- **Dialogue screen** (C3): a teacher asks each child "which sound does your name start with?" and the child answers स्/र्/श्/व्. Each line is an image, audio and text in sequence. If the conversation family's engine has this, reuse it; otherwise it is about 100 lines.
- Completion: song played to 90% or every tab opened.

## 3. Content data model

The example is real data from **Words with Swar अ** (43334b79e7). File names come from `media[].orig`. The extractor renames the hashed `story/media/R*.png` files to these names.

```json
{
  "type": "letter-words",
  "id": "L0-swar-a",
  "title": "Words with Swar अ",
  "letter": "अ",
  "source": "Republished Activities/Level 0/01 Vocab/Swar/Vocabulary Module 1 a.story",
  "intro": { "audio": "media/L1-001-10-Intro.mp3" },
  "discover": {
    "mode": "words",
    "heading": "\"अ\"चे शब्द",
    "instructions": "रंगीत चित्रे बघण्याकरिता खालील वस्तूंवर क्लिक करा",
    "instructionsEn": "Click on the objects to reveal pictures",
    "items": [
      { "mr": "अष्टकोन", "en": "Octagon",   "picture": "media/octagon.png",   "audio": "media/L1-001-11-Ashtakon.mp3" },
      { "mr": "अननस",   "en": "Pineapple", "picture": "media/pineapple.png", "audio": "media/L1-001-11-Ananas.mp3" },
      { "mr": "अक्षर",   "en": "Letter",    "picture": "media/letter.png",    "audio": "media/L1-001-11-Akshar.mp3" }
    ]
  },
  "hunt": {
    "heading": "\"अ\"चा खेळ - \"अ\" Word Hunt",
    "instructionsAudio": "media/L1-001-40-Intro.mp3",
    "attempts": 2,
    "items": [
      { "mr": "अगरबत्ती", "en": "Incense Stick", "picture": "media/001-53-agarbatti.png", "audio": "media/L1-001-42-Agarbatti.mp3", "correct": true },
      { "mr": "अजगर",   "en": "Python",  "picture": "media/001-54-python.png",  "audio": "media/L1-001-43-Ajgar.mp3",   "correct": true },
      { "mr": "अक्रोड",  "en": "Walnut",  "picture": "media/001-52-walnut.png",  "audio": "media/L1-001-44-Akrod.mp3",   "correct": true },
      { "mr": "अस्वल",   "en": "Bear",    "picture": "media/001-51-bear.png",    "audio": "media/L1-001-45-Aswal.mp3",   "correct": true },
      { "mr": "गवत",    "en": "Grass",   "picture": "media/grass.png",          "audio": "media/L1-001-46-Gavat.mp3",   "correct": false },
      { "mr": "आगगाडी", "en": "Train",   "picture": "media/train.png",          "audio": "media/L1-001-41-Aaggadi.mp3", "correct": false }
    ]
  },
  "sticker": { "mr": "अवकाशयान", "picture": "media/stk_spaceship_80.png", "locked": "media/stk_spaceship_0.png" }
}
```

A Vyanjan `discover` block, from छ (758e839406). The audio comes from `D:\Marathi school\Chha\02/04/05.mp3`, mapped through triggers:

```json
"discover": { "mode": "sentences", "skin": "ball", "heading": "\"छ\"चे शब्द",
  "items": [ { "mr": "छंदामुळे वेळ छान जातो.", "picture": "media/Hobby.png", "audio": "media/chha-s1.mp3" },
             { "mr": "छत्रीच्या छोट्या छिद्रातून पाऊस आत आला.", "picture": "media/wet boy.png", "audio": "media/chha-s2.mp3" },
             { "mr": "छोले छान लागतात.", "picture": "media/Chholeeatingboy1.png", "audio": "media/chha-s3.mp3" } ] }
```

**Fields that vary per activity:** letter, title, intro audio, discover mode/skin/3 items, hunt 6 items with `correct`, sticker. **Fixed in the engine:** layout, instructions template, feedback text, chimes, attempts (2).

`letter-chart` data has these fields:
- `cells[]` (`label`, `audio`)
- `song` (`audio`, `cues: [{cell, t}]`)
- optional `tabs[]` (`name`, `matra`, `cells[]`), `video`, `dialogues[]`

## 4. Scoring and SCORM tracking (SCORM 1.2)

**letter-words**
- **Completion:** reached the sticker screen. That means every discover card opened and the hunt solved or answers shown. The status is then `completed`, or `passed` for a first-try solve (as in crossword `lms.complete`).
- **Score:** 100 for a first-check solve, 67 for a second-check solve, 33 if Show answers was used. Stars are 3/2/1 to match.
- **Interactions worth recording.** `lms.js` needs a small `interaction()` addition that writes `cmi.interactions.n.*`, or an xAPI `answered` statement.
  1. `hunt` (type `choice`): the item set the child selected **at the first check**, result correct/wrong, and the attempt count. This captures confusions that matter to the owner: choosing a distractor such as झाड for च or गाजर for घ, or missing the "contains" words in ई/ळ/अं.
  2. For C3 only: `pick-1..3`, the first letter chosen per MCQ (e.g. ख vs क for कमळ).
- Nothing per tap or per audio play.

**letter-chart:** completion only, no score. There are no interactions, except optionally the number of tabs opened in Barakhadi Vachan.

## 5. Extraction plan (tools/extract_vocab.py, building on activities/tools/parse_story.py)

All of this reads the .story in memory with Python `zipfile`; nothing is written to B:.

1. **Pick the canonical source.** Use the Level 0 `Republished Activities` copy. Skip the 8 Newgen duplicates and the 3 stale Sem 2 copies. For ऋ, use 42aa9d2065 (Newgen Sem1 Module 7). अः has no source: extract it from the published `Words with Swar अha - Storyline output` (html5 data js), or rebuild it by hand.
2. **Slide roles.** slide.xml is the title. slide2.xml is the discover screen, and its variant comes from the layer names (`cbal_`, `Spin`, `Brust`, `Center`, none → puzzle/words). slide3.xml is the hunt (layers `Timer/Correct/Incorrect/Reveal All`). slide4.xml is the sticker.
3. **Hunt answer key.** On slide3, find the `showSubSlide` trigger whose target layer is `Correct`. Its `trigCond`s give `ChekmarkN = True/False`, with `varG` resolved to names via `story/story.xml <var>`. Then map each `ChekmarkN` to the toggle button whose OnClick `adjustVar` sets it, and map that button to the nearest picture and caption by `loc`. As a cross-check, the green letter badges in the `Reveal All` layer sit under the right items. I verified the key on all 57 four-slide projects (`TTTTFF` in most, `FFTTTT` in ओ, `TTFFFF` in ऋ).
4. **Audio ↔ item.** Follow picture `OnClick>playMedia` → `<sound g>` → `assetG` → asset in story.xml → `story/media/R….mp3|wav`. Do not trust file names. In Vyanjan modules most clips are "Recorded" or `CopiedAudio_*`, and only the Swar modules carry names like `L1-001-42-Agarbatti.mp3`. Many clips are stored as **.wav** (386 in the family), so convert them to mp3 at 64 kbps mono.
5. **Text.** Captions are the Mangal text boxes next to each picture, with the English in "( )". Strip the `Previous/Next/Check/Reveal All/Restart?` chrome.
6. **Song cues.** For each letter text box on the `Audio` layer(s), read `start` from its `txtTmCtx`/`TmCtx`. The song is the long sound on that layer (`SwarSongRU.mp3`; the Vyanjan song is a 1.24 MB "Recorded" mp3, split across `Audio`, `Audio 1-3`).
7. **Barakhadi Vachan.** The audio paths already encode the cell: `D:\Barakhadi\Barakhadi k to Dnya\Audio\<consonant>\<matraIndex>.mp3`. Confirm this against the 480 `playMedia` triggers per layer.

**Gotchas found**
- **Template leftovers in the teaser text.** Each gimmick was cloned from a template, and the old strings survive as hidden objects:
  - "कावळा कुंपणावर बसला आहे. / कपडे कपाटात कोंबले. / कुलपाची किल्ली कुठे विसरली?" appear in every puzzle module (च ट य ष ज्ञ).
  - "छंदामुळे वेळ छान जातो." and "कपडे…" appear in every crystal module (ठ थ फ र स).
  - "गुहेतून…/गारुड्याच्या…" appear in the filmstrips (ड द ब ल ह).
  - "गाणे गुणगुणत गुराखी…" appears in the balloons (न म श क्ष).
  
  Keep only text that is on a layer the triggers actually show **and** contains the target letter. Flag everything else.
- **Spin variant (7 modules: घ झ ढ ध भ व ळ):** the sentences are baked into pictures, so there is no text in the XML. They must be typed by hand.
- **Stale or wrong content in live units:**
  - 5343108ac6 "Words with Vyanjan ण" is a full copy of न (नारळ, नाच… and नवरा नवरीची…).
  - 4e4383b738 ज्ञ has correct ज्ञ sentences, but its Word Hunt is the क्ष hunt (क्षत्रिय, क्ष-किरण…).
  - घ (4711179176) has a leftover instruction: "ज्या वस्तूंमध्ये “क” हे अक्षर आहे…".
- **Stale titles:** many player titles are just "Vocabulary Module" (ण…ज्ञ). Take the title from the TalentLMS unit name instead.
- **No web objects:** the single `story/media/*.bin` (3.5 MB) in each project is Storyline's font bundle (`.fbr`, origin storyline-temp), not a web object. Ignore it.

**Expected automation: about 80% automatic.** That covers captions, Swar words, hunt keys, audio mapping, song cues and the Barakhadi grid. By hand:
- Spin sentences (7 × 3).
- Confirming the teaser sentences after the template filter (34 modules).
- Picking the sticker image.
- New content for ण (full) and ज्ञ (hunt), plus अः if there is no published data.
- The C3 dialogue order.

## 6. Reusable assets and rights flags

The family has about 727 MB of media: 3,061 PNG, 1,718 MP3, 386 WAV, 95 GIF, 13 JPEG and 1 MP4.

- **Word pictures and voice recordings:** reusable as-is after resizing (some PNGs are huge, e.g. `001-52-walnut.png` at 8.4 MB). They come from three sources:
  - Owner folders: `user:pushkar` (432 refs, e.g. `Final Activities\Learn and Trace\L1-001 a\Pictures`).
  - Newgen: `path:E:\Marathi School` (1,788), `user:sudarshan.jadhav` (476), `path:E:\Project` (262), `E:\Sudarshan` (36).
  - An "Exult Working" share (`path:\`, 545, e.g. `Exult Working\Audios\070615\A\…`).

  The vendor files are work-for-hire. Confirm the contracts assign the rights.
- **Recorded voice:** 609 `recorded-in-storyline` clips plus about 100 `CopiedAudio_*`. Whose voice is it, and is consent on file?
- **TreeTo:** Barakhadi Vachan's audio and matra images (`D:\Barakhadi`, 454, `drive-download-20201123…`) and the reworked त/प modules.
- **Stock:**
  - `stock-folder` (253): `Stock Photos\Stickers\star_1.png/round_1.png`, `the-background-352166.png`, `Stock Sounds\snd_correct.mp3`, `Audioblocks\intro_act.mp3`. Audioblocks is a subscription licence: check that redistribution survives a lapsed subscription. Otherwise replace them with generated chimes, which the plan does anyway.
  - 1 `stock:shutterstock` image: `shutterstock_134568512.png` (fort, ग hunt, b8efceaafc). Licence unknown, so replace it or find the licence.
  - `user:tdt-05` `Audio_nath.mp3` (न): unknown origin.
  - `Parchment.jpeg` (Storyline texture, `C:\Program Files (x86)\Articulate`): Articulate-licensed, so drop it.
- **Songs:** `SwarSongRU.mp3` (`user:user` desktop) and the Vyanjanmala song are unattributed. Who composed and sang them?
- **Video:** `Akshar_Video.mp4` (23 MB, `\\gold\Projects\Akshar\Animations`). Its origin is unknown. Re-encode it smaller or host it outside the SCORM zip. There is no Flash/SWF in this family.
- **Fonts:** Mangal (3,653 runs) is Microsoft's and cannot be bundled; Articulate (630) is the player font. Use the Baloo 2 Devanagari already in `activities/shared/fonts`.
- **Third-party code:** none. This family does not use the tracing web object.

## 7. Effort (calibrated on crossword, about 1 session for engine + 2 activities + packaging + tests)

| Item | Size | AI-assisted days |
|---|---|---|
| `letter-words` engine (discover modes + 5 CSS skins, hunt, sticker, `pick`, the `lms.interaction` addition) | M | 2.0 |
| `letter-chart` engine (song cues, tabs, video, dialogue) | M | 1.5 |
| Extractor (trigger graph: key, audio map, cues, template filter, wav→mp3, image resize) | M | 1.0 |
| Packaging/tests (reuse package.py, test-packages.mjs) | S | 0.5 |
| **Engines total** | | **5.0** |

**Per-activity data + QA:**
- Clean vocab module: 20 min (listen to 9–12 clips, check key and captions).
- Spin-variant module: +20 min.
- ण / ज्ञ / अः: 60–90 min each, excluding new recordings.
- Songs: 60–90 min each.
- Barakhadi Vachan: about 120 min.

That averages about **30 min** over 52 units, roughly 26 h or 3.5 days.

**Family total: about 8.5 AI-assisted days**, plus owner time to supply ण/ज्ञ/अः content and answer the rights questions.

## 8. Risks, edge cases, open questions

- **Devanagari:** captions must use real text, not images (e.g. क्ष-किरण, धुमकेतू, षट्कोन, ऐश्वर्य). Test conjunct shaping in Baloo 2 on iOS Safari and Android Chrome. Barakhadi cells built from consonant + matra must render ङ, ञ, ळ, क्ष, ज्ञ + every sign. ऋ and अः need glyph checks.
- **Audio:** iOS blocks autoplay, so start every clip from a tap. One clip at a time. Song cues must follow `currentTime` (not timers) so they survive pause and buffering. The WAVs need converting, or packages balloon (Swar अ media is 21 MB).
- **Touch and small frame:** the hunt grid needs tap targets of 44 px or more. Keep the listen tap and the answer toggle physically separate. No hover. Use the shared `fit.js` for the TalentLMS iframe, and let portrait phones scroll. The 36-cell Vyanjan chart needs 6 columns on phones.
- **The hunt's "contains vs starts with" rule:** the instruction text should say "words that have अ" and not "start with". The ई/ऊ/ळ/ष modules depend on this.

**Open questions for the owner**
1. The ण (5343108ac6) and ज्ञ hunt (4e4383b738) are copies of न/क्ष in live units. Should we supply real word lists and recordings?
2. अः has a published package but no .story. Rebuild it from the published output, or author it fresh?
3. TalentLMS Gappa Goshti units "Week 01/02/03 – Words with औ/अं/अः" are matched to stale अ copies (7c03bf316a, 99e8dbf2a2, 25476510f7). Should one rebuilt package per letter replace both the Level 0 and the Gappa Goshti units?
4. May we drop the jigsaw drag and the per-module gimmick variety in favour of one tap-reveal with light skins?
5. Is the sticker "collection" meant to persist across modules? Today it is per-module only, with no state.
6. Rights: the voices of the recorded clips, the two songs, Akshar_Video.mp4, the Shutterstock fort image, and the Audioblocks intro sound.
7. C3 (107d7c4888) ends with an open spoken question ("…कोणत्या व्यंजनापासून सुरू होतो ते सांगा"). Keep it as a prompt with no scoring?
