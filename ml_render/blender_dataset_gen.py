import bpy
import random
import os

scene = bpy.context.scene

data_count = 500
renderSize = 128
rotRange = (-360.0, 360.0)

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

def add_random_renderable():
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    rot = (random.uniform(rotRange[0], rotRange[1]), random.uniform(rotRange[0], rotRange[1]), random.uniform(rotRange[0], rotRange[1]))
    scale = random.uniform(0.1, 2.0)
    
    bpy.ops.mesh.primitive_cube_add(size=scale, enter_editmode=False, location=pos, rotation=rot)

    params.append(pos)
    params.append(rot)
    params.append(scale)
    
def add_random_light():
    pos = (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(0.5, 1.0))
    light_data = bpy.data.lights.new(name="light", type='POINT')
    light_data.energy = random.uniform(0.0, 1000)
    
    light_obj = bpy.data.objects.new(name="light", object_data = light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = pos
    
    params.append(pos)
    params.append(light_data.energy)
    

def render_scene(idx):
    #dg = bpy.context.evaluated_depsgraph_get()
    #dg.update()
    render = bpy.context.scene.render
    
    render.engine = 'CYCLES'
    render.resolution_x = renderSize
    render.resolution_y = renderSize
    render.resolution_percentage = 100
    
    render.use_file_extension=True
    render.image_settings.color_mode='RGBA'
    render.image_settings.file_format='PNG'
    render.image_settings.compression=90
    render.filepath = os.path.join("/home/chandra/ml/ml_render/data/", ('render%d.png' % i))
    
    bpy.ops.render.render(animation=False, write_still=True)
    

for i in range(data_count):
    reset_params()
    reset_scene()

    add_camera()
    add_random_renderable()
    add_random_light()

    render_scene(i)

    print(params)