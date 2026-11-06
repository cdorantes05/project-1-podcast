import numpy as np, sys, json
x=np.fromfile(sys.argv[1],np.float32); sr=16000; h=160  # 10ms frames
n=len(x)//h; r=np.sqrt((x[:n*h].reshape(n,h)**2).mean(1)); db=20*np.log10(r+1e-9)
thr=float(sys.argv[2]); minp=float(sys.argv[3]); keep=float(sys.argv[4])
sil=db<thr
# smooth: speech frames need to be sustained; treat brief blips (<60ms) inside silence as silence
runs=[];i=0
while i<n:
    j=i
    while j<n and sil[j]==sil[i]: j+=1
    runs.append([sil[i],i,j]); i=j
for k in range(1,len(runs)-1):
    if not runs[k][0] and runs[k][2]-runs[k][1]<6 and runs[k-1][0] and runs[k+1][0]: runs[k][0]=True
merged=[]
for s,a,b in runs:
    if merged and merged[-1][0]==s: merged[-1][2]=b
    else: merged.append([s,a,b])
dur=n/100; cuts=[]
for s,a,b in merged:
    L=(b-a)/100
    if s and L>=minp and a>0 and b<n:
        cuts.append((a/100+keep/2, b/100-keep/2))
removed=sum(b-a for a,b in cuts)
lens=sorted([(b-a)/100 for s,a,b in merged if s and (b-a)/100>=minp])
print(f"pauses>= {minp}s: {len(cuts)}, removed {removed:.1f}s of {dur:.1f}s -> {dur-removed:.1f}s; longest {lens[-5:]}")
json.dump(cuts,open(sys.argv[5],'w'))
