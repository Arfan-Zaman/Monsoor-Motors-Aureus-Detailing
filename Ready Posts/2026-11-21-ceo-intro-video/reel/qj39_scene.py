"""'Queue Jump' 39 s ad: fast grey-box Blender previs (animatic) that follows DIRECTOR-CUT.md B2.

Run:  blender -b -P qj39_scene.py -- <frames_dir> [file.blend] [frame frame ...]
360x640, 24 fps, 936 frames (34 s story + 5 s brand). One camera per shot, hard cuts by markers.
Shot timings live in qj39_shots.py (shared with qj39_post.py).

Sets (all in one scene, far apart):
  montage streets x=200..360 (CBD, freeway ramp, Elizabeth Quay, Northbridge, Albany Hwy)
  night servo x=+80, our yard (origin), Dave's driveway x=-80, insert rigs (dash, pump meter,
  POWER, key fob) x=600+.
Fixes vs qj_scene.py: person() arms are now named for the character's own side
(the character faces -Y, so their right arm is at -X), and the servo queue is laid out
so no car overlaps another or the C-HR's path.
"""
import os
import random
import sys
from math import cos, radians, sin

import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qj39_shots import END, FPS, SHOTS, f_of, rng  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FRAMES_DIR = argv[0] if argv else "/tmp/qj39_frames"
SAVE_BLEND = next((a for a in argv[1:] if a.endswith(".blend")), None)
TEST_FRAMES = [int(a) for a in argv[1:] if a.isdigit()]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, END
sc.render.resolution_x, sc.render.resolution_y = 360, 640
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"
sc.render.image_settings.compression = 15
sc.render.filepath = FRAMES_DIR.rstrip("/") + "/f_"
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
    try:
        sc.render.engine = eng
        break
    except Exception:
        pass
for attr, val in (("taa_render_samples", 4), ("use_raytracing", False), ("use_shadows", True),
                  ("shadow_ray_count", 1), ("shadow_step_count", 2), ("use_gtao", False)):
    try:
        setattr(sc.eevee, attr, val)
    except Exception:
        pass
try:
    sc.view_settings.view_transform = "Standard"
except Exception:
    pass


def F(n):
    """First frame of shot n."""
    return rng(n)[0]


def L(n):
    """Last frame of shot n."""
    return rng(n)[1]


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


def interp(idb, mode):
    for fc in _fcurves(idb):
        for kp in fc.keyframe_points:
            kp.interpolation = mode


# ---------------- world + sun, keyed per shot (constant) ----------------
world = bpy.data.worlds.new("World")
sc.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
sun_d = bpy.data.lights.new("Sun", "SUN")
sun = bpy.data.objects.new("Sun", sun_d)
sc.collection.objects.link(sun)
ENVS = {  # colour, strength, sun energy, sun colour, sun rot (rx, rz)
    "sunset": ((0.95, 0.50, 0.38), 0.9, 2.2, (1.0, 0.55, 0.35), (78, 200)),
    "blue": ((0.12, 0.22, 0.52), 0.8, 0.3, (0.6, 0.7, 1.0), (60, 0)),
    "dusk": ((0.48, 0.30, 0.55), 0.7, 0.7, (1.0, 0.6, 0.6), (80, 160)),
    "neon": ((0.04, 0.03, 0.10), 1.0, 0.08, (0.6, 0.6, 1.0), (40, 0)),
    "night": ((0.03, 0.05, 0.11), 1.0, 0.12, (0.6, 0.7, 1.0), (40, 0)),
    "day": ((0.55, 0.72, 0.95), 1.1, 4.5, (1.0, 0.98, 0.94), (40, 0)),
    "golden": ((0.85, 0.60, 0.40), 0.9, 3.2, (1.0, 0.72, 0.45), (76, -60)),
}
SHOT_ENV = {}
for n in range(1, 42):
    SHOT_ENV[n] = ("sunset" if n <= 3 else "blue" if n <= 5 else "dusk" if n <= 7 else "neon" if n <= 11
                   else "night" if n <= 29 else "day" if n <= 35 else "golden")
for n, e in SHOT_ENV.items():
    col, st, se, scol, (rx, rz) = ENVS[e]
    f = F(n)
    bg.inputs[0].default_value = col + (1,)
    bg.inputs[1].default_value = st
    sun_d.energy, sun_d.color = se, scol
    sun.rotation_euler = (radians(rx), 0, radians(rz))
    bg.inputs[0].keyframe_insert("default_value", frame=f)
    bg.inputs[1].keyframe_insert("default_value", frame=f)
    sun_d.keyframe_insert("energy", frame=f)
    sun_d.keyframe_insert("color", frame=f)
    sun.keyframe_insert("rotation_euler", frame=f)
for idb in (world.node_tree, sun_d, sun):
    interp(idb, "CONSTANT")

# ---------------- primitives ----------------
_m = {}


def mat(hexstr, rough=0.7, metal=0.0, emit=0.0, unique=None):
    k = (hexstr, rough, metal, emit)
    if k in _m and not unique:
        return _m[k]
    h = hexstr.lstrip("#")
    col = tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1.0,)
    m = bpy.data.materials.new(unique or ("m_" + h))
    m.diffuse_color = col
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = col
        b.inputs["Emission Strength"].default_value = emit
    if not unique:
        _m[k] = m
    return m


def fin(o, name, loc, color, parent, rough=0.7, metal=0.0, emit=0.0, material=None):
    o.name = name
    o.location = loc
    o.data.materials.append(material or mat(color, rough, metal, emit))
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None, rot=None):
    o = bpy.data.objects.new(name, None)
    sc.collection.objects.link(o)
    o.location = loc
    if rot:
        o.rotation_euler = [radians(a) for a in rot]
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
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=16, ring_count=8)
    o = bpy.context.active_object
    o.scale = scale
    bpy.ops.object.shade_smooth()
    return fin(o, name, loc, color, parent, **kw)


def cyl(name, r, d, loc, color, parent=None, rot=None, pivot_top=False, verts=16, **kw):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, vertices=verts)
    o = bpy.context.active_object
    if pivot_top:
        o.data.transform(Matrix.Translation((0, 0, -d / 2)))
    if rot:
        o.rotation_euler = [radians(a) for a in rot]
    bpy.ops.object.shade_smooth()
    return fin(o, name, loc, color, parent, **kw)


def rod(name, p0, p1, r, color, parent=None, **kw):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    o = cyl(name, r, d.length, (p0 + p1) / 2, color, parent, verts=8, **kw)
    o.rotation_euler = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler()
    return o


def text(name, body, size, loc, color, parent=None, rot=(90, 0, 0), emit=0.0, align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body, cu.size, cu.align_x, cu.align_y = body, size, align, "CENTER"
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    o.rotation_euler = [radians(a) for a in rot]
    return fin(o, name, loc, color, parent, 0.6, 0, emit)


def area(name, loc, energy, size=4, color=(1, 1, 1), rot=(0, 0, 0), parent=None):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.size, d.color = energy, size, color
    o = bpy.data.objects.new(name, d)
    sc.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = [radians(a) for a in rot]
    if parent:
        o.parent = parent
    return o


def point(name, loc, energy, color=(1, 1, 1), parent=None, radius=0.2):
    d = bpy.data.lights.new(name, "POINT")
    d.energy, d.color = energy, color
    d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d)
    sc.collection.objects.link(o)
    o.location = loc
    if parent:
        o.parent = parent
    return o


def key(o, f, loc=None, rot=None, scale=None):
    if loc is not None:
        o.location = loc
        o.keyframe_insert("location", frame=f)
    if rot is not None:
        o.rotation_euler = [radians(a) for a in rot]
        o.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        o.scale = scale if not isinstance(scale, (int, float)) else (scale,) * 3
        o.keyframe_insert("scale", frame=f)


def only_in(o, shots):
    """Render o (and children) only during the given shot numbers."""
    rngs = [rng(n) for n in shots]
    for ob in [o] + list(o.children_recursive):
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=1)
        for a, b in rngs:
            ob.hide_render = False
            ob.keyframe_insert("hide_render", frame=a)
            ob.hide_render = True
            ob.keyframe_insert("hide_render", frame=b + 1)


def show_frames(o, ranges):
    for ob in [o] + list(o.children_recursive):
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=1)
        for a, b in ranges:
            ob.hide_render = False
            ob.keyframe_insert("hide_render", frame=a)
            ob.hide_render = True
            ob.keyframe_insert("hide_render", frame=b + 1)


def mkey(mouth, f, k, kx=1.0):
    """Key the mouth opening as a multiple of its built size (the box size lives in its scale)."""
    b = mouth["base"]
    key(mouth, f, scale=(b[0] * kx, b[1], b[2] * k))


def talk(mouth, f0, f1, step=3):
    for i, f in enumerate(range(f0, f1 + 1, step)):
        mkey(mouth, f, 3.2 if i % 2 else 1)
    mkey(mouth, f1 + 1, 1)


