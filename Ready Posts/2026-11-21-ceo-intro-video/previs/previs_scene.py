"""3D blocking (previs) v3 for the Monsoor Motors CEO intro video: two shots, 32 s.

Arfan stays on his mark; in shot 2 the camera travels to his side and pushes in.

Run:  blender -b -P previs_scene.py -- <frames_dir> [save.blend] [frame frame ...]
With frame numbers it renders only those stills (quick test). Otherwise the whole video.
540x960, 24 fps. Shot 1 = frames 1-216 (9 s), Shot 2 = frames 217-768 (23 s).
Sizes in metres. People face -Y (toward the camera) by default.
"""
import sys
from math import radians

import bpy
from mathutils import Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FRAMES_DIR = argv[0] if argv else "/tmp/previs_frames"
SAVE_BLEND = argv[1] if len(argv) > 1 and argv[1].endswith(".blend") else None
TEST_FRAMES = [int(a) for a in argv[1:] if a.isdigit()]

S1_END, S2_START, END = 216, 217, 768

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, END
scene.render.resolution_x, scene.render.resolution_y = 540, 960
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = FRAMES_DIR.rstrip("/") + "/f_"

ENGINE = "BLENDER_WORKBENCH"
for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try:
        scene.render.engine = eng
        ENGINE = eng
        break
    except Exception:
        pass
if ENGINE == "BLENDER_WORKBENCH":
    scene.render.engine = ENGINE
    sh = scene.display.shading
    sh.light, sh.color_type, sh.show_shadows, sh.show_cavity = "STUDIO", "MATERIAL", True, True
else:
    try:
        scene.eevee.taa_render_samples = 16
    except Exception:
        pass
try:
    scene.view_settings.view_transform = "Standard"
except Exception:
    pass
print("ENGINE", ENGINE)

world = bpy.data.worlds.new("World")
scene.world = world
world.color = (0.60, 0.74, 0.92)
try:
    world.use_nodes = True
except Exception:
    pass
try:
    bg = world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.60, 0.74, 0.92, 1.0)
    bg.inputs[1].default_value = 1.1
except Exception:
    pass

sun_data = bpy.data.lights.new("Sun", "SUN")
sun_data.energy = 3.6
try:
    sun_data.angle = radians(6)
except Exception:
    pass
sun = bpy.data.objects.new("Sun", sun_data)
scene.collection.objects.link(sun)
sun.rotation_euler = (radians(52), 0, radians(-38))  # late-afternoon light from camera-left

_mats = {}


def mat(hexstr, rough=0.7, metal=0.0):
    k = (hexstr, rough, metal)
    if k in _mats:
        return _mats[k]
    h = hexstr.lstrip("#")
    col = tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1.0,)
    m = bpy.data.materials.new("m_" + h)
    m.diffuse_color = col
    try:
        m.use_nodes = True
    except Exception:
        pass
    try:
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = col
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal
    except Exception:
        pass
    _mats[k] = m
    return m


def finish(obj, name, loc, color, parent, rough=0.7, metal=0.0):
    obj.name = name
    obj.location = loc
    obj.data.materials.append(mat(color, rough, metal))
    if parent:
        obj.parent = parent
    return obj


def empty(name, loc=(0, 0, 0), parent=None):
    obj = bpy.data.objects.new(name, None)
    scene.collection.objects.link(obj)
    obj.location = loc
    if parent:
        obj.parent = parent
    return obj


def box(name, size, loc, color, parent=None, pivot_top=False, rot=None, rough=0.7, metal=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    if pivot_top:
        obj.data.transform(Matrix.Translation((0, 0, -0.5)))
    obj.scale = size
    if rot:
        obj.rotation_euler = [radians(a) for a in rot]
    return finish(obj, name, loc, color, parent, rough, metal)


def ball(name, radius, loc, color, parent=None, scale=(1, 1, 1), rough=0.7):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=24, ring_count=12)
    obj = bpy.context.active_object
    obj.scale = scale
    bpy.ops.object.shade_smooth()
    return finish(obj, name, loc, color, parent, rough)


def cyl(name, radius, depth, loc, color, parent=None, rot=None, pivot_top=False, rough=0.7, metal=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=24)
    obj = bpy.context.active_object
    if pivot_top:
        obj.data.transform(Matrix.Translation((0, 0, -depth / 2)))
    if rot:
        obj.rotation_euler = [radians(a) for a in rot]
    bpy.ops.object.shade_smooth()
    return finish(obj, name, loc, color, parent, rough, metal)


