#!/bin/bash
set -e
S="$1"; IN="$2"; OUT="$3"
ffmpeg -v error -stats -y -i "$IN" -filter_complex "$(cat "$S/f10.txt")" -map "[v]" -map "[a]" -fps_mode cfr -r 30000/1001 -c:v hevc_videotoolbox -b:v 14M -maxrate 18M -tag:v hvc1 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -movflags +faststart "$OUT" 2>&1 | tail -c 150
ffprobe -v error -show_entries format=duration:stream=codec_type,duration -of compact "$OUT"
