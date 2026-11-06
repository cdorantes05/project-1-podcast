import json, re, sys, numpy as np
S=sys.argv[1]
W=json.load(open(S+'/words_list.json'))
norm=lambda t: re.sub(r"[^a-z0-9']","",t.lower())
toks=[norm(t) for _,_,t in W]
x=np.fromfile(S+'/tr16.raw',np.float32) if False else None
import subprocess
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',S+'/final_audio3.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
h=160;n=len(x)//h;db=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
def find(phrase, after):
    p=[norm(t) for t in phrase.split()]
    for i in range(len(toks)-len(p)+1):
        if W[i][0]>=after-1 and toks[i:i+len(p)]==p: return i
    raise SystemExit(f"not found: {phrase!r} after {after}")
def quiet(t0,t1):
    a=max(0,int(t0*100));b=min(n,int(t1*100))
    if b<=a: return t0
    return (a+int(np.argmin(db[a:b])))/100
# (start phrase, end phrase, approx start time, label)
K=json.load(open(S+'/keeps.json'))
out=[];tot=0;t=0
for s,e,approx,label in K:
    i=find(s,approx); j=find(e,W[i][0]); j=j+len(e.split())-1
    a=quiet(W[i][0]-0.35,W[i][0]+0.05); b=quiet(W[j][1]-0.05,W[j][1]+0.4)
    out.append((a,b,label)); tot+=b-a
    print(f"{a:7.2f}-{b:7.2f} ({b-a:5.1f}s) {label}: \"{' '.join(w[2] for w in W[i:j+1])[:150]}\"")
print(f"TOTAL {tot:.1f}s = {int(tot//60)}:{tot%60:04.1f}")
json.dump(out,open(S+'/keep_times.json','w'))