# ---------------- people (character faces -Y; their right side is -X) ----------------
def person(name, shirt, pants, skin, hair, beard=None, h=1.0, loc=(0, 0, 0), rz=0, shoes="#0c0c0c",
           shorts=False, prt=None, chain=False, glasses=None, parent=None):
    r = empty(name, loc, parent)
    r.rotation_euler = (0, 0, radians(rz))
    s = h
    legs, shoe = {}, {}
    for side, x in (("R", -0.10 * s), ("L", 0.10 * s)):
        lg = empty(f"{name}_legpivot{side}", (x, 0, 0), r)
        if shorts:
            cyl(f"{name}_short{side}", 0.092 * s, 0.34 * s, (0, 0, 0.72 * s), pants, lg)
            cyl(f"{name}_leg{side}", 0.07 * s, 0.52 * s, (0, 0, 0.30 * s), skin, lg)
        else:
            cyl(f"{name}_leg{side}", 0.085 * s, 0.84 * s, (0, 0, 0.47 * s), pants, lg)
        shoe[side] = box(f"{name}_shoe{side}", (0.16 * s, 0.30 * s, 0.09 * s), (0, -0.05 * s, 0.045 * s), shoes, lg, rough=0.35)
        legs[side] = lg
    box(f"{name}_hips", (0.40 * s, 0.23 * s, 0.18 * s), (0, 0, 0.93 * s), pants, r)
    torso = box(f"{name}_torso", (0.43 * s, 0.24 * s, 0.50 * s), (0, 0, 1.25 * s), shirt, r)
    ball(f"{name}_sh", 0.14 * s, (0, 0, 1.44 * s), shirt, r, (1.75, 0.85, 0.55))
    if prt:
        rnd = random.Random(name)
        for i in range(9):
            box(f"{name}_print{i}", (0.06 * s, 0.01 * s, 0.035 * s),
                (rnd.uniform(-0.17, 0.17) * s, -0.122 * s, rnd.uniform(1.04, 1.44) * s), prt[i % len(prt)], r,
                rot=(0, rnd.uniform(-40, 40), 0))
    if chain:
        box(f"{name}_chain", (0.16 * s, 0.01 * s, 0.012 * s), (0, -0.124 * s, 1.43 * s), "#d4af37", r, metal=1, rough=0.25)
        ball(f"{name}_chaindot", 0.022 * s, (0, -0.128 * s, 1.385 * s), "#e2b93b", r, metal=1, rough=0.2, emit=0.6)
    head = empty(f"{name}_headpivot", (0, 0, 1.52 * s), r)
    cyl(f"{name}_neck", 0.05 * s, 0.10 * s, (0, 0, 0), skin, head)
    ball(f"{name}_head", 0.115 * s, (0, 0, 0.12 * s), skin, head, (0.9, 1.0, 1.12))
    ball(f"{name}_hair", 0.118 * s, (0, 0.028 * s, 0.165 * s), hair, head, (0.92, 1.0, 0.95))
    box(f"{name}_nose", (0.03 * s, 0.04 * s, 0.04 * s), (0, -0.115 * s, 0.11 * s), skin, head)
    mouth = box(f"{name}_mouth", (0.05 * s, 0.012 * s, 0.012 * s), (0, -0.104 * s, 0.06 * s), "#4a1f1f", head)
    mouth["base"] = list(mouth.scale)
    for side, x in (("R", -0.04), ("L", 0.04)):
        ball(f"{name}_eye{side}", 0.013 * s, (x * s, -0.103 * s, 0.14 * s), "#141414", head)
    gl = None
    if glasses:
        gl = box(f"{name}_glasses", (0.21 * s, 0.015 * s, 0.05 * s), (0, -0.118 * s, 0.14 * s), glasses, head, rough=0.15, metal=0.3)
    if beard:
        ball(f"{name}_beard", 0.10 * s, (0, -0.035 * s, 0.045 * s), beard, head, (0.92, 0.95, 0.85))
    arms = {}
    for side, x in (("R", -0.27 * s), ("L", 0.27 * s)):
        a = cyl(f"{name}_arm{side}", 0.05 * s, 0.58 * s, (x, 0, 1.44 * s), shirt, r, pivot_top=True)
        ball(f"{name}_hand{side}", 0.055 * s, (0, 0, -0.62 * s), skin, a)
        arms[side] = a
    return dict(root=r, R=arms["R"], L=arms["L"], head=head, legR=legs["R"], legL=legs["L"],
                mouth=mouth, glasses=gl, torso=torso)


# cast colour codes (asked for in the brief)
SKIN_A, SKIN_M = "#b98a66", "#b8875f"
ARFAN = dict(shirt="#121212", pants="#e8e2d4", skin=SKIN_A, hair="#0d0d0d", beard="#0d0d0d",
             shoes="#6b4226", prt=["#3f7f5f", "#d9cfa8", "#2f5f8f"])
MONSOOR = dict(shirt="#0f2747", pants="#3a3d42", skin=SKIN_M, hair="#5a5a5a", beard="#6a6a6a",
               shoes="#2a1a10", chain=True, h=0.97, prt=["#1d3d66"])
DAVE = dict(shirt="#ff7f61", pants="#c8bca4", skin="#d9a582", hair="#6b5034", shorts=True, shoes="#3a3a3a")
MIA = dict(shirt="#c8a2c8", pants="#c8a2c8", skin="#e2b494", hair="#8a6a45", h=0.74, shoes="#f2f2f2")
DRIVERS = {
    "guy": dict(shirt="#98ffcc", pants="#2b2d31", skin="#d6a07c", hair="#2a1d14"),
    "woman": dict(shirt="#ff9ec7", pants="#2b2d31", skin="#c68e6a", hair="#1b120c"),
    "retiree": dict(shirt="#1fb5a5", pants="#6f6a60", skin="#e0b08f", hair="#d8d8d8", prt=["#ffd23f", "#ff6f3c"]),
    "glam": dict(shirt="#ff6f61", pants="#141414", skin="#d3a07e", hair="#3a2414", glasses="#0b0b0b"),
}


# ---------------- cars (car faces -Y in its own frame; RHD driver at local -X) ----------------
CAR_KINDS = {  # W, L, body z0, body z1, roof z, cabin len, cabin y, seat (x, y), seat z offset
    "suv": (1.80, 4.4, 0.32, 0.94, 1.45, 2.2, 0.35, (-0.40, 0.15), -0.42),
    "lux": (2.00, 5.0, 0.36, 1.06, 1.62, 2.6, 0.40, (-0.45, 0.30), -0.30),
    "muscle": (1.95, 5.0, 0.28, 0.80, 1.24, 1.8, 0.60, (-0.42, 0.60), -0.62),
}


def car(name, loc, rz, paint, kind="suv", hero=False, plate_bar=False, decal=False, glass=False,
        door=False, parent=None, tail_mat=None):
    W, Ln, z0, z1, zr, cl, cy, seat, sz = CAR_KINDS[kind]
    r = empty(name, loc, parent)
    r.rotation_euler = (0, 0, radians(rz))
    box(name + "_body", (W, Ln, z1 - z0), (0, 0, (z0 + z1) / 2), paint, r, rough=0.25, metal=0.55)
    box(name + "_roof", (W - 0.18, cl, 0.07), (0, cy, zr), paint, r, rough=0.25, metal=0.5)
    for i, (px, py) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        box(f"{name}_pillar{i}", (0.07, 0.07, zr - z1), (px * (W / 2 - 0.12), cy + py * (cl / 2 - 0.05), (zr + z1) / 2),
            "#15171c", r)
    if glass:
        ws = empty(name + "_wsp", (0, cy - cl / 2 - 0.12, (zr + z1) / 2), r, rot=(-35, 0, 0))
        box(name + "_windscreen", (W - 0.25, 0.03, (zr - z1) * 1.15), (0, 0, 0), "#1d2633", ws, rough=0.05, metal=0.6)
    else:
        ws = None
    tm = tail_mat or mat("#c01818", emit=2.0)
    for x in (-0.6, 0.6):
        box(f"{name}_hl{x}", (0.42, 0.05, 0.10), (x * W / 1.8, -Ln / 2 - 0.02, z1 - 0.12), "#fff3cf", r, emit=3.0)
        box(f"{name}_tl{x}", (0.42, 0.05, 0.10), (x * W / 1.8, Ln / 2 + 0.02, z1 - 0.10), "#c01818", r, material=tm)
    wy = Ln / 3 if kind != "muscle" else Ln / 2.9
    for i, (x, y) in enumerate([(-W / 2, -wy), (W / 2, -wy), (-W / 2, wy), (W / 2, wy)]):
        cyl(f"{name}_w{i}", 0.34, 0.26, (x, y, 0.34), "#121316", r, rot=(0, 90, 0), rough=0.8)
        if hero:
            cyl(f"{name}_rim{i}", 0.22, 0.28, (x, y, 0.34), "#c8ccd2", r, rot=(0, 90, 0), rough=0.3, metal=0.8)
    box(name + "_plate", (0.5, 0.02, 0.13), (0, Ln / 2 + 0.03, z0 + 0.22), "#e8e8e8", r)
    if plate_bar:   # Monsoor Motors plate frame, shown as an orange bar
        box(name + "_frame", (0.62, 0.025, 0.06), (0, Ln / 2 + 0.045, z0 + 0.12), "#FF5F15", r, emit=1.2)
        box(name + "_frame2", (0.62, 0.025, 0.03), (0, Ln / 2 + 0.045, z0 + 0.31), "#FF5F15", r, emit=1.2)
        box(name + "_fplate", (0.5, 0.02, 0.13), (0, -Ln / 2 - 0.03, z0 + 0.22), "#e8e8e8", r)
        box(name + "_fframe", (0.62, 0.025, 0.05), (0, -Ln / 2 - 0.045, z0 + 0.12), "#FF5F15", r, emit=1.2)
    if decal:       # small door decal both sides
        for sx in (-1, 1):
            box(f"{name}_decal{sx}", (0.02, 0.32, 0.10), (sx * (W / 2 + 0.01), -0.1, z1 - 0.22), "#FF5F15", r, emit=0.8)
            box(f"{name}_decaln{sx}", (0.022, 0.32, 0.04), (sx * (W / 2 + 0.012), -0.1, z1 - 0.30), "#0F2747", r)
    if hero:
        text(name + "_badge", "HYBRID", 0.09, (W / 2 + 0.01, 1.2, z1 - 0.12), "#d9dde2", r, rot=(90, 0, 90))
    dp = None
    if door:  # driver door (right side, local -X), hinge at the front
        dp = empty(name + "_doorpivot", (-W / 2 - 0.02, -0.55, 0), r)
        box(name + "_door", (0.05, 1.05, z1 - z0 - 0.05), (0, 0.52, (z0 + z1) / 2 + 0.02), paint, dp, rough=0.25, metal=0.55)
        box(name + "_doorwin", (0.04, 0.9, (zr - z1) * 0.8), (0, 0.5, (zr + z1) / 2), "#15171c", dp)
    wheel = cyl(name + "_wheel", 0.15, 0.03, (seat[0], seat[1] - 0.45, z1 + 0.01), "#0c0c0c", r, rot=(60, 0, 0))
    r["seat"] = (seat[0], seat[1], sz)
    return dict(root=r, door=dp, windscreen=ws, wheel=wheel)


def seated(name, carobj, cast, local=None, zoff=None, **kw):
    sx, sy, sz = carobj["root"]["seat"]
    if local:
        sx, sy = local
    p = person(name, parent=carobj["root"], loc=(sx, sy, sz if zoff is None else zoff), **{**cast, **kw})
    p["legR"].scale = p["legL"].scale = (1, 1, 0.01)   # legs folded out of sight under the dash
    for side in ("R", "L"):
        p[side].rotation_euler = (radians(-55), 0, 0)
    point(name + "_fill", (sx, sy - 0.75, 1.2 + (sz + 0.42)), 25, (1.0, 0.95, 0.9), parent=carobj["root"])
    return p


def signal(name, loc, sched, both=True):
    r = empty(name, loc)
    cyl(name + "_pole", 0.07, 3.2, (0, 0, 1.6), "#2a2c30", r)
    box(name + "_house", (0.34, 0.16, 0.95), (0, 0, 3.0), "#101114", r)
    lamps = {}
    for st, z, dim, lit in (("R", 3.3, "#3a0c0c", "#ff2a1a"), ("A", 3.0, "#3a2a0c", "#ffb000"), ("G", 2.7, "#0c3a1a", "#25ff6a")):
        ball(f"{name}_d{st}", 0.095, (0, 0, z), dim, r, scale=(1, 1.0, 1))
        lamps[st] = ball(f"{name}_l{st}", 0.1, (0, 0, z), lit, r, emit=12)
    for f, state in sched:
        for st, lp in lamps.items():
            lp.hide_render = st != state
            lp.keyframe_insert("hide_render", frame=f)
    return r, lamps


