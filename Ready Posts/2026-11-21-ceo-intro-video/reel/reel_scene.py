"""3D animatic for the 29 s Monsoor Motors teaser reel: a short, funny story.

Run:  blender -b -P reel_scene.py -- <frames_dir> [file.blend] [frame frame ...]
540x960, 24 fps, 696 frames (29.0 s). Three sets far apart in one scene:
  servo (x=+80), Japanese auction yard (origin), family home (x=-80).
People face -Y by default. Sizes in metres.
"""
import sys
from math import radians, cos, sin

import bpy
from mathutils import Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FRAMES_DIR = argv[0] if argv else "/tmp/reel_frames"
SAVE_BLEND = next((a for a in argv[1:] if a.endswith(".blend")), None)
TEST_FRAMES = [int(a) for a in argv[1:] if a.isdigit()]
END = 696

# Shot table (first frame, last frame). Must match reel_post.py.
SHOTS = {
    "S1": (1, 60), "S2": (61, 134), "S3": (135, 194), "S4": (195, 302),
    "S5a": (303, 354), "S5b": (355, 405), "S5c": (406, 456), "S5d": (457, 506),
    "S6": (507, 558), "S7": (559, 624), "S8": (625, 696),
}

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, END
scene.render.resolution_x, scene.render.resolution_y = 540, 960
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = FRAMES_DIR.rstrip("/") + "/f_"
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
    try:
        scene.render.engine = eng
        break
    except Exception:
        pass
try:
    scene.eevee.taa_render_samples = 12
except Exception:
    pass
try:
    scene.view_settings.view_transform = "Standard"
except Exception:
    pass

world = bpy.data.worlds.new("World")
scene.world = world
world.color = (0.62, 0.76, 0.93)
try:
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.62, 0.76, 0.93, 1.0)
    bg.inputs[1].default_value = 1.1
except Exception:
    pass
sun_d = bpy.data.lights.new("Sun", "SUN")
sun_d.energy = 3.4
sun = bpy.data.objects.new("Sun", sun_d)
scene.collection.objects.link(sun)
sun.rotation_euler = (radians(50), 0, radians(-38))

_m = {}


def mat(hexstr, rough=0.7, metal=0.0, emit=0.0):
    k = (hexstr, rough, metal, emit)
    if k in _m:
        return _m[k]
    h = hexstr.lstrip("#")
    col = tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1.0,)
    m = bpy.data.materials.new("m_" + h)
    m.diffuse_color = col
    try:
        m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = col
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal
        if emit:
            b.inputs["Emission Color"].default_value = col
            b.inputs["Emission Strength"].default_value = emit
    except Exception:
        pass
    _m[k] = m
    return m


def fin(obj, name, loc, color, parent, rough=0.7, metal=0.0, emit=0.0):
    obj.name = name
    obj.location = loc
    obj.data.materials.append(mat(color, rough, metal, emit))
    if parent:
        obj.parent = parent
    return obj


def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
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
    scene.collection.objects.link(o)
    o.rotation_euler = [radians(a) for a in rot]
    return fin(o, name, loc, color, parent, 0.6, 0, emit)


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


def visible(o, ranges):
    """Show o only inside the given (first, last) frame ranges (and its children)."""
    objs = [o] + list(o.children_recursive)
    for ob in objs:
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=1)
        for a, b in ranges:
            ob.hide_render = False
            ob.keyframe_insert("hide_render", frame=a)
            ob.hide_render = True
            ob.keyframe_insert("hide_render", frame=b + 1)


