"""'Queue Jump' 29 s reel: simple Blender motion previs (free storyboard).

Run:  blender -b -P qj_scene.py -- <frames_dir> [file.blend] [frame frame ...]
540x960, 24 fps, 696 frames (28 s story + 1 s brand).
Sets: night servo (x=+80), Monsoor yard by day (origin), family home at golden hour (x=-80).
Motion notes: Arfan's moves are captured from his real habits (square stance, chin a touch down,
eyebrow lift on key words, few hand moves) plus confidence: a relaxed half-smile, a cheeky glance,
a small shrug, never perfectly still. Monsoor follows his 3MT video: steady stance, hand on the
car, open palm, slow head turn.
"""
import sys
from math import radians

import bpy
from mathutils import Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FRAMES_DIR = argv[0] if argv else "/tmp/qj_frames"
SAVE_BLEND = next((a for a in argv[1:] if a.endswith(".blend")), None)
TEST_FRAMES = [int(a) for a in argv[1:] if a.isdigit()]
END = 696
SHOTS = {
    "S1": (1, 72), "S2a": (73, 120), "S2b": (121, 156), "S2c": (157, 192),
    "S3": (193, 264), "S4": (265, 360), "S5": (361, 432),
    "S6a": (433, 492), "S6b": (493, 564), "S7": (565, 672), "S8": (673, 696),
}
NIGHT = [SHOTS[k] for k in ("S1", "S2a", "S2b", "S2c", "S3", "S4", "S5")]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = 24
sc.frame_start, sc.frame_end = 1, END
sc.render.resolution_x, sc.render.resolution_y = 540, 960
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = FRAMES_DIR.rstrip("/") + "/f_"
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
    try:
        sc.render.engine = eng
        break
    except Exception:
        pass
try:
    sc.eevee.taa_render_samples = 12
    sc.view_settings.view_transform = "Standard"
except Exception:
    pass

world = bpy.data.worlds.new("World")
sc.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
sun_d = bpy.data.lights.new("Sun", "SUN")
sun = bpy.data.objects.new("Sun", sun_d)
sc.collection.objects.link(sun)
sun.rotation_euler = (radians(50), 0, radians(-38))


def set_env(f, night, golden=False):
    if night:
        bg.inputs[0].default_value = (0.05, 0.08, 0.16, 1)
        bg.inputs[1].default_value = 1.4
        sun_d.energy = 0.25
        sun_d.color = (0.6, 0.7, 1.0)
    elif golden:
        bg.inputs[0].default_value = (0.75, 0.62, 0.48, 1)
        bg.inputs[1].default_value = 1.0
        sun_d.energy = 2.6
        sun_d.color = (1.0, 0.78, 0.55)
    else:
        bg.inputs[0].default_value = (0.55, 0.72, 0.95, 1)
        bg.inputs[1].default_value = 1.15
        sun_d.energy = 4.2
        sun_d.color = (1, 1, 1)
    bg.inputs[0].keyframe_insert("default_value", frame=f)
    bg.inputs[1].keyframe_insert("default_value", frame=f)
    sun_d.keyframe_insert("energy", frame=f)
    sun_d.keyframe_insert("color", frame=f)


set_env(1, True)
set_env(432, True)
set_env(433, False)
set_env(564, False)
set_env(565, False, golden=True)
set_env(696, False, golden=True)
def _fcurves(idb):
    ad = getattr(idb, "animation_data", None)
    act = ad.action if ad else None
    if not act:
        return []
    if hasattr(act, "fcurves"):
        return list(act.fcurves)
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out.extend(bag.fcurves)
    return out


for fc in _fcurves(world.node_tree) + _fcurves(sun_d):
    for kp in fc.keyframe_points:
        kp.interpolation = "CONSTANT"

_m = {}


def mat(hexstr, rough=0.7, metal=0.0, emit=0.0):
    k = (hexstr, rough, metal, emit)
    if k in _m:
        return _m[k]
    h = hexstr.lstrip("#")
    col = tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1.0,)
    m = bpy.data.materials.new("m_" + h)
    m.diffuse_color = col
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = col
        b.inputs["Emission Strength"].default_value = emit
    _m[k] = m
    return m