def text(name, body, size, loc, color, parent=None):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body, cu.size, cu.align_x = body, size, "CENTER"
    obj = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(obj)
    obj.rotation_euler = (radians(90), 0, 0)
    return finish(obj, name, loc, color, parent, 0.6)


def person(name, shirt, pants, skin, hair, beard=None):
    root = empty(name)
    for side, x in (("L", -0.10), ("R", 0.10)):
        cyl(name + "_leg" + side, 0.085, 0.84, (x, 0, 0.47), pants, root)
        box(name + "_shoe" + side, (0.16, 0.30, 0.09), (x, -0.05, 0.045), "#0c0c0c", root, rough=0.35)
    box(name + "_hips", (0.40, 0.23, 0.18), (0, 0, 0.93), pants, root)
    box(name + "_torso", (0.43, 0.24, 0.50), (0, 0, 1.25), shirt, root)
    ball(name + "_shoulders", 0.14, (0, 0, 1.44), shirt, root, (1.75, 0.85, 0.55))
    cyl(name + "_neck", 0.05, 0.10, (0, 0, 1.52), skin, root)
    ball(name + "_head", 0.115, (0, 0, 1.64), skin, root, (0.9, 1.0, 1.12))
    ball(name + "_hair", 0.118, (0, 0.028, 1.685), hair, root, (0.92, 1.0, 0.95))
    box(name + "_nose", (0.03, 0.04, 0.04), (0, -0.115, 1.63), skin, root)
    if beard:
        ball(name + "_beard", 0.10, (0, -0.035, 1.565), beard, root, (0.92, 0.95, 0.85))
    arms = []
    for side, x in (("L", -0.27), ("R", 0.27)):
        arm = cyl(name + "_arm" + side, 0.05, 0.58, (x, 0, 1.44), shirt, root, pivot_top=True)
        ball(name + "_hand" + side, 0.055, (0, 0, -0.62), skin, arm)
        arms.append(arm)
    return root, arms[0], arms[1]


def car(name, loc, rot_z, paint, hero=False):
    root = empty(name, loc)
    root.rotation_euler = (0, 0, radians(rot_z))
    box(name + "_body", (1.80, 4.36, 0.60), (0, 0, 0.62), paint, root, rough=0.25, metal=0.6)
    box(name + "_cabin", (1.56, 2.20, 0.50), (0, 0.42, 1.17), "#1b2028", root, rough=0.1, metal=0.4)
    box(name + "_screen", (1.52, 0.75, 0.05), (0, -0.92, 1.14), "#1b2028", root, rot=(-38, 0, 0), rough=0.1, metal=0.4)
    box(name + "_rear", (1.52, 0.60, 0.05), (0, 1.68, 1.16), "#1b2028", root, rot=(42, 0, 0), rough=0.1, metal=0.4)
    box(name + "_roof", (1.50, 1.75, 0.06), (0, 0.42, 1.44), paint, root, rough=0.25, metal=0.6)
    for x in (-0.62, 0.62):
        box(name + "_light%+d" % x, (0.42, 0.06, 0.11), (x, -2.18, 0.78), "#fff6cf", root, rough=0.2)
        box(name + "_tail%+d" % x, (0.42, 0.06, 0.11), (x, 2.18, 0.82), "#b01818", root, rough=0.2)
    box(name + "_grille", (1.0, 0.05, 0.22), (0, -2.19, 0.52), "#101216", root)
    for i, (x, y) in enumerate([(-0.9, -1.42), (0.9, -1.42), (-0.9, 1.40), (0.9, 1.40)]):
        cyl(name + "_wheel%d" % i, 0.34, 0.24, (x, y, 0.34), "#121316", root, rot=(0, 90, 0), rough=0.8)
        cyl(name + "_rim%d" % i, 0.20, 0.26, (x, y, 0.34), "#c8ccd2", root, rot=(0, 90, 0), rough=0.3, metal=0.8)
    if hero:
        box(name + "_plinth", (2.6, 5.2, 0.04), (0, 0, 0.02), "#0F2747", root, rough=0.5)
    return root


