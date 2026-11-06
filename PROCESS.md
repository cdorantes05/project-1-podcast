# Process: from idea to final cut

How the podcast was made, in order. Each step gives what Carolyn asked for, what was done, which file it produced, and the feedback that led to the next step. Most of the editing was done by asking Claude Code to run ffmpeg, Python and Node. This record was rebuilt from those session transcripts and from the order the files were made.

Files marked *(local)* are over GitHub's 100 MB limit and are not in the repo; the rest are linked.

## Overview

```
1. Plan       research/ (7 AI reports) ──► notebook/ (idea, topics, bumper ideas, final plan)
2. Part II    Film and cut Daisy, living room (IMG_1104) ──► podcast-final-4k.mp4
3. Part III   Film, sync, clean and cut Joanna, poster-wall room (IMG_1155) ──► joanna podcast - final.mov
4. Bumper     6 from-scratch versions, then edit the reference video ──► bumper-final.mp4
5. Part I     Record and cut Carolyn on Photo Booth ──► carolyn-screen-final.mov
6. Assemble   Join the three parts, level the loudness, build transitions ──► podcast-full-final.mp4
7. Finish     iMovie, then lighting fixes on Part III ──► final-project-2-lighting.mp4 ──► final-cut-720p.mp4 (in repo)
```

The finished episode runs in this order: **Part I** (Carolyn) → **Part II** (Daisy) → **bumper** → **Part III** (Joanna).

## 1. Planning

- **Research.** Carolyn ran seven AI research agents for podcast prep. Agents 1–4 covered the reference samples, format and hosting, gear and distribution, and a launch plan. Agents 5–7 planned her specific concept: the episode structure, mixed-media bumpers, and shooting on location. Each prompt and report is in [research/](research/README.md).
- **Idea.** [notebook/podcast-idea.md](notebook/podcast-idea.md): interview three friends in three locations, with mixed-media bumpers in between. References were YouTube playlists of video podcasts and lyric videos, plus Pinterest boards with collage, Y2K, retro-computer and CRT looks.
- **Topics.** [notebook/podcast-topics.md](notebook/podcast-topics.md): a bank of senior-year questions.
- **Bumpers.** [notebook/bumper-ideas.md](notebook/bumper-ideas.md) covers where bumpers go and three style directions. It cites *stop trying to be cool girl* (a Photo Booth window on a plain Mac desktop) as the model for a "quiet desktop" bumper. **That desktop idea became the look of the final bumper.**
- **Final plan.** [notebook/podcast-plan.md](notebook/podcast-plan.md), converted from `Podcast.pdf`, sets three 10-minute parts:
  - Part I: real life, recorded on Photo Booth.
  - Part II: Daisy, college looking back, in the living room.
  - Part III: Joanna, identity, in Carolyn's room.

## 2. Part II: Daisy interview

Source: `IMG_1104.MOV` *(local)*, 20:40 of iPhone 4K footage. Carolyn's voice was also recorded on her phone: [`podcast-carolyn-voice.m4a`](project-1/podcast-carolyn-voice.m4a).

1. **Transcribe and cut.** Carolyn asked to "edit it down to the important parts with pauses cut" and to open on the empty set.
   - Claude transcribed the footage with fal-ai/whisper (word timestamps, 2 speakers) and wrote [`cut-list.md`](project-1/cut-list.md). It keeps 7 ranges and lists why each cut was made: setup, false starts, tangents, and checking the recording.
   - Inside the kept ranges, any gap between words longer than 0.5 s was trimmed.
   - The first 3.5 s (the empty couches) crossfades into the conversation with `xfade=fade:duration=0.8`.
   - Result: `podcast-preview-720p.mp4` *(local)*, 14:48.
2. **Interviewer audio.** Carolyn asked to use the phone recording whenever she was speaking.
   - The phone audio was aligned to the camera at an offset of 131.76 s.
   - It was switched in only during her lines, using speaker labels and a per-word level comparison, with 40 ms crossfades.
   - Feedback "slightly quieter": her voice was set 3 dB under Daisy's.
3. **4K render.** `podcast-final-4k.mp4` *(local)*, 14:48, HEVC 30 Mbps.
   - The first render drifted about 1.5 s out of sync because each segment gained one frame.
   - It was fixed by trimming each segment to an exact frame count, then re-rendered.

## 3. Part III: Joanna interview

