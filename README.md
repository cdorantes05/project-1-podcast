# project-1-podcast

Project 1: podcast. Generation scripts for OpenRouter, fal, and HUIT in `utils/`, set up the same way as `tdm155ai-week-6`.

## API keys

Copy `.env.example` to `.env` in the repo root and fill in your keys:

```sh
cp .env.example .env
```

- `OPENROUTER_API_KEY` — text, image, and video through OpenRouter
- `FAL_API_KEY` — image and video through fal
- `HUIT_API_KEY` — optional, Harvard's gateways

`.env` is gitignored. Never commit or share it.

## Run the scripts

Use Node 22 or later. Run `pnpm install` once (Sharp is needed for the comic/compress tools), then:

```sh
pnpm text openrouter "Reply with the single word HELLO." --model openai/gpt-5-mini --dry-run
pnpm image fal "a small red apple on a white background" --model fal-ai/flux/dev
pnpm video fal "a paper boat drifts across a puddle" --model fal-ai/ltx-2.3/text-to-video/fast --duration 6
```

Outputs land in gitignored `output/`. Local media (audio, video captures) goes in gitignored `_media/`. See [utils/README.md](utils/README.md) for every command.
