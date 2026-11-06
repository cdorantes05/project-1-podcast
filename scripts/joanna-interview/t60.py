# Estimate decay rate after abrupt speech offsets (per 10ms frames, 500-4000 Hz band energy)
import numpy as np, sys, subprocess
from scipy.signal import stft
f=sys.argv[1]
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
fr,t,Z=stft(x,16000,nperseg=512,noverlap=352)  # 10ms hop
band=(fr>500)&(fr<4000)
e=10*np.log10((np.abs(Z[band])**2).sum(0)+1e-12)
slopes=[]
for i in range(20,len(e)-40):
    pk=e[i-20:i+1].max()
    if e[i]>=pk-1 and e[i]-e[i+30]>25:       # strong offset
        seg=e[i:i+25]
        # fit only the part between -5 and -25 dB below peak
        idx=np.where((seg<e[i]-5)&(seg>e[i]-25))[0]
        if len(idx)>=4:
            s=np.polyfit(idx*0.01,seg[idx],1)[0]
            slopes.append(s)
slopes=np.array(slopes)
print(f"offsets {len(slopes)}, median decay {np.median(slopes):.0f} dB/s -> T60 ~ {60/-np.median(slopes):.2f}s (p25 {60/-np.percentile(slopes,75):.2f}s, p75 {60/-np.percentile(slopes,25):.2f}s)")
