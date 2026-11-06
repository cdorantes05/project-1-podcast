import numpy as np, sys, wave, subprocess
f=sys.argv[1]
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
h=160; n=len(x)//h; fr=x[:n*h].reshape(n,h); db=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
thr=np.percentile(db,20)+12
sp=db>thr
# phrases: speech runs merged across gaps <300ms, min 0.8s
ph=[];i=0
idx=np.where(sp)[0]
if len(idx):
    s=idx[0];p=idx[0]
    for k in idx[1:]:
        if k-p>30:
            if p-s>=80: ph.append((s,p))
            s=k
        p=k
    if p-s>=80: ph.append((s,p))
L=[]
for a,b in ph:
    seg=x[a*h:b*h]; d=db[a:b]; act=d>thr
    L.append(10*np.log10((10**(d[act]/10)).mean()))
L=np.array(L)
print(f"{f.split('/')[-1]}: noise floor {np.percentile(db,10):.1f} dB, phrases {len(L)}, phrase level p10/p50/p90 = {np.percentile(L,10):.1f}/{np.percentile(L,50):.1f}/{np.percentile(L,90):.1f}  spread(p90-p10) {np.percentile(L,90)-np.percentile(L,10):.1f} dB, std {L.std():.1f}")
hist,edges=np.histogram(L,bins=12)
for c,e in zip(hist,edges): print(f"  {e:6.1f} {'#'*c}")
