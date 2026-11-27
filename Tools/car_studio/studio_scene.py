"""Monsoor Motors virtual studio, built in Blender (our own asset, no AI).

Run:
  blender -b -P studio_scene.py -- --out <plates dir> [--orbit 36] [--size 2048] [--samples 96] [--only front34]

Makes empty studio "plates" (backgrounds) for each camera preset, plus
plates.json with where the turntable centre sits in each image and how many
pixels one metre is there, so car_studio.py can place real car cut-outs at
the right size and spot.

Camera rig matches the shooting guide: phone ~1.0 m high, ~7 m from the car
centre, 2x lens (about 45 mm full-frame equivalent).
"""
import bpy, math, json, os, sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

OUT = arg("--out", "plates")
ORBIT = int(arg("--orbit", "0"))
SIZE = int(arg("--size", "2048"))
SAMPLES = int(arg("--samples", "96"))
ONLY = arg("--only", "")
STYLE = arg("--style", "grey")  # grey (default, clean cove) or showroom (navy + LED)
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = arg("--logo", os.path.join(HERE, "assets", "Monsoor-Logo-Horizontal-White.png"))

NAVY = (15/255, 39/255, 71/255)
ORANGE = (1.0, 95/255, 21/255)

CAM_H, CAM_D, LENS, TARGET_Z = 1.0, 7.0, 45, 0.72
# angle = where the camera stands, measured from the car's front (0 = straight on)
# (angle, lens mm): straight front/rear use a longer lens so the car fills the frame
PRESETS = {"front": (0, 62), "front34": (38, 45), "side": (90, 45), "rear34": (142, 45), "rear": (180, 62)}


