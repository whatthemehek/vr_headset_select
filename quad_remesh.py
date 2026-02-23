import bpy
import sys
import os

# ---- Get arguments after "--" ----
argv = sys.argv
argv = argv[argv.index("--") + 1:]

input_path = os.path.abspath(argv[0])
output_path = os.path.abspath(argv[1])

# Reset Blender scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import OBJ (Blender 4.x uses wm.obj_import)
bpy.ops.wm.obj_import(filepath=input_path)

obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj

bpy.ops.object.mode_set(mode='OBJECT')

# QuadriFlow Remesh
bpy.ops.object.quadriflow_remesh(
    target_faces=1000,      
)

# Export remeshed OBJ (Blender 4.x uses wm.obj_export)
bpy.ops.wm.obj_export(filepath=output_path)

print("Quad remesh complete.")