"""30 s paid-ad cut of "Queue Jump", built ONLY from what we already have (0 credits):
the saved Seedance film clips (clips/, pilot/) + our generated Higgsfield photos (elements/),
used as real shots: Perth aerial, the real-number dashes, pump screen, pre-order phone, yard.
Run: /opt/miniconda3/bin/python -I qj30_final.py <work_dir>   -> writes QJ30-FINAL.mp4"""
import os, subprocess, sys
W, H, FPS = 1080, 1920, 24
work = sys.argv[1]; os.makedirs(work, exist_ok=True)
V = '../voice/qj/'; D = 'audio/designed/'
LUT = 'graphics/QJ_GTA_Perth_Film.cube'
def run(c):
    if c[0] == 'ffmpeg': c = ['ffmpeg', '-nostdin'] + c[1:]
    subprocess.run(c, check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
C, P, E = 'clips/', 'pilot/', 'elements/'
GRADE = (f"scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,crop={W}:{H},unsharp=5:5:0.35,"
         f"split[o][g];[g]lut3d={LUT}[l];[o][l]blend=all_mode=normal:all_opacity=0.45,noise=alls=4:allf=t,fps={FPS}")
# kinds: 'c' film clip (file, in) dur | 'i' photo (file, centre_x, centre_y, zoom, drift_x) dur
#        'flash' | 'freeze' (clip, time, card) dur | 'card' (clip, time, card) dur | 's' full still dur
SEG = [
 ('i', (E+'gta/GTA-Perth-Aerial.png', 0.40, 0.5, 1.0, 0.07), 0.60, 'OPEN: Perth aerial'),
 ('c', (C+'c01.mp4', 0.0), 1.00, 'red light: X-Trail, gum bubble'),
 ('i', (E+'dash/Dash-XTrail.png', 0.49, 0.47, 1.5, 0.0), 0.45, 'DASH X-Trail 10.8'),
 ('c', (C+'c01.mp4', 1.5), 0.50, 'red light: woman'),
 ('i', (E+'dash/Dash-Sportage.png', 0.50, 0.44, 1.5, 0.0), 0.40, 'DASH Sportage 10.5'),
 ('c', (C+'c01.mp4', 2.3), 0.50, 'red light: retiree'),
 ('i', (E+'dash/Dash-Outlander.png', 0.51, 0.46, 1.5, 0.0), 0.40, 'DASH Outlander 9.5'),
 ('c', (C+'c02.mp4', 0.0), 0.50, 'GR86 launch (heard)'),
 ('flash', None, 0.20, 'speed camera FLASH'),
 ('c', (C+'c02.mp4', 0.85), 0.40, 'police lights in her mirror'),
 ('i', (E+'dash/Dash-GR86-PulledOver.png', 0.455, 0.52, 1.2, 0.0), 0.50, 'DASH GR86 pulled over, 18,645'),
 ('c', (C+'c02.mp4', 2.75), 0.50, '"Ugh... oh, come ON!"'),
 ('card', (C+'c02.mp4', 3.4, 'graphics/Card-BUSTED-GTA.png'), 0.50, 'BUSTED'),
 ('card', (C+'c02.mp4', 3.4, 'graphics/Card-DEMERITS-GTA.png'), 0.50, 'FINE (blurred) / -3 DEMERIT POINTS'),
 ('c', (C+'c03.mp4', 0.3), 0.70, 'Dave at the lights, Mia asleep'),
 ('i', (E+'dash/Dash-Tucson.png', 0.49, 0.47, 1.4, 0.0), 0.45, 'DASH Tucson 10.1'),
 ('c', (C+'c04.mp4', 0.0), 0.70, 'servo wide, Dave at pump 2'),
 ('c', (C+'c05.mp4', 0.0), 0.80, 'silent C-HR glide'),
 ('c', (C+'c05.mp4', 0.9), 0.60, 'DRIVING: Arfan hands-free'),
 ('c', (C+'c06.mp4', 0.2), 0.50, 'dog reveal: woof'),
 ('c', (C+'c07.mp4', 0.5), 0.50, 'door, Arfan steps out'),
 ('freeze', (C+'c07.mp4', 1.4, 'graphics/Card-ARFAN-CEO-GTA.png'), 0.70, 'FREEZE: ARFAN / CEO'),
 ('c', (C+'c07.mp4', 1.7), 0.90, '"What\'s up?"'),
 ('c', (C+'c08.mp4', 0.0), 0.70, 'pump 1 stops at $36.20'),
 ('c', (C+'c08.mp4', 0.8), 0.60, 'POWER press, Seiko'),
 ('c', (C+'c08.mp4', 1.6), 0.90, 'READY'),
 ('c', (C+'c09.mp4', 1.0), 1.20, 'Dave double take, "...you\'re kidding me"'),
 ('i', (E+'dash/Pump-Dave.png', 0.34, 0.47, 1.25, 0.0), 0.50, 'PUMP Dave $94.99'),
 ('c', (C+'c10.mp4', 0.3), 1.70, 'Mia: "Daaad... can we get one?"'),
 ('c', (C+'c11.mp4', 0.2), 0.60, 'NIGHT: Dave decides, Mia watching'),
 ('i', (E+'props/Phone-PreOrder-CHR.png', 0.5, 0.47, 1.05, 0.0), 0.70, 'PHONE: PRE-ORDER, 23:41'),
 ('i', (E+'gta/Yard-Final-AZ007.png', 0.47, 0.5, 1.0, 0.03), 0.60, 'YARD: next morning, SOLD, AZ 007'),
 ('c', (C+'c12.mp4', 1.9), 1.30, 'Hellcat arrives'),
 ('freeze', (C+'c12.mp4', 4.85, 'graphics/Card-MONSOOR-BOSS-GTA.png'), 0.70, 'FREEZE: MONSOOR / BOSS'),
 ('c', (P+'Pilot-Monsoor-GoodJob-crop.mp4', 0.25), 1.00, 'CU MONSOOR: "Good job!"'),
 ('c', (P+'Pilot-Arfan-MeansALot-crop.mp4', 0.65), 1.80, 'CU ARFAN: "That means a lot."'),
 ('c', (C+'c15.mp4', 0.8), 1.20, 'DELIVERY: key handover'),
 ('c', (C+'c15.mp4', 3.6), 0.80, 'handshake, Mia runs in'),
 ('c', (C+'c16.mp4', 0.0), 1.50, 'HERO: Arfan + Monsoor + dog, MISSION PASSED'),
 ('s', 'graphics/Brand-Card-1080.png', 1.40, 'brand card'),
]
def probe(f):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])
files, t, marks = [], 0.0, []
for i, (k, a, b, lab_) in enumerate(SEG):
    o = os.path.join(work, f'seg{i:02d}.mp4'); dur = b
    if os.environ.get('REUSE') and os.path.exists(o) and os.path.getsize(o) > 1000:
        pass   # segment already rendered in this work dir
    elif k == 'c':
        f, ip = a
        run(['ffmpeg', '-y', '-ss', str(ip), '-i', f, '-t', str(dur), '-an', '-filter_complex', f'[0:v]{GRADE}', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    elif k == 'i':   # photo as a shot: 9:16 window on the detail, slow drift like a handheld reframe, light grain
        f, cx, cy, zoom, dx = a; iw, ih = probe(f)
        ch = min(ih / zoom, iw * 16 / 9 / zoom); cw = ch * 9 / 16
        x0 = min(max(cx * iw - cw / 2, 0), iw - cw); y0 = min(max(cy * ih - ch / 2, 0), ih - ch)
        drift = (dx * iw) if dx else cw * 0.03
        x0 = min(x0, iw - cw - drift) if x0 + cw + drift > iw else x0
        vf = (f"crop={int(cw)}:{int(ch)}:'{x0:.1f}+{drift:.1f}*t/{dur}':'{y0:.1f}',scale={W}:{H}:flags=lanczos,unsharp=5:5:0.3,noise=alls=4:allf=t,fps={FPS}")
        run(['ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-i', f, '-t', str(dur), '-vf', vf, '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    elif k == 'flash':
        run(['ffmpeg', '-y', '-f', 'lavfi', '-i', f'color=white:s={W}x{H}:r={FPS}', '-t', str(dur), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    elif k == 's':
        n = int(dur * FPS)
        vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
              f"zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}")
        run(['ffmpeg', '-y', '-loop', '1', '-i', a, '-t', str(dur), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    elif k == 'freeze':
        (f, ts, card) = a; n = int(dur * FPS)
        run(['ffmpeg', '-y', '-ss', str(ts), '-i', f, '-loop', '1', '-i', card, '-t', str(dur), '-filter_complex',
             f'[0:v]trim=end_frame=1,loop={n}:1:0,setpts=N/{FPS}/TB,{GRADE},eq=saturation=0.8:contrast=1.06[fz];'
             f"[fz]zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}[bg];"
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    else:
        (f, ts, card) = a
        run(['ffmpeg', '-y', '-ss', str(ts), '-i', f, '-loop', '1', '-i', card, '-t', str(dur), '-filter_complex',
             f'[0:v]trim=end_frame=1,loop=999:1:0,setpts=N/{FPS}/TB,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=18,eq=brightness=-0.18:saturation=0.6[bg];'
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    files.append(o); marks.append((t, lab_)); t += dur
total = t
with open(os.path.join(work, 'list.txt'), 'w') as f:
    for o in files: f.write(f"file '{os.path.abspath(o)}'\n")
vid = os.path.join(work, 'video.mp4')
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(work, 'list.txt'), '-c', 'copy', vid])
def lab(s): return next(m[0] for m in marks if m[1].startswith(s))

OVL = [  # (file, start, duration): game-style overlays, each with its own sound below
 ('graphics/Stamp-PERTH.png', 0.05, 1.2),
 ('graphics/Tag-LAYLA.png', lab('GR86 launch'), 0.5),
 ('graphics/Tag-DAVE.png', lab('Dave at the lights')+0.05, 0.65),
 ('graphics/Stamp-SERVO.png', lab('servo wide'), 0.7),
 ('graphics/HUD-CALL-BOSS.png', lab('silent C-HR')+0.05, 1.3),
 ('graphics/Pop-PUMP-ARFAN.png', lab('pump 1 stops'), 0.7),
 ('graphics/Super-HalfFuel-720.png', lab('READY'), 0.9),
 ('graphics/Stamp-YARD.png', lab('YARD')+0.03, 0.9),
 ('graphics/Pop-PREORDER.png', lab('PHONE')+0.35, 0.35),
 ('graphics/Anim-MISSION-PASSED.mov', lab('HERO')+0.02, 1.48),
]
vid2 = os.path.join(work, 'video2.mp4')
cmd = ['ffmpeg', '-y', '-i', vid]; fc, last = [], '0:v'
for n, (png, st, du) in enumerate(OVL):
    if png.endswith('.mov'):   # animation: offset at the input, passes through after it ends
        cmd += ['-itsoffset', f'{st:.3f}', '-t', str(du), '-i', png]
        fc.append(f'[{n+1}:v]scale={W}:{H},format=rgba[o{n}]')
        fc.append(f"[{last}][o{n}]overlay=0:0:eof_action=pass:enable='between(t,{st:.3f},{st+du:.3f})'[v{n}]")
    else:                      # card: looped over the whole timeline, faded in/out at its moment
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{total:.3f}', '-i', png]
        fc.append(f'[{n+1}:v]scale={W}:{H},format=rgba,fade=t=in:st={st:.3f}:d=0.08:alpha=1,fade=t=out:st={st+du-0.15:.3f}:d=0.15:alpha=1[o{n}]')
        fc.append(f"[{last}][o{n}]overlay=0:0:enable='between(t,{st:.3f},{st+du:.3f})'[v{n}]")
    last = f'v{n}'
run(cmd + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', vid2])

MU, AM, VO, FX = 'audio/music/', 'audio/sfx/', V, D
dv, gl, door, night, yard = lab('Dave at the lights'), lab('silent C-HR'), lab('door'), lab('NIGHT'), lab('YARD')
hc, deliv, hero, brand = lab('Hellcat'), lab('DELIVERY'), lab('HERO'), lab('brand')
# (bus, file, start, gain dB, src offset, duration or None, fade-in, fade-out)
B = [
 ('m', MU+'GenZ-A.mp3', 0.00, -8, 0, dv+0.4, 0, 0.5),
 ('m', MU+'GenZ-B.mp3', dv+0.1, -15, 0, gl-dv-0.1, 0.3, 0.08),            # low servo groove, hard stop for the silent C-HR
 ('m', MU+'GenZ-B.mp3', door, -10, 0, night-door+0.15, 0, 0.4),           # groove slams in on the door
 ('m', FX+'tension_drone.wav', night+0.05, -14, 0, yard-night, 0, 0.2),
 ('m', MU+'Boss-Arrival.mp3', hc-0.05, -5, 0.25, 1.45, 0, 0.25),          # gangster hit 1: the Hellcat
 ('m', MU+'Boss-Arrival.mp3', lab('FREEZE: MONSOOR')-0.05, -5, 5.40, 1.7, 0.05, 0.5),
 ('m', FX+'warm_pad.wav', lab('CU MONSOOR')-0.2, -12, 0, 3.2, 0, 0.6),
 ('m', MU+'Delivery-GenZ.mp3', deliv-0.3, -11, 0, hero-deliv+0.35, 0.3, 0.12),
 ('m', MU+'Mission-Passed-GenZ.mp3', hero+0.03, -4, 0, 1.9, 0, 0.3),
 ('m', MU+'Delivery-GenZ.mp3', brand-0.05, -9, 8.6, None, 0.1, 0.5),
 ('a', AM+'Servo-Night-Ambience.mp3', dv, -6, 0, night-dv+0.1, 0.3, 0.4),
 ('a', AM+'Yard-Morning-Ambience.mp3', yard-0.1, -6, 0, 4.2, 0.2, 0.8),
 ('v', VO+'Glam-ComeOn-norm.wav', lab('"Ugh')+0.02, 0, 0, None, 0, 0),
 ('v', VO+'Arfan-Boss-v3a-tight-norm.wav', gl+0.05, 0, 0, None, 0, 0),
 ('v', VO+'Arfan-WhatsUp-v4a-trim-norm.wav', lab('"What')+0.08, 0, 0, None, 0, 0),
 ('v', VO+'Dave-KiddingMe-norm.wav', lab('Dave double')+0.25, 0, 0, None, 0, 0),
 ('v', VO+'Mia-v2-tight-norm.wav', lab('Mia:')+0.02, 0, 0, None, 0, 0),
 ('v', VO+'Monsoor-GoodJob-v4-smile-trim-norm.wav', lab('CU MONSOOR')+0.2, 1, 0, None, 0, 0),
 ('v', VO+'Arfan-MeansALot-LOCKEDcut-norm.wav', lab('CU ARFAN')+0.1, 1, 0, None, 0, 0),
 ('v', VO+'Arfan-YouChoose-LOCKEDcut-norm.wav', deliv+0.05, 0, 0, None, 0, 0),
 ('v', VO+'Arfan-WeBring-LOCKEDcut-norm.wav', deliv+1.0, 0, 0, None, 0, 0),
 ('f', AM+'Dog-Woof-Curious.wav', lab('dog reveal')+0.05, 1, 0, 1.3, 0, 0.3),
 ('f', FX+'super_whoosh.wav', 0.02, -6, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', lab('GR86 launch')-0.05, -6, 0, None, 0, 0),
 ('f', FX+'camera_strobe.wav', lab('speed camera FLASH'), -2, 0, None, 0, 0),
 ('f', FX+'busted_slam.wav', lab('BUSTED')-0.35, 0, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', lab('FINE'), -2, 0, None, 0, 0), ('f', FX+'cha_ching.wav', lab('FINE')+0.08, -3, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', dv+0.02, -8, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', lab('servo wide')-0.05, -8, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', gl+0.05, -6, 0, None, 0, 0),
 ('f', FX+'freeze_riser.wav', lab('FREEZE: ARFAN')-0.6, -6, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', lab('FREEZE: ARFAN'), -2, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', lab('pump 1 stops'), -4, 0, None, 0, 0), ('f', FX+'cha_ching.wav', lab('pump 1 stops')+0.05, -8, 0, None, 0, 0),
 ('f', FX+'ready_chime.wav', lab('READY'), -4, 0, None, 0, 0), ('f', FX+'super_whoosh.wav', lab('READY')-0.12, -8, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', lab('PUMP Dave'), -4, 0, None, 0, 0),
 ('f', FX+'heartbeat.wav', night+0.1, -2, 0, 1.3, 0, 0.2),
 ('f', FX+'phone_tap.wav', lab('PHONE')+0.31, -4, 0, None, 0, 0), ('f', FX+'confirm_ding.wav', lab('PHONE')+0.35, -4, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', yard-0.03, -6, 0, None, 0, 0), ('f', FX+'stamp_thud.wav', yard+0.15, -4, 0, None, 0, 0),
 ('f', FX+'freeze_riser.wav', lab('FREEZE: MONSOOR')-0.6, -6, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', lab('FREEZE: MONSOOR'), -2, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', hero-0.1, -6, 0, None, 0, 0),
 ('f', FX+'sonic_logo.wav', brand+0.1, -2, 0, None, 0, 0),
] + [('f', FX+'number_tick.wav', lab(d_)+k*0.08, -8, 0, None, 0, 0) for d_ in ('DASH X-Trail', 'DASH Sportage', 'DASH Outlander', 'DASH GR86', 'DASH Tucson') for k in range(3)]
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
        '[mus][voxsc]sidechaincompress=threshold=0.012:ratio=16:attack=10:release=300:makeup=1[mud]',
        f'[mud][amb][vox1][sfx]amix=inputs=4:normalize=0,atrim=0:{total},afade=t=out:st={total-0.4}:d=0.4,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[m]']
run(['ffmpeg', '-y', '-i', vid2] + inp + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[m]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', 'QJ30-FINAL.mp4'])
print(f'total {total:.2f}s')
for st, l in marks: print(f'{st:6.2f}  {l}')
