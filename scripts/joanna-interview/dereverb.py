# Late-reverberation suppression (Lebart et al. style spectral subtraction).
# usage: dereverb.py in.wav(f32 mono 48k raw) out.raw T60 alpha floor_db
import numpy as np, sys
from scipy.signal import stft, istft
from scipy.ndimage import uniform_filter
inp,outp=sys.argv[1],sys.argv[2]; T60=float(sys.argv[3]); alpha=float(sys.argv[4]); floor=10**(float(sys.argv[5])/20)
sr=48000
x=np.fromfile(inp,np.float32).astype(np.float64)
nper=1536; hop=384                       # 32ms window, 8ms hop
out=np.zeros_like(x); chunk=sr*60; pad=sr*2
delta=3*np.log(10)/T60
Td=0.05; Nd=int(round(Td*sr/hop))       # late reverb starts ~50ms after direct sound
decay=np.exp(-2*delta*Td)
for st in range(0,len(x),chunk):
    a=max(0,st-pad); b=min(len(x),st+chunk+pad)
    f,t,Z=stft(x[a:b],sr,nperseg=nper,noverlap=nper-hop)
    P=np.abs(Z)**2
    # smoothed power (recursive, ~ 15ms)
    Ps=np.empty_like(P); Ps[:,0]=P[:,0]; g=0.5
    for k in range(1,P.shape[1]): Ps[:,k]=g*Ps[:,k-1]+(1-g)*P[:,k]
    Pr=np.zeros_like(Ps); Pr[:,Nd:]=decay*Ps[:,:-Nd]
    G=1-alpha*Pr/(Ps+1e-12)
    G=np.clip(G,floor**2,1.0); G=np.sqrt(G)  # power-domain gain -> magnitude gain
    G=uniform_filter(G,size=(3,3),mode='nearest')  # smooth to avoid musical noise
    G[f<120]=np.maximum(G[f<120],0.7)     # leave bass body mostly intact
    _,y=istft(Z*G,sr,nperseg=nper,noverlap=nper-hop)
    y=y[:b-a]
    s0=st-a; s1=s0+min(chunk,len(x)-st)
    out[st:st+(s1-s0)]=y[s0:s1]
out.astype(np.float32).tofile(outp)
