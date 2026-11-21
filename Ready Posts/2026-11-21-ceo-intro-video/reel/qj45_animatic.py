"""45 s animatic for "Queue Jump": the 39 s Blender previs re-cut to the final plan,
with new beats as stills (element images) with a slow push, game cards and arrival sounds.
Run: /opt/miniconda3/bin/python -I qj45_animatic.py <work_dir>   -> writes QJ45-Animatic.mp4"""
import os, subprocess, sys
W, H, FPS = 720, 1280, 24
work = sys.argv[1]; os.makedirs(work, exist_ok=True)
PREV = 'QJ39-Previs.mp4'
V = '../voice/qj/'; D = 'audio/designed/'
def run(c): subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# (kind, a, b, label) kind 'p' = previs src a..b ; 's' = still image a for b seconds ; 'card' = card over blurred still
SEG = [
 ('p', 0.00, 3.65, 'red lights montage + GR86 launch (heard)'),
 ('flash', None, 0.20, 'speed camera FLASH'),
 ('s', 'elements/props/FX-Police-Mirror-Lights.png', 1.20, 'police lights in her mirror'),
 ('s', 'elements/dash/Dash-GR86-PulledOver.png', 0.80, 'pulled over: 0 km/h, ODO 18,645'),
 ('p', 4.50, 5.10, '"Ugh... oh, come ON!"'),
 ('card', 'graphics/Card-BUSTED-GTA.png', 0.90, 'BUSTED'),
 ('card', 'graphics/Card-DEMERITS-GTA.png', 1.10, 'FINE (blurred) / -3 DEMERIT POINTS'),
 ('p', 5.10, 9.75, 'Dave, servo, Mia asleep'),
 ('p', 9.75, 11.35, 'silent C-HR glide, "Boss, just got the car. Coming."'),
 ('s', 'elements/gta/Dog-InCar-crop.png', 1.00, 'dog reveal, passenger seat: one big released bark'),
 ('p', 11.35, 17.60, 'door, ARFAN, "What\'s up?", pump, POWER, READY'),
 ('p', 17.60, 19.60, 'Dave double take, "...you\'re kidding me"'),
 ('p', 19.60, 21.50, 'Mia: "Daaad... can we get one?"'),
 ('s', 'elements/gta/Yard-Final-AZ007.png', 0.80, 'next morning: yard, SOLD, AZ 007, logo flags'),
 ('p', 21.50, 28.05, 'SOLD tag, Hellcat arrives, MONSOOR, "Good job." / "That means a lot."'),
 ('p', 28.05, 39.00, 'delivery + brand card'),
]
files, t, marks = [], 0.0, []
for i, (k, a, b, lab) in enumerate(SEG):
    o = os.path.join(work, f'seg{i:02d}.mp4')
    if k == 'p':
        dur = b - a
        run(['ffmpeg', '-y', '-ss', str(a), '-i', PREV, '-t', str(dur), '-an', '-vf', f'scale={W}:{H},fps={FPS}', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    elif k == 'flash':
        dur = b
        run(['ffmpeg', '-y', '-f', 'lavfi', '-i', f'color=white:s={W}x{H}:r={FPS}', '-t', str(dur), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    elif k == 's':
        dur = b; n = int(dur * FPS)
        vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
              f"zoompan=z='1+0.04*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}")
        run(['ffmpeg', '-y', '-loop', '1', '-i', a, '-t', str(dur), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    else:  # card over a dark, blurred freeze of her face
        dur = b
        run(['ffmpeg', '-y', '-ss', '5.05', '-i', PREV, '-loop', '1', '-i', a, '-t', str(dur), '-filter_complex',
             f'[0:v]scale={W}:{H},trim=end_frame=1,loop=999:1:0,setpts=N/{FPS}/TB,gblur=sigma=14,eq=brightness=-0.18:saturation=0.6[bg];'
             f'[1:v]scale={W}:{H}[c];[bg][c]overlay=0:0,fps={FPS}', '-t', str(dur), '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', o])
    files.append(o); marks.append((t, lab, k, a)); t += dur
total = t
with open(os.path.join(work, 'list.txt'), 'w') as f:
    for o in files: f.write(f"file '{os.path.abspath(o)}'\n")
raw = os.path.join(work, 'raw.mp4'); vid = os.path.join(work, 'video.mp4')
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(work, 'list.txt'), '-c', 'copy', raw])

def at(i, off=0.0): return marks[i][0] + off   # output time of segment i (+offset)
def src(t39):  # map a previs time to output time
    for (st, lab, k, a), s in zip(marks, SEG):
        if k == 'p' and s[1] <= t39 < s[2]: return st + (t39 - s[1])
    return None
a0, a1 = src(15.15), src(17.60)
MF = os.path.expanduser('~/Library/Fonts/Montserrat-Variable.ttf')
run(['ffmpeg', '-y', '-i', raw, '-i', 'graphics/Super-HalfFuel-720.png', '-filter_complex', f"[0:v][1:v]overlay=0:0:enable='between(t,{a0},{a1})'", '-c:v', 'libx264', '-pix_fmt', 'yuv420p', vid])
MU, AM, VO, FX = 'audio/music/', 'audio/sfx/', V, D
# (bus, file, start, gain dB, src offset, duration or None, fade-in, fade-out)
B = [
 # MUSIC: one continuous bed, crossfaded, silent only for the 2.6 s silent-C-HR beat (ambience carries it)
 ('m', MU+'GenZ-A.mp3', 0.00, -7, 0, 8.60, 0, 0.6),
 ('m', MU+'GenZ-B.mp3', 8.30, -15, 0, 4.80, 0.3, 0.08),              # low servo groove, hard stop as the C-HR glides in
 ('m', MU+'GenZ-B.mp3', src(11.35), -8, 0, 11.75, 0, 0.5),             # groove slams in on the door
 ('m', MU+'Boss-Arrival.mp3', src(22.05)-0.05, -5, 0.25, 1.95, 0, 0.3),  # gangster cue hit 1: the Hellcat rolls in
 ('m', MU+'Boss-Arrival.mp3', src(23.80)-0.10, -5, 5.40, 2.10, 0.05, 0.6),  # gangster cue hit 2: MONSOOR freeze
 ('m', FX+'warm_pad.wav', src(24.80), -12, 0, None, 0, 0),                  # warm pad under Good job / That means a lot
 ('m', MU+'GenZ-C.mp3', src(28.05)-0.6, -8, 0, None, 0.8, 0.7),       # delivery + brand
 # AMBIENCE
 ('a', AM+'Servo-Night-Ambience.mp3', 8.45, -6, 0, 12.0, 0.3, 0.6),
 ('a', AM+'Servo-Night-Ambience.mp3', 19.9, -8, 1.0, 6.0, 0.6, 1.2),
 ('a', AM+'Yard-Morning-Ambience.mp3', at(13)-0.2, -6, 0, 5.0, 0.3, 1.0),
 # VOICES
 ('v', VO+'Glam-ComeOn.wav', at(4)+0.05, 2, 0, None, 0, 0),
 ('v', VO+'Arfan-Boss-v3a-tight.wav', at(8)+0.15, 2, 0, None, 0, 0),
 ('v', VO+'Arfan-WhatsUp-v4a-trim.wav', src(12.05), 3, 0, None, 0, 0),
 ('v', VO+'Dave-KiddingMe.wav', at(11)+0.4, 2, 0, None, 0, 0),
 ('v', VO+'Mia-v2.wav', at(12)+0.2, 2, 0, None, 0, 0),
 ('v', VO+'Monsoor-GoodJob-v3b-trim.wav', src(25.00), 3, 0, None, 0, 0),
 ('v', VO+'Arfan-MeansALot-LOCKEDcut.wav', src(26.45), 3, 0, None, 0, 0),
 ('v', VO+'Arfan-YouChoose-LOCKEDcut.wav', src(28.20), 3, 0, None, 0, 0),
 ('v', VO+'Arfan-WeBring-LOCKEDcut.wav', src(29.45), 3, 0, None, 0, 0),
 ('f', AM+'Dog-Bark-2.mp3', at(9)+0.12, 0, 0, 1.6, 0, 0.4),
 # SOUND ON EVERY ARRIVAL
 ('f', FX+'super_whoosh.wav', 0.10, -6, 0, None, 0, 0),
 ('f', FX+'camera_strobe.wav', at(1), -2, 0, None, 0, 0),
 ('f', FX+'busted_slam.wav', at(5)-0.35, 0, 0, None, 0, 0),
 ('f', FX+'popup_pop.wav', at(6), -2, 0, None, 0, 0),
 ('f', FX+'cha_ching.wav', at(6)+0.08, -3, 0, None, 0, 0),
 ('f', FX+'freeze_riser.wav', src(7.90)-0.6, -6, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', src(7.90), -4, 0, None, 0, 0),
] + [('f', FX+'number_tick.wav', src(7.45)+k*0.07, -10, 0, None, 0, 0) for k in range(6)] + [
 ('f', FX+'freeze_riser.wav', src(11.80)-0.6, -6, 0, None, 0, 0), ('f', FX+'freeze_hit.wav', src(11.80), -4, 0, None, 0, 0),
 ('f', FX+'ready_chime.wav', src(15.15), -4, 0, None, 0, 0),
 ('f', FX+'super_whoosh.wav', src(15.15)-0.15, -8, 0, None, 0, 0),
 ('f', FX+'stamp_thud.wav', src(21.50)+0.1, -4, 0, None, 0, 0),
 ('f', FX+'freeze_hit.wav', src(23.80), -4, 0, None, 0, 0),
 ('f', FX+'sonic_logo.wav', src(34.0), -2, 0, None, 0, 0),
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
        '[mus][voxsc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350:makeup=1[mud]',   # music dips under every line
        f'[mud][amb][vox1][sfx]amix=inputs=4:normalize=0,atrim=0:{total},afade=t=out:st={total-0.5}:d=0.5,loudnorm=I=-14:TP=-1:LRA=11[m]']
run(['ffmpeg', '-y', '-i', vid] + inp + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[m]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', 'QJ45-Animatic.mp4'])
print(f'total {total:.2f}s')
for st, lab, k, a in marks: print(f'{st:6.2f}  {lab}')
