import numpy as np, sys, subprocess
from scipy.signal import stft
def band(f):
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    fr,t,Z=stft(x,16000,nperseg=512,noverlap=352); b=(fr>300)&(fr<5000)
    return 10*np.log10((np.abs(Z[b])**2).sum(0)+1e-12)
ref=band(sys.argv[1])
ev=[i for i in range(20,len(ref)-40) if ref[i]>=ref[i-20:i+1].max()-1 and ref[i]-ref[i+30]>25]
for f in sys.argv[1:]:
    e=ref if f==sys.argv[1] else band(f)
    n=min(len(e),len(ref))
    t1=[e[i+6:i+12].mean()-e[i-3:i+1].mean() for i in ev if i+25<n]
    t2=[e[i+12:i+25].mean()-e[i-3:i+1].mean() for i in ev if i+25<n]
    print(f"{f.split('/')[-1]:14s} echo tail vs word: 60-120ms {np.median(t1):6.1f} dB   120-250ms {np.median(t2):6.1f} dB")