def lin(c):  # sRGB -> linear for material colours
    return tuple(((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c)


def mat(name, color, rough=0.5, emit=None, strength=0.0, metallic=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(color), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.05
    if emit:
        b.inputs["Emission Color"].default_value = (*lin(emit), 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


def link(obj, m):
    obj.data.materials.append(m)
    return obj


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene

    def showroom():
        # --- floor: dark glossy epoxy, like a showroom floor
        bpy.ops.mesh.primitive_circle_add(vertices=128, radius=16, fill_type="NGON")
        link(bpy.context.object, mat("Floor", (0.025, 0.035, 0.06), rough=0.28, coat=0.35))

        # --- turntable: slightly raised disc, satin grey-navy, orange LED ring at the edge
        bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=3.4, depth=0.05, location=(0, 0, 0.025))
        link(bpy.context.object, mat("Turntable", (0.10, 0.13, 0.18), rough=0.3, coat=0.4))
        bpy.ops.mesh.primitive_torus_add(major_radius=3.42, minor_radius=0.012, major_segments=256,
                                         location=(0, 0, 0.05))
        link(bpy.context.object, mat("Ring", ORANGE, emit=ORANGE, strength=18))

        # --- round cyclorama wall (no corners, so every spin angle looks the same)
        bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=11, depth=7, location=(0, 0, 3.5),
                                            end_fill_type="NOTHING")
        wall = bpy.context.object
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.flip_normals(); bpy.ops.object.mode_set(mode="OBJECT")
        link(wall, mat("Wall", NAVY, rough=0.75))
        # ceiling (dark)
        bpy.ops.mesh.primitive_circle_add(vertices=128, radius=11.2, fill_type="NGON", location=(0, 0, 7))
        link(bpy.context.object, mat("Ceiling", (0.02, 0.03, 0.05), rough=0.9))

        # --- vertical LED slats on the wall: pairs of orange strips every 45 deg,
        #     warm-white strips between them
        for i in range(16):
            a = math.radians(i * 22.5)
            orange = i % 2 == 0
            for off in ((-0.05, 0.05) if orange else (0,)):
                aa = a + off
                r = 10.9
                bpy.ops.mesh.primitive_cube_add(size=1, location=(r * math.cos(aa), r * math.sin(aa), 2.6))
                s = bpy.context.object
                s.scale = (0.06, 0.06, 4.2) if orange else (0.03, 0.03, 4.2)
                s.rotation_euler = (0, 0, aa)
                col = ORANGE if orange else (1.0, 0.93, 0.85)
                link(s, mat(f"Slat{i}{off}", col, emit=col, strength=14 if orange else 6))
        # skirting glow line where wall meets floor
        bpy.ops.mesh.primitive_torus_add(major_radius=10.85, minor_radius=0.02, major_segments=256,
                                         location=(0, 0, 0.06))
        link(bpy.context.object, mat("Skirt", ORANGE, emit=ORANGE, strength=6))

        # --- Monsoor logo on the wall, twice (front and back of the spin)
        if os.path.exists(LOGO):
            img = bpy.data.images.load(LOGO)
            aspect = img.size[0] / img.size[1]
            # one logo on the wall behind the car in the hero (front34) view, one opposite
            for k, cam_ang in enumerate((31, 211)):
                a = math.radians(cam_ang)
                w, R = 3.0, 10.8
                loc = Vector((-math.sin(a) * R, math.cos(a) * R, 4.0))
                bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
                p = bpy.context.object
                p.scale = (w, w / aspect, 1)
                p.rotation_euler = (-loc * Vector((1, 1, 0))).to_track_quat("Z", "Y").to_euler()
                m = bpy.data.materials.new(f"Logo{k}"); m.use_nodes = True
                nt = m.node_tree; nt.nodes.clear()
                tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img
                em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 2.2
                tr = nt.nodes.new("ShaderNodeBsdfTransparent")
                mix = nt.nodes.new("ShaderNodeMixShader")
                out = nt.nodes.new("ShaderNodeOutputMaterial")
                nt.links.new(tex.outputs["Color"], em.inputs["Color"])
                nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
                nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
                nt.links.new(mix.outputs[0], out.inputs[0])
                p.data.materials.append(m)

        # --- lighting: big soft light box over the turntable + two soft side fills
        def area(name, loc, size, energy, color=(1, 1, 1), rot=(0, 0, 0), shape="RECTANGLE", size_y=None):
            ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.color = color
            ld.shape = shape; ld.size = size
            if size_y: ld.size_y = size_y
            o = bpy.data.objects.new(name, ld); o.location = loc; o.rotation_euler = rot
            o.visible_glossy = False  # no hot spots reflected in the glossy floor
            sc.collection.objects.link(o)
        area("LightBox", (0, 0, 5.6), 7.0, 2600, size_y=3.6)
        # visible light-box panel (shows when the camera sees the ceiling)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 5.65))
        lb = bpy.context.object; lb.scale = (7.0, 3.6, 1)
        link(lb, mat("LightPanel", (1, 1, 1), emit=(1, 0.98, 0.95), strength=6))
        area("FillL", (-6, -4, 2.2), 4, 500, color=(1, 0.95, 0.9), rot=(math.radians(80), 0, math.radians(-55)))
        area("FillR", (6, -4, 2.2), 4, 500, color=(1, 0.95, 0.9), rot=(math.radians(80), 0, math.radians(55)))

    def grey_cove():
        """Seamless light-grey infinity cove (Carma-style): floor curves up into the wall
        with no visible edge, so real photos sit in it without perspective clashes.
        Rotationally symmetric, so it works for every angle of a 360 spin."""
        import bmesh
        flat, bend, wall_h, seg, ring = 7.0, 6.0, 14.0, 24, 256
        prof = [(0.0, 0.0)] + [(flat * i / 6, 0.0) for i in range(1, 7)]
        for i in range(1, seg + 1):
            t = (math.pi / 2) * i / seg
            prof.append((flat + bend * math.sin(t), bend * (1 - math.cos(t))))
        prof.append((flat + bend, wall_h))
        bm = bmesh.new()
        rings = []
        for j in range(ring):
            ang = 2 * math.pi * j / ring
            rings.append([bm.verts.new((r * math.cos(ang), r * math.sin(ang), z)) for r, z in prof])
        for j in range(ring):
            r0, r1 = rings[j], rings[(j + 1) % ring]
            for k in range(len(prof) - 1):
                if k == 0:
                    bm.faces.new((r0[0], r1[1], r0[1])) if r0[0] is not r1[0] else None
                else:
                    bm.faces.new((r0[k], r1[k], r1[k + 1], r0[k + 1]))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new("Cove"); bm.to_mesh(me); bm.free()
        for f in me.polygons: f.use_smooth = True
        ob = bpy.data.objects.new("Cove", me); sc.collection.objects.link(ob)
        # make sure normals face inward (towards the camera)
        bpy.context.view_layer.objects.active = ob; ob.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.normals_make_consistent(inside=True); bpy.ops.object.mode_set(mode="OBJECT")
        # painted-canvas grey: mid grey with a soft mottled texture
        m = bpy.data.materials.new("Backdrop"); m.use_nodes = True
        nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
        bsdf.inputs["Roughness"].default_value = 0.85
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 0.9; noise.inputs["Detail"].default_value = 8
        noise.inputs["Roughness"].default_value = 0.62
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*lin((0.34, 0.34, 0.34)), 1)
        ramp.color_ramp.elements[1].color = (*lin((0.58, 0.58, 0.58)), 1)
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
        ob.data.materials.append(m)
        # soft studio light: big overhead box, a front fill, gentle back light on the cove
        def area(name, loc, size, energy, rot=(0, 0, 0), size_y=None):
            ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.shape = "RECTANGLE"
            ld.size = size; ld.size_y = size_y or size
            o = bpy.data.objects.new(name, ld); o.location = loc; o.rotation_euler = rot
            o.visible_camera = False; o.visible_glossy = False
            sc.collection.objects.link(o)
        area("Top", (0, 0, 7.5), 8, 2600, size_y=5)

    if STYLE == "grey":
        grey_cove()
    else:
        showroom()

    # world: near black
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = \
        (0.32, 0.32, 0.32, 1) if STYLE == "grey" else (0.005, 0.008, 0.015, 1)

    # camera
    cd = bpy.data.cameras.new("Cam"); cd.lens = LENS; cd.sensor_width = 36
    cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam

    # render settings
    sc.render.engine = "CYCLES"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"; prefs.get_devices()
        for d in prefs.devices: d.use = True
        sc.cycles.device = "GPU"
    except Exception as e:
        print("GPU not available, using CPU:", e)
    sc.view_settings.view_transform = "AgX"
    sc.render.image_settings.file_format = "PNG"
    return sc, cam


def place(cam, angle_deg):
    # car front faces -Y; camera angle measured from the front, going round the car's left side
    a = math.radians(angle_deg)
    cam.location = (CAM_D * math.sin(a), -CAM_D * math.cos(a), CAM_H)
    d = Vector((0, 0, TARGET_Z)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def info(sc, cam, w, h):
    bpy.context.view_layer.update()
    def px(p):
        v = world_to_camera_view(sc, cam, Vector(p))
        return (v.x * w, (1 - v.y) * h)
    c = px((0, 0, 0.05))
    right = (cam.matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized()
    a = px(Vector((0, 0, 0.05)) - right * 1.0)
    b = px(Vector((0, 0, 0.05)) + right * 1.0)
    return {"ground_centre": [round(c[0], 1), round(c[1], 1)],
            "px_per_m": round(math.dist(a, b) / 2.0, 2),
            "horizon_y": round(px(cam.location + Vector((-cam.location.x, -cam.location.y, 0)).normalized() * 1000)[1], 1)}


def main():
    sc, cam = build()
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(OUT, "plates.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    jobs = []
    for name, (ang, lens) in PRESETS.items():
        if not ONLY or name in ONLY.split(","):
            jobs.append((f"{name}", ang, lens, SIZE, SIZE))
    for i in range(ORBIT):
        jobs.append((f"orbit_{i:02d}", i * 360 / ORBIT, LENS, 1920, 1280))
    for name, ang, lens, w, h in jobs:
        sc.render.resolution_x, sc.render.resolution_y = w, h
        cam.data.lens = lens
        place(cam, ang)
        meta[name] = {"angle": ang, "size": [w, h], "camera": {"height_m": CAM_H, "distance_m": CAM_D, "lens_mm": lens},
                      **info(sc, cam, w, h)}
        sc.render.filepath = os.path.join(OUT, f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", name)
    json.dump(meta, open(meta_path, "w"), indent=2)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "monsoor_studio.blend"))


main()