# ---------------- MONTAGE STREETS ----------------
def street(ox, kind, sched, n_seed):
    rnd = random.Random(n_seed)
    box(f"st{ox}_ground", (60, 170, 0.1), (ox, 0, -0.05), "#26272b", rough=0.4, metal=0.1)
    for sx in (-1, 1):
        box(f"st{ox}_path{sx}", (5, 170, 0.15), (ox + sx * 7.5, 0, 0.075), "#6d6a66")
    for y in range(-80, 81, 6):
        box(f"st{ox}_dash{y}", (0.12, 2.5, 0.01), (ox, y, 0.006), "#d8d8d8")
    box(f"st{ox}_stop", (4.9, 0.35, 0.01), (ox + 2.5, 0.0, 0.007), "#f0f0f0")
    signal(f"st{ox}_sig", (ox + 5.6, -0.6, 0), sched)
    if kind == "cbd":
        for i in range(16):
            sx = rnd.choice((-1, 1))
            x = ox + sx * rnd.uniform(12, 26)
            y = rnd.uniform(-70, 70)
            hgt = rnd.uniform(35, 95)
            box(f"st{ox}_tw{i}", (rnd.uniform(8, 13), rnd.uniform(8, 13), hgt), (x, y, hgt / 2),
                rnd.choice(["#5d6878", "#7b8696", "#3f4a5a", "#8d97a6"]), rough=0.15, metal=0.6)
            for k in range(3):
                box(f"st{ox}_win{i}_{k}", (0.2, 7, 1.2), (x - sx * 6.6, y, rnd.uniform(8, hgt - 4)), "#ffd29a", emit=1.5)
        point(f"st{ox}_warm", (ox + 1, 8, 6), 1500, (1.0, 0.7, 0.5), radius=2)
    elif kind == "ramp":
        box(f"st{ox}_fwy", (12, 170, 1.0), (ox - 20, 0, 7.5), "#5a5d63")
        box(f"st{ox}_fwyrail", (0.3, 170, 0.9), (ox - 14.2, 0, 8.4), "#8a8d93")
        for y in range(-80, 81, 14):
            box(f"st{ox}_col{y}", (1.2, 1.2, 7), (ox - 20, y, 3.5), "#6a6d73")
            ball(f"st{ox}_fl{y}", 0.25, (ox - 14.3, y, 9.3), "#ffd29a", emit=8)
        for y in range(-80, 81, 5):
            ball(f"st{ox}_bridge{y}", 0.35, (ox - 60, y, 5 + 2 * abs((y % 40) - 20) / 20), "#fff0c8", emit=10)
        box(f"st{ox}_water", (30, 170, 0.05), (ox - 48, 0, 0.02), "#0e1e3a", rough=0.08, metal=0.5)
        point(f"st{ox}_amb", (ox + 2, 6, 7), 1200, (0.75, 0.82, 1.0), radius=2)
    elif kind == "eq":
        box(f"st{ox}_river", (16, 170, 0.04), (ox - 18, 0, 0.12), "#1d3c66", rough=0.06, metal=0.5)
        for i, (y, z) in enumerate([(18, 2), (22, 5), (26, 6.5), (30, 5), (34, 2)]):
            box(f"st{ox}_arch{i}", (0.6, 4.2, 0.6), (ox - 18, y, z), "#f2f2f2", rot=(0, 0, 0), emit=0.3)
        box(f"st{ox}_spire", (3, 3, 30), (ox - 9, 45, 15), "#7c8aa0", rough=0.1, metal=0.7)
        for i in range(8):
            x = ox + rnd.choice((-1, 1)) * rnd.uniform(14, 28)
            hgt = rnd.uniform(30, 80)
            box(f"st{ox}_tw{i}", (9, 9, hgt), (x, rnd.uniform(30, 90), hgt / 2), "#4a5568", rough=0.2, metal=0.5)
        point(f"st{ox}_amb", (ox + 1, 7, 6), 1200, (1.0, 0.75, 0.75), radius=2)
    elif kind in ("northbridge", "albany"):
        neon = ["#ff2fa8", "#18e0d0", "#a040ff", "#ffcf3a"] if kind == "northbridge" else ["#ff9a2a", "#ffd23f", "#ff5f15", "#e8e8e8"]
        for i in range(14):
            sx = -1 if i % 2 else 1
            y = -70 + i * 10 + rnd.uniform(-2, 2)
            hgt = rnd.uniform(5, 12) if kind == "northbridge" else rnd.uniform(4, 7)
            box(f"st{ox}_b{i}", (8, 9, hgt), (ox + sx * 14, y, hgt / 2), rnd.choice(["#2c2a33", "#3a3440", "#2f3238"]))
            box(f"st{ox}_sign{i}", (0.2, rnd.uniform(3, 6), 0.9), (ox + sx * 9.9, y, hgt - 1.2), rnd.choice(neon), emit=6)
        for y in range(-70, 71, 18):
            cyl(f"st{ox}_lp{y}", 0.06, 7, (ox + 9.6, y, 3.5), "#55585e")
            point(f"st{ox}_lpl{y}", (ox + 8.6, y, 6.8), 900, (1.0, 0.68, 0.38), radius=0.5)
        point(f"st{ox}_amb", (ox + 1, 6, 6), 400, (0.7, 0.6, 1.0), radius=2)


MONT = {"cbd": 200, "ramp": 240, "eq": 280, "nb": 320, "alb": 360}
street(MONT["cbd"], "cbd", [(1, "R")], 1)
street(MONT["ramp"], "ramp", [(1, "R")], 2)
street(MONT["eq"], "eq", [(1, "R")], 3)
street(MONT["nb"], "northbridge", [(1, "R"), (f_of(3.30), "G")], 4)
street(MONT["alb"], "albany", [(1, "R"), (f_of(5.85), "G")], 5)

LANE = 2.8
# --- 1-2 GenZ guy, white Seltos, CBD
ox = MONT["cbd"]
seltos = car("seltos", (ox + LANE, 9, 0), 0, "#f2f2f2")
guy = seated("guy", seltos, DRIVERS["guy"])
key(seltos["root"], 1, (ox + LANE, 10.5, 0), (0, 0, 0))
key(seltos["root"], 8, (ox + LANE, 2.5, 0), (0, 0, 0))
key(seltos["root"], 10, (ox + LANE, 2.45, -0.02), (1.4, 0, 0))   # nose dips on the stop
key(seltos["root"], 13, (ox + LANE, 2.45, 0), (0, 0, 0))
bubble = ball("guy_bubble", 0.03, (0, -0.13, 0.06), "#ff8fc8", guy["head"], emit=0.4)
key(bubble, 12, scale=0.4)
key(bubble, 15, scale=1.8)
key(bubble, 16, scale=0.01)
key(guy["head"], 12, rot=(12, 0, 0))          # eyes on the gauge, chewing
key(guy["head"], 18, rot=(12, 0, 0))
key(guy["head"], 22, rot=(-4, 0, 0))          # looks up
key(guy["root"], 16, loc=guy["root"].location.copy())
key(guy["root"], 19, loc=guy["root"].location + Vector((0, 0, -0.03)))   # shoulders drop
for f in range(12, 23, 2):
    mkey(guy["mouth"], f, 2.2 if f % 4 else 1)

# --- 4 GenZ woman, red CX-3, freeway ramp
ox = MONT["ramp"]
cx3 = car("cx3", (ox + LANE, 2.5, 0), 0, "#b3121b")
wom = seated("woman", cx3, DRIVERS["woman"])
key(wom["L"], F(4), rot=(-55, 0, 0))
key(wom["L"], F(4) + 4, rot=(-150, -25, 0))   # tucks hair behind her ear
key(wom["L"], F(4) + 8, rot=(-150, -25, 0))
key(wom["L"], L(4), rot=(-60, 0, 0))
key(wom["head"], F(4), rot=(0, 0, 0))
key(wom["head"], F(4) + 6, rot=(-4, 0, 0))    # eyebrow up
key(wom["head"], L(4), rot=(4, 14, 0))        # slow tired head tilt

# --- 6 retiree, blue Kona, Elizabeth Quay, hunched
ox = MONT["eq"]
kona = car("kona", (ox + LANE, 2.5, 0), 0, "#1f5fbf")
ret = seated("retiree", kona, DRIVERS["retiree"])
ret["root"].rotation_euler = (radians(16), 0, 0)    # hunched over the wheel
rg = box("retiree_readers", (0.2, 0.015, 0.035), (0, -0.118, 0.115), "#8a6a2a", ret["head"], metal=0.5)
for i, rzv in enumerate((0, 9, -9, 9, -9, 0)):      # small headshake x2
    key(ret["head"], F(6) + i * 2, rot=(-8, 0, rzv))
key(ret["head"], L(6), rot=(-6, 0, 0))

# --- 8-11 glam driver, black lux V8 SUV, Northbridge
ox = MONT["nb"]
lux = car("lux", (ox + LANE, 2.8, 0), 0, "#0b0b0d", kind="lux")
glam = seated("glam", lux, DRIVERS["glam"])
lr = lux["root"]
key(lr, 1, (ox + LANE, 2.8, 0), (0, 0, 0))
key(lr, F(8) + 5, (ox + LANE, 2.8, 0), (0, 0, 0))
key(lr, F(8) + 8, (ox + LANE, 2.4, 0), (-2.5, 0, 0))      # launch, rear squats
key(lr, L(8), (ox + LANE, 0.6, 0), (-2.0, 0, 0))
key(lr, F(10), (ox + LANE, -17.0, 0), (-0.5, 0, 0))
key(lr, L(10), (ox + LANE, -25.5, 0), (-0.5, 0, 0))
key(lr, F(11), (ox + LANE, -27.0, 0), (0, 0, 0))
key(lr, L(11), (ox + LANE, -36.0, 0), (0.6, 0, 0))
interp(lr, "LINEAR")
# 60 sign + fixed speed camera on the kerb
cyl("nb_60pole", 0.05, 2.6, (ox + 5.6, -13, 1.3), "#8a8d93")
cyl("nb_60disc", 0.36, 0.03, (ox + 5.6, -13, 2.5), "#c01818", rot=(90, 0, 0))
cyl("nb_60in", 0.29, 0.035, (ox + 5.6, -13, 2.5), "#f2f2f2", rot=(90, 0, 0))
text("nb_60txt", "60", 0.3, (ox + 5.6, -12.96, 2.5), "#101010", rot=(90, 0, 180))
text("nb_60txtb", "60", 0.3, (ox + 5.6, -13.04, 2.5), "#101010", rot=(90, 0, 0))
cyl("nb_campole", 0.09, 3.6, (ox + 5.8, -22, 1.8), "#6a6d73")
box("nb_cambox", (0.45, 0.6, 0.45), (ox + 5.8, -22, 3.7), "#c9c9c2")
box("nb_camlens", (0.25, 0.05, 0.25), (ox + 5.8, -21.68, 3.7), "#101010")
strobe = box("nb_strobe", (0.32, 0.06, 0.12), (ox + 5.8, -21.66, 3.98), "#ffffff", emit=60)
flash_l = point("nb_flash", (ox + 5.2, -21.4, 3.6), 0, (1, 1, 1), radius=0.3)
FL0 = f_of(4.20)
show_frames(strobe, [(FL0, FL0 + 2)])
for f, e in ((FL0 - 1, 0), (FL0, 40000), (FL0 + 2, 40000), (FL0 + 3, 0)):
    flash_l.data.energy = e
    flash_l.data.keyframe_insert("energy", frame=f)
