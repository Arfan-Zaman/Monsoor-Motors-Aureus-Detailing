"""3D blocking (previs) for the Monsoor Motors CEO intro video: two shots.

Run:  blender -b -P previs_scene.py -- <frames_dir> [save.blend]
Renders 540x960 PNG frames (24 fps) with the fast Workbench engine.
Shot 1 = frames 1-264 (11 s), Shot 2 = frames 265-648 (16 s).
All sizes are in metres. People face -Y (toward the camera) by default.
"""
import sys
from math import radians

import bpy
from mathutils import Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FRAMES_DIR = argv[0] if argv else "/tmp/previs_frames"
SAVE_BLEND = argv[1] if len(argv) > 1 else None

S1_END, S2_START, END = 264, 265, 648

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, END
scene.render.resolution_x, scene.render.resolution_y = 540, 960
scene.render.resolution_percentage = 100
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = FRAMES_DIR.rstrip("/") + "/f_"
sh = scene.display.shading
sh.light = "STUDIO"
sh.color_type = "OBJECT"
sh.show_shadows = True
sh.shadow_intensity = 0.35
sh.show_cavity = True
world = bpy.data.worlds.new("World")
world.color = (0.62, 0.72, 0.82)
scene.world = world


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1.0,)


def link(obj, parent=None, loc=(0, 0, 0), color=None):
    scene.collection.objects.link(obj)
    obj.location = loc
    if parent:
        obj.parent = parent
    if color:
        obj.color = rgb(color)
    return obj


def empty(name, loc=(0, 0, 0), parent=None):
    return link(bpy.data.objects.new(name, None), parent, loc)


def box(name, size, loc, color, parent=None, pivot_top=False):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    if pivot_top:  # origin at the top face, so it swings like an arm
        obj.data.transform(Matrix.Translation((0, 0, -0.5)))
    obj.scale = size
    obj.location = loc
    obj.color = rgb(color)
    if parent:
        obj.parent = parent
    return obj


def ball(name, radius, loc, color, parent=None, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=24, ring_count=12)
    obj = bpy.context.active_object
    obj.name = name
    obj.location = loc
    obj.scale = scale
    obj.color = rgb(color)
    bpy.ops.object.shade_smooth()
    if parent:
        obj.parent = parent
    return obj


def wheel(name, loc, parent):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.34, depth=0.24, vertices=24)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = (0, radians(90), 0)
    obj.location = loc
    obj.color = rgb("#15171a")
    obj.parent = parent
    return obj


def text(name, body, size, loc, color, parent=None):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = "CENTER"
    obj = bpy.data.objects.new(name, cu)
    link(obj, parent, loc, color)
    obj.rotation_euler = (radians(90), 0, 0)  # stand up, readable from -Y
    return obj


def person(name, label, shirt, pants, skin, hair, beard=None):
    root = empty(name)
    box(name + "_legL", (0.16, 0.18, 0.86), (-0.10, 0, 0.43), pants, root)
    box(name + "_legR", (0.16, 0.18, 0.86), (0.10, 0, 0.43), pants, root)
    box(name + "_shoeL", (0.17, 0.30, 0.09), (-0.10, -0.05, 0.045), "#101010", root)
    box(name + "_shoeR", (0.17, 0.30, 0.09), (0.10, -0.05, 0.045), "#101010", root)
    box(name + "_torso", (0.44, 0.24, 0.60), (0, 0, 1.16), shirt, root)
    box(name + "_neck", (0.11, 0.11, 0.08), (0, 0, 1.49), skin, root)
    head = ball(name + "_head", 0.115, (0, 0, 1.63), skin, root, (0.9, 1.0, 1.12))
    ball(name + "_hair", 0.118, (0, 0.025, 1.675), hair, root, (0.92, 1.0, 0.95))
    box(name + "_nose", (0.03, 0.04, 0.04), (0, -0.115, 1.62), skin, root)
    if beard:
        ball(name + "_beard", 0.10, (0, -0.035, 1.555), beard, root, (0.92, 0.95, 0.85))
    arm_l = box(name + "_armL", (0.10, 0.11, 0.62), (-0.28, 0, 1.44), shirt, root, pivot_top=True)
    arm_r = box(name + "_armR", (0.10, 0.11, 0.62), (0.28, 0, 1.44), shirt, root, pivot_top=True)
    return root, arm_l, arm_r, head


def key(obj, frame, loc=None, rot=None):
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert("location", frame=frame)
    if rot is not None:
        obj.rotation_euler = [radians(a) for a in rot]
        obj.keyframe_insert("rotation_euler", frame=frame)


# ---------- set: yard, wall, sign, C-HR stand-in ----------
box("ground", (40, 40, 0.1), (0, 6, -0.05), "#8d9096")
box("wall", (16, 0.3, 4.2), (0, 9.0, 2.1), "#f1ede6")
box("sign", (5.4, 0.12, 0.95), (0, 8.78, 3.25), "#0F2747")
text("sign_text", "MONSOOR MOTORS", 0.46, (0, 8.70, 3.08), "#ffffff")
box("sign_bar", (5.4, 0.13, 0.08), (0, 8.77, 2.72), "#FF5F15")