def person(name, shirt, pants, skin, hair, beard=None, h=1.0, root_loc=(0, 0, 0)):
    r = empty(name, root_loc)
    s = h
    for side, x in (("L", -0.10 * s), ("R", 0.10 * s)):
        cyl(f"{name}_leg{side}", 0.085 * s, 0.84 * s, (x, 0, 0.47 * s), pants, r)
        box(f"{name}_shoe{side}", (0.16 * s, 0.30 * s, 0.09 * s), (x, -0.05 * s, 0.045 * s), "#0c0c0c", r, rough=0.35)
    box(f"{name}_hips", (0.40 * s, 0.23 * s, 0.18 * s), (0, 0, 0.93 * s), pants, r)
    box(f"{name}_torso", (0.43 * s, 0.24 * s, 0.50 * s), (0, 0, 1.25 * s), shirt, r)
    ball(f"{name}_sh", 0.14 * s, (0, 0, 1.44 * s), shirt, r, (1.75, 0.85, 0.55))
    cyl(f"{name}_neck", 0.05 * s, 0.10 * s, (0, 0, 1.52 * s), skin, r)
    ball(f"{name}_head", 0.115 * s, (0, 0, 1.64 * s), skin, r, (0.9, 1.0, 1.12))
    ball(f"{name}_hair", 0.118 * s, (0, 0.028 * s, 1.685 * s), hair, r, (0.92, 1.0, 0.95))
    box(f"{name}_nose", (0.03 * s, 0.04 * s, 0.04 * s), (0, -0.115 * s, 1.63 * s), skin, r)
    if beard:
        ball(f"{name}_beard", 0.10 * s, (0, -0.035 * s, 1.565 * s), beard, r, (0.92, 0.95, 0.85))
    arms = []
    for side, x in (("L", -0.27 * s), ("R", 0.27 * s)):
        a = cyl(f"{name}_arm{side}", 0.05 * s, 0.58 * s, (x, 0, 1.44 * s), shirt, r, pivot_top=True)
        ball(f"{name}_hand{side}", 0.055 * s, (0, 0, -0.62 * s), skin, a)
        arms.append(a)
    return r, arms[0], arms[1]


def car(name, loc, rz, paint, parent=None, hero=False):
    r = empty(name, loc, parent)
    r.rotation_euler = (0, 0, radians(rz))
    box(name + "_body", (1.78, 4.30, 0.60), (0, 0, 0.62), paint, r, rough=0.25, metal=0.6)
    box(name + "_cabin", (1.55, 2.15, 0.50), (0, 0.40, 1.17), "#1b2028", r, rough=0.1, metal=0.4)
    if hero:
        box(name + "_roof", (1.50, 1.75, 0.06), (0, 0.40, 1.44), paint, r, rough=0.25, metal=0.6)
        box(name + "_spoiler", (1.40, 0.35, 0.05), (0, 1.55, 1.46), paint, r, rough=0.25, metal=0.6)
        for x in (-0.62, 0.62):
            box(name + f"_lt{x}", (0.42, 0.06, 0.11), (x, -2.16, 0.80), "#fff6cf", r, emit=0.6)
            box(name + f"_tl{x}", (0.42, 0.06, 0.11), (x, 2.16, 0.84), "#b01818", r)
        text(name + "_badge", "HYBRID", 0.09, (0.91, -1.2, 0.86), "#d9dde2", r, rot=(90, 0, 90))
    for i, (x, y) in enumerate([(-0.9, -1.40), (0.9, -1.40), (-0.9, 1.38), (0.9, 1.38)]):
        cyl(f"{name}_w{i}", 0.34, 0.24, (x, y, 0.34), "#121316", r, rot=(0, 90, 0), rough=0.8)
        if hero:
            cyl(f"{name}_rim{i}", 0.22, 0.26, (x, y, 0.34), "#c8ccd2", r, rot=(0, 90, 0), rough=0.3, metal=0.8)
            if y < 0:
                box(f"{name}_cal{i}", (0.05, 0.16, 0.12), (x * 0.86, y, 0.40), "#1f4fd8", r)
    return r


# ====================== SET 1: SERVO (x = +80) ======================
SX = 80
box("servo_ground", (40, 40, 0.1), (SX, 4, -0.05), "#55585e", rough=0.9)
box("servo_road", (60, 8, 0.02), (SX, -8, 0.01), "#3b3d42", rough=0.95)
box("servo_canopy", (14, 9, 0.6), (SX, 2, 5.2), "#e9ecef")
box("servo_canopy_band", (14.05, 9.05, 0.22), (SX, 2, 4.95), "#d23b2a")
for x in (-5, 5):
    box(f"servo_col{x}", (0.4, 0.4, 5), (SX + x, 2, 2.5), "#d8dbe0")
