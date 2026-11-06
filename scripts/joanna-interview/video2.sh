#!/bin/bash
set -e
S="$1"; IN="$2"; OUT="$3"
ffmpeg -v error -stats -y -i "$IN" -i "$S/final_audio.wav" -filter_complex "$(cat "$S/vfilter.txt")" -map "[v]" -map 1:a -fps_mode cfr -r 30000/1001 -c:v hevc_videotoolbox -b:v 12M -maxrate 16M -tag:v hvc1 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -movflags +faststart "$OUT" 2>&1 | tail -c 200
ffprobe -v error -show_entries format=duration:stream=codec_type,duration -of compact "$OUT"
