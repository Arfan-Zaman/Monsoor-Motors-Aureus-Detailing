"""Original instrumental music for the three reels, made locally with Stable Audio 3 (Stability AI
Community Licence: free commercial use under US$1M annual revenue). 0 credits.

    ~/local-ai/.venv/bin/python make_music.py [1] [2] [3]

Three seeds per reel; keeps the take whose tempo is closest to the reference's and whose beat is strongest."""
import os, sys, shutil
import numpy as np, librosa
from mlx_audio.music.utils import load_model
from mlx_audio.audio_io import write as audio_write
import mlx.core as mx

HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(os.path.dirname(HERE), "Audio", "music"); C = os.path.join(M, "candidates")
os.makedirs(C, exist_ok=True)
MODEL = os.path.expanduser("~/local-ai/models/stable-audio-3-mlx")
NEG = "vocals, singing, voice, speech, rap, lyrics, choir, low quality, distorted, muddy"
SPEC = {   # reel: (prompt, target BPM, seconds)  -- direction taken from each reference's audio
    "1": ("Dark aggressive trap instrumental, 117 BPM, heavy 808 sub bass, hard punchy kick and snappy snare, crisp hi-hats, "
          "tense dark synth stabs, cinematic hype product launch teaser, big drops, modern, clean mix, no vocals", 117, 24),
    "2": ("Calm minimal ambient instrumental, 94 BPM, soft felt piano melody, warm analog pads, light brushed drums, "
          "gentle and understated, premium brand film background, spacious, clean mix, no vocals", 94, 30),
    "3": ("Cinematic moody hip hop instrumental, 100 BPM, deep punchy boom bap drums, warm analog synth chords, sub bass, "
          "confident luxury car montage, starts strong on the first beat, clean mix, no vocals", 100, 16),
}
model = load_model(MODEL)
for reel in (sys.argv[1:] or list(SPEC)):
    prompt, bpm, secs = SPEC[reel]; best = None
    for seed in (11, 23, 37):
        res = list(model.generate(text=prompt, duration=secs, steps=8, seed=seed, cfg_scale=1.0, negative_prompt=NEG))
        a = res[0].audio if len(res) == 1 else mx.concatenate([r.audio for r in res], axis=0)
        out = os.path.join(C, f"m{reel}_seed{seed}.wav"); audio_write(out, a, res[0].sample_rate)
        y, sr = librosa.load(out, sr=22050); t, _ = librosa.beat.beat_track(y=y, sr=sr); t = float(np.atleast_1d(t)[0])
        err = min(abs(t - bpm), abs(t * 2 - bpm), abs(t / 2 - bpm)) / bpm
        punch = float(np.mean(librosa.onset.onset_strength(y=y, sr=sr)))
        score = punch * (1 - min(err * 4, 0.9))
        print(f"reel {reel} seed {seed}: tempo {t:.0f} (target {bpm}) punch {punch:.2f} score {score:.2f}", flush=True)
        if best is None or score > best[0]: best = (score, out)
    shutil.copyfile(best[1], os.path.join(M, f"m{reel}.wav")); print(f"reel {reel}: kept {os.path.basename(best[1])}", flush=True)
    js = os.path.join(M, f"m{reel}.wav.beats.json")
    if os.path.exists(js): os.remove(js)