pump = empty("pump", (SX, 0.6, 0))
box("pump_body", (0.9, 0.55, 1.9), (0, 0, 0.95), "#e4e7ea", pump)
box("pump_top", (0.95, 0.6, 0.25), (0, 0, 2.0), "#d23b2a", pump)
box("pump_screen", (0.6, 0.04, 0.3), (0, -0.29, 1.45), "#0d1a10", pump, emit=0.3)
digits = text("pump_digits", "$ 0.00", 0.12, (0, -0.32, 1.40), "#7dff8a", pump, emit=3.0)
car("dad_old_car", (SX + 1.6, 0.4, 0), 0, "#7a7f86")
box("shop", (10, 6, 3.5), (SX + 2, 12, 1.75), "#f2efe8")
text("shop_sign", "SERVO", 0.8, (SX + 2, 8.95, 3.0), "#d23b2a", emit=0.4)
dad, dad_l, dad_r = person("Dad", "#5a7fa8", "#3d4450", "#c79c7a", "#2b2016", h=1.0, root_loc=(SX + 0.7, -0.2, 0))
dad.rotation_euler = (0, 0, radians(-150))
wallet = empty("wallet", (0, -0.32, 1.05), dad)
box("wallet_l", (0.11, 0.02, 0.09), (-0.055, 0, 0), "#4a2d18", wallet, rot=(0, 0, 25))
box("wallet_r", (0.11, 0.02, 0.09), (0.055, 0, 0), "#4a2d18", wallet, rot=(0, 0, -25))
moth = empty("moth", (SX + 0.7, -0.52, 1.10))
ball("moth_body", 0.012, (0, 0, 0), "#8a7f6a", moth, (1, 2.5, 1))
box("moth_wl", (0.05, 0.035, 0.004), (-0.028, 0, 0), "#b8ad94", moth)
box("moth_wr", (0.05, 0.035, 0.004), (0.028, 0, 0), "#b8ad94", moth)
key(moth, 1, (SX + 0.7, -0.52, 1.10))
key(moth, 30, (SX + 0.7, -0.52, 1.10))
key(moth, 44, (SX + 0.55, -0.62, 1.38))
key(moth, 60, (SX + 0.85, -0.75, 1.75))
for f, ax in [(1, 0), (14, -70), (60, -70)]:
    key(dad_r, f, rot=(ax, 0, 0))
key(wallet, 1, scale=(0.01, 0.01, 0.01))
key(wallet, 22, scale=(0.01, 0.01, 0.01))
key(wallet, 26, scale=(1, 1, 1))

# ====================== SET 2: AUCTION YARD (origin) ======================
box("yard_ground", (70, 70, 0.1), (0, 10, -0.05), "#6f7277", rough=0.9)
for x in (-1.6, 1.4):
    box(f"bay{x}", (0.10, 4.6, 0.01), (x, -0.2, 0.03), "#eceff2")
hall = empty("hall", (0, 22, 0))
box("hall_body", (34, 9, 7.5), (0, 0, 3.75), "#c9ced4", hall, metal=0.3, rough=0.5)
box("hall_glass", (20, 0.1, 1.2), (0, -4.52, 5.0), "#7fa7c4", hall, rough=0.1, metal=0.5)
box("hall_sign", (9, 0.15, 1.3), (0, -4.6, 6.6), "#1f4fae", hall)
text("hall_sign_t", "AUTO AUCTION", 0.62, (0, -4.72, 6.35), "#ffffff", hall)
box("hall_canopy", (12, 2.2, 0.18), (0, -5.6, 3.6), "#d8dbe0", hall)
paints = ["#f2f3f5", "#c3c7cc", "#1b1d21", "#f2f3f5", "#25385c", "#c3c7cc", "#f2f3f5", "#2a2c30"]
k = 0
for row, y in enumerate((7.0, 10.6, 14.2)):
    for i in range(14):
        x = -15.6 + i * 2.4
        car(f"auc_{row}_{i}", (x, y, 0), 0, paints[k % len(paints)])
        box(f"lot_{row}_{i}", (0.30, 0.02, 0.22), (x + 0.45, y - 1.35, 1.25), "#ffffff", rough=0.9)
        k += 1
for x in (-17, 17):
    cyl(f"pole{x}", 0.08, 11, (x, 4, 5.5), "#9aa0a6", metal=0.7)
    box(f"lamps{x}", (1.6, 0.4, 0.3), (x, 4, 11), "#9aa0a6")
for x in (-3.4, 3.8):
    cyl(f"cone{x}", 0.18, 0.55, (x, 4.8, 0.27), "#ff6a13")
