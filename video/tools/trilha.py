import numpy as np, soundfile as sf, json, subprocess, sys
D=sys.argv[1] if len(sys.argv) > 1 else "build/audio"; SR=44100; LEAD=0.4
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
# reconstruct sentence timings
pauses=[[0.7,0.6],[0.5,0.5,0.4,0.5,0.7],[0.5,0.5,0.5,0.6],[0.5,0.7],[0.4,0.5,0.7],[0.5,0.3,0.6,1.5]]
t=LEAD; n=0; scene_starts=[]; seg_starts=[]
for sc in pauses:
    scene_starts.append(t)
    for p in sc:
        seg_starts.append(t); t+=dur(f"{D}/seg{n:02d}.wav")+p; n+=1
total=t+1.0
timing={"scene_starts":scene_starts,"seg_starts":seg_starts,"total":total}
json.dump(timing,open(f"{D}/timing.json","w"),indent=1)
N=int(total*SR); tt=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N)
def lowpass(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/np.sqrt(1+(f/fc)**4); return np.fft.irfft(X,len(x))
def saw(freq,ph=0): return 2*((tt*freq+ph)%1)-1
rng=np.random.default_rng(7)
# 1) drone: A1 + E2 detuned saws, dark lowpass, slow swell
drone=sum(saw(f*d,rng.random()) for f in (55,82.41,110) for d in (0.997,1.003))
drone=lowpass(drone,180)
lfo=0.75+0.25*np.sin(2*np.pi*0.11*tt)
env=np.clip(tt/3,0,1)*np.clip((total-tt)/2.5,0,1)
drone*=lfo*env*0.10
# dissonant high string tension (Bb over A) that grows toward verdict
tension=lowpass(saw(116.54,0.3)+saw(233.08,0.6),900)*0.025*np.clip((tt-scene_starts[1])/(scene_starts[5]-scene_starts[1]),0,1)
L+=drone+tension; R+=drone*0.95+np.roll(tension,300)
# 2) heartbeat pulse (lub-dub) from scene 2 to verdict, accelerating
def thump(at,amp,f0=60):
    i=int(at*SR); n=int(0.35*SR)
    if i+n>N: return
    k=np.arange(n)/SR; s=np.sin(2*np.pi*(f0*k+ (f0*1.5)*(1-np.exp(-k*30))/30))*np.exp(-k*14)
    L[i:i+n]+=s*amp; R[i:i+n]+=s*amp
beat=scene_starts[1]
while beat<scene_starts[5]-0.2:
    prog=(beat-scene_starts[1])/(scene_starts[5]-scene_starts[1])
    thump(beat,0.32+0.2*prog); thump(beat+0.22,0.2+0.12*prog)
    beat+=0.95-0.35*prog
# 3) impacts (braam): sub drop + noise burst + reverb tail
ir_n=int(2.8*SR); ir=rng.standard_normal(ir_n)*np.exp(-np.arange(ir_n)/SR*2.2); ir/=np.abs(ir).sum()/40
def impact(at,amp=1.0):
    i=int(at*SR); n=int(3.2*SR)
    if i>=N: return
    n=min(n,N-i); k=np.arange(n)/SR
    sub=np.sin(2*np.pi*(38*k+ (110-38)*(1-np.exp(-k*6))/6))*np.exp(-k*1.6)
    br=lowpass((saw(55)[:n]+saw(55.4)[:n]+saw(82.6)[:n]),400)*np.exp(-k*1.2)*0.35
    nz=lowpass(rng.standard_normal(n),2500)*np.exp(-k*9)*0.5
    s=(sub*0.9+br+nz)*amp
    wet=np.fft.irfft(np.fft.rfft(s,2*n)*np.fft.rfft(ir,2*n),2*n)[:n]*0.12
    L[i:i+n]+=s+wet; R[i:i+n]+=s+np.roll(wet,700)
# 4) riser into the verdict scene
def riser(end,length):
    a=int((end-length)*SR); b=int(end*SR); n=b-a; k=np.arange(n)/n
    nz=rng.standard_normal(n); X=np.fft.rfft(nz); f=np.fft.rfftfreq(n,1/SR)
    nz=np.fft.irfft(X*(f>300)*(f<6000),n)
    ph=np.cumsum(2*np.pi*(200+800*k**2)/SR); tone=np.sin(ph)*0.15
    s=(nz*0.25+tone)*k**2.5
    L[a:b]+=s; R[a:b]+=s
for s in scene_starts[1:5]: impact(s-0.05,0.8)
impact(seg_starts[2*0+0] if False else seg_starts[9],0.7)   # "Ele votou não."
riser(scene_starts[5],3.0); impact(scene_starts[5],1.0)
fato=seg_starts[18]; riser(fato,1.6); impact(fato,1.2)        # "Fato."
impact(seg_starts[0],0.9)                                       # abertura
mix=np.stack([L,R],1); mix=np.tanh(mix*1.4)/np.tanh(1.4)
mix*=0.89/np.abs(mix).max()
sf.write(f"{D}/music.wav",mix,SR)
print(json.dumps(timing))
