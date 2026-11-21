# Monsoor's BGM "Gangster of Miami" v3: his LOCKED laugh used as a Gen Z vocal-chop instrument on the beat.
# In : audio/music/Gangster-of-Miami-inst.mp3 (ElevenLabs Music job 9742203d, 92.3 BPM), ../voice/qj/Monsoor-Laugh-LOCKED.wav
# Out: audio/music/Monsoor-BGM-Gangster-of-Miami-v3.wav
import subprocess, numpy as np, wave
sr = 48000
def rd(f):
    return np.frombuffer(subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', f, '-ac', '2', '-ar', str(sr), '-f', 's16le', '-'],
                                        capture_output=True).stdout, '<i2').reshape(-1, 2) / 32768
m = rd('audio/music/Gangster-of-Miami-inst.mp3'); L = rd('../voice/qj/Monsoor-Laugh-LOCKED.wav')
n = len(m); t = np.arange(n) / sr
beat = 60 / 92.3; t0 = 0.635; bar = 4 * beat; s16 = beat / 4

def chop(a, d, fo=0.04):
    s = L[int(a * sr):int((a + d) * sr)].copy()
    k = int(0.005 * sr); s[:k] *= np.linspace(0, 1, k)[:, None]
    k = int(fo * sr); s[-k:] *= np.linspace(1, 0, k)[:, None]
    return s / (np.abs(s).max() + 1e-9)
def pitch(s, st):                       # tape-style pitch (changes length too, like a sampler)
    r = 2 ** (st / 12); idx = np.arange(0, len(s) - 1, r)
    return np.stack([np.interp(idx, np.arange(len(s)), s[:, c]) for c in (0, 1)], 1)
def tapestop(s):                        # slows to a stop: a Gen Z transition
    k = len(s); sp = np.linspace(1, 0.15, k); idx = np.cumsum(sp); idx = idx[idx < k - 1]
    return np.stack([np.interp(idx, np.arange(k), s[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0, len(idx))[:, None]

HA1, HA2, HA3 = chop(3.30, 0.22), chop(3.83, 0.22), chop(4.43, 0.26)   # three 'ha' syllables from the locked laugh
HA_LO = pitch(HA3, -5)                  # deep boss 'HA'
HA_HI = pitch(HA1, +4)                  # chipmunk-ish answer
ROLL = chop(3.30, 1.62)                 # the natural rolling 'ha ha ha ha'
GOOD = chop(5.35, 2.30, fo=0.12)        # 'Good... good.'
FULL = chop(0.05, 4.90, fo=0.2)

lay = np.zeros((n + sr * 3, 2)); duck = np.ones(n + sr * 3)
def put(s, at_beat, g, pan=0.0, d=0.6):
    at = int((t0 + at_beat * beat) * sr); s = s * g
    s = s * np.array([1 + pan, 1 - pan])
    lay[at:at + len(s)] += s; duck[at:at + len(s)] = np.minimum(duck[at:at + len(s)], d)

bars = int((n / sr - t0) / bar)
for b in range(bars):
    B = 4 * b
    if b in (0,):                                       # intro: one big deep HA
        put(HA_LO, B, 0.9, d=0.5); continue
    if b in (11,):                                      # 'Good... good.' bar
        put(GOOD, B, 0.85, d=0.45); continue
    if b in (14, 15) and b == 14:                       # full laugh rides two bars
        put(FULL, B, 0.75, d=0.5); continue
    if b == 15: continue
    # the groove: HA on 1, ha-ha 16ths on the and-of-2, deep HA on 3, answer on 4-and (panned)
    put(HA1, B + 0, 0.55)
    put(HA2, B + 1.5, 0.42, pan=-0.3); put(HA2, B + 1.75, 0.38, pan=0.3)
    put(HA_LO, B + 2, 0.6)
    put(HA_HI, B + 3.5, 0.35, pan=0.4 if b % 2 else -0.4)
    if b % 4 == 3:                                      # every 4th bar: 16th-note stutter roll + tape stop into the next bar
        for k in range(6): put(HA1[:int(0.09 * sr)], B + 2.5 + k * 0.25, 0.3 + 0.06 * k, pan=(-1) ** k * 0.25)
        put(tapestop(ROLL[:int(0.6 * sr)]), B + 3.95, 0.5)
    if b in (3, 7):                                     # rolling laugh fill before the drops
        put(ROLL, B + 2.0, 0.35, d=0.75)
# small 1/8 echo on the chop layer, alternate sides
k = int(beat / 2 * sr); base = lay.copy()
for i, g in ((1, 0.22), (2, 0.1)):
    sh = np.zeros_like(base); sh[k * i:] = base[:-k * i]; sh[:, i % 2] *= 0.5; lay += g * sh
lay = lay[:n]; duck = np.convolve(duck[:n], np.ones(1200) / 1200, 'same')
x = m * duck[:, None] + lay * 0.9

# dynamics: filtered intro opening into the drop at bar 5, riser + warm minor-9 pad, wider and louder lift at bar 13
cut = np.interp(t, [0, t0 + 4 * bar - 0.3, t0 + 4 * bar], [700, 4000, 20000]); a = 1 - np.exp(-2 * np.pi * cut / sr)
y = np.zeros_like(x)
for i in range(1, n): y[i] = y[i - 1] + a[i] * (x[i] - y[i - 1])
x = y; lift = t0 + 12 * bar
key = [110.0, 130.81, 164.81, 196.0, 246.94]
pad = sum(np.sin(2 * np.pi * f * t) * (0.6 if f < 150 else 0.35) for f in key) + 0.2 * sum(np.sin(4 * np.pi * f * t) for f in key)
pe = np.interp(t, [lift - bar, lift, n / sr - 2, n / sr], [0, 0.16, 0.16, 0])
ris = np.random.default_rng(3).standard_normal(n) * np.interp(t, [lift - 2 * bar, lift - 0.02, lift], [0, 0.1, 0])
x[:, 0] += pad * pe + ris; x[:, 1] += np.roll(pad, 240) * pe + np.roll(ris, 120)
g = np.interp(t, [0, t0 + 4 * bar, t0 + 4 * bar + 0.05, lift, lift + 0.05], [0.85, 0.9, 1.1, 1.0, 1.25]); x *= g[:, None]
mid = (x[:, 0] + x[:, 1]) / 2; side = (x[:, 0] - x[:, 1]) / 2 * np.interp(t, [lift - 0.1, lift], [1, 1.5]); x = np.stack([mid + side, mid - side], 1)
x /= np.abs(x).max() * 1.02
w = wave.open('audio/music/BGM-v3-tmp.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'audio/music/BGM-v3-tmp.wav', '-af',
                'bass=g=3:f=70,acompressor=threshold=0.12:ratio=3:attack=10:release=150:makeup=2,loudnorm=I=-10:TP=-1.0:LRA=8,alimiter=limit=0.89:level=false',
                '-ar', '48000', 'audio/music/Monsoor-BGM-Gangster-of-Miami-v3.wav'], check=True)
subprocess.run(['rm', 'audio/music/BGM-v3-tmp.wav'])
print('ok')
