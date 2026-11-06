# project-1-podcast

A video podcast for Project 1 about senior year and the end of college, planned as three parts of about 10 minutes, each with its own setting and topic ([full plan](notebook/podcast-plan.md)):

- **Part I – Real life, becoming an adult.** Me on the laptop's Photo Booth, in a corner covered with photos, lit by Christmas lights and lamps.
- **Part II – College, looking back.** Daisy and I on the two living room couches: hot takes on what's overrated and underrated on campus, move-in day advice, how Harvard changed her, what she's scared and excited about, and the boring places she'll miss (the Cronkite basement, Lamont, the Memorial Hall balcony, the walk from Lamont to Widener).
- **Part III – Identity and growing up.** Joanna, in my room, in the style of the *In Your Dreams* podcast.

The episode runs Part I → Part II → bumper → Part III. The bumper is a retro-desktop screen where windows open, a note types "interview joanna at 6:00pm", and the opening still of Part III fades in on a WordPad page before the interview grows out of the window.

**Watch it:** [`project-1/final-cut-720p.mp4`](project-1/final-cut-720p.mp4) (34 minutes, compressed to 720p so it fits on GitHub).

## How it was made

The full step-by-step record, with the feedback behind each change, is in **[PROCESS.md](PROCESS.md)**. In short:

1. **Planning.** Seven AI research reports ([research/](research/README.md)) fed the planning notes in [notebook/](notebook/README.md), ending in the [three-part plan](notebook/podcast-plan.md). Visual inspiration is on [Pinterest](https://www.pinterest.com/carolynd2811/final-podcast-idea/).
2. **Part II, Daisy.** Claude transcribed the 20:40 take with Whisper and wrote [`cut-list.md`](project-1/cut-list.md). The take was cut to 14:48 with pauses tightened, and my phone audio was switched in whenever I spoke.
3. **Part III, Joanna.**
   - The phone audio was synced to the camera, then cleaned up in rounds of feedback: de-reverb, noise reduction, per-voice EQ, and −16 LUFS.
   - The before/after samples are in `project-1/`.
   - The interview was then cut to 9:36.
4. **Bumper.** Six versions were drawn from scratch in code (`bumper` to `bumper-v6`). I then switched to editing the reference video itself with `refswap.py`. [`bumper-ref-edit-v2/bumper-final.mp4`](project-1/bumper-ref-edit-v2/bumper-final.mp4) is the one used.
5. **Part I, me on Photo Booth.** A screen recording paired with my phone audio, cut to 9:44.
6. **Assembly.** The three parts and the bumper were joined with ffmpeg and each section was levelled to −16 LUFS. Two transitions were built: the interview grows out of a QuickTime window, and Part III grows out of the bumper's WordPad window.
7. **Finishing.** I finished the edit in iMovie and darkened the over-lit person in Part III ([before/after](project-1/lighting-fix-before-after.png)). After exporting `final-project-2.mp4`, I evened out the lighting of the poster-wall scene to match the couch scene; that version, `final-project-2-lighting.mp4`, is the final cut.

The scripts Claude wrote along the way are in [scripts/](scripts/README.md). If you are an AI reading this repo, start with [AGENTS.md](AGENTS.md).

## What's in the repo

| Path | What it is |
| --- | --- |
| `PROCESS.md` | Step-by-step history: every version, the feedback behind it, and the settings used |
| `AGENTS.md` | Reading guide for AI assistants |
| `project-1/final-cut-720p.mp4` | The finished episode, compressed to fit under GitHub's 100 MB limit |
| `project-1/cut-list.md` | What was kept and cut from the raw interview, with timecodes |
| `project-1/bumper*/` | Bumper versions: `bumper.mjs` draws each frame, `timeline.json` sets the timing, `bumper.mp4` is the render |
| `project-1/bumper-ref-edit*/` | The approach that was used: `refswap.py` swaps the photo and note text inside `reference-bumper.mp4` while keeping the pointer and windows that pass over them |
| `project-1/transitions/` | A minimize-to-taskbar transition (made, but not in the joined cut) |
| `project-1/*.m4a` | Voice recordings and echo/EQ before-after samples |
| `project-1/*.png` | Opening still and the lighting before/after |
| `notebook/podcast-plan.md` | The final plan: setting, lighting, bumpers and questions for each part |
| `notebook/` | Planning notes from `tdm155ai-week-5`: podcast idea, topics, bumper ideas and examples |
| `research/` | The seven AI research prompts and reports behind the plan |
| `scripts/` | Editing scripts recovered from the Claude sessions (sync, audio, cuts, lighting) |
| `utils/` | Course-template generation scripts (OpenRouter, fal, HUIT), not part of the podcast pipeline |

### Not in the repo

GitHub won't store files over 100 MB, so these stay on my computer in `~/AI/project-1/`:

- Raw footage: `IMG_1104.MOV`, `IMG_1155.MOV`, `IMG_1155 - joanna audio.mov`
- Intermediate edits: `joanna podcast - 10 min / edited / final.mov`, `podcast-full*.mp4`, `podcast-final-1*.mp4`, `podcast-final-4k.mp4`, `podcast-preview-720p.mp4`
- Screen recordings: `carolyn-screen*.mov`
- The full-quality final: `final-project-2-lighting.mp4` (1080p, 3.3 GB), and the iMovie export before the grade, `final-project-2.mp4`

## Rebuilding a bumper

The bumper scripts use Node 22+ and [Sharp](https://sharp.pixelplumbing.com/), plus `ffmpeg` on your PATH:

```sh
node project-1/bumper-v6/bumper.mjs "project-1/IMG_1155 opening still (0m17s).png" out/bumper --text "interview joanna at 6:00pm"
```

Flags: `--pixel` (whole-screen pixel size, default 2) and `--photo-pixel` (extra pixelation of the photo, default 3). Note that `bumper.mjs` loads Sharp from `~/AI/tdm155ai-week-6`; change that line to `import sharp from 'sharp'` to use this repo's copy after `pnpm install`.

The reference-swap version needs Python with `numpy`, `Pillow` and `scipy`:

```sh
python project-1/bumper-ref-edit-v2/refswap.py project-1/reference-bumper.mp4 STILL.png OUT.mp4 "note text"
```

## Generation scripts and API keys

Copy `.env.example` to `.env` in the repo root and fill in your keys:

```sh
cp .env.example .env
```

- `OPENROUTER_API_KEY` for text, image and video through OpenRouter
- `FAL_API_KEY` for image and video through fal
- `HUIT_API_KEY` (optional) for Harvard's gateways

`.env` is gitignored. Never commit or share it.

Use Node 22 or later and run `pnpm install` once, then:

```sh
pnpm text openrouter "Reply with the single word HELLO." --model openai/gpt-5-mini --dry-run
pnpm image fal "a small red apple on a white background" --model fal-ai/flux/dev
pnpm video fal "a paper boat drifts across a puddle" --model fal-ai/ltx-2.3/text-to-video/fast --duration 6
```

Outputs land in the gitignored `output/` folder. See [utils/README.md](utils/README.md) for every command.
