import json, re, sys, numpy as np, subprocess
S=sys.argv[1]
d=json.load(open(S+'/dtw.json'))['transcription']
W=[]
for s in d:
    for t in s['tokens']:
        txt=t['text']
        if txt.startswith('[_') or not txt.strip(): continue
        if txt.startswith(' ') or not W: W.append([t['t_dtw']/100,txt.strip()])
        else: W[-1][1]+=txt
norm=lambda t: re.sub(r"[^a-z0-9']","",t.lower())
toks=[norm(t) for _,t in W]
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',S+'/final_audio3.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
h=160;n=len(x)//h;db=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
dbs=np.convolve(db,np.ones(3)/3,'same')
import difflib
def find(phrase, after, limit=150):
    p=[norm(t) for t in phrase.split()]; L=len(p); best=(0,None)
    for i in range(len(toks)-L+1):
        if W[i][0]<after-6 or W[i][0]>after+limit: continue
        r=difflib.SequenceMatcher(None,toks[i:i+L],p).ratio()
        if r>best[0]+1e-9: best=(r,i)
    if best[0]<0.6: raise SystemExit(f"not found: {phrase!r} after {after} best {best}")
    return best[1]
def quiet(t0,t1):
    a=max(0,int(t0*100));b=min(n,int(t1*100))
    if b<=a+1: return (t0+t1)/2
    return (a+int(np.argmin(dbs[a:b])))/100
K=json.load(open(S+'/keeps.json'))
out=[]
for s,e,approx,label in K:
    i=find(s,approx,12); j=find(e,W[i][0]-5,120)
    sp=[norm(t) for t in s.split()]; ep=[norm(t) for t in e.split()]
    cand=[k for k in range(max(0,i-3),i+4) if toks[k]==sp[0]]
    if cand: i=min(cand,key=lambda k:abs(k-i))
    L=len(ep); cand=[k for k in range(j,j+L+4) if k<len(toks) and toks[k]==ep[-1]]
    j = cand[-1] if cand else j+L-1
    if W[j][0]<W[i][0]: raise SystemExit('order '+label); 
    a=quiet(max(W[i-1][0]+0.12, W[i][0]-1.2), W[i][0]+0.03) if i>0 else 0
    nxt=W[j+1][0] if j+1<len(W) else n/100
    b=quiet(W[j][0]+0.15, min(nxt+0.03, W[j][0]+2.0))
    out.append((a,b,label))
    print(f"{a:7.2f}-{b:7.2f} ({b-a:5.1f}s) {label}: {W[i][1]} {W[i+1][1]} ... {W[j-1][1]} {W[j][1]} | next: {W[j+1][1] if j+1<len(W) else ''}")
json.dump(out,open(S+'/keep_times.json','w'))
