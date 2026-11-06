# project-1-podcast

A video podcast for Project 1 about senior year and the end of college, planned as three parts of about 10 minutes, each with its own setting and topic ([full plan](notebook/podcast-plan.md)):

- **Part I – Real life, becoming an adult.** Me on the laptop's Photo Booth, in a corner covered with photos, lit by Christmas lights and lamps.
- **Part II – College, looking back.** Daisy and I on the two living room couches: hot takes on what's overrated and underrated on campus, move-in day advice, how Harvard changed her, what she's scared and excited about, and the boring places she'll miss (the Cronkite basement, Lamont, the Memorial Hall balcony, the walk from Lamont to Widener).
- **Part III – Identity and growing up.** Joanna, in my room, in the style of the *In Your Dreams* podcast.

The parts are joined by retro-desktop **bumpers**: a late-90s computer screen where windows open, a note gets typed, and a photo from the shoot appears before it zooms into the next segment.

**Watch it:** [`project-1/final-cut-720p.mp4`](project-1/final-cut-720p.mp4) (about 34 minutes, compressed to 720p so it fits on GitHub).

## How it was made

1. **Planning** (`notebook/`). The idea started as three friends in three locations with mixed-media bumpers between them. The notebook has the original pitch, the final [three-part plan](notebook/podcast-plan.md) with the look and questions for each part, a bank of interview topics, and research on bumper styles with real examples (Chicken Shop Date, Friends Keep Secrets, *stop trying to be cool girl*) and a mockup of where bumpers sit in an episode. Visual inspiration is on [Pinterest](https://www.pinterest.com/carolynd2811/final-podcast-idea/).
2. **Shooting.** The interviews were filmed on an iPhone (`IMG_1104.MOV`, `IMG_1155.MOV`), with audio recorded separately (`*.m4a`). My part was a screen recording of Photo Booth (`carolyn-screen*.mov`).
3. **Cutting** (`project-1/cut-list.md`). Daisy's 20:40 raw take (`IMG_1104.MOV`) was cut to about 15 minutes: the setup and false starts, side tangents and the "did we catch that on video?" ending were removed, and long pauses were shortened.
4. **Audio cleanup.** The voice tracks were treated for echo and EQ. The before/after samples are in `project-1/`.
5. **Lighting fix.** The final footage was color-corrected; `lighting-fix-before-after.png` shows the difference.
6. **Bumper.** The bumper is generated in code, not edited by hand. Each `bumper*` folder is one version, from the first draft to the final one.
7. **Edit.** Everything was assembled in Adobe Premiere Pro, with a "minimize to taskbar" transition (`project-1/transitions/`) carrying the desktop look into the episode.

## What's in the repo

| Path | What it is |
| --- | --- |
| `project-1/final-cut-720p.mp4` | The finished episode, compressed to fit under GitHub's 100 MB limit |
| `project-1/cut-list.md` | What was kept and cut from the raw interview, with timecodes |
| `project-1/bumper*/` | Bumper versions: `bumper.mjs` draws each frame, `timeline.json` sets the timing, `bumper.mp4` is the render |
| `project-1/bumper-ref-edit*/` | A different approach: `refswap.py` swaps the photo and note text inside `reference-bumper.mp4` while keeping the pointer and windows that pass over them |
| `project-1/transitions/` | The minimize-to-taskbar transition |
| `project-1/*.m4a` | Voice recordings and echo/EQ before-after samples |
| `project-1/*.png` | Opening still and the lighting before/after |
| `notebook/podcast-plan.md` | The final plan: setting, lighting, bumpers and questions for each part |
| `notebook/` | Planning notes from `tdm155ai-week-5`: podcast idea, topics, bumper ideas and examples |
| `utils/` | Text, image and video generation scripts (OpenRouter, fal, HUIT) |

### Not in the repo

GitHub won't store files over 100 MB, so these stay on my computer in `~/AI/project-1/`:

- Raw footage: `IMG_1104.MOV`, `IMG_1155.MOV`, `IMG_1155 - joanna audio.mov`
- Intermediate edits: `joanna podcast - 10 min / edited / final.mov`, `podcast-full*.mp4`, `podcast-final-1*.mp4`, `podcast-final-4k.mp4`, `podcast-preview-720p.mp4`
- Screen recordings: `carolyn-screen*.mov`
- The full-quality final: `final-project-2.mp4` (1080p, 5.2 GB)

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
