"""20 s teaser: only Monsoor's entry, in slow motion, on his Gangster of Miami BGM. Built from the full story's rendered segments.
Run: /opt/miniconda3/bin/python -I qj_teaser_monsoor.py <dir with segNN.mp4 + labels.txt>  -> QJ-TEASER-MONSOOR-20s.mp4"""
import os, sys, subprocess
SD = sys.argv[1]; W, H, FPS, TOTAL = 1080, 1920, 24, 20.0
MU, VO, FX = 'audio/music/', '../voice/qj/', 'audio/designed/'
def run(c): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + c, check=True)
labs = [l.split(None, 1)[1].strip() for l in open(os.path.join(SD, 'labels.txt')) if l.strip()]
def seg(p): return os.path.join(SD, f'seg{[i for i, l in enumerate(labs) if l.startswith(p)][0]:02d}.mp4')
BLEND = 'minterpolate=fps=48:mi_mode=blend,fps=24'   # frame blending: natural motion blur, no warped guessed frames
CUTS = [  # (label, in, [(src from, src to, speed)...], out duration or None)
    ('YARD', 0.0, [(0.0, 1.5, 1.0)], 1.5),                              # the yard, next morning
    ('HELLCAT', 0.0, [(0.0, 2.0, 1.0), (2.0, 4.5, 0.55)], None),        # rolls in at real speed, ramps to 0.55x as he steps out
    ('FREEZE: MONSOOR', 0.0, [(0.0, 1.0, 1.0)], 2.8),                   # MONSOOR / BOSS freeze on the drop (held)
    ('CU MONSOOR', 0.0, [(0.0, 2.5, 1.0)], 2.5),                        # real speed: "Good job!" and his smile
    ('HERO', 0.0, [(0.0, 2.5, 1.0)], 2.5),                              # hero at the Hellcat (already a gentle slow-mo)
    ('BRAND', 0.0, [(0.0, 3.0, 1.0)], None)]
work = os.path.join(SD, 'tm'); os.makedirs(work, exist_ok=True); parts, at, t = [], {}, 0.0
for i, (lab, ip, ramp, d) in enumerate(CUTS):
    o = os.path.join(work, f'p{i}.mp4')
    if d is None and lab == 'BRAND': d = TOTAL - t
    if d is None: d = sum((b - a) / sp for a, b, sp in ramp)
    ch = ''.join(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp}{(',' + BLEND) if sp < 1 else ''}[r{k}];" for k, (a, b, sp) in enumerate(ramp))
    ch += ''.join(f'[r{k}]' for k in range(len(ramp))) + f'concat=n={len(ramp)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=5,trim=0:{d},setpts=PTS-STARTPTS,scale={W}:{H},fps={FPS}'
    run(['-i', seg(lab), '-an', '-filter_complex', ch, '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    parts.append(o); at[lab] = t; t += d
lst = os.path.join(work, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
vid = os.path.join(work, 'video.mp4'); run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid])
fz = at['FREEZE: MONSOOR']; drop = 0.635 + 16 * 60 / 92.3
EV = [('m', MU+'Monsoor-BGM-Gangster-of-Miami-v3.wav', fz - drop, -3, 0.0, None, 0.6, 0),          # filtered build under the slow arrival, drop on the BOSS freeze
      ('f', FX+'sub_rumble.wav', at['HELLCAT'], -3, 0, None, 0.3, 0),
      ('f', FX+'loafer_steps_brick.wav', at['HELLCAT'] + 2.0 + 0.98 / 0.55, 0, 0, None, 0, 0),        # his steps, slowed with the picture
      ('v', VO+'Monsoor-GoodJob-v4-smile-trim-norm.wav', at['CU MONSOOR'] + 0.57, 2, 0, None, 0, 0),
      ('f', FX+'door_slam_heavy.wav', fz - 0.03, 0, 0, None, 0, 0), ('f', FX+'sub_drop.wav', fz, -2, 0, None, 0, 0),
      ('f', FX+'sub_drop.wav', at['BRAND'], -5, 0, None, 0, 0)]
inp, flt, bus = [], [], {'m': [], 'f': [], 'v': []}
for k, (b, f, st, g, ip, d, fi, fo) in enumerate(EV):
    if st < 0: ip, st = ip - st, 0.0
    inp += ['-ss', f'{ip:.3f}', '-i', f]
    ch = f'[{k+1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB'
    if 'loafer' in f: ch += ',asetrate=48000*0.75,aresample=48000'   # slow-motion weight
    if fi: ch += f',afade=t=in:d={fi}'
    ch += f',adelay={int(st*1000)}|{int(st*1000)}[e{k}]'; flt.append(ch); bus[b].append(f'[e{k}]')
for b in bus: flt.append(''.join(bus[b]) + f'amix=inputs={len(bus[b])}:normalize=0:duration=longest[{b}b]')
flt.append('[vb]asplit=2[v1][vsc]'); flt.append('[mb][vsc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300:makeup=1[md]'); flt.append(f'[md][fb][v1]amix=inputs=3:normalize=0,atrim=0:{TOTAL},afade=t=out:st={TOTAL-0.6}:d=0.6,alimiter=limit=0.5:level=false,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.7:level=false[a]')
run(['-i', vid] + inp + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[a]', '-t', f'{TOTAL}', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', 'QJ-TEASER-MONSOOR-20s.mp4'])
for l in at: print(f'{at[l]:6.2f}  {l}')