def fin(o, name, loc, color, parent, rough=0.7, metal=0.0, emit=0.0):
    o.name = name
    o.location = loc
    o.data.materials.append(mat(color, rough, metal, emit))
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    sc.collection.objects.link(o)
    o.location = loc
    if parent:
        o.parent = parent
    return o


def box(name, size, loc, color, parent=None, pivot_top=False, rot=None, **kw):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.active_object
    if pivot_top:
        o.data.transform(Matrix.Translation((0, 0, -0.5)))
    o.scale = size
    if rot:
        o.rotation_euler = [radians(a) for a in rot]
    return fin(o, name, loc, color, parent, **kw)


def ball(name, r, loc, color, parent=None, scale=(1, 1, 1), **kw):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=20, ring_count=10)
    o = bpy.context.active_object
    o.scale = scale
    bpy.ops.object.shade_smooth()
    return fin(o, name, loc, color, parent, **kw)


def cyl(name, r, d, loc, color, parent=None, rot=None, pivot_top=False, **kw):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=20)
    o = bpy.context.active_object
    if pivot_top:
        o.data.transform(Matrix.Translation((0, 0, -d / 2)))
    if rot:
        o.rotation_euler = [radians(a) for a in rot]
    bpy.ops.object.shade_smooth()
    return fin(o, name, loc, color, parent, **kw)


def text(name, body, size, loc, color, parent=None, rot=(90, 0, 0), emit=0.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body, cu.size, cu.align_x = body, size, "CENTER"
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    o.rotation_euler = [radians(a) for a in rot]
    return fin(o, name, loc, color, parent, 0.6, 0, emit)


def area(name, loc, energy, size=4, color=(1, 1, 1), rot=(0, 0, 0)):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.size, d.color = energy, size, color
    o = bpy.data.objects.new(name, d)
    sc.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = [radians(a) for a in rot]
    return o


def key(o, f, loc=None, rot=None, scale=None):
    if loc is not None:
        o.location = loc
        o.keyframe_insert("location", frame=f)
    if rot is not None:
        o.rotation_euler = [radians(a) for a in rot]
        o.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        o.scale = scale
        o.keyframe_insert("scale", frame=f)


def only_in(o, ranges):
    for ob in [o] + list(o.children_recursive):
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=1)
        for a, b in ranges:
            ob.hide_render = False
            ob.keyframe_insert("hide_render", frame=a)
            ob.hide_render = True
            ob.keyframe_insert("hide_render", frame=b + 1)


def person(name, shirt, pants, skin, hair, beard=None, h=1.0, loc=(0, 0, 0), rz=0):
    r = empty(name, loc)
    r.rotation_euler = (0, 0, radians(rz))
    s = h
    for side, x in (("L", -0.10 * s), ("R", 0.10 * s)):
        cyl(f"{name}_leg{side}", 0.085 * s, 0.84 * s, (x, 0, 0.47 * s), pants, r)
        box(f"{name}_shoe{side}", (0.16 * s, 0.30 * s, 0.09 * s), (x, -0.05 * s, 0.045 * s), "#0c0c0c", r, rough=0.35)
    box(f"{name}_hips", (0.40 * s, 0.23 * s, 0.18 * s), (0, 0, 0.93 * s), pants, r)
    box(f"{name}_torso", (0.43 * s, 0.24 * s, 0.50 * s), (0, 0, 1.25 * s), shirt, r)
    ball(f"{name}_sh", 0.14 * s, (0, 0, 1.44 * s), shirt, r, (1.75, 0.85, 0.55))
    head = empty(f"{name}_headpivot", (0, 0, 1.52 * s), r)
    cyl(f"{name}_neck", 0.05 * s, 0.10 * s, (0, 0, 0), skin, head)
    ball(f"{name}_head", 0.115 * s, (0, 0, 0.12 * s), skin, head, (0.9, 1.0, 1.12))
    ball(f"{name}_hair", 0.118 * s, (0, 0.028 * s, 0.165 * s), hair, head, (0.92, 1.0, 0.95))
    box(f"{name}_nose", (0.03 * s, 0.04 * s, 0.04 * s), (0, -0.115 * s, 0.11 * s), skin, head)
    if beard:
        ball(f"{name}_beard", 0.10 * s, (0, -0.035 * s, 0.045 * s), beard, head, (0.92, 0.95, 0.85))
    arms = []
    for side, x in (("L", -0.27 * s), ("R", 0.27 * s)):
        a = cyl(f"{name}_arm{side}", 0.05 * s, 0.58 * s, (x, 0, 1.44 * s), shirt, r, pivot_top=True)
        ball(f"{name}_hand{side}", 0.055 * s, (0, 0, -0.62 * s), skin, a)
        arms.append(a)
    return r, arms[0], arms[1], head


