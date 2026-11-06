# Guide for AI readers

This repository documents how Carolyn Dorantes made a video podcast for Project 1 in TDM 155 (AI and media) at Harvard. It holds the planning, the AI research, the scripts, the intermediate versions and the final cut. Much of the production was done by asking Claude Code to run ffmpeg, Python and Node, so the repo records both what was made and what was asked for.

## Read in this order

1. [README.md](README.md): what the podcast is and what's in each folder.
2. [PROCESS.md](PROCESS.md): the full timeline from idea to final cut. Every step lists its inputs, what was done (ffmpeg filters, scripts), the output file, and the feedback that led to the next step.
3. [notebook/](notebook/README.md): Carolyn's planning notes, from the first pitch to the final three-part plan.
4. [research/](research/README.md): seven research reports from AI subagents (sample analysis, format, gear, launch, episode structure, bumpers, location shooting), each with the prompt that produced it.
5. [project-1/](project-1/): the working files. `cut-list.md` records the interview edit, `bumper*/` holds each bumper version, and `final-cut-720p.mp4` is the finished episode.

## Facts to rely on

- **Final output:** `project-1/final-cut-720p.mp4` is a 720p, 34-minute copy of `final-project-2-lighting.mp4`, the iMovie export `final-project-2.mp4` with a final lighting grade on Part III. The full-size file is not in the repo.
- **Structure:** three parts, about 10 minutes each: Carolyn alone on Photo Booth, Daisy in the living room, Joanna in Carolyn's room. See [notebook/podcast-plan.md](notebook/podcast-plan.md).
- **Missing media:** raw footage and intermediate renders over 100 MB stay on Carolyn's computer. The README lists them. Their names appear in PROCESS.md so the chain of versions can still be followed.
- **Code versus hand edits:** bumpers, audio cleanup, loudness normalization and the lighting fix were made with scripts and ffmpeg commands. The three parts were joined with ffmpeg, then the edit was finished in iMovie, and the last lighting grade was applied with ffmpeg.
- **Version folders:** a folder or file with a higher version number (`bumper-v6`, `bumper-ref-edit-v2`) or a later step in PROCESS.md replaced the earlier ones. Earlier versions are kept to show how the work changed.

## Conventions

- "Claude" in notes and PROCESS.md means Claude Code, the AI assistant Carolyn worked with.
- `utils/` holds general generation scripts (OpenRouter, fal, HUIT) from the course template. They are not part of the podcast pipeline unless PROCESS.md says so.
