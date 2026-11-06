# Smoother late-reverb suppression: gain smoothed in time (attack/release) and frequency, plus dry blend.
# usage: dereverb2.py in.raw out.raw T60 alpha floor_db dry_mix
import numpy as np, sys
from scipy.signal import stft, istft
from scipy.ndimage import uniform_filter1d
inp,outp=sys.argv[1],sys.argv[2]; T60=float(sys.argv[3]); alpha=float(sys.argv[4]); floor=10**(float(sys.argv[5])/20); dry=float(sys.argv[6])
sr=48000; x=np.fromfile(inp,np.float32).astype(np.float64)
nper=2048; hop=512                      # 43ms window, 10.7ms hop: fewer artifacts than shorter windows
out=np.zeros_like(x); chunk=sr*60; pad=sr*2
delta=3*np.log(10)/T60; Td=0.06; Nd=max(1,int(round(Td*sr/hop))); decay=np.exp(-2*delta*Nd*hop/sr)
flux=[]
for st in range(0,len(x),chunk):
    a=max(0,st-pad); b=min(len(x),st+chunk+pad)
    f,t,Z=stft(x[a:b],sr,nperseg=nper,noverlap=nper-hop)
    P=np.abs(Z)**2
    P=uniform_filter1d(P,5,axis=0)       # smooth power across neighbouring frequencies
    Ps=np.empty_like(P); Ps[:,0]=P[:,0]
    for k in range(1,P.shape[1]): Ps[:,k]=0.6*Ps[:,k-1]+0.4*P[:,k]
    Pr=np.zeros_like(Ps); Pr[:,Nd:]=decay*Ps[:,:-Nd]
    G=np.sqrt(np.clip(1-alpha*Pr/(Ps+1e-12),floor**2,1.0))
    # time smoothing: fast attack (gain rising = speech onset), slow release
    Gs=np.empty_like(G); Gs[:,0]=G[:,0]
    for k in range(1,G.shape[1]):
        up=G[:,k]>Gs[:,k-1]
        Gs[:,k]=np.where(up,0.3*Gs[:,k-1]+0.7*G[:,k],0.75*Gs[:,k-1]+0.25*G[:,k])
    Gs=uniform_filter1d(Gs,9,axis=0)     # wider frequency smoothing (~200 Hz)
    Gs[f<150]=np.maximum(Gs[f<150],0.8)
    flux.append(np.mean(np.abs(np.diff(20*np.log10(Gs[(f>300)&(f<5000)]+1e-6),axis=1))))
    _,y=istft(Z*Gs,sr,nperseg=nper,noverlap=nper-hop); y=y[:b-a]
    s0=st-a; n=min(chunk,len(x)-st); out[st:st+n]=y[s0:s0+n]
out=(1-dry)*out+dry*x
out.astype(np.float32).tofile(outp)
print(f"gain flicker {np.mean(flux):.2f} dB/frame")