def car(name, loc, rz, paint, parent=None, hero=False, ute=False):
    r = empty(name, loc, parent)
    r.rotation_euler = (0, 0, radians(rz))
    L = 5.2 if ute else 4.4
    box(name + "_body", (1.80, L, 0.62), (0, 0, 0.63), paint, r, rough=0.3, metal=0.5)
    box(name + "_cabin", (1.56, 1.9 if ute else 2.2, 0.52), (0, -0.6 if ute else 0.35, 1.2), "#161a22", r, rough=0.1, metal=0.4)
    if hero:
        box(name + "_spoiler", (1.40, 0.35, 0.05), (0, 1.5, 1.47), paint, r, rough=0.25, metal=0.6)
        text(name + "_badge", "HYBRID", 0.09, (0.91, -1.2, 0.86), "#d9dde2", r, rot=(90, 0, 90))
        box(name + "_frame", (0.52, 0.03, 0.16), (0, 2.21, 0.50), "#0F2747", r)   # Monsoor plate frame
    for x in (-0.62, 0.62):
        box(f"{name}_hl{x}", (0.40, 0.05, 0.10), (x, -L / 2 - 0.02, 0.80), "#fff3cf", r, emit=2.5)
        box(f"{name}_tl{x}", (0.40, 0.05, 0.10), (x, L / 2 + 0.02, 0.84), "#c01818", r, emit=2.0)
    for i, (x, y) in enumerate([(-0.9, -L / 3), (0.9, -L / 3), (-0.9, L / 3), (0.9, L / 3)]):
        cyl(f"{name}_w{i}", 0.34, 0.24, (x, y, 0.34), "#121316", r, rot=(0, 90, 0), rough=0.8)
        if hero:
            cyl(f"{name}_rim{i}", 0.22, 0.26, (x, y, 0.34), "#c8ccd2", r, rot=(0, 90, 0), rough=0.3, metal=0.8)
    return r


# ---------------- SET A: NIGHT SERVO (x = +80) ----------------
SX = 80
box("sv_ground", (60, 50, 0.1), (SX, 6, -0.05), "#2f3136", rough=0.35)
box("sv_road", (90, 9, 0.02), (SX, -10, 0.01), "#1e1f22", rough=0.6)
box("sv_canopy", (16, 10, 0.6), (SX, 2, 5.2), "#e9ecef", emit=0.4)
for x in (-6, 0, 6):
    area(f"sv_down{x}", (SX + x, 2, 4.8), 4000, 4, (0.92, 0.96, 1.0), rot=(0, 0, 0))
for x in (-6, 6):
    box(f"sv_col{x}", (0.45, 0.45, 5), (SX + x, 2, 2.5), "#d8dbe0")
board = empty("price_board", (SX - 10, -6, 0))
box("pb_post", (0.4, 0.4, 5), (0, 0, 2.5), "#3a3d42", board)
box("pb_face", (2.2, 0.3, 2.8), (0, 0, 5.4), "#0a0d18", board)
price = text("pb_price", "1.799", 0.55, (0, -0.17, 5.4), "#ffcf3a", board, emit=6.0)
box("sv_shop", (12, 7, 3.6), (SX + 3, 13, 1.8), "#3a3a3a")
for x in range(-40, 41, 12):   # streetlights along the road
    cyl(f"sl_pole{x}", 0.06, 6, (SX + x, -14.5, 3), "#55585e")
    area(f"sl_light{x}", (SX + x, -12.5, 5.8), 2500, 3, (1.0, 0.75, 0.45))
