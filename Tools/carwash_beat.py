"""Synthesise a free 130 BPM drift-phonk style beat (no samples, no licences).

Structure in beats (1 beat = 60/130 s):
  0-4   intro: cowbell melody + hats + riser
  4-20  groove: kick, clap, hats, 808, cowbell
  20-24 build: snare roll + riser, no kick/808
  24-44 drop: full groove, heavier 808, 16th hats
  44-60 groove
  60    final hit, rings out over the end card (silence after)
Usage: python3 carwash_beat.py out.wav
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
BPM = 130
BEAT = 60 / BPM
STEP = BEAT / 4
TOTAL_BEATS = 64
N = int(TOTAL_BEATS * BEAT * SR) + SR
rng = np.random.default_rng(7)
out = np.zeros(N)


def t_(dur):
    return np.arange(int(dur * SR)) / SR


def place(sig, beat, gain=1.0):
    i = int(beat * BEAT * SR)
    j = min(N, i + len(sig))
    out[i:j] += sig[: j - i] * gain


def bp(sig, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), sig)


def hp(sig, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), sig)


def kick():
    t = t_(0.35)
    f = 45 + 110 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.5 * np.sin(ph) * np.exp(-t * 9))


def clap():
    t = t_(0.25)
    n = rng.standard_normal(len(t))
    env = np.exp(-t * 18)
    for d in (0.0, 0.012, 0.024):  # flam
        k = int(d * SR)
        env[k:k + 200] += 0.6
    return bp(n * env, 900, 5000) * 1.6


def snare(dur=0.15):
    t = t_(dur)
    n = rng.standard_normal(len(t))
    body = np.sin(2 * np.pi * 190 * t) * 0.4
    return bp(n, 1500, 8000) * np.exp(-t * 25) + body * np.exp(-t * 30)


def hat(open_=False):
    t = t_(0.18 if open_ else 0.05)
    n = rng.standard_normal(len(t))
    return hp(n, 7000) * np.exp(-t * (12 if open_ else 70)) * 0.5


def cowbell(semi):
    t = t_(0.28)
    r = 2 ** (semi / 12)
    sq = np.sign(np.sin(2 * np.pi * 540 * r * t)) + np.sign(np.sin(2 * np.pi * 800 * r * t))
    return bp(sq, 450 * r, 2600 * r) * np.exp(-t * 11) * 0.45


def bass808(freq, dur, drive=2.0):
    t = t_(dur)
    f = freq * (1 + 0.6 * np.exp(-t * 40))  # pitch punch
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1, t * 200) * np.exp(-t * 1.6)
    return np.tanh(drive * np.sin(ph) * env)


def riser(beats):
    t = t_(beats * BEAT)
    n = rng.standard_normal(len(t))
    sig = np.zeros_like(n)
    chunks = 32
    L = len(n) // chunks
    for c in range(chunks):
        lo = 300 + 6000 * (c / chunks) ** 2
        sig[c * L:(c + 1) * L] = bp(n[c * L:(c + 1) * L], lo, min(lo * 3, 18000))
    return sig * np.linspace(0, 0.5, len(t))


# F# minor; roots per bar (4 beats): F#, F#, D, E
ROOTS = [46.25, 46.25, 36.71, 41.20]
BELL = [[0, None, 0, None, 3, None, 0, None, 7, None, 5, None, 3, None, 0, None],
        [0, None, 0, None, 3, None, 5, None, 7, None, 10, None, 7, None, 5, 3]]


def bar(b0, kind):
    bar_i = int(b0 // 4)
    root = ROOTS[bar_i % 4]
    pat = BELL[bar_i % 2]
    for s in range(16):
        beat = b0 + s / 4
        if pat[s] is not None:
            place(cowbell(pat[s]), beat, 0.9 if kind != "intro" else 0.7)
        if kind == "intro":
            if s % 2 == 0:
                place(hat(), beat, 0.5)
            continue
        if kind == "build":
            continue
        if s in (0, 8, 11):
            place(kick(), beat, 1.0)
        if s in (4, 12):
            place(clap(), beat, 0.8)
        if kind == "drop":
            place(hat(open_=(s % 8 == 6)), beat, 0.6 if s % 2 == 0 else 0.35)
        elif s % 2 == 0:
            place(hat(), beat, 0.55)
    if kind in ("groove", "drop"):
        drive = 3.5 if kind == "drop" else 2.2
        g = 0.75 if kind == "drop" else 0.6
        place(bass808(root, 6 * STEP, drive), b0, g)
        place(bass808(root, 4 * STEP, drive), b0 + 1.5, g)
        place(bass808(root * (1.5 if bar_i % 2 else 1.335), 6 * STEP, drive), b0 + 2.5, g)


for b in range(0, 4, 4):
    bar(b, "intro")
place(riser(4), 0, 0.5)
for b in range(4, 20, 4):
    bar(b, "groove")
# build 20-24: cowbell carries, snare roll accelerates
bar(20, "build")
roll = [0, 1, 2, 2.5, 3, 3.25, 3.5, 3.625, 3.75, 3.875]
for k, r in enumerate(roll):
    place(snare(), 20 + r, 0.3 + 0.07 * k)
place(riser(4), 20, 0.8)
for b in range(24, 44, 4):
    bar(b, "drop")
for b in range(44, 60, 4):
    bar(b, "groove")
# final hit at beat 60, then let it ring
place(kick(), 60, 1.1)
place(clap(), 60, 0.9)
place(bass808(ROOTS[0], 1.8, 3.0), 60, 0.9)
place(cowbell(0), 60, 0.8)

end = int(TOTAL_BEATS * BEAT * SR)
out = out[:end]
fade = int(0.05 * SR)
out[-fade:] *= np.linspace(1, 0, fade)
out /= np.max(np.abs(out)) * 1.12
stereo = np.stack([out, out], axis=1)
wavfile.write(sys.argv[1], SR, (stereo * 32767).astype(np.int16))
print("seconds:", len(out) / SR)