chr_ = car("CHR", (0.45, 3.4, 0), -62, "#0d0e10", hero=True)
monsoor, m_l, m_r = person("Monsoor", "#141414", "#1a1a1a", "#b8875f", "#8c8c8c", beard="#9a9a9a", h=0.97, root_loc=(-0.42, 0, 0))
arfan, a_l, a_r = person("Arfan", "#0c0c0d", "#3a2618", "#b98a66", "#0d0d0d", beard="#0d0d0d", root_loc=(0.42, 0.08, 0))
key(monsoor, 1, rot=(0, 0, 18))
key(monsoor, 195, rot=(0, 0, 18))
key(monsoor, 230, rot=(0, 0, 34))
key(arfan, 1, rot=(0, 0, -16))
key(arfan, 170, rot=(0, 0, -16))
key(arfan, 205, rot=(0, 0, 0))
key(arfan, 280, rot=(0, 0, 20))
# S3 handshake + the over-keen shoulder slap
for f, ax, ay in [(1, 0, 0), (140, 0, 0), (152, -62, -18), (166, -62, -18), (170, 0, -70), (176, 0, -96), (182, 0, -70), (194, 0, 0)]:
    key(m_r, f, rot=(ax, ay, 0))
for f, ax, ay in [(1, 0, 0), (140, 0, 0), (152, -62, 18), (166, -62, 18), (176, 0, 0)]:
    key(a_l, f, rot=(ax, ay, 0))
key(arfan, 176, loc=(0.42, 0.08, 0))
key(arfan, 178, loc=(0.47, 0.08, -0.03))   # the slap lands
key(arfan, 184, loc=(0.42, 0.08, 0))
# S4: hand on heart on "means a lot", open palms on "hello mates"
for f, ax, ay in [(195, 0, 0), (205, -55, -20), (240, -55, -20), (252, 0, 0), (262, -35, 0), (300, -35, 0)]:
    key(a_r, f, rot=(ax, ay, 0))
for f, ax in [(252, 0), (262, -35), (300, -35), (302, 0)]:
    key(a_l, f, rot=(ax, 0, 0))

# S5b: Arfan crouched by the C-HR with a torch (separate copy, shown only in S5b)
arf_b, ab_l, ab_r = person("ArfanTorch", "#0c0c0d", "#3a2618", "#b98a66", "#0d0d0d", beard="#0d0d0d", root_loc=(-2.25, 1.55, 0))
arf_b.rotation_euler = (radians(12), 0, radians(118))   # leaning in over the bonnet
torch = cyl("torch", 0.03, 0.22, (0, 0, -0.66), "#202226", ab_r, rot=(90, 0, 0))
key(ab_r, 355, rot=(-55, 0, 0))
key(ab_r, 380, rot=(-62, 0, 14))
key(ab_r, 405, rot=(-55, 0, -12))
visible(arf_b, [SHOTS["S5b"]])

# ====================== SET 3: FAMILY HOME (x = -80) ======================
HX = -80
box("home_ground", (40, 40, 0.1), (HX, 6, -0.05), "#6b8f4e", rough=0.95)
box("street", (60, 7, 0.02), (HX, -9, 0.01), "#3b3d42", rough=0.95)
box("driveway", (4.2, 11, 0.03), (HX + 2.4, -2.5, 0.02), "#a7a39b", rough=0.9)
box("house", (11, 8, 3.2), (HX, 6, 1.6), "#efe6d6")
box("roof", (11.6, 8.6, 0.4), (HX, 6, 3.6), "#7a3b2e", rot=(0, 0, 0))
box("garage", (3.6, 0.1, 2.5), (HX + 2.4, 1.94, 1.25), "#d8d2c4")
box("door", (1.0, 0.1, 2.1), (HX - 2.2, 1.94, 1.05), "#5b3a26")
for x in (-4.2, -0.4):
    box(f"win{x}", (1.6, 0.1, 1.1), (HX + x, 1.94, 1.8), "#9cc0dc", rough=0.1)