area("sv_fill", (SX - 20, -20, 8), 6000, 12, (0.55, 0.65, 1.0), rot=(55, 0, -40))
box("sv_shopglass", (9, 0.1, 2.2), (SX + 3, 9.45, 1.3), "#ffd9a0", emit=2.5)
pumps = []
for i, x in enumerate((-4, 4)):
    p = empty(f"pump{i}", (SX + x, 0.8, 0))
    box(f"pump{i}_b", (0.9, 0.55, 1.9), (0, 0, 0.95), "#e4e7ea", p)
    box(f"pump{i}_s", (0.6, 0.04, 0.3), (0, -0.29, 1.45), "#7dff8a", p, emit=2.0)
    pumps.append(p)
queue_cols = ["#8a8f96", "#d6d8db", "#3c4a5c", "#6e2b2b", "#e8e8e8", "#2b2d31", "#94a0ab", "#5d6b3a"]
for i in range(8):
    car(f"q{i}", (SX - 4 - i * 0.0, -2.6 - i * 5.2, 0) if i < 2 else (SX - 12 - (i - 2) * 5.4, -7.6, 0),
        0 if i < 2 else 90, queue_cols[i], ute=(i % 3 == 0))
dave_car = car("dave_car", (SX + 4 + 1.3, 0.6, 0), 0, "#7a7f86")
bpy.data.objects["dave_car_cabin"].hide_render = True   # previs: see Mia through the "glass"
dave, dv_l, dv_r, dv_h = person("Dave", "#2c3e5c", "#c2ae86", "#c99d7c", "#5b4630", loc=(SX + 4.1, -0.4, 0), rz=-60)
mia_in_car = person("MiaCar", "#1f2a44", "#7c7f86", "#d8ae90", "#8a6a45", h=0.6, loc=(SX + 5.6, 1.4, 0.55), rz=0)[0]
chr_n = car("CHR_night", (SX - 30, -7.6, 0), 90, "#0b0c0e", hero=True)
arf_n, an_l, an_r, an_h = person("ArfanNight", "#0c0c0d", "#3a2618", "#b98a66", "#0d0d0d", beard="#0d0d0d", loc=(SX - 5.7, -1.6, 0), rz=-90)
only_in(arf_n, [SHOTS["S4"]])
only_in(mia_in_car, [SHOTS["S2c"], SHOTS["S5"]])

