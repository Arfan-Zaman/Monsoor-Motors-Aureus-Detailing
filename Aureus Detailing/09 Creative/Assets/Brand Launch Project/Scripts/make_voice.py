"""Voice for the brand launch reels: one designed voice, cloned for every line so it never drifts. Free, local.

Voice design prompt (Qwen3-TTS VoiceDesign) is in BRIEF.md; the chosen take is audio/voice/voice-ref.wav.
    ~/local-ai/.venv/bin/python make_voice.py
"""
import os, re, subprocess, sys
import numpy as np, soundfile as sf
from mlx_audio.tts.utils import load_model

HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(os.path.dirname(HERE), "Audio", os.environ.get("AUREUS_VOICE_DIR", "voice"))
REF = os.path.join(V, "voice-ref.wav")
REF_TEXT = os.environ.get("AUREUS_REF_TEXT", "We come to you. Every panel, every spoke, by hand. Done properly, or it's not done.")
LINES_V1 = {
    "r1_ready": "Perth. You ready?",
    "r2_01": "We come to you.",
    "r2_02": "Most places rush it.",
    "r2_03": "Shiny today. Swirls tomorrow.",
    "r2_04": "Not here.",
    "r2_05": "At Aureus, it's foam first,",
    "r2_06": "machine polish,",
    "r2_07": "then wax, by hand.",
    "r2_08": "Every spoke.",
    "r2_09": "By hand.",
    "r2_10": "Steam for the leather.",
    "r2_11": "Done properly, or it's not done.",
    "r2_12": "Gold Detail. One ninety-nine. We come to you.",
}
LINES_V2 = {   # "Done properly" v2 (G-Wagon), old-Aussie Voice 3
    "b2_01": "We come to you, mate.",
    "b2_02": "Pink foam first.",
    "b2_03": "Lifts the grit before I touch the paint.",
    "b2_04": "Most places rush it.",
    "b2_05": "Not at Aureus.",
    "b2_06": "Machine polish. Wax, by hand.",
    "b2_07": "Every spoke.",
    "b2_08": "Done properly, or it's not done.",
    "b2_09": "Gold Detail. From one ninety-nine. We come to you.",
    "b2_10": "Then rinse it clean.",
    "b2_11": "Inside, steam for the leather.",
    "b2_12": "Gold Detail for your four-wheel drive. Two nineteen. We come to you.",
}
LINES = LINES_V2 if os.environ.get("AUREUS_VOICE_DIR") == "voice-v2" else LINES_V1
WHISPER = os.path.expanduser("~/.cache/whisper.cpp/ggml-base.en.bin")
norm = lambda s: re.sub(r"[^a-z ]", "", s.lower().replace("199", "one ninety nine").replace("-", " ")).split()

def heard(wav):
    t = wav + ".16k.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-ac", "1", "-ar", "16000", t], check=True)
    o = subprocess.run(["whisper-cli", "-m", WHISPER, "-f", t, "-nt"], capture_output=True, text=True).stdout; os.remove(t); return o.strip()

m = load_model("mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16")
only = sys.argv[1:]
for name, text in LINES.items():
    if only and name not in only: continue
    out = os.path.join(V, f"{name}.wav"); best = None
    for take in range(3):
        r = list(m.generate(text=text, ref_audio=REF, ref_text=REF_TEXT))
        a = np.concatenate([np.array(x.audio) for x in r]); sf.write(out, a, r[0].sample_rate)
        h = heard(out); want, got = norm(text), norm(h)
        score = len(set(want) & set(got)) / max(1, len(set(want)))
        print(f"{name} take {take}: {len(a)/r[0].sample_rate:.2f}s heard: {h!r} match {score:.2f}", flush=True)
        if best is None or score > best[0]: best = (score, a.copy(), r[0].sample_rate)
        if score >= 0.99: break
    sf.write(out, best[1], best[2])