car = empty("CHR", (0.35, 3.5, 0))
car.rotation_euler = (0, 0, radians(-62))  # mostly side-on so it spans the frame behind them
box("chr_body", (1.80, 4.36, 0.62), (0, 0, 0.62), "#b9bec6", car)
box("chr_cabin", (1.58, 2.35, 0.52), (0, 0.35, 1.19), "#2a2f38", car)
box("chr_roof", (1.50, 1.90, 0.06), (0, 0.45, 1.47), "#b9bec6", car)
box("chr_bonnet", (1.70, 1.10, 0.10), (0, -1.55, 0.96), "#b9bec6", car)
box("chr_lightL", (0.42, 0.06, 0.12), (-0.62, -2.18, 0.78), "#fff4c2", car)
box("chr_lightR", (0.42, 0.06, 0.12), (0.62, -2.18, 0.78), "#fff4c2", car)
box("chr_plate", (0.46, 0.04, 0.12), (0, -2.19, 0.46), "#f5f5f5", car)
for i, (x, y) in enumerate([(-0.9, -1.42), (0.9, -1.42), (-0.9, 1.40), (0.9, 1.40)]):
    wheel("chr_wheel%d" % i, (x, y, 0.34), car)

# ---------- people ----------
monsoor, m_arm_l, m_arm_r, _ = person(
    "Monsoor", "MONSOOR  founder", "#0F2747", "#3b3f46", "#b98a66", "#1a1a1a")
arfan, a_arm_l, a_arm_r, _ = person(
    "Arfan", "ARFAN  CEO", "#101012", "#3f2a1e", "#b98a66", "#0d0d0d", beard="#0d0d0d")

# Shot 1: side by side, turned a little toward each other.
key(monsoor, 1, (-0.38, 0.0, 0), (0, 0, 22))
key(monsoor, 250, (-0.38, 0.0, 0), (0, 0, 22))
key(arfan, 1, (0.38, 0.12, 0), (0, 0, -14))
key(arfan, 205, (0.38, 0.12, 0), (0, 0, -14))
# Monsoor presents Arfan with the arm nearest him (frames 110-215).
for f, a in [(1, 0), (110, 0), (140, -62), (190, -62), (215, 0)]:
    key(m_arm_r, f, rot=(0, a, 0))
# Arfan turns to the lens and starts his first step just before the cut.
key(arfan, 250, (0.38, 0.12, 0), (0, 0, 0))
# Shot 2: Arfan walks forward and takes the frame; Monsoor eases back and watches.
for f, y, z in [(262, -0.10, 0.02), (276, -0.45, 0.0), (290, -0.80, 0.02), (304, -1.10, 0.0)]:
    key(arfan, f, (0.34 - (f - 250) * 0.0022, y, z))
key(arfan, 318, (0.18, -1.30, 0), (0, 0, 0))
key(arfan, END, (0.18, -1.30, 0), (0, 0, 0))
key(monsoor, 330, (-0.62, 0.55, 0), (0, 0, 12))
key(monsoor, END, (-0.62, 0.55, 0), (0, 0, 12))
# Arfan: open-hands gesture on the promise (frames 400-480).
for f, a in [(1, 0), (385, 0), (410, -38), (470, -38), (495, 0)]:
    key(a_arm_l, f, rot=(a, 0, 0))
for f, a, side in [(1, 0, 0), (385, 0, 0), (410, -38, 0), (470, -38, 0), (495, 0, 0),
                   (545, 0, 0), (570, 0, -68), (615, 0, -68), (640, 0, 0)]:
    key(a_arm_r, f, rot=(a, side, 0))  # last move: points back to the C-HR

# ---------- cameras ----------
def camera(name, lens):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_start, cam.clip_end = 0.1, 200
    obj = link(bpy.data.objects.new(name, cam))
    tgt = empty(name + "_target")
    con = obj.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    return obj, tgt

# Shot 1: 35 mm, eye level, wide two-shot, slow push-in.
cam_a, tgt_a = camera("Cam_Shot1", 35)
key(cam_a, 1, (0.0, -4.20, 1.50))
key(cam_a, S1_END, (0.0, -3.50, 1.50))
key(tgt_a, 1, (0.0, 0.0, 1.35))
key(tgt_a, S1_END, (0.03, 0.0, 1.35))

# Shot 2: 50 mm, starts off to Arfan's side, small arc and push-in to a medium shot.
cam_b, tgt_b = camera("Cam_Shot2", 50)
key(cam_b, S2_START, (1.05, -5.10, 1.52))
key(cam_b, 330, (0.70, -4.75, 1.52))
key(cam_b, 520, (0.22, -4.25, 1.50))
key(cam_b, END, (0.05, -4.10, 1.50))
key(tgt_b, S2_START, (0.20, -0.10, 1.25))
key(tgt_b, 318, (0.02, -1.30, 1.28))
key(tgt_b, END, (0.0, -1.30, 1.30))

m1 = scene.timeline_markers.new("SHOT_1", frame=1)
m1.camera = cam_a
m2 = scene.timeline_markers.new("SHOT_2", frame=S2_START)
m2.camera = cam_b
scene.camera = cam_a

if SAVE_BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_BLEND)
bpy.ops.render.render(animation=True)
