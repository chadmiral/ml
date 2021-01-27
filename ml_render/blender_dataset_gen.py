import bpy
import random
import os
import math

data_count = 10
renderSize = 256
rotRange = (-360.0, 360.0)

scene = bpy.context.scene
params = []

def reset_params():
    print("reset params")
    params = []
    

def reset_scene():
    print("reset scene")
    for o in scene.objects:
        o.select_set(state=True)
    bpy.ops.object.delete()

def add_camera():
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_obj = bpy.data.objects.new('Camera', camera_data)
    
    camera_obj.location = (0.0, 0.0, 5.0)
    #camera_obj.rotation = (0.0, 0.0, 0.0)
    
    bpy.context.collection.objects.link(camera_obj)
    bpy.context.scene.camera = camera_obj
    
def add_background():
    box_width = 1.5
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( 0.0,  0.0, -box_width), rotation=(0.0, 0.0, 0.0))
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( box_width,  0.0,  0.0), rotation=(0.0,  math.pi / 2.0, 0.0))
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=(-box_width,  0.0,  0.0), rotation=(0.0, -math.pi / 2.0, 0.0))
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( 0.0, -box_width,  0.0), rotation=( math.pi / 2.0, 0.0, 0.0))
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( 0.0,  box_width,  0.0), rotation=(-math.pi / 2.0, 0.0, 0.0))

def add_random_renderable():
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    rot = (random.uniform(rotRange[0], rotRange[1]), random.uniform(rotRange[0], rotRange[1]), random.uniform(rotRange[0], rotRange[1]))
    scale = random.uniform(0.0, 1.0)
    diffuse_rgb = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
    metallic = random.uniform(0.0, 1.0)
    
    sphere = bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=scale, enter_editmode=False, location=pos, rotation=rot)
    
    #create and add material
    sphereMat = bpy.data.materials.new(name="sphereMat")
    sphereMat.use_nodes=True
    bsdf = sphereMat.node_tree.nodes.get("Principled BSDF")
    
    #set some random PBR parameters
    bsdf.inputs[0].default_value[0] = diffuse_rgb[0]
    bsdf.inputs[0].default_value[1] = diffuse_rgb[1]
    bsdf.inputs[0].default_value[2] = diffuse_rgb[2]
    
    bsdf.inputs[4].default_value = metallic
    
    bpy.context.selected_objects[0].data.materials.append(sphereMat)
    

    params.append(pos)
    params.append(rot)
    params.append(scale)
    params.append(diffuse_rgb)
    params.append(metallic)
    
def add_random_light():
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    light_data = bpy.data.lights.new(name="light", type='POINT')
    light_data.energy = random.uniform(0.0, 100)
    rgb = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
    
    light_data.color.r = rgb[0]
    light_data.color.g = rgb[1]
    light_data.color.b = rgb[2]
    
    light_obj = bpy.data.objects.new(name="light", object_data = light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = pos
    
    params.append(pos)
    params.append(rgb)
    params.append(light_data.energy)
    

def render_scene(idx):
    render = bpy.context.scene.render
    
    render.engine = 'CYCLES'
    render.resolution_x = renderSize
    render.resolution_y = renderSize
    render.resolution_percentage = 100
    
    render.use_file_extension=True
    render.image_settings.color_mode='RGBA'
    render.image_settings.file_format='PNG'
    render.image_settings.compression=90
    render.filepath = os.path.join("/home/chandra/ml/ml_render/data/", ('render%05d.png' % i))
    
    bpy.ops.render.render(animation=False, write_still=True)
    
    scene.cycles.progressive='PATH'
    scene.cycles.samples = 64
    scene.cycles.max_bounces=16
    scene.cycles.use_denoising=True
    

for i in range(data_count):
    reset_params()
    reset_scene()

    add_camera()
    add_background()
    add_random_renderable()
    add_random_light()

    render_scene(i)

    print(params)
