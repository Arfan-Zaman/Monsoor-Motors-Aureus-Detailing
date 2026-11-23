"""20 s teaser: C-HR and Monsoor up front. Built only from the full-story's rendered (graded) segments, no new generations.
Run: /opt/miniconda3/bin/python -I qj_teaser.py <dir with segNN.mp4 + labels.txt from a qj_long.py render>  -> QJ-TEASER-20s.mp4"""
import os, sys, subprocess
SD = sys.argv[1]
W, H, FPS, TOTAL = 1080, 1920, 24, 20.0
MU, VO, FX, AM = 'audio/music/', '../voice/qj/', 'audio/designed/', 'audio/sfx/'
def run(c): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + c, check=True)

labs = [l.split(None, 1)[1].strip() for l in open(os.path.join(SD, 'labels.txt')) if l.strip()]
def seg(prefix): return os.path.join(SD, f'seg{[i for i, l in enumerate(labs) if l.startswith(prefix)][0]:02d}.mp4')

HB = 60 / 140 * 2   # half bar of the 140 BPM BGM
CUTS = [  # (label prefix, in-point inside the rendered segment, duration)
    ('PUMP Dave', 0.0, HB),            # the pain: Dave's big fill
    ('C-HR arrives', 0.0, 0.35),        # the C-HR on the road
    ('CALL DASH', 0.0, 0.5),
    ('ARRIVE', 0.3, 1.2),               # rolls in, Mia watching
    ('DOG woof', 0.0, HB),
    ('DOOR', 0.0, 1.0),                 # splash
    ('LEAN', 0.0, 0.5),
    ('FREEZE: ARFAN', 0.0, 1.75),       # GTA freeze, ARFAN / CEO
    ('WHATSUP', 0.35, 1.71),            # "What's up?"
    ('FILL', 0.4, HB),
    ('POWER, READY', 0.9, 1.1),         # C-HR READY
    ('HELLCAT', 1.8, 1.71),             # Monsoor arrives
    ('FREEZE: MONSOOR', 0.0, 1.0),      # MONSOOR / BOSS
    ('CU MONSOOR', 0.0, 1.71),          # "Good job!"
    ('HERO', 0.0, 1.71),
]
used = sum(d for _, _, d in CUTS); CUTS.append(('BRAND', 0.0, TOTAL - used))
work = os.path.join(SD, 'tz'); os.makedirs(work, exist_ok=True)
t, at, parts = 0.0, {}, []
for i, (lab, ip, d) in enumerate(CUTS):
    o = os.path.join(work, f'p{i:02d}.mp4')
    run(['-ss', f'{ip:.3f}', '-i', seg(lab), '-t', f'{d:.3f}', '-an', '-vf', f'fps={FPS},scale={W}:{H}', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    at[lab] = t; parts.append(o); t += d
lst = os.path.join(work, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
vid = os.path.join(work, 'video.mp4'); run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid])

A = at
# (bus, file, start, gain dB, in-point, duration or None, fade in, fade out)
EV = [('m', MU+'Arfan-MiamiDon-BGM.mp3', 0.0, -4, 0.0, A['HELLCAT'] + 0.05, 0.0, 0.25),                     # Arfan's beat until Monsoor arrives
      ('m', MU+'Monsoor-BGM-Gangster-of-Miami-v3.wav', A['HELLCAT'], -4, 0.635 + 16 * 60 / 92.3 - (A['FREEZE: MONSOOR'] - A['HELLCAT']), None, 0.2, 0),  # his drop lands on the BOSS freeze
      ('v', VO+'Arfan-WhatsUp-v4a-trim-norm.wav', A['WHATSUP'] + 0.45, 0, 0, None, 0, 0),
      ('v', VO+'Monsoor-GoodJob-v4-smile-trim-norm.wav', A['CU MONSOOR'] + 0.57, 1, 0, None, 0, 0),
      ('f', AM+'CHR-Arrive-Fast-Stop.mp3', A['ARRIVE'] - 0.6, -1, 0, None, 0, 0.3),
      ('f', FX+'sub_rumble.wav', A['ARRIVE'] + 1.0, -8, 0, 1.0, 0, 0.4),
      ('f', AM+'Dog-Woof-Curious.wav', A['DOG woof'] - 0.05, -2, 0, HB, 0, 0.15),
      ('f', FX+'stamp_thud.wav', A['DOOR'] + 0.2, -6, 0, None, 0, 0), ('f', FX+'slowmo_whoomp.wav', A['DOOR'] + 0.2, -5, 0, None, 0, 0),
      ('f', FX+'door_slam_heavy.wav', A['FREEZE: ARFAN'] - 0.03, 0, 0, None, 0, 0), ('f', FX+'sub_drop.wav', A['FREEZE: ARFAN'], -3, 0, None, 0, 0),
      ('f', FX+'fuel_clickoff.wav', A['FILL'] + 0.2, -3, 0, None, 0, 0),
      ('f', FX+'phone_tap.wav', A['POWER, READY'], -5, 0, None, 0, 0), ('f', FX+'ready_chime.wav', A['POWER, READY'] + 0.2, -4, 0, None, 0, 0),
      ('f', FX+'sub_rumble.wav', A['HELLCAT'], -4, 0, None, 0, 0), ('f', FX+'loafer_steps_brick.wav', A['HELLCAT'] + 1.18, -1, 0, None, 0, 0),
      ('f', FX+'door_slam_heavy.wav', A['FREEZE: MONSOOR'] - 0.03, 0, 0, None, 0, 0), ('f', FX+'sub_drop.wav', A['FREEZE: MONSOOR'], -3, 0, None, 0, 0),
      ('f', FX+'sub_drop.wav', A['HERO'], -5, 0, None, 0, 0)]
inp, flt, bus = [], [], {'m': [], 'v': [], 'f': []}
for k, (b, f, st, gdb, ip, d, fi, fo) in enumerate(EV):
    inp += ['-ss', f'{ip:.3f}'] + (['-t', f'{d:.3f}'] if d else []) + ['-i', f]
    chain = f'[{k+1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gdb}dB'
    if fi: chain += f',afade=t=in:d={fi}'
    if fo and d: chain += f',afade=t=out:st={max(d - fo, 0):.3f}:d={fo}'
    chain += f',adelay={int(st * 1000)}|{int(st * 1000)}[e{k}]'
    flt.append(chain); bus[b].append(f'[e{k}]')
for b in bus: flt.append(''.join(bus[b]) + f'amix=inputs={len(bus[b])}:normalize=0:duration=longest[{b}b]')
flt += ['[vb]asplit=2[v1][vsc]', '[mb][vsc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300:makeup=1[md]',
        f'[md][v1][fb]amix=inputs=3:normalize=0,atrim=0:{TOTAL},afade=t=out:st={TOTAL-0.5}:d=0.5,alimiter=limit=0.5:level=false,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.7:level=false[a]']
run(['-i', vid] + inp + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[a]', '-t', f'{TOTAL}', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', 'QJ-TEASER-20s.mp4'])
for lab in at: print(f'{at[lab]:6.2f}  {lab}')