interp(flash_l.data, "CONSTANT")
# busted: freeze, mouth falls open, glasses slide crooked, eyes shut in a wince
mkey(glam["mouth"], F(11), 1)
mkey(glam["mouth"], F(11) + 3, 4.5, 1.1)
mkey(glam["mouth"], L(11), 4.5, 1.1)
key(glam["glasses"], F(11) + 2, loc=glam["glasses"].location.copy(), rot=(0, 0, 0))
key(glam["glasses"], F(11) + 9, loc=glam["glasses"].location + Vector((0.01, 0, -0.035)), rot=(0, 14, 0))
key(glam["head"], F(11), rot=(0, 0, 0))
key(glam["head"], F(11) + 6, rot=(-5, 0, 0))
key(glam["head"], L(11), rot=(5, 0, -4))

# --- 12 Dave in grey ASX, Albany Hwy, Mia asleep behind
ox = MONT["alb"]
asx_m = car("asx_m", (ox + LANE, 2.5, 0), 0, "#7a7f86")
dave_m = seated("dave_m", asx_m, DAVE)
mia_m = seated("mia_m", asx_m, MIA, local=(-0.40, 1.15), zoff=-0.1)
mia_m["head"].rotation_euler = (radians(10), radians(-28), 0)   # asleep against the window
green_spill = point("alb_green", (ox + 4, -1.5, 2.2), 0, (0.3, 1.0, 0.45), radius=1)
for f, e in ((1, 0), (f_of(5.85) - 1, 0), (f_of(5.85), 500)):
    green_spill.data.energy = e
    green_spill.data.keyframe_insert("energy", frame=f)
interp(green_spill.data, "CONSTANT")
dh = dave_m["head"]
key(dh, F(12), rot=(4, 0, 0))
key(dh, F(12) + 6, rot=(4, 0, 0))                  # jaw sets, breath out
key(dh, F(12) + 11, rot=(-6, 0, 22))               # eyes to the mirror (Mia)
key(dh, F(12) + 15, rot=(-6, 0, 22))
key(dh, F(12) + 18, rot=(8, 0, 0))                 # small resigned nod
key(dh, L(12), rot=(2, 0, 0))
key(dave_m["root"], F(12) + 4, loc=dave_m["root"].location.copy())
key(dave_m["root"], F(12) + 8, loc=dave_m["root"].location + Vector((0, 0, -0.025)))

# ---------------- NIGHT SERVO (x = +80) ----------------
SX = 80
box("sv_ground", (70, 50, 0.1), (SX, 5, -0.05), "#2f3136", rough=0.3, metal=0.1)
box("sv_road", (110, 8, 0.02), (SX, -10, 0.01), "#1e1f22", rough=0.5)
box("sv_canopy", (16, 10, 0.5), (SX, 2, 5.2), "#e9ecef", emit=0.5)
box("sv_fascia", (16.2, 10.2, 0.35), (SX, 2, 5.6), "#00a8a8", emit=2.5)
for x in (-6, 0, 6):
    area(f"sv_down{x}", (SX + x, 2, 4.8), 3500, 4, (0.92, 0.96, 1.0))
for x in (-7.2, 7.2):
    box(f"sv_col{x}", (0.45, 0.45, 5), (SX + x, 2, 2.5), "#d8dbe0")
board = empty("price_board", (SX - 11, -6.6, 0))
box("pb_post", (0.4, 0.4, 5), (0, 0, 2.5), "#3a3d42", board)
box("pb_face", (2.4, 0.3, 3.0), (0, 0, 5.4), "#0a0d18", board)
box("pb_top", (2.4, 0.32, 0.5), (0, 0, 6.65), "#00a8a8", board, emit=2)
for i, (lab, p) in enumerate((("ULP", "1.799"), ("E10", "1.779"), ("DSL", "1.899"))):
    text(f"pb_l{i}", lab, 0.32, (-0.75, -0.17, 5.95 - i * 0.62), "#ffcf3a", board, emit=6)
    text(f"pb_p{i}", p, 0.45, (0.35, -0.17, 5.95 - i * 0.62), "#ffcf3a", board, emit=6)
box("sv_shop", (14, 7, 3.6), (SX + 2, 13, 1.8), "#3a3a3a")
box("sv_shopglass", (11, 0.1, 2.2), (SX + 2, 9.45, 1.3), "#ffd9a0", emit=2.0)
box("sv_neon", (11, 0.12, 0.25), (SX + 2, 9.42, 3.1), "#ff2fa8", emit=8)
for x in range(-48, 49, 12):
    cyl(f"sl_pole{x}", 0.06, 6, (SX + x, -14.5, 3), "#55585e")
    area(f"sl_light{x}", (SX + x, -13, 5.8), 2200, 3, (1.0, 0.68, 0.38))
area("sv_fill", (SX - 20, -20, 8), 5000, 12, (0.55, 0.65, 1.0), rot=(55, 0, -40))
PUMP1, PUMP2 = (SX - 3.5, 0.8), (SX + 3.5, 0.8)
for i, (px, py) in enumerate((PUMP1, PUMP2)):
    box(f"isl{i}", (0.9, 2.6, 0.15), (px, py, 0.075), "#c9ccd0")
    box(f"pump{i}_b", (0.5, 0.9, 1.9), (px, py, 1.0), "#e4e7ea")
    for sx in (-1, 1):
        box(f"pump{i}_s{sx}", (0.02, 0.55, 0.3), (px + sx * 0.26, py, 1.45), "#7dff8a", emit=2.0)
        text(f"pump{i}_n{sx}", str(i + 1), 0.25, (px + sx * 0.26, py, 1.8), "#0F2747", rot=(90, 0, 90 * sx))
puddle = cyl("puddle", 0.55, 0.004, (SX - 4.15, 1.75, 0.004), "#3a2a12", rough=0.03, metal=0.7)
box("puddle_glint", (0.25, 0.08, 0.002), (SX - 4.05, 1.55, 0.008), "#ffb347", emit=2.5)

# Dave's ASX at pump 2 (faces +Y; filler left rear, toward the pump), queue behind and on the road
asx = car("asx", (SX + 5.6, 2.1, 0), 180, "#7a7f86")
qcols = ["#d6d8db", "#3c4a5c", "#6e2b2b", "#e8e8e8", "#2b2d31", "#94a0ab"]
car("q0", (SX + 5.6, -3.4, 0), 180, qcols[0])
for i, x in enumerate((SX + 1.0, SX - 13.0, SX - 18.6, SX - 24.2, SX + 6.6)):
    car(f"q{i + 1}", (x, -8.2, 0), 90, qcols[(i + 1) % len(qcols)])
dave = person("Dave", loc=(SX + 4.25, 0.75, 0), rz=-60, **DAVE)
mia = seated("Mia", asx, MIA, local=(-0.40, 1.15), zoff=-0.1)
rod("dave_hose", (PUMP2[0] + 0.26, PUMP2[1], 1.15), (SX + 4.68, 0.62, 0.85), 0.025, "#111111")
box("dave_nozzle", (0.08, 0.2, 0.08), (SX + 4.55, 0.62, 0.86), "#1a7a2a")
dv = dave
key(dv["R"], 1, rot=(-10, 0, 0))
key(dv["L"], 1, rot=(40, -80, 0))                  # left hand up on the roof (nozzle latched in)
key(dv["head"], 1, rot=(4, 0, -36))                # eyes on the meter
# 15 shifts weight, rolls neck
key(dv["root"], F(15), (SX + 4.25, 0.75, 0), (0, 0, -60))
key(dv["root"], F(15) + 6, (SX + 4.25, 0.72, 0), (0, 3, -58))   # shifts weight
key(dv["head"], F(15), rot=(0, 10, -20))
key(dv["head"], F(15) + 6, rot=(-6, -10, -20))                  # rolls neck
key(dv["head"], L(15), rot=(4, 0, -36))             # eyes go to the meter
# 17 the wince: narrows eyes, looks away at the road, back, exhale, head drops, small smirk
key(dv["head"], F(17), rot=(4, 0, -36))
key(dv["head"], F(17) + 8, rot=(2, 0, -36))
key(dv["head"], F(17) + 14, rot=(0, 0, 40))         # away at the road
key(dv["head"], F(17) + 20, rot=(0, 0, 40))
key(dv["head"], F(17) + 25, rot=(4, 0, -36))        # back to the meter
key(dv["head"], F(17) + 29, rot=(18, 0, -30))       # head drops
key(dv["head"], L(17), rot=(14, 0, -26))
key(dv["head"], F(24), rot=(4, 0, -36))             # 24: eyes on the meter
key(dv["head"], L(24), rot=(5, 0, -36))
# 28 double take: glances up, back down, freezes, looks up quickly, watches, slow blink
f0 = F(28)
for df, r in ((0, (5, 0, -36)), (6, (-6, 0, -55)), (12, (5, 0, -36)), (20, (5, 0, -36)), (26, (-8, 0, -70)),
              (36, (-6, 0, -78)), (48, (-6, 0, -85))):
    key(dv["head"], f0 + df, rot=r)
mkey(dv["mouth"], f0 + 26, 1)
mkey(dv["mouth"], f0 + 30, 2.6)
# Mia: asleep (18), awake at the open window (29)
mh = mia["head"]
key(mh, 1, rot=(10, -28, 0))
key(mh, F(29) - 1, rot=(10, -28, 0))
key(mia["root"], F(29) - 1, loc=mia["root"].location.copy(), rot=(0, 0, 0))
key(mia["root"], F(29), loc=mia["root"].location + Vector((-0.30, 0, -0.05)), rot=(0, 0, -90))  # chin on the sill
key(mh, F(29), rot=(14, 0, 0))
key(mh, F(29) + 5, rot=(10, 0, 35))                 # eyes to Dad
key(mh, L(29), rot=(8, 0, 35))
talk(mia["mouth"], f_of(19.85), f_of(20.25))
talk(mia["mouth"], f_of(20.55), f_of(21.25))
key(mh, f_of(20.9), rot=(4, 0, 35))                 # brows lift on "one"