def key(obj, frame, loc=None, rot=None):
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert("location", frame=frame)
    if rot is not None:
        obj.rotation_euler = [radians(a) for a in rot]
        obj.keyframe_insert("rotation_euler", frame=frame)


# ---------- set: forecourt, showroom, stock, dressing ----------
box("ground", (60, 60, 0.1), (0, 8, -0.05), "#5d6066", rough=0.9)
box("forecourt", (11, 9, 0.02), (0, 3.2, 0.01), "#75787e", rough=0.85)
for x in (-4.4, -1.6, 1.2, 4.0):  # bay lines
    box("bay%+.1f" % x, (0.10, 4.6, 0.01), (x, 6.2, 0.03), "#eceff2")
# Showroom: glass front, dark frame, fascia sign with orange stripe, canopy.
box("showroom", (17, 6, 4.6), (0, 13.0, 2.3), "#f1ede6")
box("glass", (13.6, 0.08, 2.5), (0, 9.96, 1.35), "#8fb9d0", rough=0.08, metal=0.5)
for x in (-6.8, -4.1, -1.4, 1.4, 4.1, 6.8):
    box("mullion%+.1f" % x, (0.10, 0.14, 2.6), (x, 9.93, 1.35), "#1c1f25")
box("canopy", (15.0, 1.8, 0.16), (0, 9.2, 2.78), "#1c1f25")
box("fascia", (15.0, 0.20, 1.20), (0, 9.86, 3.55), "#0F2747")
box("fascia_stripe", (15.0, 0.22, 0.10), (0, 9.85, 2.94), "#FF5F15")
text("fascia_text", "MONSOOR MOTORS", 0.62, (0, 9.72, 3.33), "#ffffff")
# Stock: hero C-HR on a navy plinth behind the two men, more cars in the bays.
car("CHR", (0.35, 3.5, 0), -62, "#b9bec6", hero=True)
car("stock1", (-3.0, 6.3, 0), 0, "#8a1f24")
car("stock2", (-5.6, 6.3, 0), 0, "#e9ebee")
car("stock3", (2.6, 6.6, 0), 0, "#23406b")
car("stock4", (5.4, 6.6, 0), 0, "#2a2c30")
# Dressing: feather banners, light poles, planters, bollards.
for x, col in ((-3.4, "#0F2747"), (3.6, "#FF5F15")):
    cyl("pole%+.1f" % x, 0.025, 3.4, (x, 2.2, 1.7), "#d7dade", metal=0.7, rough=0.3)
    box("banner%+.1f" % x, (0.55, 0.03, 2.3), (x + 0.3, 2.2, 2.1), col)
for x in (-6.2, 6.4):
    cyl("lamp%+.1f" % x, 0.06, 5.4, (x, 4.2, 2.7), "#2b2e33", metal=0.6)
    box("lamphead%+.1f" % x, (0.9, 0.35, 0.10), (x * 0.94, 4.2, 5.4), "#2b2e33")
for x in (-2.3, 2.5):
    box("planter%+.1f" % x, (0.55, 0.55, 0.50), (x, 1.2, 0.25), "#2b2e33")
    ball("shrub%+.1f" % x, 0.36, (x, 1.2, 0.72), "#2f6b3a", rough=0.9)
for x in (-1.3, -0.65, 0.0, 0.65, 1.3):
    cyl("bollard%+.2f" % x, 0.05, 0.5, (x + 0.35, 1.75, 0.25), "#d7dade", metal=0.7, rough=0.3)

# ---------- people ----------
monsoor, m_arm_l, m_arm_r = person("Monsoor", "#0F2747", "#3b3f46", "#b98a66", "#1a1a1a")
arfan, a_arm_l, a_arm_r = person("Arfan", "#101012", "#3f2a1e", "#b98a66", "#0d0d0d", beard="#0d0d0d")

# Both stay on their marks for the whole video. Only the camera travels.
key(monsoor, 1, (-0.40, 0.0, 0), (0, 0, 20))
key(monsoor, 150, (-0.40, 0.0, 0), (0, 0, 20))
key(monsoor, 200, (-0.40, 0.0, 0), (0, 0, 34))   # turns to watch Arfan
key(monsoor, END, (-0.40, 0.0, 0), (0, 0, 34))
key(arfan, 1, (0.40, 0.10, 0), (0, 0, -14))
key(arfan, 190, (0.40, 0.10, 0), (0, 0, -14))
key(arfan, 240, (0.40, 0.10, 0), (0, 0, 0))      # squares up to the lens
key(arfan, 330, (0.40, 0.10, 0), (0, 0, 0))
key(arfan, 410, (0.40, 0.10, 0), (0, 0, 21))     # follows the camera to his side
key(arfan, END, (0.40, 0.10, 0), (0, 0, 21))

