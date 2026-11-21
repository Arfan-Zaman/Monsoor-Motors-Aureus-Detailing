"""FINAL 45 s cut for "Queue Jump": Seedance film clips (clips/, pilot/) on the animatic timeline,
film LUT at partial strength, upscale to 1080x1920, game cards, freeze intros, full mix (-14 LUFS).
Run: /opt/miniconda3/bin/python -I qj45_final.py <work_dir>   -> writes QJ45-FINAL.mp4"""
import os, subprocess, sys
W, H, FPS = 1080, 1920, 24
work = sys.argv[1]; os.makedirs(work, exist_ok=True)
V = '../voice/qj/'; D = 'audio/designed/'
LUT = 'graphics/QJ_GTA_Perth_Film.cube'
def run(c): subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
C = 'clips/'; P = 'pilot/'
# GRADE: film LUT blended 45% over the source, then gentle grain; upscale with lanczos + light sharpen
GRADE = (f"scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,crop={W}:{H},unsharp=5:5:0.35,"
         f"split[o][g];[g]lut3d={LUT}[l];[o][l]blend=all_mode=normal:all_opacity=0.45,noise=alls=4:allf=t,fps={FPS}")
# (kind, a, b, label)
#  'c'      : a=(clip, in_point) ; b=(previs_a, previs_b) keeps the animatic's timing map, or a float duration
#  'flash'  : white frame for b seconds
#  'freeze' : a=(clip, time, card) ; b=duration
#  'card'   : a=(clip, time, card) over a dark blurred frame ; b=duration
#  's'      : still image a for b seconds (slow push)
SEG = [
 ('c', (C+'c01.mp4', 0.0), (0.00, 3.15), 'red lights montage'),
 ('c', (C+'c02.mp4', 0.0), (3.15, 3.65), 'GR86 launch (heard)'),
 ('flash', None, 0.20, 'speed camera FLASH'),
 ('c', (C+'c02.mp4', 0.85), 0.85, 'police lights in her mirror'),
 ('c', (C+'c02.mp4', 1.85), 0.80, 'pulled over: 0 km/h'),
 ('c', (C+'c02.mp4', 2.65), (4.50, 5.10), '"Ugh... oh, come ON!"'),
 ('card', (C+'c02.mp4', 3.4, 'graphics/Card-BUSTED-GTA.png'), 0.90, 'BUSTED'),
 ('card', (C+'c02.mp4', 3.4, 'graphics/Card-DEMERITS-GTA.png'), 1.10, 'FINE (blurred) / -3 DEMERIT POINTS'),
 ('c', (C+'c03.mp4', 0.0), (5.10, 6.45), 'Dave, servo: at the lights'),
 ('c', (C+'c04.mp4', 0.0), (6.45, 9.25), 'servo wide, Dave at pump 2'),
 ('c', (C+'c03.mp4', 2.6), (9.25, 9.75), 'Mia asleep'),
 ('c', (C+'c05.mp4', 0.0), (9.75, 10.55), 'silent C-HR glide, "Boss, just got the car. Coming."'),
 ('c', (C+'c05.mp4', 0.8), 0.80, 'DRIVING: Arfan hands-free, dog beside him'),
 ('c', (C+'c06.mp4', 0.2), 0.75, 'dog reveal, passenger seat: woof'),
 ('c', (C+'c07.mp4', 0.6), (11.35, 12.20), 'door, Arfan steps out'),
 ('freeze', (C+'c07.mp4', 1.4, 'graphics/Card-ARFAN-CEO-GTA.png'), 1.00, 'FREEZE: ARFAN / CEO'),
 ('c', (C+'c07.mp4', 1.6), (12.20, 13.65), '"What\'s up?"'),
 ('c', (C+'c08.mp4', 0.0), (13.65, 17.40), 'pump, POWER, READY'),
 ('c', (C+'c09.mp4', 1.0), (17.40, 19.60), 'Dave double take, "...you\'re kidding me"'),
 ('c', (C+'c10.mp4', 0.3), (19.60, 21.40), 'Mia: "Daaad... can we get one?"'),
 ('c', (C+'c11.mp4', 0.0), 1.00, 'NIGHT: Dave decides, Mia watching the phone'),
 ('c', (C+'c11.mp4', 2.3), 1.00, 'PHONE: thumb taps PRE-ORDER'),
 ('c', (C+'c12.mp4', 0.0), 0.80, 'next morning: yard, SOLD, AZ 007, logo flags'),
 ('c', (C+'c12.mp4', 1.2), (21.50, 24.30), 'SOLD tag, Hellcat arrives, Monsoor steps out'),
 ('freeze', (C+'c12.mp4', 4.85, 'graphics/Card-MONSOOR-BOSS-GTA.png'), 1.00, 'FREEZE: MONSOOR / BOSS'),
 ('c', (C+'c12.mp4', 4.6), (24.30, 24.70), 'Monsoor walks up to Arfan'),
 ('c', (P+'Pilot-Monsoor-GoodJob-crop.mp4', 0.25), 1.30, 'CU MONSOOR: "Good job!"'),
 ('c', (P+'Pilot-Arfan-MeansALot-crop.mp4', 0.65), 2.05, 'CU ARFAN: "That means a lot."'),
 ('c', (C+'c15.mp4', 0.0), (28.05, 32.85), 'delivery: keys to Dave, Mia runs out'),
 ('c', (C+'c16.mp4', 0.0), 1.95, 'HERO: Arfan + Monsoor + dog at the Hellcat, MISSION PASSED'),
 ('s', 'graphics/Brand-Card-1080.png', 1.70, 'brand card'),
]
files, t, marks = [], 0.0, []
for i, (k, a, b, lab_) in enumerate(SEG):
    o = os.path.join(work, f'seg{i:02d}.mp4')
    if k == 'c':
        f, ip = a; dur = (b[1] - b[0]) if isinstance(b, tuple) else b
        run(['ffmpeg', '-y', '-ss', str(ip), '-i', f, '-t', str(dur), '-an', '-filter_complex', f'[0:v]{GRADE}', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    elif k == 'flash':
        dur = b
        run(['ffmpeg', '-y', '-f', 'lavfi', '-i', f'color=white:s={W}x{H}:r={FPS}', '-t', str(dur), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    elif k == 's':
        dur = b; n = int(dur * FPS)
        vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
              f"zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}")
        run(['ffmpeg', '-y', '-loop', '1', '-i', a, '-t', str(dur), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    elif k == 'freeze':
        (f, ts, card), dur = a, b; n = int(dur * FPS)
        run(['ffmpeg', '-y', '-ss', str(ts), '-i', f, '-loop', '1', '-i', card, '-t', str(dur), '-filter_complex',
             f'[0:v]trim=end_frame=1,loop={n}:1:0,setpts=N/{FPS}/TB,{GRADE},eq=saturation=0.8:contrast=1.06[fz];'
             f"[fz]zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}[bg];"
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    else:  # card over a dark, blurred frame
        (f, ts, card), dur = a, b
        run(['ffmpeg', '-y', '-ss', str(ts), '-i', f, '-loop', '1', '-i', card, '-t', str(dur), '-filter_complex',
             f'[0:v]trim=end_frame=1,loop=999:1:0,setpts=N/{FPS}/TB,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=18,eq=brightness=-0.18:saturation=0.6[bg];'
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    files.append(o); marks.append((t, lab_, k, a)); t += dur
total = t
with open(os.path.join(work, 'list.txt'), 'w') as f:
    for o in files: f.write(f"file '{os.path.abspath(o)}'\n")
raw = os.path.join(work, 'raw.mp4'); vid = os.path.join(work, 'video.mp4')
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(work, 'list.txt'), '-c', 'copy', raw])

def lab(t): return next(m[0] for m in marks if m[1].startswith(t))
def src(t39):  # map a previs time to output time (segments that keep a previs range)
    for (st, l, k, a), s in zip(marks, SEG):
        if k == 'c' and isinstance(s[2], tuple) and s[2][0] <= t39 < s[2][1]: return st + (t39 - s[2][0])
    return None
a0, a1 = src(15.15), src(17.30)
# fuel super, scaled to full res; READY dash digits softened (odometer not legible-correct in the render)
run(['ffmpeg', '-y', '-i', raw, '-i', 'graphics/Super-HalfFuel-720.png', '-filter_complex',
     f"[1:v]scale={W}:{H}[sup];[0:v][sup]overlay=0:0:enable='between(t,{a0},{a1})'", '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', vid])

# GAME-STYLE OVERLAYS (graphics/make_gta_cards.py), each with its own sound below
OVL = [  # (png, start, duration)
 ('graphics/Stamp-PERTH.png', 0.25, 1.5),
 ('graphics/Tag-LAYLA.png', src(3.15), 0.5),
 ('graphics/Tag-DAVE.png', lab('Dave, servo')+0.1, 0.9),
 ('graphics/Stamp-SERVO.png', src(6.45), 1.0),
 ('graphics/HUD-CALL-BOSS.png', lab('silent C-HR')+0.05, 1.55),
 ('graphics/Pop-PUMP-ARFAN.png', src(13.65), 0.75),
 ('graphics/Pop-PUMP-DAVE.png', lab('Dave double')+0.3, 0.85),
 ('graphics/Stamp-YARD.png', lab('next morning')+0.05, 1.2),
 ('graphics/Pop-PREORDER.png', lab('PHONE')+0.50, 0.50),
 ('graphics/Anim-MISSION-PASSED.mov', lab('HERO')+0.02, 1.93),
]
vid2 = os.path.join(work, 'video2.mp4')
cmd = ['ffmpeg', '-y', '-i', vid]
fc, last = [], '0:v'
for n, (png, st, du) in enumerate(OVL):
    if png.endswith('.mov'):
        cmd += ['-t', str(du), '-i', png]
        fc.append(f'[{n+1}:v]scale={W}:{H},format=rgba,setpts=PTS+{st}/TB[o{n}]')
    else:
        cmd += ['-loop', '1', '-t', str(du), '-i', png]
        fc.append(f'[{n+1}:v]scale={W}:{H},format=rgba,fade=t=in:st=0:d=0.08:alpha=1,fade=t=out:st={du-0.15}:d=0.15:alpha=1,setpts=PTS+{st}/TB[o{n}]')
    fc.append(f'[{last}][o{n}]overlay=0:0:eof_action=pass[v{n}]'); last = f'v{n}'
run(cmd + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', vid2])
vid = vid2
MU, AM, VO, FX = 'audio/music/', 'audio/sfx/', V, D
# (bus, file, start, gain dB, src offset, duration or None, fade-in, fade-out)
B = [
 # MUSIC: one continuous bed, crossfaded, silent only for the 2.6 s silent-C-HR beat (ambience carries it)
 ('m', MU+'GenZ-A.mp3', 0.00, -8, 0, 8.60, 0, 0.6),
 ('m', MU+'GenZ-B.mp3', 8.30, -15, 0, 4.80, 0.3, 0.08),              # low servo groove, hard stop as the C-HR glides in
 ('m', MU+'GenZ-B.mp3', src(11.35), -10, 0, lab('NIGHT')-src(11.35)+0.15, 0, 0.4),             # groove slams in on the door
 ('m', MU+'Boss-Arrival.mp3', src(22.05)-0.05, -5, 0.25, 1.95, 0, 0.3),  # gangster cue hit 1: the Hellcat rolls in
 ('m', MU+'Boss-Arrival.mp3', lab('FREEZE: MONSOOR')-0.05, -5, 5.40, 2.30, 0.05, 0.6),  # gangster cue hit 2: MONSOOR / BOSS freeze
 ('m', FX+'warm_pad.wav', lab('CU MONSOOR')-0.2, -12, 0, None, 0, 0),                  # warm pad under Good job / That means a lot
 ('m', MU+'Delivery-GenZ.mp3', src(28.05)-0.4, -11, 0, lab('HERO')-src(28.05)+0.45, 0.4, 0.12),
 ('m', MU+'Mission-Passed-GenZ.mp3', lab('HERO')+0.03, -4, 0, 2.3, 0, 0.35),
 ('m', MU+'Delivery-GenZ.mp3', lab('brand')-0.05, -9, 8.6, None, 0.1, 0.5),
 # AMBIENCE
 ('a', AM+'Servo-Night-Ambience.mp3', 8.45, -6, 0, 12.0, 0.3, 0.6),
 ('a', AM+'Servo-Night-Ambience.mp3', 19.9, -8, 1.0, lab('NIGHT')-19.9+0.1, 0.6, 0.4),
 ('a', AM+'Yard-Morning-Ambience.mp3', lab('next morning')-0.2, -6, 0, 5.0, 0.3, 1.0),
 # VOICES
 ('v', VO+'Glam-ComeOn-norm.wav', lab('"Ugh')+0.05, 0, 0, None, 0, 0),
 ('v', VO+'Arfan-Boss-v3a-tight-norm.wav', lab('silent C-HR')+0.15, 0, 0, None, 0, 0),
 ('v', VO+'Arfan-WhatsUp-v4a-trim-norm.wav', src(12.30), 0, 0, None, 0, 0),
 ('v', VO+'Dave-KiddingMe-norm.wav', lab('Dave double')+0.4, 0, 0, None, 0, 0),
 ('v', VO+'Mia-v2-tight-norm.wav', lab('Mia:')+0.1, 0, 0, None, 0, 0),
 ('v', VO+'Monsoor-GoodJob-v4-smile-trim-norm.wav', lab('CU MONSOOR')+0.25, 1, 0, None, 0, 0),
 ('v', VO+'Arfan-MeansALot-LOCKEDcut-norm.wav', lab('CU ARFAN')+0.15, 1, 0, None, 0, 0),
 ('v', VO+'Arfan-YouChoose-LOCKEDcut-norm.wav', src(28.35), 0, 0, None, 0, 0),
 ('v', VO+'Arfan-WeBring-LOCKEDcut-norm.wav', src(29.45), 0, 0, None, 0, 0),
 ('f', AM+'Dog-Woof-Curious.wav', lab('dog reveal')+0.05, 1, 0, None, 0, 0),
 # sounds for the game overlays
 ('f', FX+'super_whoosh.wav', src(3.15)-0.05, -6, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', lab('Dave, servo')+0.05, -8, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', src(6.45)-0.05, -8, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', lab('silent C-HR')+0.05, -6, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', src(13.65), -4, 0, None, 0, 0), ('f', FX+'cha_ching.wav', src(13.70), -8, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', lab('Dave double')+0.3, -4, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', lab('next morning'), -6, 0, None, 0, 0),
 ('f', FX+'heartbeat.wav', lab('NIGHT')+0.75, -2, 0, None, 0, 0),
 ('m', FX+'tension_drone.wav', lab('NIGHT')+0.2, -14, 0, None, 0, 0),
 ('f', FX+'phone_tap.wav', lab('PHONE')+0.46, -4, 0, None, 0, 0),
 ('f', FX+'confirm_ding.wav', lab('PHONE')+0.50, -4, 0, None, 0, 0), ('f', FX+'popup_pop.wav', lab('PHONE')+0.50, -6, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', lab('HERO')-0.1, -6, 0, None, 0, 0),
 # SOUND ON EVERY ARRIVAL
 ('f', FX+'super_whoosh.wav', 0.10, -6, 0, None, 0, 0),
 ('f', FX+'camera_strobe.wav', lab('speed camera FLASH'), -2, 0, None, 0, 0),
 ('f', FX+'busted_slam.wav', lab('BUSTED')-0.35, 0, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', lab('FINE'), -2, 0, None, 0, 0),
 ('f', FX+'cha_ching.wav', lab('FINE')+0.08, -3, 0, None, 0, 0),
] + [('f', FX+'number_tick.wav', src(7.45)+k*0.07, -10, 0, None, 0, 0) for k in range(6)] + [
 ('f', FX+'freeze_riser.wav', lab('FREEZE: ARFAN')-0.6, -6, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', lab('FREEZE: ARFAN'), -2, 0, None, 0, 0), ('f', FX+'busted_slam.wav', lab('FREEZE: ARFAN')-0.35, -8, 0, None, 0, 0),
 ('f', FX+'ready_chime.wav', src(15.15), -4, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', src(15.15)-0.15, -8, 0, None, 0, 0),
 ('f', FX+'stamp_thud.wav', lab('SOLD tag')+0.1, -4, 0, None, 0, 0),
 ('f', FX+'freeze_riser.wav', lab('FREEZE: MONSOOR')-0.6, -6, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', lab('FREEZE: MONSOOR'), -2, 0, None, 0, 0), ('f', FX+'busted_slam.wav', lab('FREEZE: MONSOOR')-0.35, -8, 0, None, 0, 0),
 ('f', FX+'sonic_logo.wav', lab('brand')+0.1, -2, 0, None, 0, 0),
]
inp, flt, buses = [], [], {'m': [], 'a': [], 'v': [], 'f': []}
for j, (bus, f, st, g, off, dur, fi, fo) in enumerate(B):
    inp += ['-ss', str(off), '-i', f]
    ch = f'[{j+1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB'
    if dur: ch += f',atrim=0:{dur}'
    if fi: ch += f',afade=t=in:d={fi}'
    if fo and dur: ch += f',afade=t=out:st={max(dur-fo,0)}:d={fo}'
    ms = int(max(st, 0) * 1000); ch += f',adelay={ms}|{ms},apad=whole_dur={total}[x{j}]'
    flt.append(ch); buses[bus].append(f'[x{j}]')
def mixbus(k, n): return ''.join(buses[k]) + f'amix=inputs={len(buses[k])}:normalize=0:duration=longest[{n}]'
flt += [mixbus('m', 'mus'), mixbus('a', 'amb'), mixbus('v', 'vox'), mixbus('f', 'sfx'),
        '[vox]asplit=2[vox1][voxsc]',
        '[mus][voxsc]sidechaincompress=threshold=0.012:ratio=16:attack=10:release=300:makeup=1[mud]',   # music dips under every line
        f'[mud][amb][vox1][sfx]amix=inputs=4:normalize=0,atrim=0:{total},afade=t=out:st={total-0.5}:d=0.5,loudnorm=I=-14:TP=-1:LRA=11[m]']
run(['ffmpeg', '-y', '-i', vid] + inp + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[m]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', 'QJ45-FINAL.mp4'])
print(f'total {total:.2f}s')
for st, lab, k, a in marks: print(f'{st:6.2f}  {lab}')