Source: `IMG_1155.MOV` *(local)*, plus Carolyn's phone recording [`joanna podcast recording.m4a`](project-1/joanna%20podcast%20recording.m4a). Scripts: [scripts/joanna-interview/](scripts/joanna-interview/).

1. **Sync** (`sync.py`). The camera audio was cross-correlated against the phone recording, giving an offset of 37.75 s that held at 4 check points. After "Yes, trim it", the result was `IMG_1155 - joanna audio.mov` *(local)*, 21:02.
2. **Opening still.** A 1920×1080 frame at 0:17, [`IMG_1155 opening still (0m17s).png`](project-1/IMG_1155%20opening%20still%20%280m17s%29.png). It was later used in the bumper.
3. **Tighten pauses** (`pauses.py`, `video.sh`, `video2.sh`).
   - 28 pauses of 0.9 s or more were shortened to 0.45 s.
   - The first render drifted 270 ms because iPhone video has a variable frame rate. It was re-rendered at a constant frame rate.
   - Result: `joanna podcast - edited.mov` *(local)*, 20:39.
4. **Audio to "professional studio" quality.** Carolyn asked for both voices equally loud and the room sound dampened. The audio went through several rounds of her feedback; the final chain (`audio.sh`, `master2.sh`) is:
   1. `dereverb.py`: custom spectral de-reverb (T60 0.8 s, strength 1.8).
   2. `highpass=90, lowpass=14000, afftdn=nr=24, adeclick`.
   3. `level.py`: evens out loudness phrase by phrase and ducks the gaps between phrases.
   4. `voiceeq.py`: a separate EQ for each voice, pulling both toward the same tone.
   5. De-esser and gentle compression.
   6. Two-pass `loudnorm` to −16 LUFS, then a limiter.

   The feedback rounds:
   - **"I can still hear an echo."** The de-reverb step was added. In [`echo before-after sample.m4a`](project-1/echo%20before-after%20sample.m4a) she compared original, option 2 (stronger) and option 3 (smoother, `dereverb2.py`, made after she called option 2 "slightly robotic"). **She chose option 2.**
   - **"Equalizing the audio some more"** ("voices sound different", "overall tone off"). A shared EQ was replaced by the per-voice EQ. Comparison: [`EQ before-after sample.m4a`](project-1/EQ%20before-after%20sample.m4a).
5. **Cut to 10 minutes** (`plan.py`, `plan2.py`, `phrases.py`, `render10.sh`).
   - The footage was transcribed with a local `whisper-cli` and a list of phrases to keep was built (`keeps.json`, `merged10.json`).
   - She asked to remove the entrepreneurial-ventures question. She tried a pause after a joke, then replaced the joke with the end of the investing answer.
   - Result: `joanna podcast - 10 min.mov` *(local)*, 9:36.
   - `joanna podcast - final.mov` *(local)* is the same length and was exported by Carolyn herself.

## 4. Bumper

Goal: a retro-desktop bumper that leads from Part II into Part III, modelled on `reference-bumper.mp4` ([in repo](project-1/reference-bumper.mp4)). Two approaches were tried.

**Approach A: draw the desktop from scratch.** `bumper.mjs` uses Node and Sharp to draw a generic late-90s desktop frame by frame (1920×1080, 24 fps, 8 s).

| Version | Change | Carolyn's feedback that led to it |
|---|---|---|
| [`bumper/`](project-1/bumper/) | First draft: windows open and a note types "joanna podcast :)" | First attempt |
| [`bumper-v2`](project-1/bumper-v2/) | Note says "interview joanna at 6:00pm", clock 5:58 PM | "Change the text" |
| [`bumper-v3-pixel`](project-1/bumper-v3-pixel/) | Whole screen at half resolution with 32 colour levels, photo pixelated more | "More pixelated, like the reference" → "Looks good" |
| [`bumper-v4-still`](project-1/bumper-v4-still/) | Ends on an image-viewer window showing the opening still | Asked for it to end on the still |
| [`bumper-v5`](project-1/bumper-v5/) | Paint canvas left blank, so the still appears only at the end | "Remove the other still… using this to transition into one of the videos" |
| [`bumper-v6`](project-1/bumper-v6/) | Mouse pointer moved off the photo | "Move it off" |

Note: `bumper/bumper.mjs` was edited in place and now holds the v6 code, but `bumper/bumper.mp4` is still the v1 render.