# The black C-HR (servo) with Arfan
tail_chr = mat("#c01818", emit=1.2, unique="chr_tail")
chr_s = car("chr_s", (SX - 28, -11.8, 0), 90, "#0b0c0e", hero=True, plate_bar=True, decal=True, door=True, tail_mat=tail_chr)
cr = chr_s["root"]
arf_seat = seated("ArfanSeated", chr_s, ARFAN, glasses="#2a2a2a")
only_in(arf_seat["root"], [19, 26, 27, 28])
CHR_PARK = (SX - 5.6, 2.0, 0)
key(cr, 1, (SX - 70, -11.8, 0), (0, 0, 90))
key(cr, F(19) - 1, (SX - 70, -11.8, 0), (0, 0, 90))
key(cr, F(19), (SX - 30, -11.8, 0), (0, 0, 90))
key(cr, F(19) + 14, (SX - 13.5, -11.8, 0), (0, 0, 90))
key(cr, F(19) + 22, (SX - 7.6, -8.6, 0), (0, -1.5, 125))     # body roll into the swing
key(cr, F(19) + 30, (SX - 5.7, -2.0, 0), (0, -1.0, 172))
key(cr, F(19) + 34, (SX - 5.6, 1.85, 0), (0, 0, 180))
key(cr, F(19) + 36, (SX - 5.6, 2.0, -0.02), (1.2, 0, 180))     # stops, nose dips
key(cr, F(19) + 38, CHR_PARK, (0, 0, 180))
key(cr, L(26), CHR_PARK, (0, 0, 180))
key(cr, L(27), (SX - 5.6, 2.25, 0), (0, 0, 180))               # starts to roll
key(cr, F(28) + 12, (SX - 5.6, 5.6, 0), (0, 0, 180))
key(cr, F(28) + 22, (SX - 4.2, 7.5, 0), (0, 0, 125))
key(cr, F(28) + 33, (SX + 4.0, 7.9, 0), (0, 0, 90))
key(cr, L(28), (SX + 12.5, 7.9, 0), (0, 0, 90))
dp = chr_s["door"]
key(dp, 1, rot=(0, 0, 0))
key(dp, F(20) - 1, rot=(0, 0, 0))
key(dp, F(20), rot=(0, 0, 62))
key(dp, F(21) + 0, rot=(0, 0, 62))
key(dp, F(21) + 3, rot=(0, 0, 0))                                # door clunk 11.82
for f, e in ((1, 1.2), (L(27) - 4, 1.2), (L(27), 5.0)):          # tail-lights brighten
    tail_chr.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = e
    tail_chr.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].keyframe_insert("default_value", frame=f)
# Arfan standing at pump 1 (faces +X, away from the car)
arf = person("Arfan", loc=(SX - 4.25, 1.9, 0), rz=90, glasses="#2a2a2a", **ARFAN)
only_in(arf["root"], [20, 21, 22, 23, 24])
key(arf["legR"], F(20), loc=(-0.10, 0, 0.14))
key(arf["legR"], F(20) + 4, loc=(-0.10, 0, 0.0))                # boot plants flat
key(arf["L"], F(21), rot=(35, 0, 0))                             # pushes the door shut behind him
key(arf["L"], F(21) + 4, rot=(0, 0, 0))
key(arf["head"], F(21), rot=(4, 0, -25))
key(arf["head"], F(21) + 6, rot=(0, 0, 5))                       # glances at Dave
key(arf["head"], F(21) + 9, rot=(9, 0, 5))                       # small nod
key(arf["head"], F(21) + 12, rot=(-2, 0, 5))
talk(arf["mouth"], f_of(12.10), f_of(12.80))
key(arf["head"], f_of(12.85), rot=(-2, 0, 5))
key(arf["head"], f_of(12.95), rot=(8, 0, -40))                   # looks back
key(arf["R"], f_of(12.85), rot=(0, 0, 0))
key(arf["R"], L(21), rot=(-55, 10, 0))                           # reaches for the nozzle
rod("chr_hose", (PUMP1[0] - 0.26, PUMP1[1], 1.15), (SX - 4.66, 0.55, 0.88), 0.025, "#111111")
only_in(bpy.data.objects["chr_hose"], [22, 23, 24])
# nozzle insert (22): right hand with silver ring seats the nozzle in the filler
flap = box("chr_flap", (0.02, 0.18, 0.16), (SX - 4.72, 0.5, 0.9), "#0b0c0e", rot=(0, 0, 0))
noz = empty("noz_rig", (SX - 4.3, 0.55, 0.9))
box("noz_body", (0.28, 0.07, 0.09), (0, 0, 0), "#1a7a2a", noz)
box("noz_spout", (0.14, 0.03, 0.03), (-0.2, 0, -0.01), "#9aa0a8", noz, metal=0.8)
ball("noz_hand", 0.06, (0.05, 0, 0.06), SKIN_A, noz, scale=(1.3, 0.9, 0.8))
cyl("noz_ring", 0.022, 0.012, (0.0, -0.045, 0.06), "#d8dce2", noz, rot=(90, 0, 0), metal=1, rough=0.15)
only_in(noz, [22])
key(noz, F(22), (SX - 4.15, 0.55, 0.92))
key(noz, f_of(13.28), (SX - 4.48, 0.55, 0.9))
key(noz, f_of(13.33), (SX - 4.47, 0.55, 0.905))                  # one squeeze

# ---------------- OUR YARD (origin), next morning ----------------
box("yd_ground", (70, 60, 0.1), (0, 4, -0.05), "#a5503d", rough=0.85)
box("yd_road", (90, 7, 0.02), (0, -13, 0.01), "#3b3d42")
for x0, x1 in ((-30, 5.5), (10.5, 30)):
    box(f"yd_fence{x0}", (x1 - x0, 0.08, 1.8), ((x0 + x1) / 2, -9, 0.9), "#1a1a1a", rough=0.5, metal=0.5)
for x in (5.5, 10.5):
    box(f"yd_gate{x}", (0.3, 0.3, 2.2), (x, -9, 1.1), "#0F2747")
box("yd_bldg", (40, 3, 5), (0, 17, 2.5), "#1d4fb0")
box("yd_signbar", (14, 0.1, 1.2), (0, 15.45, 4.0), "#0F2747")
box("yd_signbar2", (14, 0.12, 0.2), (0, 15.4, 3.3), "#FF5F15", emit=0.8)
for x in (-12, -6, 5, 12):
    cyl(f"yd_palmtrunk{x}", 0.2, 8, (x, 14.5, 4), "#7a6449")
    for k in range(6):
        box(f"yd_frond{x}_{k}", (0.5, 3.2, 0.08), (x, 14.5, 8.0), "#3d6b2c", rot=(25, 0, k * 60))
for i, x in enumerate((-9, -6.2, -3.4, 2.8, 5.6, 8.4)):
    car(f"yd_car{i}", (x, 8.5, 0), 0, ["#b8bcc2", "#2b3a55", "#f0f0f0", "#6d7277", "#f0f0f0", "#3a3d42"][i])
for i, (x, y) in enumerate(((-4.5, -7.6), (3.8, -7.6), (12, -7.6), (-12, -7.6))):
    cyl(f"flagpole{i}", 0.03, 4.0, (x, y, 2.0), "#222222")
    box(f"flag{i}", (0.7, 0.03, 2.6), (x + 0.36, y, 2.6), "#FF5F15" if i % 2 else "#0F2747")
chr_y = car("chr_y", (-1.0, 1.0, 0), 0, "#0b0c0e", hero=True, plate_bar=True, decal=True, glass=True)


def sold_tag(name, ws):
    t = empty(name, (0.38, -0.03, 0.08), ws)
    box(name + "_card", (0.32, 0.01, 0.16), (0, 0, 0), "#f5f2e8", t, emit=0.3)
    text(name + "_txt", "SOLD", 0.09, (0, -0.008, 0), "#d01818", t, emit=1.0)
    return t


sold = sold_tag("sold_tag", chr_y["windscreen"])
show_frames(sold, [(F(30), END)])
hand_s = ball("sold_hand", 0.06, (0.5, -0.06, 0.08), SKIN_A, chr_y["windscreen"], scale=(1.4, 0.4, 1.0))
cyl("sold_ring", 0.02, 0.012, (0.42, -0.08, 0.1), "#d8dce2", chr_y["windscreen"], rot=(90, 0, 0), metal=1, rough=0.15)
for o in (hand_s, bpy.data.objects["sold_ring"]):
    only_in(o, [30])
    key(o, F(30), loc=o.location.copy())
    key(o, L(30), loc=o.location + Vector((-0.14, 0, 0.0)))     # palm flat, small press, smooth
# muscle car + Monsoor
mus = car("muscle", (8, -16, 0), 180, "#08080a", kind="muscle", hero=False, door=True)
mr = mus["root"]
MUS_STOP = (6.0, -2.6, 0)
key(mr, F(31), (8.0, -17.0, 0), (0, 0, 180))
key(mr, F(31) + 9, (8.0, -9.0, 0), (0, 0, 180))
key(mr, F(31) + 18, (7.4, -3.8, 0), (0, 0, 228))
key(mr, F(31) + 24, (6.2, -2.65, 0), (0, 0, 268))
key(mr, f_of(23.20) - 2, MUS_STOP, (0, 0, 270))
key(mr, f_of(23.20), MUS_STOP, (1.2, 0, 270))                 # rocks once as the engine cuts
key(mr, f_of(23.20) + 3, MUS_STOP, (-0.6, 0, 270))
key(mr, L(31), MUS_STOP, (0, 0, 270))
mons_seat = seated("MonsoorSeated", mus, MONSOOR, glasses="#111111")
only_in(mons_seat["root"], [31])
mdp = mus["door"]
key(mdp, F(31), rot=(0, 0, 0))
key(mdp, F(32) - 1, rot=(0, 0, 0))
key(mdp, F(32), rot=(0, 0, 65))
key(mdp, f_of(23.85) - 2, rot=(0, 0, 65))
key(mdp, f_of(23.85) + 1, rot=(0, 0, 0))                       # door thunk 23.85
mons = person("Monsoor", loc=(6.6, -1.2, 0), rz=180, glasses="#111111", **MONSOOR)
only_in(mons["root"], [32, 33, 34, 35])
mo = mons["root"]
key(mons["legR"], F(32), loc=(-0.097, 0, 0.22))
key(mons["legR"], F(32) + 5, loc=(-0.097, 0, 0.0))             # loafer lands flat
key(mo, F(32), (6.6, -1.35, 0), (0, 0, 180))
key(mo, F(33) - 1, (6.6, -1.35, 0), (0, 0, 180))
key(mo, F(33), (6.6, -1.3, -0.22), (0, 0, 180))
key(mo, F(33) + 6, (6.6, -1.15, 0), (0, 0, 180))                # rises
key(mo, F(33) + 14, (6.5, -1.1, 0), (0, 0, 180))
key(mo, F(33) + 18, (6.3, -1.05, 0), (0, 0, -100))              # turns to Arfan, starts walking
key(mo, L(33), (5.4, -1.0, 0), (0, 0, -92))
key(mons["R"], F(33) + 2, rot=(0, 0, 0))
key(mons["R"], F(33) + 5, rot=(10, 70, 0))                      # easy door push, hand rests on the roof
key(mons["R"], F(33) + 14, rot=(10, 70, 0))
key(mons["R"], F(33) + 19, rot=(0, 0, 0))
MON_FIN = (2.15, -1.0, 0)
key(mo, F(34), (2.45, -1.0, 0), (0, 0, -90))
key(mo, F(34) + 6, MON_FIN, (0, 0, -90))
key(mo, END, MON_FIN, (0, 0, -90))
ML = mons["L"]
key(ML, F(34) + 2, rot=(-20, 0, 0))
key(ML, f_of(25.20), rot=(-86, 0, 4))                            # hand lands on Arfan's right shoulder
key(ML, f_of(25.20) + 3, rot=(-81, 0, 4))                        # one soft pat
key(ML, f_of(25.20) + 6, rot=(-86, 0, 4))
key(ML, END, rot=(-86, 0, 4))
talk(mons["mouth"], f_of(25.30), f_of(25.80))
# Arfan in the yard: at the windscreen (30-33), then facing Monsoor (34-35)
arf_y = person("ArfanYard", loc=(0.25, -0.6, 0), rz=180, glasses="#7fbf8f", **ARFAN)
only_in(arf_y["root"], [30, 31, 32, 33, 34, 35])
ay = arf_y["root"]
key(ay, F(30), (0.05, -0.75, 0), (0, 0, 160))
key(ay, L(31), (0.1, -0.85, 0), (0, 0, 150))
key(ay, L(33), (0.4, -0.9, 0), (0, 0, 110))
key(ay, F(34), (1.5, -1.0, 0), (0, 0, 90))
key(ay, END, (1.5, -1.0, 0), (0, 0, 90))
key(arf_y["R"], F(30), rot=(-80, 0, 20))
key(arf_y["R"], L(30) + 2, rot=(0, 0, 0))
ayh = arf_y["head"]
key(ayh, F(34), rot=(0, 0, 0))
key(ayh, f_of(25.25), rot=(6, 0, 0))                             # shoulder dips
key(ayh, f_of(25.60), rot=(-2, 0, 6))                            # looks at him
key(ayh, L(34), rot=(7, 0, 4))                                   # chin a touch down
key(ayh, F(35) + 6, rot=(4, 0, 2))
key(ayh, f_of(26.70), rot=(-4, 0, 2))                            # eyebrow lift, smile becomes real
talk(arf_y["mouth"], f_of(26.45), f_of(28.01))
key(ayh, f_of(27.40), rot=(10, 0, 0))                            # glances down
key(ayh, L(35), rot=(0, 0, 3))                                   # back up
key(arf_y["torso"], f_of(25.25) - 2, loc=arf_y["torso"].location.copy())
key(arf_y["torso"], f_of(25.25) + 2, loc=arf_y["torso"].location + Vector((0, 0, -0.015)))
sweep = area("yd_sweep", (-6, -4, 2.0), 0, 1.5, (1.0, 0.85, 0.6), rot=(90, 0, 0))
for f, e, x in ((F(41) - 1, 0, -6), (f_of(35.3), 0, -6), (f_of(35.4), 600, -5), (f_of(37.2), 600, 3.5), (f_of(37.3), 0, 3.5)):
    sweep.data.energy = e
    sweep.data.keyframe_insert("energy", frame=f)
    key(sweep, f, loc=(x, -4, 2.0))

