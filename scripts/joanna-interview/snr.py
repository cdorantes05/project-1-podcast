import numpy as np, sys, subprocess
for f in sys.argv[1:]:
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    h=160;n=len(x)//h;db=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
    sp=np.percentile(db,75)
    q=np.sort(db)
    print(f"{f.split('/')[-1]:18s} speech(p75) {sp:6.1f}  quietest 5% {np.percentile(db,2.5):6.1f}  10% {np.percentile(db,10):6.1f}  => background {sp-np.percentile(db,5):.0f} dB below voices")
