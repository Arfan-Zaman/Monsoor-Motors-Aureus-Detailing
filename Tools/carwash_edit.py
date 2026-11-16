"""Beat-cut the car wash reel at 130 BPM from Car wash/Shots, then add the beat.
Usage: python3 carwash_edit.py <beat.wav> <workdir>
Writes Car wash/Car-Wash-Reel.mp4 and Car wash/Car-Wash-Reel-No-Music.mp4
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/mdarfanuzzaman/Documents/Monsoor Motors/Car wash")
SHOTS = ROOT / "Shots"
FPS, BPM = 30, 130
GRADE = "eq=contrast=1.07:saturation=1.05:brightness=0.005,colortemperature=temperature=6200:mix=0.35"

# (shot prefix, beats, speed, punch-in zoom)
EDIT = [
    ("01", 4, 0.75, False),   # hook, slow-mo gloss
    ("02", 2, 1.0, False), ("03", 2, 1.0, True), ("04", 2, 1.0, False),
    ("05", 2, 1.0, True), ("06", 2, 1.0, False), ("07", 2, 1.0, True),
    ("08", 2, 1.0, False), ("09", 2, 1.0, True), ("10", 2, 1.0, False),
    ("11", 2, 1.0, True),     # process ends on beat 24 (the drop)
    ("12", 4, 0.67, True), ("13", 4, 0.67, False), ("14", 4, 0.67, True),
    ("15", 4, 0.67, False), ("16", 4, 0.67, True),   # reveal, slow-mo
    ("17", 6, 1.0, False), ("18", 4, 1.0, True), ("19", 6, 1.0, False),
    ("20", 4, 1.0, False),    # end card
]


def run(cmd):
    subprocess.run(cmd, check=True)


def main(beat_wav, work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    frame_per_beat = FPS * 60 / BPM
    cum, prev, parts = 0, 0, []
    for i, (pre, beats, speed, zoom) in enumerate(EDIT):
        cum += beats
        end = round(cum * frame_per_beat)
        frames, prev = end - prev, end
        src = next(SHOTS.glob(f"{pre}-*.mp4"))
        vf = [f"setpts=PTS/{speed}", f"fps={FPS}"]
        if zoom:  # slow push-in from 100% to 108% across the shot
            vf += ["scale=2160:3840:flags=lanczos",
                   f"zoompan=z='1+0.08*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                   f":d=1:s=1080x1920:fps={FPS}"]
        if pre != "20":
            vf.append(GRADE)
        vf.append("setsar=1,format=yuv420p")
        out = work / f"seg{i:02d}.mp4"
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src), "-vf", ",".join(vf),
             "-frames:v", str(frames), "-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
             "-r", str(FPS), str(out)])
        parts.append(out)
    (work / "list.txt").write_text("".join(f"file '{p}'\n" for p in parts))
    silent = ROOT / "Car-Wash-Reel-No-Music.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
         str(work / "list.txt"), "-c", "copy", "-movflags", "+faststart", str(silent)])
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(silent), "-i", beat_wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(ROOT / "Car-Wash-Reel.mp4")])
    print("frames total:", prev, "seconds:", prev / FPS)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