# ---------------- DAVE'S DRIVEWAY, golden hour (x = -80) ----------------
HX = -80
box("hm_ground", (60, 50, 0.1), (HX, 6, -0.05), "#6f8f47", rough=0.95)
box("hm_street", (90, 8, 0.02), (HX, -10, 0.01), "#3b3d42")
box("hm_path", (90, 1.6, 0.1), (HX, -5.3, 0.05), "#b9b2a5")
box("hm_drive", (4.4, 10, 0.03), (HX + 3, -1.0, 0.02), "#a9a49a")
box("hm_house", (14, 8, 3.0), (HX, 8, 1.5), "#c8955f")
box("hm_roof", (14.6, 8.6, 0.5), (HX, 8, 3.3), "#9b4a33")
box("hm_garage", (4.0, 0.1, 2.4), (HX + 3, 3.95, 1.2), "#e3d8c3")
box("hm_door", (1.0, 0.1, 2.1), (HX - 2, 3.95, 1.05), "#5a3420")
box("hm_window", (2.2, 0.1, 1.2), (HX - 5, 3.95, 1.6), "#ffd9a0", emit=0.6)
box("hm_letterbox", (0.4, 0.4, 1.0), (HX + 0.4, -4.4, 0.5), "#a5683f")
ball("hm_tree", 1.8, (HX - 7.5, 0.5, 3.2), "#4f7a38")
cyl("hm_trunk", 0.18, 2.4, (HX - 7.5, 0.5, 1.2), "#5a3d26")
car("asx_home", (HX - 4.5, -7.1, 0), 90, "#7a7f86")
chr_h = car("chr_h", (HX - 8, -11.5, 0), 90, "#0b0c0e", hero=True, plate_bar=True, decal=True, glass=True)
ch = chr_h["root"]
sold_h = sold_tag("sold_tag_h", chr_h["windscreen"])
key(ch, F(36), (HX - 7.0, -11.5, 0), (0, 0, 90))
key(ch, F(36) + 12, (HX + 0.2, -11.0, 0), (0, 0, 108))
key(ch, F(36) + 22, (HX + 2.9, -5.2, 0), (0, 0, 172))
key(ch, F(36) + 28, (HX + 3.0, -1.3, 0), (0, 0, 180))
key(ch, L(36) - 1, (HX + 3.0, -1.2, -0.02), (1.2, 0, 180))       # nose dips, settles
key(ch, L(36) + 2, (HX + 3.0, -1.2, 0), (0, 0, 180))
arf_hs = seated("ArfanHomeSeated", chr_h, ARFAN, glasses="#7fbf8f")
only_in(arf_hs["root"], [36])
dave_h = person("DaveHome", loc=(HX + 5.9, -1.5, 0), rz=-45, **DAVE)
only_in(dave_h["root"], [36, 37, 38, 39, 40])
arf_h = person("ArfanHome", loc=(HX + 4.3, -0.6, 0), rz=150, glasses="#7fbf8f", **ARFAN)
only_in(arf_h["root"], [37, 38, 39, 40])
ah = arf_h["root"]
key(ah, F(37), (HX + 4.3, -0.5, 0), (0, 0, 150))
key(ah, F(37) + 14, (HX + 4.7, -1.4, 0), (0, 0, 60))
key(ah, L(37), (HX + 5.0, -1.9, 0), (0, 0, 45))                  # the two in a V
key(ah, F(40) + 10, (HX + 5.0, -1.9, 0), (0, 0, 45))
key(ah, F(40) + 22, (HX + 4.75, -2.15, 0), (0, 0, 45))           # half-pace back
key(arf_h["R"], F(37) + 12, rot=(0, 0, 0))
key(arf_h["R"], L(37) - 2, rot=(-75, 0, 0))                      # palm comes up flat with the keys
key(arf_h["R"], F(40) + 4, rot=(-75, 0, 0))
key(arf_h["R"], F(40) + 12, rot=(0, 0, 0))
fob = box("fob_h", (0.05, 0.08, 0.025), (0, 0, -0.67), "#101010", arf_h["R"])
show_frames(fob, [(F(37) + 10, F(40) + 6)])
dhh = dave_h
key(dhh["head"], F(37), rot=(0, 0, 0))
key(dhh["R"], F(40), rot=(0, 0, 0))
key(dhh["R"], F(40) + 8, rot=(-60, 0, 0))                        # Dave weighs the keys
key(dhh["head"], F(40) + 8, rot=(12, 0, 0))                      # grins at the keys
key(dhh["head"], F(40) + 24, rot=(-2, 0, 55))                    # looks down the street
key(dhh["head"], L(40), rot=(-2, 0, 50))
fob_d = box("fob_d", (0.05, 0.08, 0.025), (0, 0, -0.67), "#101010", dhh["R"])
show_frames(fob_d, [(F(40) + 7, END)])
mia_h = person("MiaHome", loc=(HX - 2, 3.4, 0), rz=180, **MIA)
only_in(mia_h["root"], [39, 40])
mr2 = mia_h["root"]
key(mr2, F(39), (HX - 2, 3.6, 0), (0, 0, 180))
key(mr2, F(39) + 2, (HX - 2, 3.2, 0), (0, 0, 220))               # bursts out of the front door
for i, (x, y, z) in enumerate(((HX - 0.8, 2.6, 0.06), (HX + 0.6, 2.1, 0), (HX + 1.9, 1.85, 0.06),
                               (HX + 3.3, 1.75, 0), (HX + 4.5, 1.2, 0.05), (HX + 4.55, 0.4, 0),
                               (HX + 4.45, -0.2, 0.04))):
    key(mr2, F(39) + 5 + i * 4 + (1 if i in (2, 5) else 0), (x, y, z), (0, 0, 245 if i < 4 else 200))  # uneven strides
key(mr2, F(40), (HX + 4.35, -0.35, 0), (0, 0, 270))
key(mr2, L(40), (HX + 4.32, -0.35, 0), (0, 0, 270))
for side in ("R", "L"):
    key(mia_h[side], F(39), rot=(25, 0, 0))
    key(mia_h[side], F(39) + 6, rot=(-35, 0, 0))
    key(mia_h[side], F(39) + 12, rot=(30, 0, 0))
    key(mia_h[side], F(39) + 18, rot=(-35, 0, 0))
    key(mia_h[side], F(40), rot=(-80, 0, 0))                     # palms flat on the door
    key(mia_h[side], L(40), rot=(-80, 0, 0))

# ---------------- INSERT RIGS (x = 600+) ----------------
def dial(name, r, loc, parent, face="#1a1d24"):
    cyl(name + "_ring", r * 1.08, 0.012, loc, "#9aa0a8", parent, rot=(90, 0, 0), metal=0.8, rough=0.3)
    cyl(name, r, 0.016, (loc[0], loc[1] - 0.004, loc[2]), face, parent, rot=(90, 0, 0))
    for k in range(9):
        a = radians(-135 + k * 270 / 8)
        box(f"{name}_tick{k}", (0.003, 0.002, r * 0.16),
            (loc[0] + 0.85 * r * sin(a), loc[1] - 0.014, loc[2] + 0.85 * r * cos(a)),
            "#e8e8e8", parent, rot=(0, -135 + k * 270 / 8, 0), emit=1.5)
    pv = empty(name + "_pivot", (loc[0], loc[1] - 0.016, loc[2]), parent)
    box(name + "_needle", (0.004, 0.002, r * 0.85), (0, 0, r * 0.38), "#ff5a1f", pv, emit=4)
    return pv


def speed_angle(v, vmax=240):
    return -135 + v * 270 / vmax


rigs = {}


