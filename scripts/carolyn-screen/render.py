import json, subprocess, os, sys
src="/Users/carolyndorantes/AI/project-1/carolyn-screen-with-audio.mov"
segs=json.load(open('segments.json'))
os.makedirs('parts',exist_ok=True)
lst=open('parts/list.txt','w')
for i,(a,b) in enumerate(segs):
    d=b-a; f=f"parts/s{a:.3f}_{b:.3f}.mov"; fd=min(0.015,d/4)
    if not os.path.exists(f):
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(a),"-i",src,"-t",f"{d:.3f}",
          "-vf","fps=60","-c:v","h264_videotoolbox","-b:v","30M","-pix_fmt","yuv420p",
          "-af",f"afade=t=in:d={fd},afade=t=out:st={d-fd:.3f}:d={fd}","-c:a","aac","-b:a","192k","-ar","44100",f+".tmp.mov"],check=True)
        os.rename(f+".tmp.mov",f)
    lst.write(f"file '{os.path.basename(f)}'\n"); print(i,flush=True)
lst.close()
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i","parts/list.txt","-c","copy","-movflags","+faststart",
  "/Users/carolyndorantes/AI/project-1/carolyn-screen-edited-10min.mov"],check=True)
print("done")
