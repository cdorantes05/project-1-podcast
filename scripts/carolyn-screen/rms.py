import wave, struct, math, sys
w=wave.open('audio.wav'); sr=w.getframerate()
for a,b in [(672.6,675.0)]:
    w.setpos(int(a*sr)); n=int((b-a)*sr); d=struct.unpack('<%dh'%n, w.readframes(n))
    step=sr//10; out=[]
    for i in range(0,n-step+1,step):
        c=d[i:i+step]; r=math.sqrt(sum(x*x for x in c)/len(c)) or 1
        out.append("%.1f:%d"%(a+i/sr, 20*math.log10(r/32768)))
    print(" ".join(out))