def dash_rig(name, ox, kind):
    r = empty(name, (ox, 0, 1.0))
    box(name + "_panel", (0.7, 0.05, 0.34), (0, 0.03, 0), "#0e1014", r)
    box(name + "_hood", (0.72, 0.25, 0.04), (0, -0.08, 0.19), "#0e1014", r)
    cyl(name + "_wheel", 0.19, 0.03, (0, -0.42, -0.22), "#0a0a0a", r, rot=(70, 0, 0))
    point(name + "_light", (0, -0.6, 0.35), 3.0, (1.0, 0.95, 0.9), r, radius=0.3)
    out = {"root": r}
    if kind in ("seltos", "asx", "v8", "cx3"):
        out["speedo"] = dial(name + "_spd", 0.075, (-0.07, 0, 0.0), r)
        out["fuel"] = dial(name + "_fuel", 0.036, (0.08, 0, -0.035), r)
        out["fuel"].rotation_euler = (0, radians(-50), 0)              # needle near E
        if kind in ("seltos", "asx"):
            ball(name + "_lowfuel", 0.009, (0.08, -0.02, 0.025), "#ffb000", r, emit=10)
        if kind in ("asx", "cx3"):
            box(name + "_mid", (0.07, 0.004, 0.035), (0.08, -0.012, 0.045), "#9fd0ff", r, emit=1.5)
    if kind == "kona":
        box(name + "_screen", (0.30, 0.006, 0.11), (0, -0.012, 0.0), "#1e4d8c", r, emit=1.2)
        for k in range(10):
            box(f"{name}_bar{k}", (0.012, 0.004, 0.008 + 0.006 * k), (-0.11 + k * 0.016, -0.016, -0.03 + 0.003 * k),
                "#7fd3ff", r, emit=4)
        box(name + "_fuelbar", (0.02, 0.004, 0.05), (0.12, -0.016, -0.01), "#ffb000", r, emit=4)
    if kind == "chr":
        box(name + "_screen", (0.30, 0.006, 0.11), (0, -0.012, 0.0), "#05070a", r)
        ready = text(name + "_ready", "READY", 0.03, (0, -0.017, 0.022), "#59ff9a", r, emit=8)
        trip = box(name + "_trip", (0.16, 0.004, 0.035), (0, -0.016, -0.025), "#9fd0ff", r, emit=1.4)
        show_frames(ready, [(f_of(15.25), END)])
        show_frames(trip, [(f_of(15.65), END)])
    if kind == "v8":
        a60 = radians(speed_angle(60))
        text(name + "_60", "60", 0.012, (-0.07 + 0.05 * sin(a60), -0.017, 0.05 * cos(a60)), "#ffffff", r, emit=3)
    rigs[name] = out
    return out


d_seltos = dash_rig("dash_seltos", 600, "seltos")
d_cx3 = dash_rig("dash_cx3", 604, "cx3")
d_kona = dash_rig("dash_kona", 608, "kona")
d_v8 = dash_rig("dash_v8", 612, "v8")
d_asx = dash_rig("dash_asx", 616, "asx")
d_chr = dash_rig("dash_chr", 620, "chr")
d_seltos["speedo"].rotation_euler = (0, radians(speed_angle(0)), 0)
d_cx3["speedo"].rotation_euler = (0, radians(speed_angle(0)), 0)
d_asx["speedo"].rotation_euler = (0, radians(speed_angle(0)), 0)
key(d_v8["speedo"], F(9), rot=(0, speed_angle(64), 0))
key(d_v8["speedo"], L(9), rot=(0, speed_angle(67), 0))
interp(d_v8["speedo"], "LINEAR")
d_v8["fuel"].rotation_euler = (0, radians(-55), 0)

# pump meter (pumps identical: one face for #16 and #23)
pm = empty("pumpmeter", (630, 0, 1.0))
box("pm_face", (0.6, 0.06, 0.7), (0, 0.03, 0), "#e4e7ea", pm)
box("pm_win", (0.44, 0.01, 0.26), (0, -0.005, 0.05), "#06080a", pm)
pm_dollar = text("pm_dollar", "$ --.--", 0.05, (0.0, -0.012, 0.12), "#4f8f5a", pm, emit=1.5)
pm_lit = text("pm_litres", "00.00 L", 0.05, (0.0, -0.012, 0.0), "#9dff9a", pm, emit=6)
text("pm_ulp", "ULP 91", 0.04, (0, -0.012, -0.22), "#0F2747", pm)
point("pm_light", (0, -0.6, 0.3), 3.0, (0.9, 0.95, 1.0), pm, radius=0.3)


def litres(f):
    a16, b16 = rng(16)
    a23, b23 = rng(23)
    if f <= b16 + 1:
        u = max(0, min(1, (f - a16) / max(1, b16 - a16)))
        return 31.4 + 1.6 * u
    stop = f_of(14.10)
    u = max(0, min(1, (f - a23) / max(1, stop - a23)))
    return 9.20 + 0.64 * u


def pump_handler(scn, *a):
    f = scn.frame_current
    v = litres(f)
    pm_lit.data.body = "%05.2f L" % v
    pm_dollar.data.body = "$ %05.2f" % (v * 1.799)


bpy.app.handlers.frame_change_pre.append(pump_handler)
pump_handler(sc)

# POWER button (left index finger, olive Seiko)
pw = empty("powerrig", (640, 0, 1.0))
box("pw_console", (0.4, 0.3, 0.05), (0, 0, 0), "#121418", pw)
cyl("pw_btn", 0.022, 0.014, (0, 0, 0.032), "#1c1f24", pw)
cyl("pw_btnring", 0.026, 0.008, (0, 0, 0.028), "#3fa9ff", pw, emit=4)
text("pw_txt", "POWER", 0.012, (0, -0.045, 0.027), "#d8d8d8", pw, rot=(0, 0, 0), emit=2)
fing = empty("pw_finger", (0.0, 0.0, 0.07), pw)
box("pw_fing", (0.018, 0.075, 0.018), (0, 0.03, 0), SKIN_A, fing)
ball("pw_handb", 0.05, (0.0, 0.11, 0.02), SKIN_A, fing, scale=(1.2, 1.1, 0.6))
cyl("pw_wrist", 0.032, 0.12, (0.0, 0.2, 0.03), SKIN_A, fing, rot=(90, 0, 0))
cyl("pw_watch", 0.03, 0.012, (0.0, 0.19, 0.068), "#556b2f", fing, rot=(0, 0, 0))
cyl("pw_strap", 0.035, 0.03, (0.0, 0.19, 0.03), "#3b4a22", fing, rot=(90, 0, 0))
point("pw_light", (0.1, -0.2, 0.4), 2.5, (1, 0.95, 0.9), pw, radius=0.3)
pf = f_of(14.85)
key(fing, F(25), loc=(0, 0, 0.08))
key(fing, pf - 2, loc=(0, 0, 0.05))
key(fing, pf, loc=(0, 0, 0.042))           # one firm press, held 3 frames
key(fing, pf + 3, loc=(0, 0, 0.042))
key(fing, pf + 7, loc=(0, 0, 0.075))       # lift

# key fob on Arfan's open palm
fr = empty("fobrig", (650, 0, 1.0))
ball("fb_palm", 0.055, (0, 0, 0), SKIN_A, fr, scale=(1.0, 1.35, 0.35))
for k, x in enumerate((-0.036, -0.012, 0.012, 0.036)):
    box(f"fb_fing{k}", (0.017, 0.07, 0.016), (x, -0.1, 0.005), SKIN_A, fr)
box("fb_thumb", (0.018, 0.05, 0.016), (0.06, -0.02, 0.008), SKIN_A, fr, rot=(0, 0, -35))
cyl("fb_ring", 0.012, 0.012, (0.012, -0.075, 0.006), "#d8dce2", fr, rot=(90, 0, 0), metal=1, rough=0.15)
box("fb_fob", (0.036, 0.062, 0.014), (-0.004, 0.0, 0.028), "#111111", fr, rough=0.3)
box("fb_fobbtn", (0.02, 0.012, 0.004), (-0.004, -0.012, 0.036), "#5a5a5a", fr)
cyl("fb_keyring", 0.012, 0.003, (-0.004, 0.04, 0.026), "#c8ccd2", fr, metal=1)
cyl("fb_wrist", 0.035, 0.12, (0.0, 0.13, -0.005), SKIN_A, fr, rot=(90, 0, 0))
point("fb_light", (-0.25, -0.1, 0.25), 3.0, (1.0, 0.75, 0.5), fr, radius=0.3)
key(fr, F(38), loc=(650, 0, 1.0))
key(fr, L(38), loc=(650, 0.004, 1.003))

# ---------------- CAMERAS ----------------
cams = {}


def camera(name, lens, parent=None):
    c = bpy.data.cameras.new(name)
    c.lens = lens
    c.clip_start, c.clip_end = 0.02, 500
    o = bpy.data.objects.new(name, c)
    sc.collection.objects.link(o)
    if parent:
        o.parent = parent
    t = empty(name + "_t", (0, 0, 0), parent)
    con = o.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = t, "TRACK_NEGATIVE_Z", "UP_Y"
    cams[name] = o
    return o, t


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def move(n, lens, c0, c1, t0, t1, shake=0.0, parent=None, f0=None, f1=None):
    """Camera for shot n: c0->c1 position, t0->t1 aim; shake = handheld amplitude (m)."""
    cam, tgt = camera(f"C{n:02d}", lens, parent)
    a, b = rng(n)
    f0 = f0 or a
    f1 = f1 or b
    if not shake:
        key(cam, f0, c0)
        key(cam, f1, c1)
        key(tgt, f0, t0)
        key(tgt, f1, t1)
        return cam
    rnd = random.Random(n)
    frames = list(range(f0, f1 + 1, 3))
    if frames[-1] != f1:
        frames.append(f1)
    for f in frames:
        u = (f - f0) / max(1, f1 - f0)
        u = u * u * (3 - 2 * u)
        jit = Vector([rnd.uniform(-shake, shake) for _ in range(3)])
        key(cam, f, Vector(lerp(c0, c1, u)) + jit)
        key(tgt, f, Vector(lerp(t0, t1, u)) + jit * 0.4)
    return cam


def wpos(obj, f):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    return tuple(obj.matrix_world.translation)


def push(c, t, pct):
    """Point pct of the way from camera c toward target t (a % push)."""
    return lerp(c, t, pct)


ox = MONT["cbd"]
# 1 WS low, 75mm, ahead of the car, tracking back with it, settling
move(1, 75, (ox + 5.2, -10.5, 0.45), (ox + 5.0, -14.2, 0.42), (ox + LANE, 10.5, 1.1), (ox + LANE, 2.5, 1.0))
# 2 MCU through the windscreen, same take settled, idle vibration
hp = (ox + LANE - 0.40, 2.6, 1.24)
move(2, 75, (hp[0] + 0.05, 0.75, 1.46), (hp[0] + 0.05, 0.78, 1.46), hp, hp, shake=0.003)
# 3 CU high over the wheel on the Seltos cluster, 3% push
R = (600, 0, 1.0)
R = (600.01, 0, 1.0)
move(3, 100, (R[0], -1.1, 1.38), push((R[0], -1.1, 1.38), R, 0.03), R, R)
ox = MONT["ramp"]
hp = (ox + LANE - 0.40, 2.65, 1.24)
# 4 MCU passenger side, handheld breathing
move(4, 75, (ox + LANE + 1.35, 1.95, 1.27), (ox + LANE + 1.33, 1.93, 1.27), hp, hp, shake=0.006)
R = (604, 0, 1.0)
move(5, 100, (604.02, -0.75, 1.30), push((604.02, -0.75, 1.30), R, 0.03), (604.03, 0, 1.0), (604.03, 0, 1.0))
ox = MONT["eq"]
hp = (ox + LANE - 0.40, 2.25, 1.16)
# 6 MCU slight low from the dash side, car rig
move(6, 75, (ox + LANE - 0.30, 0.55, 1.06), (ox + LANE - 0.29, 0.57, 1.06), hp, hp, shake=0.003)
R = (608, 0, 1.0)
move(7, 100, (608, -1.5, 1.45), (608, -1.5, 1.45), R, R)
ox = MONT["nb"]
# 8 WS low at the kerb, 32mm, static then a short track
move(8, 32, (ox + 6.0, -5.5, 0.45), (ox + 6.0, -5.5, 0.45), (ox + LANE, 2.6, 1.1), (ox + LANE, 2.6, 1.1),
     f0=F(8), f1=F(8) + 6)