# price ticking in S1
def tick(scn, *a):
    f = scn.frame_current
    if f <= 72:
        price.data.body = "%.3f" % (1.799 + 0.010 * min(8, f // 8))
bpy.app.handlers.frame_change_pre.append(tick)

# Dave at the pump: hand on nozzle, then the pained head-drop (S2b)
for f, ax in [(1, 0), (121, -55), (156, -55)]:
    key(dv_r, f, rot=(ax, 0, 0))
key(dv_h, 121, rot=(0, 0, 0))
key(dv_h, 138, rot=(-14, 0, 6))
key(dv_h, 156, rot=(-18, 0, -4))
# S3 the C-HR glides in on the road and turns into pump 0's free lane; heads turn
key(chr_n, 193, (SX - 30, -10.0, 0), (0, 0, 90))
key(chr_n, 240, (SX - 8, -10.0, 0), (0, 0, 90))
key(chr_n, 264, (SX - 4, -2.4, 0), (0, 0, 0))
key(chr_n, 360, (SX - 4, -2.4, 0), (0, 0, 0))
key(chr_n, 361, (SX - 4, -2.4, 0), (0, 0, 0))
key(chr_n, 432, (SX + 30, -10.0, 0), (0, 0, 90))
key(dv_h, 230, rot=(0, 0, 0))
key(dv_h, 250, rot=(0, 0, -55))      # Dave's head follows the silent car
key(dv_h, 432, rot=(0, 0, -70))
# S4 Arfan: easy step out, cheeky glance and nod to the queue, small shrug, nozzle in
key(arf_n, 265, (SX - 5.7, -1.8, 0), (0, 0, -90))
key(arf_n, 300, (SX - 5.7, -0.9, 0), (0, 0, -150))
key(an_h, 265, rot=(0, 0, 0))
key(an_h, 290, rot=(-6, 0, 18))      # glance at the queue
key(an_h, 300, rot=(4, 0, 18))       # the nod
key(an_h, 312, rot=(-5, 0, 12))      # half-smile, chin a touch down
key(an_h, 360, rot=(-5, 0, 0))
for f, ax, ay in [(265, 0, 0), (296, -25, -10), (306, -25, -10), (314, 0, 0), (330, -60, 0), (360, -60, 0)]:
    key(an_r, f, rot=(ax, ay, 0))
for f, ay in [(265, 0), (318, 0), (324, 12), (332, 0)]:   # the small shrug
    key(an_l, f, rot=(0, ay, 0))

# ---------------- SET B: MONSOOR YARD, DAY (origin) ----------------
box("yd_ground", (60, 60, 0.1), (0, 8, -0.05), "#a5503d", rough=0.85)   # red brick paving
box("yd_fence", (30, 0.2, 2.4), (0, 14, 1.2), "#1d4fb0")                   # the blue sign next door
for x in (-6, 5):
    cyl(f"yd_palmtrunk{x}", 0.18, 7, (x, 17, 3.5), "#7a6449")
    ball(f"yd_palm{x}", 1.8, (x, 17, 7.3), "#3d6b2c", scale=(1, 1, 0.45))
for i, x in enumerate((-7, -4.4, -1.8, 0.8, 3.4, 6)):
    car(f"yd_car{i}", (x, 9.5, 0), 180, ["#b8bcc2", "#2b3a55", "#f0f0f0", "#6d7277", "#f0f0f0", "#3a3d42"][i])
for x in (-3.2, 3.6):
    cyl(f"flagpole{x}", 0.03, 4.0, (x, 4.2, 2.0), "#222222")
    box(f"flag{x}", (0.7, 0.03, 2.8), (x + 0.35, 4.2, 2.6), "#151515")
    box(f"flagmark{x}", (0.45, 0.035, 0.45), (x + 0.35, 4.19, 3.4), "#c62828")
chr_y = car("CHR_yard", (1.2, 3.2, 0), -70, "#0b0c0e", hero=True)
mons, m_l, m_r, m_h = person("Monsoor", "#141414", "#1a1a1a", "#b8875f", "#4a4a4a", beard="#5c5c5c", h=0.97, loc=(-0.55, 0.2, 0), rz=10)
arf_y, ay_l, ay_r, ay_h = person("ArfanYard", "#0c0c0d", "#3a2618", "#b98a66", "#0d0d0d", beard="#0d0d0d", loc=(0.75, 0.6, 0), rz=-30)
dave_y, dy_l, dy_r, dy_h = person("DaveYard", "#2c3e5c", "#c2ae86", "#c99d7c", "#5b4630", loc=(-0.4, -1.3, 0), rz=170)
mia_y, my_l, my_r, my_h = person("MiaYard", "#1f2a44", "#7c7f86", "#d8ae90", "#8a6a45", h=0.6, loc=(0.15, -1.6, 0), rz=170)
only_in(dave_y, [SHOTS["S6a"]])
only_in(mia_y, [SHOTS["S6a"]])
# S6a Monsoor hands Dave the keys (open palm, like his 3MT video), Mia bounces
for f, ax in [(433, 0), (450, -60), (470, -60), (484, -20)]:
    key(m_r, f, rot=(ax, 0, 0))
for f, ax in [(433, 0), (456, -55), (480, -55)]:
    key(dy_r, f, rot=(ax, 0, 0))
for f, z in [(433, 0), (446, 0.12), (452, 0), (462, 0.12), (468, 0)]:
    key(mia_y, f, loc=(0.15, -1.6, z))
# S6b Monsoor turns, hand on Arfan's shoulder: "Good job." Arfan, humble, looks at him.
key(mons, 493, (-0.55, 0.2, 0), (0, 0, 10))
key(mons, 512, (0.05, 0.55, 0), (0, 0, -70))
key(m_h, 493, rot=(0, 0, 0))
key(m_h, 512, rot=(-4, 0, -10))
for f, ax, ay in [(493, -20, 0), (510, -20, 0), (522, -95, -58), (564, -95, -58)]:
    key(m_l, f, rot=(ax, ay, 0))      # left hand lands on Arfan's shoulder
key(arf_y, 493, (0.75, 0.6, 0), (0, 0, -30))
key(arf_y, 520, (0.75, 0.6, 0), (0, 0, 55))     # turns to Monsoor
key(ay_h, 520, rot=(0, 0, 0))
key(ay_h, 534, rot=(-9, 0, 6))                   # humble chin-down, small smile
key(ay_h, 548, rot=(-4, 0, -4))                  # eyebrow lift on "a lot"
key(ay_h, 564, rot=(-7, 0, 0))
for f, ax, ay in [(493, 0, 0), (536, 0, 0), (546, -40, -30), (558, -40, -30), (564, -30, -20)]:
    key(ay_r, f, rot=(ax, ay, 0))      # hand to chest, briefly

# ---------------- SET C: FAMILY HOME, GOLDEN HOUR (x = -80) ----------------
HX = -80
box("hm_ground", (50, 50, 0.1), (HX, 6, -0.05), "#6f8f47", rough=0.95)
box("hm_street", (80, 8, 0.02), (HX, -10, 0.01), "#3b3d42")
box("hm_drive", (4.4, 12, 0.03), (HX + 2.4, -2.8, 0.02), "#a9a49a")
box("hm_house", (12, 8, 3.0), (HX, 6, 1.5), "#c8955f")
box("hm_roof", (12.6, 8.6, 0.5), (HX, 6, 3.3), "#9b4a33")
box("hm_garage", (4.0, 0.1, 2.4), (HX + 2.4, 1.95, 1.2), "#e3d8c3")
box("hm_letterbox", (0.4, 0.4, 1.0), (HX - 1.0, -6.2, 0.5), "#a5683f")
ball("hm_tree", 1.7, (HX - 6.5, 0.5, 3.0), "#4f7a38")
cyl("hm_trunk", 0.18, 2.2, (HX - 6.5, 0.5, 1.1), "#5a3d26")
chr_h = car("CHR_home", (HX + 2.4, -12, 0), 180, "#0b0c0e", hero=True)
key(chr_h, 565, (HX + 2.4, -13.0, 0), (0, 0, 180))
key(chr_h, 610, (HX + 2.4, -3.0, 0), (0, 0, 180))
dave_h, dh_l, dh_r, dh_hd = person("DaveHome", "#2c3e5c", "#c2ae86", "#c99d7c", "#5b4630", loc=(HX - 0.4, -2.2, 0), rz=-20)
mia_h, mh_l, mh_r, mh_hd = person("MiaHome", "#1f2a44", "#7c7f86", "#d8ae90", "#8a6a45", h=0.6, loc=(HX - 1.6, 1.5, 0), rz=-150)
key(mia_h, 600, (HX - 1.6, 1.5, 0))
key(mia_h, 630, (HX + 1.0, -1.6, 0))      # runs to the car
for f, ax in [(600, 0), (612, -150), (622, -110), (632, -150), (672, -150)]:
    key(mh_r, f, rot=(ax, 0, 0))
key(dh_hd, 630, rot=(0, 0, 0))
key(dh_hd, 650, rot=(-4, 0, 30))           # looks at the car, then down the street, pleased
key(dh_hd, 672, rot=(2, 0, -25))

# ---------------- CAMERAS (commercial setups) ----------------
cams = {}


def camera(name, lens, parent=None, fstop=None, focus=None):
    c = bpy.data.cameras.new(name)
    c.lens = lens
    c.clip_start, c.clip_end = 0.05, 400
    if fstop:
        c.dof.use_dof = True
        c.dof.aperture_fstop = fstop
    o = bpy.data.objects.new(name, c)
    sc.collection.objects.link(o)
    if parent:
        o.parent = parent
    t = empty(name + "_t", (0, 0, 0), parent)
    con = o.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = t, "TRACK_NEGATIVE_Z", "UP_Y"
    if focus is not None:
        c.dof.focus_object = focus
    cams[name] = o
    return o, t


def move(cam, tgt, f0, f1, c0, c1, t0, t1):
    key(cam, f0, c0)
    key(cam, f1, c1)
    key(tgt, f0, t0)
    key(tgt, f1, t1)


# S1 50mm low push-in on the price board, queue lights behind
c, t = camera("C1", 50, fstop=2.0)
move(c, t, 1, 72, (SX - 13.0, -10.5, 1.4), (SX - 12.0, -9.2, 2.2), (SX - 10, -6, 5.3), (SX - 10, -6, 5.4))
# S2a crane down over the queue (24mm)
c, t = camera("C2a", 24)
move(c, t, 73, 120, (SX - 22, -16, 9.0), (SX - 18, -14, 4.0), (SX - 6, -6, 0.5), (SX - 5, -5, 0.8))
# S2b 50mm on Dave at the pump, slow dolly in
c, t = camera("C2b", 50, fstop=2.2)
move(c, t, 121, 156, (SX + 1.6, -3.4, 1.55), (SX + 2.2, -2.9, 1.55), (SX + 4.1, -0.4, 1.55), (SX + 4.1, -0.4, 1.5))
# S2c 85mm through the back window on Mia asleep
c, t = camera("C2c", 85, fstop=4.0)
move(c, t, 157, 192, (SX + 8.6, -0.2, 1.5), (SX + 8.4, -0.1, 1.48), (SX + 5.6, 1.4, 1.45), (SX + 5.6, 1.4, 1.45))
# S3 low tracking car rig beside the C-HR (24mm), then it swings in
c, t = camera("C3", 24)
move(c, t, 193, 264, (SX - 27, -13.2, 0.7), (SX - 10, -13.0, 1.1), (SX - 22, -10.0, 0.7), (SX - 4, -2.4, 0.8))
# S4 50mm gimbal arc on Arfan
c, t = camera("C4", 50, fstop=2.0)
move(c, t, 265, 360, (SX - 8.6, -3.4, 1.55), (SX - 7.6, -4.4, 1.5), (SX - 5.7, -1.4, 1.55), (SX - 5.7, -0.9, 1.6))
# S5 35mm two-shot from inside Dave's car: Dave in the foreground, Mia behind, C-HR leaving
c, t = camera("C5", 28, fstop=2.8)
move(c, t, 361, 432, (SX + 4.75, 0.35, 1.78), (SX + 4.7, 0.3, 1.78), (SX + 1.5, -8.0, 1.2), (SX + 0.0, -9.5, 1.2))
# S6a 35mm wide at the yard, slow push
c, t = camera("C6a", 35, fstop=4)
move(c, t, 433, 492, (-1.5, -6.6, 1.6), (-1.1, -5.6, 1.6), (0.0, 0.0, 1.2), (0.1, 0.0, 1.25))
# S6b 85mm two-shot on Monsoor and Arfan, push-in
c, t = camera("C6b", 85, fstop=2.0)
move(c, t, 493, 564, (0.6, -6.5, 1.55), (0.5, -5.6, 1.55), (0.15, 0.5, 1.55), (0.2, 0.55, 1.58))
# S7 golden hour: 35mm low as the C-HR rolls in, then a crane-up pull-back over the family
c, t = camera("C7", 35)
move(c, t, 565, 672, (HX - 3.0, -9.0, 0.9), (HX - 5.5, -14.0, 5.5), (HX + 2.4, -6.0, 0.8), (HX + 1.0, -1.5, 1.0))
# S8 brand card over the held last frame
c, t = camera("C8", 35)
move(c, t, 673, 696, (HX - 5.5, -14.0, 5.5), (HX - 5.6, -14.2, 5.6), (HX + 1.0, -1.5, 1.0), (HX + 1.0, -1.5, 1.0))

for s, cname in [("S1", "C1"), ("S2a", "C2a"), ("S2b", "C2b"), ("S2c", "C2c"), ("S3", "C3"), ("S4", "C4"),
                 ("S5", "C5"), ("S6a", "C6a"), ("S6b", "C6b"), ("S7", "C7"), ("S8", "C8")]:
    sc.timeline_markers.new(s, frame=SHOTS[s][0]).camera = cams[cname]
sc.camera = cams["C1"]

if SAVE_BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_BLEND)
if TEST_FRAMES:
    for f in TEST_FRAMES:
        sc.frame_set(f)
        sc.render.filepath = FRAMES_DIR.rstrip("/") + "/f_%04d.png" % f
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
