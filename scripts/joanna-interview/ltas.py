import numpy as np, sys, json
from scipy.signal import welch
S=sys.argv[1]; src=sys.argv[2]; sr=48000
x=np.fromfile(src,np.float32)
d=json.load(open(S+'/diar2.json')); T=d['times']; sc=np.array(d['score'])
cf=np.array([100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500])
def ltas(sel):
    segs=np.concatenate([x[int(a*sr):int(b*sr)] for (a,b),s in zip(T,sel) if s])
    f,p=welch(segs,sr,nperseg=8192)
    out=np.array([10*np.log10(p[(f>=c/2**(1/6))&(f<c*2**(1/6))].mean()) for c in cf])
    return out-out[(cf>=250)&(cf<=4000)].mean()
conf=np.abs(sc)>np.percentile(np.abs(sc),30)
J=ltas((sc<0)&conf); C=ltas((sc>0)&conf)
# typical long-term speech spectrum shape (relative dB), used as a broadcast-voice target
tgt=np.array([-10,-6,-3,-1,0,0,-0.5,-1,-2.5,-4,-6,-7.5,-9,-10.5,-11.5,-12.5,-14,-15.5,-17,-19,-22,-25.0])
tgt=tgt-tgt[(cf>=250)&(cf<=4000)].mean()
print(' Hz    Joanna Carolyn  target')
for c,j,k,t in zip(cf,J,C,tgt): print(f'{c:6d} {j:6.1f} {k:6.1f} {t:6.1f}')
json.dump({'cf':cf.tolist(),'J':J.tolist(),'C':C.tolist(),'tgt':tgt.tolist()},open(S+'/ltas.json','w'))
