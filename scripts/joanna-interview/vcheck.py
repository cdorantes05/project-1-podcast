import re,subprocess,numpy as np,sys
S,src,out=sys.argv[1:4]
segs=[(float(a),float(b)) for a,b in re.findall(r'between\(t,([\d.]+),([\d.]+)\)',open(S+'/sel.txt').read())]
def grab(f,t):
    r=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.4f}','-i',f,'-frames:v','1','-vf','scale=160:90,format=gray','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(r,np.uint8).astype(float)
for ot in [300.0,700.0,1100.0,1230.0]:
    acc=0
    for a,b in segs:
        if ot<acc+(b-a): st=a+(ot-acc); break
        acc+=b-a
    o=grab(out,ot); fd=1001/30000
    errs={k:np.abs(o-grab(src,st+k*fd)).mean() for k in range(-4,5)}
    best=min(errs,key=errs.get)
    print(f'out {ot}s -> src {st:.2f}s: best match offset {best} frames (err {errs[best]:.2f}, at0 {errs[0]:.2f})')