# Monsoor: hand on heart on "trust", then presents Arfan (arm nearest him).
for f, ax, ay in [(1, 0, 0), (30, 0, 0), (55, -55, 20), (95, -55, 20), (120, 0, 0)]:
    key(m_arm_l, f, rot=(ax, ay, 0))
for f, ay in [(1, 0), (128, 0), (155, -64), (200, -64), (225, 0)]:
    key(m_arm_r, f, rot=(0, ay, 0))

# Arfan's gestures (frame numbers match the script beats in previs_post.py).
A_L = [(1, 0, 0), (300, 0, 0), (325, -35, 0), (352, -35, 0), (375, 0, 0),      # "here is my promise"
       (560, 0, 0), (580, -30, 12), (636, -30, 12), (655, 0, 0),               # "no surprises, no pressure"
       (700, 0, 0), (716, -42, 28), (750, -42, 28), (END, -20, 12)]            # "we bring it to your home": arms open
A_R = [(1, 0, 0), (300, 0, 0), (325, -35, 0), (352, -35, 0), (375, 0, 0),
       (420, 0, 0), (448, 0, -70), (505, 0, -70), (530, 0, 0),                 # sweeps to the cars behind
       (560, 0, 0), (580, -30, -12), (636, -30, -12), (655, 0, 0),
       (662, -84, 0), (694, -84, 0),                                           # "YOU choose the car": points at the lens
       (716, -42, -28), (750, -42, -28), (END, -20, -12)]
for f, ax, ay in A_L:
    key(a_arm_l, f, rot=(ax, ay, 0))
for f, ax, ay in A_R:
    key(a_arm_r, f, rot=(ax, ay, 0))


# ---------- cameras ----------
def camera(name, lens):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_start, cam.clip_end = 0.1, 300
    obj = bpy.data.objects.new(name, cam)
    scene.collection.objects.link(obj)
    tgt = empty(name + "_target")
    con = obj.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    return obj, tgt


# Shot 1: 35 mm, eye level, wide two-shot with the sign above, slow push-in.
cam_a, tgt_a = camera("Cam_Shot1", 35)
key(cam_a, 1, (-0.10, -3.75, 1.50))
key(cam_a, S1_END, (-0.04, -3.15, 1.50))
key(tgt_a, 1, (0.0, 0.0, 1.30))
key(tgt_a, S1_END, (0.04, 0.0, 1.32))

# Shot 2: 50 mm. Starts as a tighter two-shot, trucks right to Arfan's side,
# then pushes in and drops slightly below eye level for the last line.
cam_b, tgt_b = camera("Cam_Shot2", 50)
key(cam_b, S2_START, (0.20, -4.10, 1.50))
key(cam_b, 300, (0.55, -3.90, 1.50))
key(cam_b, 410, (1.55, -3.00, 1.48))
key(cam_b, 640, (1.42, -2.65, 1.44))
key(cam_b, 716, (1.10, -1.75, 1.34))
key(cam_b, END, (1.08, -1.65, 1.34))
key(tgt_b, S2_START, (0.12, 0.05, 1.34))
key(tgt_b, 300, (0.22, 0.08, 1.36))
key(tgt_b, 410, (0.38, 0.10, 1.40))
key(tgt_b, 640, (0.40, 0.10, 1.42))
key(tgt_b, 716, (0.40, 0.10, 1.48))
key(tgt_b, END, (0.40, 0.10, 1.48))

scene.timeline_markers.new("SHOT_1", frame=1).camera = cam_a
scene.timeline_markers.new("SHOT_2", frame=S2_START).camera = cam_b
scene.camera = cam_a

if SAVE_BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_BLEND)
if TEST_FRAMES:
    for f in TEST_FRAMES:
        scene.frame_set(f)
        scene.render.filepath = FRAMES_DIR.rstrip("/") + "/f_%04d.png" % f
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
