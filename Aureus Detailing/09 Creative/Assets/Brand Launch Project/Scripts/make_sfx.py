"""Close-mic detailing sounds (ASMR) for the reels, made locally with Stable Audio 3. 0 credits.
    ~/local-ai/.venv/bin/python make_sfx.py"""
import os
import mlx.core as mx
from mlx_audio.music.utils import load_model
from mlx_audio.audio_io import write as audio_write

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), "Audio", "sfx"); os.makedirs(OUT, exist_ok=True)
NEG = "music, melody, drums, beat, vocals, speech, singing"
SFX = {
    "rinse": "close-up sound of a pressure washer spraying water onto a car panel, hiss and splatter, water running off, outdoor, no music",
    "foam": "foam cannon spraying thick snow foam onto a car, soft hiss and bubbling crackle of foam, close microphone, no music",
    "polish": "dual action car polisher motor humming and whirring on paint, steady electric buzz, close microphone, no music",
    "brush": "stiff wheel brush scrubbing a wet alloy wheel, bristle scratching, water dripping, close microphone, no music",
    "drips": "water droplets dripping off a car onto wet concrete, gentle trickle, quiet, close microphone, no music",
    "wipe": "microfibre towel wiping over glossy car paint, soft squeak and swish, close microphone, no music",
    "amb": "quiet Australian suburban morning ambience, magpies warbling in gum trees, distant birds, light breeze, no music",
    "roof": "open rooftop car park ambience at sunset, distant city hum, light wind, no music",
    "trolley": "small plastic wheels of a utility trolley rolling over brick paving, footsteps, close microphone, no music",
}
m = load_model(os.path.expanduser("~/local-ai/models/stable-audio-3-mlx"))
for name, prompt in SFX.items():
    r = list(m.generate(text=prompt, duration=8, steps=8, seed=7, negative_prompt=NEG))
    a = r[0].audio if len(r) == 1 else mx.concatenate([x.audio for x in r], axis=0)
    audio_write(os.path.join(OUT, f"{name}.wav"), a, r[0].sample_rate); print("ok", name, flush=True)
