# Phrase-by-phrase leveler + downward expander between phrases. Mono float32 in/out via raw files.
import numpy as np, sys
from scipy.ndimage import maximum_filter1d, uniform_filter1d
inp,outp,sr=sys.argv[1],sys.argv[2],int(sys.argv[3])
target=float(sys.argv[4]) if len(sys.argv)>4 else -24.0
x=np.fromfile(inp,np.float32)
h=sr//100; n=len(x)//h
db=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
floor=np.percentile(db,10); thr=floor+12
sp=db>thr
# speech mask with hangover: fill gaps <250ms, extend 120ms each side
m=sp.copy()
gaps=uniform_filter1d(m.astype(float),25)>0  # not used directly
idx=np.where(sp)[0]
mask=np.zeros(n,bool); phrases=[]
if len(idx):
    s=p=idx[0]
    for k in idx[1:]:
        if k-p>25: phrases.append((s,p+1)); s=k
        p=k
    phrases.append((s,p+1))
gain_db=np.full(n,np.nan)
for a,b in phrases:
    d=db[a:b]; act=d[d>thr]
    lvl=10*np.log10((10**(act/10)).mean()) if len(act) else db[a:b].max()
    if b-a<20: lvl=max(lvl, np.median([]) if False else lvl)  # short blips: still level, but clamp below
    g=np.clip(target-lvl,-12,12)
    if b-a<15: g=min(g,3)          # don't hugely boost tiny noises/breaths
    A=max(0,a-12); B=min(n,b+12)
    gain_db[A:B]=g; mask[A:B]=True
# between phrases: hold neighbor gain but duck by 14 dB (expander)
valid=~np.isnan(gain_db)
gi=np.interp(np.arange(n),np.where(valid)[0],gain_db[valid])
duck=np.where(mask,0.0,-22.0)
# smooth: fast-ish attack (open early via max filter), slower release
duck=maximum_filter1d(duck,size=9)          # open 40ms early/late
duck=uniform_filter1d(duck,size=8)           # ~80ms ramps
gi=uniform_filter1d(gi,size=15)              # 150ms gain ramps between phrases
g=10**((gi+duck)/20)
# upsample to sample rate
t=(np.arange(n)+0.5)*h
gs=np.interp(np.arange(len(x)),t,g).astype(np.float32)
(x*gs).astype(np.float32).tofile(outp)
print(f"phrases {len(phrases)}, noise floor {floor:.1f} dB, target {target} dB")
