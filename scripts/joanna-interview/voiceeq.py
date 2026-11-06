# Per-speaker linear-phase EQ toward a target speech curve, blended by soft speaker weights.
import numpy as np, sys, json
from scipy.signal import firwin2, fftconvolve
from scipy.ndimage import uniform_filter1d
S=sys.argv[1]; src=sys.argv[2]; dst=sys.argv[3]; strength=float(sys.argv[4]); cap=float(sys.argv[5])
sr=48000; x=np.fromfile(src,np.float32).astype(np.float64)
L=json.load(open(S+'/ltas.json')); cf=np.array(L['cf']); tgt=np.array(L['tgt'])
Jm,Cm=np.array(L['J']),np.array(L['C']); M=(Jm+Cm)/2
match=float(sys.argv[6]) if len(sys.argv)>6 else 0.85
def sm(c): return np.convolve(np.pad(c,1,mode='edge'),[0.25,0.5,0.25],'valid')
def corr(spec):
    c=match*(M-spec)+strength*(tgt-M)
    pass
    c[cf<=125]=np.minimum(c[cf<=125],0)
    c-=np.interp(1000,cf,c)
    return np.clip(c,-cap,cap)
cJ,cC=corr(Jm),corr(Cm)
print(' Hz   JoannaEQ CarolynEQ'); [print(f'{c:6d} {a:+6.1f} {b:+6.1f}') for c,a,b in zip(cf,cJ,cC)]
def fir(c):
    fq=np.concatenate([[0],cf,[16000,sr/2]]); g=np.concatenate([[c[0]],c,[c[-1],c[-1]]])
    return firwin2(4097,fq/(sr/2),10**(g/20))
D=2048
yJ=fftconvolve(x,fir(cJ))[D:D+len(x)]; yC=fftconvolve(x,fir(cC))[D:D+len(x)]
d=json.load(open(S+'/diar2.json')); T=d['times']; sc=np.array(d['score'])
# soft weight toward Carolyn's EQ: confident phrases get full EQ, unsure ones get a blend
w=1/(1+np.exp(-sc/ (0.15*np.std(sc))))
fr=np.full(len(x)//480+1,np.nan)
for (a,b),wi in zip(T,w): fr[int(a*100):int(b*100)+1]=wi
idx=np.where(~np.isnan(fr))[0]; fr=np.interp(np.arange(len(fr)),idx,fr[idx])
fr=uniform_filter1d(fr,10)                                     # ~100ms crossfades
W=np.interp(np.arange(len(x)),np.arange(len(fr))*480,fr)
y=(1-W)*yJ+W*yC
y.astype(np.float32).tofile(dst)
print('weights: share fully Joanna-EQ',f'{(w<0.2).mean():.0%}','fully Carolyn-EQ',f'{(w>0.8).mean():.0%}','blended',f'{((w>=0.2)&(w<=0.8)).mean():.0%}')