ball("tree", 1.6, (HX - 6.5, 1.0, 3.2), "#3e6b34")
cyl("trunk", 0.18, 2.4, (HX - 6.5, 1.0, 1.2), "#5a3d26")
dad_h, dh_l, dh_r = person("DadHome", "#5a7fa8", "#3d4450", "#c79c7a", "#2b2016", root_loc=(HX + 0.6, -1.6, 0))
kid, k_l, k_r = person("Kid", "#f2b43a", "#2f4e8c", "#c79c7a", "#2b2016", h=0.62, root_loc=(HX + 0.05, -1.75, 0))
arf_c, ac_l, ac_r = person("ArfanHome", "#0c0c0d", "#3a2618", "#b98a66", "#0d0d0d", beard="#0d0d0d", root_loc=(HX + 1.55, -1.35, 0))
key(arf_c, 1, rot=(0, 0, 70))
key(dad_h, 1, rot=(0, 0, -60))
key(kid, 1, rot=(0, 0, -30))
for f, ax in [(507, 0), (522, -60), (545, -60), (556, -20)]:
    key(ac_l, f, rot=(ax, 0, 0))
for f, ax in [(507, 0), (530, 0), (540, -60), (556, -60)]:
    key(dh_r, f, rot=(ax, 0, 0))
for f, ax in [(507, 0), (520, -150), (530, -120), (540, -150), (556, -150)]:   # kid cheering
    key(k_r, f, rot=(ax, 0, 0))
    key(k_l, f, rot=(ax, 0, 0))
visible(arf_c, [SHOTS["S6"]])
visible(dad_h, [SHOTS["S6"]])
visible(kid, [SHOTS["S6"], SHOTS["S8"]])

# The delivered C-HR: rolls up the driveway in S5d, parked in S6/S8, drives past the servo in S7.
dchr = car("CHR_delivery", (HX + 2.4, -12, 0), 0, "#0d0e10", hero=True)
dchr.rotation_euler = (0, 0, radians(180))
key(dchr, 457, (HX + 2.4, -9.5, 0), (0, 0, 180))
key(dchr, 500, (HX + 2.4, -2.6, 0), (0, 0, 180))
key(dchr, 558, (HX + 2.4, -2.6, 0), (0, 0, 180))
key(dchr, 559, (SX - 14, -8.6, 0), (0, 0, 90))          # S7: on the road past the servo
key(dchr, 624, (SX + 12, -8.6, 0), (0, 0, 90))
key(dchr, 625, (HX + 2.4, -2.6, 0), (0, 0, 180))         # S8: back home
dad_wave = empty("dad_wave_arm", (0, 0, 0), dchr)          # a waving hand out of the window
wv = cyl("wave_arm", 0.045, 0.45, (-0.95, -0.3, 1.25), "#c79c7a", dad_wave, rot=(0, 30, 0), pivot_top=True)
ball("wave_hand", 0.06, (0, 0, -0.48), "#c79c7a", wv)
for f, ay in [(559, 30), (570, 10), (580, 40), (590, 10), (600, 40), (612, 10), (624, 30)]:
    key(wv, f, rot=(0, ay, 0))
visible(dad_wave, [SHOTS["S7"]])
# end-card family: dad + kid next to the parked car
dad_e, de_l, de_r = person("DadEnd", "#5a7fa8", "#3d4450", "#c79c7a", "#2b2016", root_loc=(HX + 0.6, -3.2, 0))
key(dad_e, 1, rot=(0, 0, -20))
for f, ax in [(625, 0), (640, -140), (650, -110), (660, -140), (696, -140)]:
    key(de_r, f, rot=(ax, 0, 0))
visible(dad_e, [SHOTS["S8"]])
key(kid, 625, loc=(HX - 0.1, -3.4, 0), rot=(0, 0, -10))
key(kid, 624, loc=(HX + 0.05, -1.75, 0), rot=(0, 0, -30))

# ====================== CAMERAS ======================
cams = {}


def camera(name, lens, parent=None):
    c = bpy.data.cameras.new(name)
    c.lens = lens
    c.clip_start, c.clip_end = 0.05, 400
    o = bpy.data.objects.new(name, c)
    scene.collection.objects.link(o)
    if parent:
        o.parent = parent
    t = empty(name + "_t", (0, 0, 0), parent)
    con = o.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = t, "TRACK_NEGATIVE_Z", "UP_Y"
    cams[name] = o
    return o, t


def move(cam, tgt, f0, f1, c0, c1, t0, t1, mid=None):
    key(cam, f0, c0)
    if mid:
        key(cam, mid[0], mid[1])
    key(cam, f1, c1)
    key(tgt, f0, t0)
    key(tgt, f1, t1)


