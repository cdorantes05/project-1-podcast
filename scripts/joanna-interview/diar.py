# Two-speaker split for a mono phone recording: per-phrase features (raw level = mic distance, spectral shape), 2-means.
import numpy as np, sys, json
from scipy.signal import stft
S=sys.argv[1]; sr=48000
x=np.fromfile(S+'/rc48.raw',np.float32)            # raw (unprocessed) cut audio, edited timeline
h=480; n=len(x)//h
db=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
thr=np.percentile(db,10)+12; sp=db>thr
# short phrases: split on gaps >150ms, keep >=0.4s
idx=np.where(sp)[0]; ph=[]; s=p=idx[0]
for k in idx[1:]:
    if k-p>15:
        if p-s>=40: ph.append((s,p+1))
        s=k
    p=k
if p-s>=40: ph.append((s,p+1))
f,t,Z=stft(x,sr,nperseg=2048,noverlap=2048-480); P=np.abs(Z)**2
edges=np.array([100,200,300,500,800,1200,2000,3000,4500,7000,12000])
feat=[]
for a,b in ph:
    seg=P[:,a:b]; act=db[a:b]>thr
    spec=seg[:,act[:seg.shape[1]]].mean(1) if act.any() else seg.mean(1)
    bands=[10*np.log10(spec[(f>=edges[i])&(f<edges[i+1])].mean()+1e-20) for i in range(len(edges)-1)]
    lvl=10*np.log10((10**(db[a:b][act]/10)).mean())
    bands=np.array(bands)-np.mean(bands)
    feat.append(np.concatenate([[lvl],bands]))
F=np.array(feat); Z_=(F-F.mean(0))/F.std(0)
w=np.ones(F.shape[1]); w[0]=2.0                        # level (distance) is the strongest cue
Z_=Z_*w
# 2-means, init by level extremes
c=np.array([Z_[np.argmin(F[:,0])],Z_[np.argmax(F[:,0])]])
for _ in range(50):
    lab=np.argmin(((Z_[:,None,:]-c[None])**2).sum(2),1)
    c=np.array([Z_[lab==k].mean(0) for k in (0,1)])
times=[(a*h/sr,b*h/sr) for a,b in ph]
json.dump({'times':times,'lab':lab.tolist(),'lvl':F[:,0].tolist()},open(S+'/diar.json','w'))
print('cluster sizes',np.bincount(lab),'mean raw level',[round(F[lab==k,0].mean(),1) for k in (0,1)])
# validation against known turns (edited timeline)
known={'Carolyn':[(41,57),(202,212),(280,293),(369,381),(470,486),(584,591),(1095,1099),(1162,1172),(1230,1238)],
       'Joanna':[(57,88),(212,232),(234,248),(293,342),(381,433),(441,461),(593,700),(1009,1084),(1099,1160),(1204,1229)]}
for name,rng in known.items():
    l=[lab[i] for i,(a,b) in enumerate(times) if any(r0<=a and b<=r1 for r0,r1 in rng)]
    print(name, 'phrases',len(l),'-> cluster counts',np.bincount(l,minlength=2))
