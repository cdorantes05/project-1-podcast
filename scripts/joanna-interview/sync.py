import numpy as np, sys
sr=8000
v=np.fromfile(sys.argv[1],np.float32); a=np.fromfile(sys.argv[2],np.float32)
def env(x,hop=80):  # 100 Hz envelope
    n=len(x)//hop; e=np.abs(x[:n*hop]).reshape(n,hop).mean(1); e=e-e.mean(); return e/(e.std()+1e-9)
ev,ea=env(v),env(a)
N=1<<int(np.ceil(np.log2(len(ev)+len(ea))))
c=np.fft.irfft(np.fft.rfft(ev,N)*np.conj(np.fft.rfft(ea,N)),N)
lags=np.concatenate([np.arange(0,len(ev)),np.arange(-len(ea)+1,0)])
cc=np.concatenate([c[:len(ev)],c[N-len(ea)+1:]])
i=np.argmax(cc); lag=lags[i]
srt=np.sort(cc)[::-1]
print("offset_s",lag/100,"peak",cc[i]/min(len(ev),len(ea)),"2nd/peak",srt[50]/srt[0])
# check consistency at different segments
for start in [60,400,800,1100]:
    seg=ea[start*100:(start+60)*100]; best=None
    for L in range(int(lag)-300,int(lag)+301):
        p=start*100+L
        if p<0 or p+len(seg)>len(ev): continue
        r=np.dot(seg,ev[p:p+len(seg)]); 
        if best is None or r>best[0]: best=(r,L)
    print(start, best[1]/100)
