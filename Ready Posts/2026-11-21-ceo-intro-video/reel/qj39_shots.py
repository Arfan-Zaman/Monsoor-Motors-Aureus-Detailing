"""Shared shot table for the 39 s 'Queue Jump' previs (qj39_scene.py + qj39_post.py).

Times come straight from DIRECTOR-CUT.md section B2. 24 fps, 936 frames.
Frame f (1-based) shows time (f-1)/24. Shot n covers frames rng(n) inclusive.
"""
FPS, END = 24, 936

# (n, in, out, size/angle, lens + move, short description)
SHOTS = [
    (1, 0.00, 0.45, "WS / low", "75mm low car-rig track, settling", "Seltos rolls to the red, St Georges Tce"),
    (2, 0.45, 0.90, "MCU / eye", "75mm same take, settled", "GenZ guy: gum bubble pops"),
    (3, 0.90, 1.30, "CU / high", "100mm over the wheel, 3% push", "Seltos cluster near E, low-fuel lamp"),
    (4, 1.30, 1.85, "MCU / eye (pass. side)", "75mm handheld breathing", "GenZ woman, CX-3, Kwinana ramp"),
    (5, 1.85, 2.25, "ECU / high", "100mm, push 3%", "CX-3 tacho + digital readout"),
    (6, 2.25, 2.75, "MCU / slight low", "75mm dash side, car rig", "Retiree hunched, Kona, Eliz. Quay"),
    (7, 2.75, 3.15, "CU / high", "100mm", "Kona digital cluster"),
    (8, 3.15, 3.65, "WS / low", "32mm low kerb, static then track", "Lux V8 SUV: green, launch"),
    (9, 3.65, 4.05, "ECU / high", "100mm", "V8 speedo 64 -> 67"),
    (10, 4.05, 4.50, "WS / low", "32mm tracking", "Passes 60 sign + speed camera FLASH"),
    (11, 4.50, 5.10, "CU / eye", "75mm pass. side, car rig", "Glam driver busted"),
    (12, 5.10, 6.00, "MCU / eye", "50mm pass. window, 2% push", "Dave in ASX, Albany Hwy, Mia asleep"),
    (13, 6.00, 6.45, "CU / high", "100mm", "ASX dials + MID"),
    (14, 6.45, 6.90, "WS / low", "40mm, 3% push", "Static servo price board, queue"),
    (15, 6.90, 7.45, "MWS / eye", "50mm dolly push begins", "Queue, Dave at pump 2"),
    (16, 7.45, 7.90, "ECU / eye", "100mm", "Pump 2 litres rolling"),
    (17, 7.90, 9.25, "MCU / eye", "50mm end of push", "Dave's wince"),
    (18, 9.25, 9.75, "CU / eye", "75mm, 2% push", "Mia asleep on the window"),
    (19, 9.75, 11.35, "WS / low", "32mm low car rig, real speed", "Black C-HR glides in, silent"),
    (20, 11.35, 11.80, "ECU / ground", "32mm ground level", "Arfan's boot in the puddle"),
    (21, 11.80, 13.20, "MS > MCU / eye", "50mm gimbal straight push", "Arfan: 'What's up?'"),
    (22, 13.20, 13.65, "CU / eye", "100mm", "Nozzle into C-HR filler"),
    (23, 13.65, 14.25, "ECU / eye", "100mm", "Pump 1 meter stops 9.84 L"),
    (24, 14.25, 14.65, "MS / eye", "50mm locked off", "Dave still filling"),
    (25, 14.65, 15.15, "ECU / high", "100mm", "POWER press, olive Seiko"),
    (26, 15.15, 17.05, "CU / eye", "100mm, 3% pull-out", "READY, 4.3 L/100km"),
    (27, 17.05, 17.60, "MS / low", "50mm, 3% push", "C-HR rear 3/4, plate frame"),
    (28, 17.60, 19.60, "MCU / eye", "50mm locked, breathing", "Dave's double take, C-HR leaves"),
    (29, 19.60, 21.50, "CU / eye", "75mm slight handheld", "Mia: 'Dad... can we get one?'"),
    (30, 21.50, 22.05, "ECU / eye", "100mm", "SOLD tag on the black C-HR"),
    (31, 22.05, 23.35, "WS / low", "32mm low track, settling", "Muscle car rumbles in"),
    (32, 23.35, 23.80, "ECU / ground", "32mm ground level", "Monsoor's loafer on brick"),
    (33, 23.80, 24.90, "MS / low", "32mm same take, settled low", "Monsoor rises, door, walks"),
    (34, 24.90, 26.35, "MCU / OTS", "75mm slow push", "Hand on shoulder: 'Good job.'"),
    (35, 26.35, 28.05, "CU / eye", "75mm end of push", "Arfan: 'That means a lot.'"),
    (36, 28.05, 29.35, "WS / low", "32mm low kerb, track then settle", "C-HR into Dave's driveway"),
    (37, 29.35, 30.55, "MS / eye", "50mm gimbal push, V", "Arfan walks to Dave, palm up"),
    (38, 30.55, 31.05, "ECU / high", "100mm", "Key fob on open palm"),
    (39, 31.05, 32.35, "WS / low", "32mm same take as 36", "Mia runs out across the lawn"),
    (40, 32.35, 34.00, "MS / eye", "50mm end of push", "Mia's palms on the door, Dave grins"),
    (41, 34.00, 39.00, "MS / low", "40mm still, 3% push, light sweep", "Brand card: C-HR golden hour"),
]


def f_of(t):
    return int(round(t * FPS)) + 1


def rng(n):
    s = SHOTS[n - 1]
    return int(round(s[1] * FPS)) + 1, int(round(s[2] * FPS))


def shot_at(f):
    for s in SHOTS:
        a, b = rng(s[0])
        if a <= f <= b:
            return s
    return SHOTS[-1]
