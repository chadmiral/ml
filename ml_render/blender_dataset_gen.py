import bpy
import random
import os
import math
import numpy as np
import csv

data_count = 12800
renderSize = 128
rotRange = (0.0, 360.0)
max_light_energy = 100.0

scene = bpy.context.scene
fields = []
params = []

def reset_params():
    print("reset params")
    params.clear()
    fields.clear()
    

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
    
def gen_pbr_material(name="none"):
    diffuse_rgb = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
    metalness=random.uniform(0.0, 1.0)
    roughness=random.uniform(0.0, 1.0)

    mat = bpy.data.materials.new(name="randMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")

    #set some random PBR params
    for i in range(3):
        bsdf.inputs[0].default_value[i] = diffuse_rgb[i]

    bsdf.inputs[4].default_value = metalness
    bsdf.inputs[7].default_value = roughness

    params.append(list(diffuse_rgb))
    params.append(metalness)
    params.append(roughness)

    fields.append(name + "_diffuse_r")
    fields.append(name + "_diffuse_g")
    fields.append(name + "_diffuse_b")
    fields.append(name + "_metalness")
    fields.append(name + "_roughness")

    return mat

def add_background():
    box_width = 1.5
    
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( 0.0,  0.0, -box_width), rotation=(0.0, 0.0, 0.0))
    m = gen_pbr_material("back_plane")
    bpy.context.selected_objects[0].data.materials.append(m)

    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( box_width,  0.0,  0.0), rotation=(0.0,  math.pi / 2.0, 0.0))
    m = gen_pbr_material("right_plane")
    bpy.context.selected_objects[0].data.materials.append(m)
    
    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=(-box_width,  0.0,  0.0), rotation=(0.0, -math.pi / 2.0, 0.0))
    m = gen_pbr_material("left_plane")
    bpy.context.selected_objects[0].data.materials.append(m)

    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( 0.0, -box_width,  0.0), rotation=( math.pi / 2.0, 0.0, 0.0))
    m = gen_pbr_material("bottom_plane")
    bpy.context.selected_objects[0].data.materials.append(m)

    bpy.ops.mesh.primitive_plane_add(size=10.0, enter_editmode=False, location=( 0.0,  box_width,  0.0), rotation=(-math.pi / 2.0, 0.0, 0.0))
    m = gen_pbr_material("top_plane")
    bpy.context.selected_objects[0].data.materials.append(m)


def add_random_renderable():
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    rot = (random.uniform(rotRange[0], rotRange[1]), random.uniform(rotRange[0], rotRange[1]), random.uniform(rotRange[0], rotRange[1]))
    scale = random.uniform(0.0, 1.0)
    
    sphere = bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=scale, enter_editmode=False, location=pos, rotation=rot)
    
    #create and add material
    sphereMat = gen_pbr_material("sphere")
    
    bpy.context.selected_objects[0].data.materials.append(sphereMat)

    remap_pos = 0.5 * (np.array(pos) + np.array([1.0, 1.0, 1.0]))
    remap_rot = np.array(rot) / 360.0

    params.append(list(remap_pos))
    params.append(list(remap_rot))
    params.append(scale)

    fields.append("sphere_pos_x")
    fields.append("sphere_pos_y")
    fields.append("sphere_pos_z")
    fields.append("sphere_rot_x")
    fields.append("sphere_rot_y")
    fields.append("sphere_rot_z")
    fields.append("sphere_scale")
    
def add_random_light():
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    light_data = bpy.data.lights.new(name="light", type='POINT')
    light_data.energy = random.uniform(0.0, max_light_energy)
    rgb = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
    
    light_data.color.r = rgb[0]
    light_data.color.g = rgb[1]
    light_data.color.b = rgb[2]
    
    light_obj = bpy.data.objects.new(name="light", object_data = light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = pos

    remap_pos = 0.5 * (np.array(pos) + np.array([1.0, 1.0, 1.0]))
    remap_energy = light_data.energy / max_light_energy
    
    params.append(list(remap_pos))
    params.append(list(rgb))
    params.append(remap_energy)

    fields.append("light_pos_x")
    fields.append("light_pos_y")
    fields.append("light_pos_z")
    fields.append("light_r")
    fields.append("light_g")
    fields.append("light_b")
    fields.append("light_energy")
    

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
    render.filepath = os.path.join("/home/chandra/ml/ml_render/data/judkins_box", ('render%05d.png' % i))
    
    bpy.ops.render.render(animation=False, write_still=True)
    
    scene.cycles.progressive='PATH'
    scene.cycles.samples = 64
    scene.cycles.max_bounces=16
    scene.cycles.use_denoising=True

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list
    

out_params = []
for i in range(data_count):
    reset_params()
    reset_scene()

    add_camera()
    add_background()
    add_random_renderable()
    add_random_light()

    render_scene(i)

    out_params.append(flatten_list(params))

print('param vector size: %d' % len(fields))

with open('data/labels.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(out_params)
