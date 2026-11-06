import numpy as np, sys, json
from scipy.signal import stft, resample_poly
S=sys.argv[1]; sr=48000
x=np.fromfile(S+'/rc48.raw',np.float32)
d=json.load(open(S+'/diar.json')); times=d['times']; lvl=np.array(d['lvl'])
y=resample_poly(x,1,6).astype(np.float64); fs=8000
def f0(seg):
    out=[]
    for st in range(0,len(seg)-320,160):
        fr=seg[st:st+320]*np.hanning(320)
        if np.sqrt((fr**2).mean())<1e-4: continue
        ac=np.correlate(fr,fr,'full')[319:]; ac/=ac[0]+1e-12
        lo,hi=int(fs/400),int(fs/120)          # 120-400 Hz
        k=lo+np.argmax(ac[lo:hi])
        if ac[k]>0.5: out.append(fs/k)
    return np.median(out) if len(out)>3 else np.nan
F0=np.array([f0(y[int(a*fs):int(b*fs)]) for a,b in times])
# spectral tilt & centroid from processed-free raw
f,t,Z=stft(x,sr,nperseg=2048,noverlap=2048-480); P=np.abs(Z)**2; hop=480/sr
cent=[];tilt=[]
for a,b in times:
    sp=P[:,int(a/hop):int(b/hop)].mean(1)
    cent.append((f*sp).sum()/sp.sum()); tilt.append(10*np.log10(sp[(f>2000)&(f<5000)].sum()/sp[(f>200)&(f<1000)].sum()))
F=np.column_stack([lvl,np.nan_to_num(F0,nan=np.nanmedian(F0)),np.log(cent),tilt])
known={'C':[(41,57),(202,212),(280,293),(369,381),(470,486),(584,591),(1095,1099),(1162,1172),(1230,1238)],
       'J':[(57,88),(212,232),(234,248),(293,342),(381,433),(441,461),(593,700),(1009,1084),(1099,1160),(1204,1229)]}
lab_true=np.full(len(times),-1)
for i,(a,b) in enumerate(times):
    for k,(name,r) in enumerate([('J',known['J']),('C',known['C'])]):
        if any(r0<=a and b<=r1 for r0,r1 in r): lab_true[i]=k   # J=0, C=1
for name,col in zip(['level','F0','centroid','tilt'],F.T):
    print(f"{name:9s} Joanna {np.median(col[lab_true==0]):8.2f}  Carolyn {np.median(col[lab_true==1]):8.2f}")
# supervised-ish: LDA trained on known turns (just 2-class Fisher), then temporal smoothing
m0=F[lab_true==0].mean(0); m1=F[lab_true==1].mean(0)
Sw=np.cov(F[lab_true==0].T)+np.cov(F[lab_true==1].T)
w=np.linalg.solve(Sw+1e-6*np.eye(4),m1-m0); sc=F@w; th=(m0@w+m1@w)/2
s=sc-th
# smoothing: weighted average of neighbour scores within +-2.5s
mid=np.array([(a+b)/2 for a,b in times]); dur=np.array([b-a for a,b in times])
sm=np.array([np.sum(s[np.abs(mid-m)<2.5]*dur[np.abs(mid-m)<2.5])/np.sum(dur[np.abs(mid-m)<2.5])*0.5+0.5*s[i] for i,m in enumerate(mid)])
for nm,sv in [('raw',s),('smoothed',sm)]:
    lab=(sv>0).astype(int)
    # leave-out sanity: accuracy on labelled phrases (note: trained on same labels)
    acc=[(lab[lab_true==k]==k).mean() for k in (0,1)]
    print(f"{nm}: Joanna correct {acc[0]:.0%}, Carolyn correct {acc[1]:.0%}, overall split J/C = {np.bincount(lab)}")
json.dump({'times':times,'score':sm.tolist()},open(S+'/diar2.json','w'))