**Approach B, which was used: edit the reference video itself.** Carolyn asked to "use the reference bumper" instead of drawing a new one. `refswap.py` (Python, numpy, Pillow, scipy) finds the clean background of each frame and swaps in new content underneath anything that moves over it, so the real pointer and window fades stay on top.

- [`bumper-ref-edit/`](project-1/bumper-ref-edit/): the still is in the Paint window and the note text is replaced. A 1080p copy was made.
- [`bumper-ref-edit-v2/`](project-1/bumper-ref-edit-v2/): she asked for "the word app [to] open to the still" and to remove the still from the background. The Paint canvas is blank and the still fades in on the WordPad page. **[`bumper-final.mp4`](project-1/bumper-ref-edit-v2/bumper-final.mp4) is the bumper used in the episode.**

## 5. Part I: Carolyn on Photo Booth

Source: a screen recording of Photo Booth, `carolyn-screen.mov` *(local)*, plus her phone recording `carolyn-recording.m4a` ([in repo](project-1/carolyn-recording.m4a)). Scripts: [scripts/carolyn-screen/](scripts/carolyn-screen/).

1. **Audio.** The phone audio was paired with the screen recording at a 46 s offset ("Looks synced"). Result: `carolyn-screen-with-audio.mov` *(local)*.
2. **Cut to about 10 minutes.**
   - Transcribed with `whisper-cli`, and pauses found with `silencedetect`.
   - Six tangents and false starts were cut (`plan.py`, `segments.json`), and pauses over 0.75 s were shortened.
   - Result: a 9:44 cut, saved as `carolyn-screen-final.mov` *(local)*.

## 6. Putting it together

1. **Join.** `podcast-full.mp4` *(local)* joins Part I → Part II → bumper → Part III, all scaled to 4K at 29.97 fps.
2. **Even out loudness.** The sections measured very differently: Part I −31 LUFS, Part II −33.5, Part III −16. In `podcast-full-normalized.mp4` *(local)* each section was normalized to −16 LUFS separately.
3. **Transitions.** `podcast-full-final.mp4` *(local)*, 34:25:
   - Part I → Part II: the last 11 s of the screen recording show Carolyn opening the interview video in QuickTime. The interview then grows out of the QuickTime window to full screen over 1 s.
   - Bumper → Part III: at 7 s into the bumper, the Joanna video fades in inside the WordPad window and grows to full screen.
4. **Minimize transition.** [`transitions/minimize-to-taskbar.mp4`](project-1/transitions/minimize-to-taskbar.mp4) is a 1 s clip where the end of Part II shrinks into the WordPad taskbar button. Carolyn said she would add it by hand later.

## 7. Finishing and lighting

1. **iMovie.** Carolyn finished the edit in iMovie and exported `podcast-final-1.mp4` *(local)*, 34:21, 1080p.
2. **Lighting fix for Part III** (scripts: [scripts/lighting-fix/](scripts/lighting-fix/)). Carolyn first asked to brighten the person on the left. She then changed this to "make the person on the right… darker", then "slightly more dark".
   - The final fix applies from 24:47 (1486.9 s): a soft oval mask over the right-hand person, with a darkening curve and a slight colour shift.
   - Her face brightness went from 133 to 113, matching the person on the left.
   - Result: `podcast-final-1-lighting-fix.mp4` *(local)*. [`lighting-fix-before-after.png`](project-1/lighting-fix-before-after.png) shows four moments before and after.
3. **iMovie export.** `final-project-2.mp4` *(local)*, 1080p, 34:17, 5.2 GB.
4. **Final grade.** `final-project-2-lighting.mp4` *(local)*, made from the iMovie export. **This is the final version.** Scripts: [scripts/lighting-final-project-2/](scripts/lighting-final-project-2/).
   - From 24:41.5 to the end, a brightness curve makes the poster-wall scene match the couch scene: blacks 37 vs 34, whites 190 vs 183, average 119 vs 118.
   - The 720p copy in this repo, [`final-cut-720p.mp4`](project-1/final-cut-720p.mp4), was made from it (two-pass H.264 at 290 kbps, AAC 64 kbps).

## What isn't recorded

- The Part II and assembly scripts were not saved. Their steps above come from the session transcripts.
- What changed between `podcast-full-final.mp4` and the iMovie exports is not recorded.
- The origin of `reference-bumper.mp4` and of the screen and phone recordings is not recorded; Carolyn supplied them.
- The Adobe Premiere Pro project in Carolyn's `~/AI` folder (`video-podcast.prproj`) was made before this pipeline. It is not known whether it was used.