# S1 hook: close on the pump total and the wallet, slow push
c, t = camera("C1", 40)
move(c, t, 1, 60, (SX - 1.5, -2.7, 1.55), (SX - 1.1, -2.2, 1.50), (SX + 0.35, 0.3, 1.30), (SX + 0.45, 0.1, 1.32))
# S2 trust: crane down over the auction rows to the two men and the C-HR
c, t = camera("C2", 24)
move(c, t, 61, 134, (-4.5, -11.0, 6.5), (-1.1, -5.4, 1.9), (0.0, 6.0, 1.0), (0.1, 1.0, 1.25))
# S3 two-shot handshake
c, t = camera("C3", 35)
move(c, t, 135, 194, (0.0, -3.9, 1.5), (0.0, -3.45, 1.5), (0.0, 0.0, 1.32), (0.0, 0.0, 1.35))
# S4 Arfan: camera trucks to his side
c, t = camera("C4", 50)
move(c, t, 195, 302, (0.3, -4.1, 1.5), (1.45, -3.0, 1.46), (0.25, 0.05, 1.38), (0.42, 0.08, 1.48))
# S5a tracking along the auction row
c, t = camera("C5a", 35)
move(c, t, 303, 354, (-14.0, 2.2, 1.5), (-6.5, 2.2, 1.5), (-11.0, 7.5, 1.0), (-3.5, 7.5, 1.0))
# S5b torch inspection, low and close (car-relative)
c, t = camera("C5b", 40)
move(c, t, 355, 405, (-4.2, -0.6, 1.35), (-3.9, -0.2, 1.30), (-1.7, 2.0, 1.0), (-1.6, 2.1, 1.0))
# S5c hero orbit of the C-HR
piv = empty("orbit_pivot", (0.45, 3.4, 0))
c, t = camera("C5c", 32, piv)
key(c, 406, (5.6, -4.8, 1.35))
key(t, 406, (0, 0, 0.8))
key(piv, 406, rot=(0, 0, 0))
key(piv, 456, rot=(0, 0, 38))
# S5d the C-HR rolls up the driveway, low street angle
c, t = camera("C5d", 35)
move(c, t, 457, 506, (HX - 2.5, -11.0, 1.1), (HX - 2.0, -10.5, 1.1), (HX + 2.4, -8.0, 0.8), (HX + 2.4, -3.0, 0.9))
# S6 key handover at the home
c, t = camera("C6", 35)
move(c, t, 507, 558, (HX - 0.6, -5.8, 1.5), (HX - 0.4, -5.2, 1.45), (HX + 0.8, -1.6, 1.2), (HX + 0.8, -1.6, 1.22))
# S7 drives past the servo, waving at the pump
c, t = camera("C7", 28)
move(c, t, 559, 624, (SX - 2.0, -14.5, 1.3), (SX + 2.0, -14.5, 1.3), (SX - 8.0, -8.6, 1.0), (SX + 6.0, -8.6, 1.0))
# S8 end card: wide pull-back at the home
c, t = camera("C8", 30)
move(c, t, 625, 696, (HX + 1.0, -9.5, 1.6), (HX + 1.0, -11.5, 2.4), (HX + 1.2, -2.5, 1.3), (HX + 1.2, -2.0, 1.6))

order = [("S1", "C1"), ("S2", "C2"), ("S3", "C3"), ("S4", "C4"), ("S5a", "C5a"), ("S5b", "C5b"),
         ("S5c", "C5c"), ("S5d", "C5d"), ("S6", "C6"), ("S7", "C7"), ("S8", "C8")]
for s, cname in order:
    m = scene.timeline_markers.new(s, frame=SHOTS[s][0])
    m.camera = cams[cname]
scene.camera = cams["C1"]

# pump total spinning like a pokie machine during S1
_vals = [0, 13.40, 27.90, 41.20, 58.75, 76.30, 89.15, 104.60, 121.90, 137.45]


def spin(sc, *a):
    f = sc.frame_current
    if 1 <= f <= 60:
        i = min(int((f - 1) / 6), len(_vals) - 1)
        nxt = _vals[min(i + 1, len(_vals) - 1)]
        v = _vals[i] + (nxt - _vals[i]) * (((f - 1) % 6) / 6)
        digits.data.body = "$ %.2f" % v


bpy.app.handlers.frame_change_pre.append(spin)

if SAVE_BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_BLEND)
if TEST_FRAMES:
    for f in TEST_FRAMES:
        scene.frame_set(f)
        scene.render.filepath = FRAMES_DIR.rstrip("/") + "/f_%04d.png" % f
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