c8 = cams["C08"]
key(c8, L(8), (ox + 5.6, -7.0, 0.45))
key(bpy.data.objects["C08_t"], L(8), (ox + LANE, 0.2, 1.0))
R = (612, 0, 1.0)
move(9, 100, (611.93, -0.62, 1.22), (611.93, -0.62, 1.22), (611.93, 0, 1.0), (611.93, 0, 1.0))
# 10 WS low tracking: car comes at us past the 60 sign and the speed camera
move(10, 32, (ox + 7.3, -31.0, 0.5), (ox + 7.0, -32.5, 0.5), (ox + LANE + 0.5, -17.0, 1.6), (ox + LANE + 1.0, -24.0, 1.6))
# 11 CU passenger side, car rig (camera rides with the car)
move(11, 75, (0.5, -0.45, 1.38), (0.5, -0.44, 1.38), (-0.45, 0.30, 1.36), (-0.45, 0.30, 1.34), shake=0.003, parent=lr)
ox = MONT["alb"]
# 12 MCU outside the passenger window, slow 2% push, Mia asleep behind
c0 = (ox + LANE + 2.1, 2.2, 1.28)
t12 = (ox + LANE - 0.4, 3.05, 1.2)
move(12, 50, c0, push(c0, t12, 0.02), t12, t12)
R = (616, 0, 1.0)
move(13, 100, (616.0, -1.1, 1.38), (616.0, -1.1, 1.38), (616.0, 0, 1.0), (616.0, 0, 1.0))
# servo
c0 = (SX - 15.5, -16.5, 0.5)
t14 = (SX - 11, -6.6, 4.6)
move(14, 40, c0, push(c0, t14, 0.03), t14, t14)
move(15, 50, (SX + 2.0, -6.6, 1.6), (SX + 2.3, -5.4, 1.6), (SX + 4.4, 0.8, 1.3), (SX + 4.4, 0.8, 1.35))
move(16, 100, (630, -1.15, 1.06), (630, -1.15, 1.06), (630, 0, 1.03), (630, 0, 1.03))
# 17 MCU, end of the same push, on Dave's face
move(17, 50, (SX + 2.95, -0.75, 1.66), (SX + 3.1, -0.55, 1.66), (SX + 4.25, 0.75, 1.62), (SX + 4.25, 0.75, 1.62))
# 18 CU Mia asleep against the window (rear right, outside), 2% push
mpos = wpos(mia["head"], F(18))
mpos = (mpos[0], mpos[1], mpos[2] + 0.08)
c0 = (mpos[0] + 1.0, mpos[1] + 0.5, mpos[2] + 0.06)
move(18, 75, c0, push(c0, mpos, 0.02), mpos, mpos)
# 19 WS low car rig alongside the C-HR, then it swings in to pump 1
move(19, 32, (SX - 27.0, -15.6, 0.55), (SX - 12.0, -15.6, 0.55), (SX - 26.0, -11.8, 0.8), (SX - 10.0, -9.0, 0.8),
     f0=F(19), f1=F(19) + 18)
c19 = cams["C19"]
key(c19, L(19), (SX - 9.5, -14.5, 0.6))
key(bpy.data.objects["C19_t"], L(19), (SX - 4.5, 0.8, 1.0))
# 20 ECU ground: Arfan's boot in the puddle
bp = (SX - 4.2, 1.8, 0.06)
move(20, 32, (SX - 3.98, 1.25, 0.07), (SX - 3.98, 1.25, 0.07), bp, bp)
# 21 MS -> MCU, 50mm gimbal straight push on Arfan by pump 1
ah21 = (SX - 4.25, 1.9, 1.62)
move(21, 50, (SX - 1.5, 4.6, 1.62), (SX - 3.25, 2.95, 1.64), ah21, ah21, shake=0.002)
# 22 CU nozzle into the filler
fp = (SX - 4.62, 0.52, 0.9)
move(22, 100, (SX - 3.75, -0.25, 1.02), (SX - 3.75, -0.25, 1.02), fp, fp)
move(23, 100, (630, -1.15, 1.06), (630, -1.15, 1.06), (630, 0, 1.03), (630, 0, 1.03))
# 24 MS Dave still filling, locked off, C-HR soft behind
move(24, 50, (SX + 7.4, -0.6, 1.72), (SX + 7.4, -0.6, 1.72), (SX + 1.0, 1.4, 1.3), (SX + 1.0, 1.4, 1.3))
R = (640, 0.07, 1.05)
move(25, 100, (640.3, -0.08, 1.42), (640.3, -0.08, 1.42), R, R)
# 26 CU C-HR cluster, 3% pull-out
R = (620, 0, 1.0)
c0 = (620, -1.5, 1.3)
move(26, 100, push(c0, R, 0.03), c0, R, R)
# 27 MS low rear three-quarter at the pump, 3% push
t27 = (SX - 5.6, -0.2, 0.75)
c0 = (SX - 8.6, -4.6, 0.65)
move(27, 50, c0, push(c0, t27, 0.03), t27, t27)
# 28 MCU Dave's double take; C-HR leaves behind him
move(28, 50, (SX + 3.1, -0.6, 1.64), (SX + 3.1, -0.6, 1.64), (SX + 4.3, 0.85, 1.7), (SX + 4.3, 0.85, 1.7),
     shake=0.002)
# 29 CU Mia awake at the open rear window, slight handheld
mpos = wpos(mia["head"], F(29) + 2)
mpos = (mpos[0], mpos[1], mpos[2] + 0.08)
move(29, 75, (mpos[0] + 1.25, mpos[1] - 0.15, mpos[2] + 0.04), (mpos[0] + 1.22, mpos[1] - 0.14, mpos[2] + 0.04),
     mpos, mpos, shake=0.005)
# 30 ECU SOLD tag on the windscreen
tp = wpos(sold, F(30))
move(30, 100, (tp[0] + 0.05, tp[1] - 0.95, tp[2] + 0.12), (tp[0] + 0.05, tp[1] - 0.95, tp[2] + 0.12), tp, tp)
# 31 WS low track alongside the muscle car, settling
move(31, 32, (14.0, -8.2, 0.5), (14.4, -6.9, 0.5), (8.0, -12.0, 0.8), (7.6, -5.0, 0.8), f0=F(31), f1=F(31) + 14)
key(cams["C31"], L(31), (14.5, -6.7, 0.5))
key(bpy.data.objects["C31_t"], L(31), (5.5, -2.4, 0.9))
# 32 ECU ground: the loafer lands (match cut with #20)
lp = (6.7, -1.32, 0.07)
move(32, 32, (7.05, -0.72, 0.12), (7.05, -0.72, 0.12), lp, lp)
# 33 MS low, settled: Monsoor rises, door, smile, first step
move(33, 32, (8.1, 0.45, 0.42), (8.1, 0.45, 0.42), (6.4, -1.2, 1.2), (5.8, -1.1, 1.25))
# 34 MCU OTS over Monsoor's right shoulder onto Arfan, slow push
c0 = (3.25, -0.42, 1.68)
t34 = (1.55, -1.05, 1.62)
move(34, 75, c0, push(c0, t34, 0.08), t34, t34)
# 35 CU Arfan, end of the push, Monsoor's hand at the frame edge
move(35, 75, (2.42, -0.15, 1.7), (2.40, -0.17, 1.7), (1.5, -1.05, 1.64), (1.5, -1.05, 1.64))
# 36 WS low at the kerb, short track then settle
move(36, 32, (HX + 6.8, -7.6, 0.5), (HX + 7.2, -6.6, 0.5), (HX + 1.0, -10.5, 0.9), (HX + 3.0, -1.2, 0.9),
     f0=F(36), f1=F(36) + 26)
key(cams["C36"], L(36), (HX + 7.2, -6.6, 0.5))
key(bpy.data.objects["C36_t"], L(36), (HX + 2.4, -0.4, 1.0))
# 37 MS 50mm gimbal push, the two in a V
move(37, 50, (HX + 7.9, -6.0, 1.6), (HX + 7.4, -5.1, 1.6), (HX + 4.9, -1.1, 1.25), (HX + 5.1, -1.4, 1.2), shake=0.002)
R = (650, 0, 1.01)
move(38, 100, (650, -0.26, 1.52), (650, -0.26, 1.52), R, R)
# 39 WS low, same set-up as 36 (settled): Mia runs out
move(39, 32, (HX + 7.2, -6.6, 0.5), (HX + 7.2, -6.6, 0.5), (HX + 1.6, 0.4, 1.0), (HX + 3.4, -0.2, 0.9))
# 40 MS eye, end of the 37 push
move(40, 50, (HX + 7.4, -5.1, 1.55), (HX + 7.3, -4.9, 1.55), (HX + 4.9, -1.0, 1.0), (HX + 4.9, -1.0, 1.0),
     shake=0.002)
# 41 brand: golden-hour hero of the black C-HR in our yard, 3% push
c0 = (3.6, -5.6, 0.75)
t41 = (-0.9, 1.0, 1.0)
move(41, 40, c0, push(c0, t41, 0.03), t41, t41)

# per-shot visibility: yard actors are off for the brand hero, sold tag on the home car from 36
only_in(mons["root"], [32, 33, 34, 35])
for o in (mr,):
    only_in(o, [31, 32, 33, 34, 35])
show_frames(sold_h, [(F(36), END)])

for s in SHOTS:
    n = s[0]
    sc.timeline_markers.new(f"S{n:02d}", frame=F(n)).camera = cams[f"C{n:02d}"]
sc.camera = cams["C01"]
sc.frame_set(1)

if SAVE_BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_BLEND)
if TEST_FRAMES:
    for f in TEST_FRAMES:
        sc.frame_set(f)
        n = next(s[0] for s in SHOTS if rng(s[0])[0] <= f <= rng(s[0])[1])
        sc.camera = cams[f"C{n:02d}"]
        sc.render.filepath = FRAMES_DIR.rstrip("/") + "/f_%04d.png" % f
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
