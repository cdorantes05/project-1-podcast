#!/bin/bash
set -e
S="$1"; IN="$2"
AF="highpass=f=80,afftdn=nr=10:nf=-55,equalizer=f=200:t=q:w=1:g=-1.5,equalizer=f=3500:t=q:w=1.2:g=2,deesser=i=0.3,acompressor=threshold=-28dB:ratio=3:attack=8:release=180:makeup=2"
ffmpeg -v error -y -i "$IN" -filter_complex "$(cat "$S/afilter.txt");[cat]${AF}[out]" -map "[out]" -ar 48000 -c:a pcm_s24le "$S/stage1.wav"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$S/stage1.wav"
M=$(ffmpeg -hide_banner -i "$S/stage1.wav" -af loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | python3 -I -c "import sys,json;t=sys.stdin.read();a=t.rindex('{');d=json.loads(t[a:t.index('}',a)+1]);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$S/stage1.wav" -af "loudnorm=I=-16:TP=-1.5:LRA=9:${M}:linear=true,alimiter=limit=0.84:level=false" -ar 48000 -c:a pcm_s24le "$S/final_audio.wav"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$S/final_audio.wav"
ffmpeg -hide_banner -i "$S/final_audio.wav" -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input (Integrated|True)"
