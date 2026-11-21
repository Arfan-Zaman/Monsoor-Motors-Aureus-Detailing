"""FULL-STORY upload version of "Queue Jump" (organic post, not an ad): every Seedance clip at full length
+ our Higgsfield photos in story order, game cards, freezes, and sound designed shot by shot.
Run: REUSE=1 /opt/miniconda3/bin/python -I qj_long.py <work_dir>   -> writes QJ-FULL-STORY.mp4"""
import os, subprocess, sys
W, H, FPS = 1080, 1920, 24
work = sys.argv[1]; os.makedirs(work, exist_ok=True)
V = '../voice/qj/'; D = 'audio/designed/'
LUT = 'graphics/QJ_GTA_Perth_Film.cube'
def run(c):
    if c[0] == 'ffmpeg': c = ['ffmpeg', '-nostdin'] + c[1:]
    subprocess.run(c, check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
C, P, E = 'clips/', 'pilot/', 'elements/'
# shake on bold moments: label prefix -> (amplitude px, speed, decay per s; 0 = steady handheld)
SHAKE = {'GR86': (9, 21, 0), 'BUSTED': (18, 34, 6), 'FREEZE: ARFAN': (16, 34, 7), 'DOOR': (7, 30, 5), 'DOG': (8, 30, 5),
         'HELLCAT': (6, 41, 0), 'FREEZE: MONSOOR': (16, 34, 7), 'HERO': (10, 34, 5)}
def shake(label):
    for k, (a, f, d) in SHAKE.items():
        if label.startswith(k):
            m = a + 4; env = f'exp(-{d}*t)' if d else '1'
            return (f",crop={W-2*m}:{H-2*m}:'{m}+{a}*{env}*sin({f}*t)+{a*0.4}*sin({f*0.37}*t)':'{m}+{a}*{env}*cos({f*1.31}*t)',"
                    f"scale={W}:{H}:flags=lanczos")
    return ''
GRADE = (f"scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,crop={W}:{H},unsharp=5:5:0.35,"
         f"split[o][g];[g]lut3d={LUT}[l];[o][l]blend=all_mode=normal:all_opacity=0.62,"
         f"colorbalance=rs=-0.04:bs=0.05:rm=0.02:bm=-0.01:rh=0.05:gh=0.01:bh=-0.05,eq=saturation=1.1:contrast=1.05,noise=alls=4:allf=t,fps={FPS}")
SEG = [
 ('i', (E+'gta/GTA-Perth-Aerial.png', 0.40, 0.5, 1.0, 0.08), 1.50, 'OPEN: Perth aerial'),
 ('c', (C+'c01.mp4', 0.0), 5.00, 'MONTAGE red lights'),
 ('i', (E+'dash/Dash-XTrail.png', 0.49, 0.47, 1.5, 0.0), 1.00, 'DASH X-Trail'),
 ('i', (E+'dash/Dash-Sportage.png', 0.50, 0.44, 1.5, 0.0), 1.00, 'DASH Sportage'),
 ('i', (E+'dash/Dash-Outlander.png', 0.51, 0.46, 1.5, 0.0), 1.00, 'DASH Outlander'),
 ('c', (C+'c02.mp4', 0.0), 5.00, 'GR86 launch, flash, police, come ON'),
 ('card', (C+'c02.mp4', 3.4, 'graphics/Card-BUSTED-GTA.png'), 1.00, 'BUSTED'),
 ('card', (C+'c02.mp4', 3.4, 'graphics/Card-DEMERITS-GTA.png'), 1.00, 'FINE / -3 DEMERIT POINTS'),
 ('c', (C+'c03.mp4', 1.0), 2.00, 'DAVE at the lights'),
 ('i', (E+'dash/Dash-Tucson.png', 0.49, 0.47, 1.4, 0.0), 1.00, 'DASH Tucson'),
 ('c', (C+'c04.mp4', 1.5), 2.00, 'SERVO wide'),
 ('c', (C+'c05.mp4', 0.6), 0.35, 'C-HR arrives, Arfan on the call'),          # him driving
 ('i', (E+'props/Prop-HandsFree-Call.png', 0.56, 0.5, 1.0, 0.0), 0.50, 'CALL DASH: driver POV, wheel and call screen'),   # Higgsfield POV still, handheld drift   # dash POV in the middle of the drive, before the call
 ('c', (C+'c05.mp4', 1.9), 1.65, 'CALL BACK: his face on the call'),          # back on him for the whole line (lips from clip 1.9)
 ('c', (C+'c10.mp4', 0.0), 1.00, 'MIA LOOKS out from her dad\'s car'),
 ('c', (C+'c18.mp4', 1.0), 2.00, 'ARRIVE: C-HR rolls in, Mia watching'),
 ('c', (C+'c06.mp4', 0.0), 1.00, 'DOG woof'),
 ('ramp', (C+'c07.mp4', [(0.0, 0.2, 1.0), (0.2, 0.6, 0.5), (0.6, 1.35, 1.5)]), 1.50, 'DOOR: splash, steps out'),   # old footstep: real speed hit, slow-mo crown, speed-up into the freeze
 ('freeze', (E+'gta/Freeze-Arfan-GTA-art.png', 0, 'graphics/Card-ARFAN-CEO-GTA.png'), 1.75, 'FREEZE: ARFAN / CEO'),   # Higgsfield GTA-style key art of the c19 4.7 s side look (job 33523b55)   # freeze on his side look
 ('ramp', (C+'c19.mp4', [(4.7, 5.0, 0.4), (5.0, 5.5, 1.0), (5.5, 6.0, 0.33)]), 2.75, 'WHATSUP'),   # thaws from the freeze in slow-mo, real speed on 'What's up?' (lips at clip 5.1 = seg 0.85), slow-mo smile   # new take: slow-mo lean out of the freeze, real speed into 'What's up?' (lips at clip 5.1 = 33.0 s, same as the voice)
 ('c', (C+'c19.mp4', 6.0), 3.00, 'FILL: Arfan fills the C-HR'),
 ('c', (C+'c19.mp4', 9.0), 2.50, 'POWER, READY'),
 ('c', (C+'c09.mp4', 0.3), 3.50, 'DAVE double take'),
 ('i', (E+'dash/Pump-Dave.png', 0.34, 0.47, 1.25, 0.0), 1.00, 'PUMP Dave'),
 ('c', (C+'c10.mp4', 1.0), 3.00, 'MIA line'),
 ('c', (C+'c11.mp4', 1.2), 2.50, 'NIGHT: Dave decides'),
 ('i', (E+'props/Phone-PreOrder-CHR.png', 0.5, 0.47, 1.05, 0.0), 1.50, 'PHONE: PRE-ORDER'),
 ('i', (E+'gta/Yard-Final-AZ007.png', 0.47, 0.5, 1.0, 0.04), 1.50, 'YARD: next morning'),
 ('c', (C+'c12.mp4', 0.4), 4.50, 'HELLCAT arrives, Monsoor rises'),
 ('freeze', (C+'c12.mp4', 4.85, 'graphics/Card-MONSOOR-BOSS-GTA.png'), 1.00, 'FREEZE: MONSOOR / BOSS'),
 ('c', (P+'Pilot-Monsoor-GoodJob-crop.mp4', 0.5), 2.50, 'CU MONSOOR'),
 ('c', (P+'Pilot-Arfan-MeansALot-crop.mp4', 1.8), 2.50, 'CU ARFAN'),
 ('c', (C+'c15.mp4', 0.0), 5.00, 'DELIVERY'),
 ('ramp', (C+'c16.mp4', [(0.0, 1.75, 0.7)]), 2.50, 'HERO'),   # gentle slow-mo on the MISSION PASSED hero
 ('s', 'graphics/Brand-Card-1080.png', 3.00, 'BRAND'),
]
# c19 (final Seedance take) matched to the neighbouring clips before the common grade: exposure, warmth, saturation
MATCH = {'CALL DASH': 'colorchannelmixer=rr=1.75:gg=1.2:bb=0.9,eq=gamma=1.25:saturation=0.6,', 'WHATSUP': 'eq=gamma=1.2:saturation=1.05,colorbalance=rm=0.03:bm=-0.01,',
         'FILL': 'eq=gamma=1.12:saturation=1.45,colorbalance=rm=0.02:gm=0.02,',
         'POWER, READY': 'colorchannelmixer=rr=1.75:gg=1.2:bb=0.9,eq=gamma=1.25:saturation=0.6,'}
# dog close-up: tight 9:16 crop on his head with a slow handheld drift so he feels alive
PRE = {'CU ARFAN': "zoompan=z='1+0.09*(1-cos(PI*min(on/60\\,1)))/2':x='iw/2-(iw/zoom/2)+6*sin(on/17)':y='ih*0.42-(ih/zoom*0.42)':d=1:s=1080x1920:fps=24,", 'CALL DASH': "crop=660:1173:x='30+4*sin(t*37)+20*t':y='54+3*sin(t*29)',", 'DOG woof': "crop=396:704:x='236+16*t+8*sin(t*3.1)':y='60+5*sin(t*4.3)',"}
def probe(f):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])
files, t, marks = [], 0.0, []
for i, (k, a, b, lab_) in enumerate(SEG):
    o = os.path.join(work, f'seg{i:02d}.mp4'); dur = b
    if os.environ.get('REUSE') and os.path.exists(o) and os.path.getsize(o) > 1000:
        pass   # segment already rendered in this work dir
    elif k == 'ramp':
        f, parts = a
        ch = ''.join(f"[0:v]trim={s0}:{s1},setpts=(PTS-STARTPTS)/{sp}[r{j}];" for j, (s0, s1, sp) in enumerate(parts))
        ch += ''.join(f'[r{j}]' for j in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=0,trim=0:{dur},setpts=PTS-STARTPTS,minterpolate=fps=60:mi_mode=blend,'
        run(['ffmpeg', '-y', '-i', f, '-an', '-filter_complex', f'{ch}{MATCH.get(lab_.split(":")[0], "") if "c19" in f else ""}{GRADE}{shake(lab_)}', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    elif k == 'c':
        f, ip = a
        run(['ffmpeg', '-y', '-ss', str(ip), '-i', f, '-t', str(dur), '-an', '-filter_complex', f'[0:v]{PRE.get(lab_.split(":")[0], "")}{MATCH.get(lab_.split(":")[0], "") if "c19" in f else ""}{GRADE}{shake(lab_)}', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', o])
    elif k == 'i':   # photo as a shot: 9:16 window on the detail, slow drift like a handheld reframe, light grain
        f, cx, cy, zoom, dx = a; iw, ih = probe(f)
        ch = min(ih / zoom, iw * 16 / 9 / zoom); cw = ch * 9 / 16
        x0 = min(max(cx * iw - cw / 2, 0), iw - cw); y0 = min(max(cy * ih - ch / 2, 0), ih - ch)
        drift = (dx * iw) if dx else cw * 0.03
        x0 = min(x0, iw - cw - drift) if x0 + cw + drift > iw else x0
        vf = (f"crop={int(cw)}:{int(ch)}:'{x0:.1f}+{drift:.1f}*t/{dur}':'{y0:.1f}'," + GRADE.replace(f'scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,crop={W}:{H},', f'scale={W}:{H}:flags=lanczos,'))
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
        if 'ARFAN' in lab_:   # ARFAN freeze: Higgsfield GTA key art, saturated, animated push with a drift
            head = (f'[0:v]scale={W}:{H}:flags=lanczos,loop={n}:1:0,setpts=N/{FPS}/TB,eq=saturation=1.12:contrast=1.04,noise=alls=3:allf=t,'
                    f"zoompan=z='1.0+0.08*(1-cos(PI*on/{n}))/2':x='iw/2-(iw/zoom/2)+14*sin(on/9)':y='ih*0.4-(ih/zoom*0.4)':d=1:s={W}x{H}:fps={FPS}[fz];")
        else:
            head = f'[0:v]trim=end_frame=1,loop={n}:1:0,setpts=N/{FPS}/TB,{GRADE},eq=saturation=0.8:contrast=1.06[fz];'
        run(['ffmpeg', '-y', '-ss', str(ts), '-i', f, '-loop', '1', '-i', card, '-t', str(dur), '-filter_complex',
             head +
             f"[fz]zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}[bg];"
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}{shake(lab_)}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    else:
        (f, ts, card) = a
        run(['ffmpeg', '-y', '-ss', str(ts), '-i', f, '-loop', '1', '-i', card, '-t', str(dur), '-filter_complex',
             f'[0:v]trim=end_frame=1,loop=999:1:0,setpts=N/{FPS}/TB,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=18,eq=brightness=-0.18:saturation=0.6[bg];'
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}{shake(lab_)}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    files.append(o); marks.append((t, lab_)); t += dur
total = t
with open(os.path.join(work, 'list.txt'), 'w') as f:
    for o in files: f.write(f"file '{os.path.abspath(o)}'\n")
vid = os.path.join(work, 'video.mp4')
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(work, 'list.txt'), '-c', 'copy', vid])
def lab(s): return next(m[0] for m in marks if m[1].startswith(s))

L = lab
OVL = [  # (file, start, duration)
 ('graphics/Stamp-PERTH.png', 0.15, 1.6),
 ('graphics/Tag-LAYLA.png', L('GR86')+0.05, 0.8),
 ('graphics/Tag-DAVE.png', L('DAVE at')+0.1, 1.2),
 ('graphics/Stamp-SERVO.png', L('SERVO')+0.1, 1.4),
 ('graphics/HUD-CALL-BOSS.png', L('C-HR arrives')+0.1, 2.3),
 ('graphics/Pop-PUMP-ARFAN.png', L('FILL')+0.6, 1.2),
 ('graphics/Super-HalfFuel-720.png', L('POWER')+1.1, 1.4),
 ('graphics/White-Flash.png', L('GR86')+1.72, 0.22),
 ('graphics/White-Flash.png', L('FREEZE: ARFAN'), 0.16),   # flash into the GTA key-art freeze
 ('graphics/Pop-PUMP-DAVE.png', L('PUMP Dave')+0.05, 1.1),
 ('graphics/Pop-PREORDER.png', L('PHONE')+0.6, 0.9),
 ('graphics/Stamp-YARD.png', L('YARD')+0.1, 1.4),
 ('graphics/Anim-MISSION-PASSED.mov', round((L('HERO')+0.5)*2)/2-0.15, 1.95),
]
vid2 = os.path.join(work, 'video2.mp4')
cmd = ['ffmpeg', '-y', '-i', vid]; fc, last = [], '0:v'
for n, (png, st, du) in enumerate(OVL):
    if png.endswith('.mov'):
        cmd += ['-itsoffset', f'{st:.3f}', '-t', str(du), '-i', png]
        fc.append(f'[{n+1}:v]scale={W}:{H},format=rgba[o{n}]')
        fc.append(f"[{last}][o{n}]overlay=0:0:eof_action=pass:enable='between(t,{st:.3f},{st+du:.3f})'[v{n}]")
    else:
        cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{total:.3f}', '-i', png]
        fc.append(f'[{n+1}:v]scale={W}:{H},format=rgba,fade=t=in:st={st:.3f}:d=0.08:alpha=1,fade=t=out:st={st+du-0.15:.3f}:d=0.15:alpha=1[o{n}]')
        fc.append(f"[{last}][o{n}]overlay=0:0:enable='between(t,{st:.3f},{st+du:.3f})'[v{n}]")
    last = f'v{n}'
run(cmd + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', vid2])

MU, AM, VO, FX = 'audio/music/', 'audio/sfx/', V, D
import numpy as np
def onset(f):   # time of the first strong hit in a music file
    x=np.frombuffer(subprocess.run(['ffmpeg','-nostdin','-v','error','-t','4','-i',f,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout,'<i2').astype(float)/32768
    hop=80; n=len(x)//hop; e=20*np.log10(np.sqrt(np.mean(x[:n*hop].reshape(n,hop)**2,axis=1))+1e-9)
    return float(np.argmax(e > e.max()-10)*hop/8000)
def g(t): return round(t*2)/2   # snap to the beat grid
def loop(bus, f, start, end, gain, seglen, xf=0.5, off=None):   # repeat a cue on the beat grid, each copy's first hit on a beat
    on = onset(f) if off is None else off
    out, t = [], g(start)
    while t < end - 0.3:
        d = min(seglen, end - t + xf)
        out.append((bus, f, t, gain, on, d, 0.05 if t == g(start) else xf, xf)); t += seglen - xf
    return out
busted, servo, chr_, door, fill = L('BUSTED'), L('SERVO'), L('C-HR arrives'), L('DOOR'), L('FILL')
night, yard, hc, fzm, cum, cua = L('NIGHT'), L('YARD'), L('HELLCAT'), L('FREEZE: MONSOOR'), L('CU MONSOOR'), L('CU ARFAN')
deliv, hero, brand = L('DELIVERY'), L('HERO'), L('BRAND')
B = []
# MUSIC (all in the opening track's style), no loops: each cue plays once, changes land on bars / scene changes
oA, oB, oC = onset(MU+'GenZ-A.mp3'), onset(MU+'GenZ-B.mp3'), onset(MU+'GenZ-C.mp3')
B += [('m', MU+'GenZ-A.mp3', 0.0, -9, oA, 8.5, 0.05, 1.0),                         # opening groove, out before its fade
      ('m', MU+'GenZ-B.mp3', 7.5, -9, oB, busted+2.0-7.5, 1.0, 0.6),               # same key and tempo, crossfaded on a bar
      ('m', MU+'GenZ-B.mp3', g(L('DAVE at')), -16, oB+2.0, chr_-g(L('DAVE at')), 0.5, 0.15),   # low under Dave and the servo, stops dead for the silent C-HR
      ('m', MU+'Arfan-MiamiDon-BGM.mp3', L('FREEZE: ARFAN'), -8, 0.0, L('DAVE double')-L('FREEZE: ARFAN')+0.3, 0.02, 0.5),  # Arfan's main-character theme: ARFAN / CEO intro to the READY button
      ('m', MU+'GenZ-C.mp3', g(L('DAVE double')), -14, oC, night-g(L('DAVE double'))+0.2, 0.5, 0.4),  # brighter, hopeful under "kidding me" / Mia
      ('m', FX+'tension_drone.wav', night+0.05, -13, 0, None, 0.1, 0.3)]
B += [('m', MU+'GenZ-B-muffled.wav', chr_, -9, oB, 3.3, 0.3, 0.4),
      ('m', MU+'Gangster-of-Miami-inst.mp3', chr_+3.0, -8, 0.635+16*60/92.3, L('DOG woof')+1.0-(chr_+3.0), 0.15, 0.5),   # Monsoor's BGM under his laugh, end of 'coming' to end of the dog shot
      ('m', MU+'GenZ-B-muffled.wav', L('DOG woof')+0.9, -9, oB+L('DOG woof')+0.9-chr_, g(L('FREEZE: ARFAN'))-L('DOG woof')-0.9, 0.3, 0.05),            # low muffled pulse under the silent C-HR, builds to the slam
      ('v', VO+'Monsoor-Laugh-LOCKED-phone.wav', chr_+3.1, 0, 0, L('DOG woof')+1.0-(chr_+3.1), 0.05, 0.5),   # LOCKED laugh over the phone from the end of 'coming' to the end of the dog shot                                  # Monsoor laughs back over the phone: "Ha ha ha... Good, good."
      ('f', FX+'loafer_steps_brick.wav', hc+2.98, -1, 0, None, 0, 0),                                   # his loafers on the brick
      ]
B += [('f', FX+'sub_drop.wav', 0.0, -5, 0, None, 0, 0),                          # PERTH opener
      ('f', FX+'sub_drop.wav', busted, -3, 0, None, 0, 0),                      # BUSTED
      ('f', FX+'sub_drop.wav', L('FREEZE: ARFAN'), -3, 0, None, 0, 0),          # ARFAN / CEO + groove slam
      ('f', FX+'sub_rumble.wav', hc+0.6, -4, 0, None, 0, 0),                    # Hellcat rolls into the yard
      ('f', FX+'sub_drop.wav', fzm, -3, 0, None, 0, 0),                         # MONSOOR / BOSS
      ('f', FX+'sub_drop.wav', g(hero+0.5), -3, 0, None, 0, 0)]                 # MISSION PASSED slam                           # a last little boss laugh under the end card
# Monsoor's BGM 'Gangster of Miami': filtered build under the Hellcat, his 'HA' pickup into the freeze, the drop lands on MONSOOR / BOSS, out after 'Good job!'
BGM_DROP = 0.635 + 16*60/92.3
B += [('m', MU+'Monsoor-BGM-Gangster-of-Miami-v3.wav', hc, -7, BGM_DROP-(fzm-hc), cum+2.4-hc, 0.4, 0.8),
      ('m', MU+'Arfan-MiamiDon-BGM.mp3', cua, -10, 10.3, deliv+2.9-cua, 0.05, 0.5)]   # Arfan's BGM from his close-up to the end of 'We bring it to your home'
B += [('m', MU+'Delivery-GenZ.mp3', deliv+2.4, -8, 0, hero-deliv-2.4+0.6, 0.5, 0.15),
      ('m', MU+'Mission-Passed-GenZ.mp3', g(hero+0.5), -11, onset(MU+'Mission-Passed-GenZ.mp3'), 2.4, 0, 0.6),   # MISSION PASSED sting, hands over to Monsoor's BGM
      ('m', MU+'Monsoor-BGM-Gangster-of-Miami-v3.wav', g(hero+0.5)-0.3, -5, 0.635+12*4*60/92.3-0.3, None, 0.3, 0),   # his BGM lift lands on the slam, laugh chops ride to the end
      ]
# AMBIENCE
B += loop('a', AM+'Servo-Night-Ambience.mp3', L('DAVE at'), night, -7, 11.0, xf=1.0, off=0.0)
B += [('a', AM+'Yard-Morning-Ambience.mp3', deliv-0.3, -10, 0, 5.0, 0.4, 0.8), ('a', AM+'Yard-Morning-Ambience.mp3', deliv+4.2, -11, 0, 5.0, 0.6, 1.0), ('m', FX+'warm_pad.wav', deliv+3.4, -13, 0, None, 0.4, 0.6),
      ('a', AM+'Yard-Morning-Ambience.mp3', yard, -6, 0, 5.0, 0.3, 0.6),
      ('a', AM+'Yard-Morning-Ambience.mp3', yard+4.4, -8, 0, 5.0, 0.6, 1.0)]
# VOICES (placed on each clip's lip timing)
B += [('v', VO+'Glam-Ugh-Sync.wav', L('GR86')+3.42, 0, 0, None, 0, 0),   # soft 'ugh' + 'Come on!' locked to her lips in c02 (cross-correlated with the clip audio)
      ('v', VO+'Arfan-Boss-v3a-tight-norm.wav', chr_+0.85, 0, 0, None, 0, 0),
      ('v', VO+'Arfan-WhatsUp-v4a-trim-norm.wav', L('WHATSUP')+0.80, 0, 0, None, 0, 0),
      ('v', VO+'Dave-KiddingMe-norm.wav', L('DAVE double')+0.00, 0, 0, None, 0, 0),
      ('v', VO+'Mia-v2-tight-norm.wav', L('MIA line')+0.48, 0, 0, None, 0, 0),
      ('v', VO+'Monsoor-GoodJob-v4-smile-trim-norm.wav', cum+0.57, 1, 0, None, 0, 0),
      ('v', VO+'Arfan-MeansALot-LIPSYNC.wav', cua+1.45, 2, 0, None, 0, 0),
      ('v', VO+'Arfan-YouChoose-LOCKEDcut-norm.wav', deliv+0.3, 0, 0, None, 0, 0),
      ('v', VO+'Arfan-WeBring-LOCKEDcut-norm.wav', deliv+1.5, 0, 0, None, 0, 0)]
# SOUND DESIGN, shot by shot
B += [('f', FX+'sting_kidding_brass.wav', L('DAVE double')+2.95, -7, 0, None, 0, 0),   # comic brass button on 'you're kidding me'
      ('f', FX+'sting_mia_cute.wav', L('MIA line')+2.6, -8, 0, None, 0, 0),         # cute climb + boing after 'can we get one?'
      ('f', FX+'sting_preorder_pluck.wav', L('PHONE: PRE-ORDER')+0.15, -7, 0, None, 0, 0)]   # playful 'ba-da-bing' on the pre-order
B += [('f', FX+'super_whoosh.wav', 0.25, -6, 0, None, 0, 0),
      ('f', FX+'popup_pop.wav', L('MONTAGE')+1.46, -8, 0, None, 0, 0)]                            # gum bubble pop
B += [('f', FX+'number_tick.wav', L(d)+0.15+k*0.08, -8, 0, None, 0, 0) for d in ('DASH X-Trail', 'DASH Sportage', 'DASH Outlander', 'DASH Tucson') for k in range(3)]
B += [('f', FX+'super_whoosh.wav', L('GR86')-0.05, -6, 0, None, 0, 0),
      ('f', FX+'camera_strobe.wav', L('GR86')+1.70, -2, 0, None, 0, 0),
      ('f', FX+'busted_slam.wav', busted-0.35, 0, 0, None, 0, 0),
      ('f', FX+'police_siren_onbeat.wav', L('GR86'), -3, 0, None, 0, 0),
      ('f', AM+'CHR-Arrive-Fast-Stop.mp3', L('ARRIVE')-0.7, -1, 0, None, 0, 0.3),      # C-HR comes in fast, hard stop, body rocks with a low rumble
      ('f', FX+'sub_rumble.wav', L('ARRIVE')+1.4, -7, 0, 1.2, 0, 0.5),                  # the stop: low vibration through the floor        # siren from her launch, wail on the 2-beat, winds down onto the downbeat as FINE ends
      ('f', FX+'popup_pop.wav', L('FINE'), -2, 0, None, 0, 0), ('f', FX+'cha_ching.wav', L('FINE')+0.08, -3, 0, None, 0, 0),
      ('f', FX+'super_whoosh.wav', L('DAVE at')+0.15, -8, 0, None, 0, 0),
      ('f', FX+'super_whoosh.wav', servo+0.15, -8, 0, None, 0, 0),
      ('f', FX+'popup_pop.wav', chr_+0.3, -6, 0, None, 0, 0),
      ('f', AM+'Dog-Woof-Curious.wav', L('DOG')-0.05, -1, 0, 1.05, 0, 0.15),
      ('f', FX+'stamp_thud.wav', door+0.2, -6, 0, None, 0, 0), ('f', FX+'slowmo_whoomp.wav', door+0.2, -4, 0, None, 0, 0), ('f', FX+'super_whoosh.wav', door+1.0, -9, 0, None, 0, 0),   # splash, time slows, whips back to speed                                   # sneaker splash hit
      ('f', FX+'door_slam_heavy.wav', L('FREEZE: ARFAN')-0.03, 0, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', L('FREEZE: ARFAN'), -6, 0, None, 0, 0),
      # the fill: nozzle in, pump runs, meter ticks, auto shut-off at 36.20, nozzle out, flap, nozzle holstered
      ('f', FX+'fuel_pump_run.wav', fill+0.0, -6, 0, 0.6, 0.05, 0.05),         # pump running while he holds the nozzle
      ('f', FX+'fuel_clickoff.wav', fill+0.6, -2, 0, None, 0, 0),             # auto shut-off at 36.20
      ('f', FX+'cha_ching.wav', fill+0.7, -10, 0, None, 0, 0),
      ('f', FX+'fuel_nozzle_out.wav', fill+1.0, -4, 0, None, 0, 0),           # nozzle out
      ('f', FX+'fuel_flap_click.wav', fill+2.75, -3, 0, None, 0, 0),           # flap shut
      ('f', FX+'fuel_holster.wav', fill+2.4, -8, 0, None, 0, 0),
      ('f', FX+'phone_tap.wav', L('POWER')+0.5, -4, 0, None, 0, 0), ('f', FX+'ready_chime.wav', L('POWER')+1.1, -4, 0, None, 0, 0), ('f', FX+'super_whoosh.wav', L('POWER')+1.05, -8, 0, None, 0, 0),
      ('f', FX+'fuel_clickoff.wav', L('DAVE double')+0.7, -4, 0, None, 0, 0),                     # Dave's pump finally stops
      ('f', FX+'popup_pop.wav', L('PUMP Dave')+0.05, -4, 0, None, 0, 0),
      ('f', FX+'heartbeat.wav', night+0.2, -2, 0, None, 0, 0),
      ('f', FX+'phone_tap.wav', L('PHONE')+0.55, -4, 0, None, 0, 0), ('f', FX+'confirm_ding.wav', L('PHONE')+0.6, -4, 0, None, 0, 0),
      ('f', FX+'super_whoosh.wav', yard+0.05, -6, 0, None, 0, 0), ('f', FX+'stamp_thud.wav', yard+0.4, -5, 0, None, 0, 0),
      ('f', FX+'door_slam_heavy.wav', fzm-0.03, 0, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', fzm, -6, 0, None, 0, 0),
      ('f', FX+'super_whoosh.wav', hero+0.3, -6, 0, None, 0, 0),
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
        '[mus][voxsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350:makeup=1[mud]',
        f'[mud][amb][vox1][sfx]amix=inputs=4:normalize=0,atrim=0:{total},afade=t=out:st={total-0.6}:d=0.6,alimiter=limit=0.5:attack=1:release=60:level=false,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.7:attack=0.3:release=40:level=false[m]']
run(['ffmpeg', '-y', '-i', vid2] + inp + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[m]', '-t', f'{total:.3f}', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', 'QJ-FULL-STORY.mp4'])
print(f'total {total:.2f}s')
for st, l in marks: print(f'{st:6.2f}  {l}')
