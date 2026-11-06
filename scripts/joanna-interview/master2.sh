#!/bin/bash
set -e
S="$1"
AF="deesser=i=0.4,acompressor=threshold=-26dB:ratio=2.5:attack=10:release=150:makeup=1"
ffmpeg -v error -y -i "$S/lv.wav" -af "$AF" -c:a pcm_f32le "$S/m1.wav"
M=$(ffmpeg -hide_banner -i "$S/m1.wav" -af loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json -f null - 2>&1 | python3 -I -c "import sys,json;t=sys.stdin.read();a=t.rindex('{');d=json.loads(t[a:t.index('}',a)+1]);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$S/m1.wav" -af "loudnorm=I=-16:TP=-1.5:LRA=7:${M}:linear=true,alimiter=limit=0.84:level=false" -ar 48000 -c:a pcm_s24le "$S/final_audio2.wav"
ffmpeg -hide_banner -i "$S/final_audio2.wav" -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input (Integrated|True)"
