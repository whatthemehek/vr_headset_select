import bpy
import sys
import os

argv = sys.argv
argv = argv[argv.index("--") + 1:]

input_path = os.path.abspath(argv[0])
output_path = os.path.abspath(argv[1])

bpy.ops.wm.read_factory_settings(use_empty=True)

# Import
bpy.ops.wm.obj_import(filepath=input_path)

mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if not mesh_objects:
    raise Exception("No mesh objects found.")

for obj in mesh_objects:
    obj.select_set(True)

bpy.context.view_layer.objects.active = mesh_objects[0]

if len(mesh_objects) > 1:
    bpy.ops.object.join()

obj = bpy.context.active_object

# Clean basic issues
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')

original_face_count = len(obj.data.polygons)

print(f"Original faces: {original_face_count}")

# --------- TRY QUADRIFLOW FIRST ----------
bpy.ops.object.quadriflow_remesh(target_faces=1500)

after_qf_faces = len(obj.data.polygons)

print(f"After QuadriFlow faces: {after_qf_faces}")

# # If QuadriFlow failed (face count barely changed), fallback
# if abs(after_qf_faces - original_face_count) < 50:
#     print("QuadriFlow likely failed — applying voxel remesh fallback")

#     # Undo QuadriFlow result
#     bpy.ops.wm.read_factory_settings(use_empty=True)
#     bpy.ops.wm.obj_import(filepath=input_path)

#     mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
#     for obj in mesh_objects:
#         obj.select_set(True)
#     bpy.context.view_layer.objects.active = mesh_objects[0]
#     if len(mesh_objects) > 1:
#         bpy.ops.object.join()

#     obj = bpy.context.active_object

#     bpy.ops.object.mode_set(mode='EDIT')
#     bpy.ops.mesh.select_all(action='SELECT')
#     bpy.ops.mesh.remove_doubles()
#     bpy.ops.mesh.normals_make_consistent(inside=False)
#     bpy.ops.object.mode_set(mode='OBJECT')

#     # Coarse voxel to force manifold
#     bpy.ops.object.modifier_add(type='REMESH')
#     remesh = obj.modifiers[-1]
#     remesh.mode = 'VOXEL'
#     remesh.voxel_size = 0.05
#     bpy.ops.object.modifier_apply(modifier=remesh.name)

#     # Now QuadriFlow again
#     bpy.ops.object.quadriflow_remesh(target_faces=1500)

#     print(f"After fallback QuadriFlow faces: {len(obj.data.polygons)}")

# Export result
bpy.ops.wm.obj_export(filepath=output_path)

print("Quad remesh pipeline complete.")