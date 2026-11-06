# Scripts

These are the scripts Claude Code wrote while editing the podcast, recovered from the session scratchpads. They are kept as a record of the process, not as a pipeline that runs from end to end. Paths inside them point to Carolyn's machine and to temporary folders, and the media they read isn't in this repo. [PROCESS.md](../PROCESS.md) explains each step.

## joanna-interview/: Part III (Nov 5)

| File | Step |
|---|---|
| `sync.py` | Finds the offset between the camera audio and the phone recording (37.75 s) |
| `pauses.py`, `video.sh`, `video2.sh`, `vfilter.txt`, `vcheck.py`, `cuts-45.json`, `cuts-48.json` | Shorten long pauses, render at a constant frame rate, and check sync |
| `diar.py`, `diar2.py` | Rough two-speaker split, used by the per-voice EQ |
| `t60.py`, `snr.py`, `ltas.py` | Measurements: reverb time, noise level, long-term spectrum |
| `dereverb.py` | De-reverb "option 2", **used** |
| `dereverb2.py` | De-reverb "option 3", smoother, **rejected** |
| `level.py` | Evens out loudness phrase by phrase |
| `voiceeq.py` | Per-voice EQ toward a shared target |
| `audio.sh`, `afilter.txt`, `master.sh`, `master2.sh` | Audio chain and final mastering to −16 LUFS (`master2.sh` is the later one) |
| `plan.py`, `plan2.py`, `phrases.py`, `tail.py`, `keeps_v1.json`, `keeps.json`, `keep_times.json`, `merged10.json`, `render10.sh` | The 10-minute cut: phrase selection and render |

## carolyn-screen/: Part I (Nov 5)

| File | Step |
|---|---|
| `rms.py` | Loudness check |
| `plan_old.py`, `old.json` | First cut plan |
| `plan.py`, `segments.json` | Final cut plan: six tangents removed and pauses shortened |
| `render.py`, `concat-list.txt` | Render the segments and join them |

## lighting-fix/: Part III lighting in podcast-final-1 (Nov 5)

ffmpeg filter graphs in order:

- `fc.txt` and `render.txt`: brighten the person on the left. This was **replaced**.
- `fcR.txt` and `renderR.txt`: darken the person on the right.
- `fcR2.txt` and `renderR2.txt`: the same, darker. **This is the final version.**

## lighting-final-project-2/: Part III grade in final-project-2 (Nov 6)

`grade.txt` is the brightness curve that matches the poster-wall scene to the couch scene.

## Not recovered

- The bumper scripts are with their renders in `project-1/bumper*/` (`bumper.mjs`, `refswap.py`).
- The scripts for Part II (`render.sh`, `mix.py`) and for joining the parts were not saved.
