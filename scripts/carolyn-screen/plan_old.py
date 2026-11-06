import re, json
keep=[(272.9,274.1),(289.3,988.6)]
cuts=[(374.2,384.5,"big job / first job repeat"),(674.5,696.5,"habit false starts"),(721.7,733.2,"snow & other park detail"),(583.4,590.2,"mole description"),(856.6,875.4,"'kinda hard... hmm' stall"),(925.5,931.2,"'it really taught me that, hmm' restart")]
segs=[]
for a,b in keep:
    cur=[(a,b)]
    for c0,c1,_ in cuts:
        nxt=[]
        for x,y in cur:
            if c1<=x or c0>=y: nxt.append((x,y))
            else:
                if c0>x: nxt.append((x,c0))
                if c1<y: nxt.append((c1,y))
        cur=nxt
    segs+=cur
sil=[tuple(map(float,re.match(r'([\d.]+)-([\d.]+)',l).groups())) for l in open('sil.txt')]
PAD=0.2
out=[]
for x,y in sorted(segs):
    s=x
    for p,q in sil:
        if q-p>0.75 and p>x+0.3 and q<y-0.3:
            out.append((s,p+PAD)); s=q-PAD
    out.append((s,y))
out=[(round(a,3),round(b,3)) for a,b in out if b-a>0.05]
tot=sum(b-a for a,b in out)
print(len(out),"segments, total %.1fs = %d:%02d"%(tot,tot//60,tot%60))
json.dump(out,open('old.json','w'))
