import os
import subprocess
from simple_obj_loader import load_obj


# -------------------------------------------------
# Ensure quadmesh exists (never remesh quad files)
# -------------------------------------------------
def ensure_quadmesh(original_path):
    filename = os.path.basename(original_path)

    # If already a quad file, just return it
    if "_quad_" in filename:
        return original_path

    quad_path = original_path.replace("_model.obj", "_quad_model.obj")

    if os.path.exists(quad_path):
        return quad_path

    print(f"[REMESH] Generating quad mesh for {filename}")

    blender_path = r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe"

    subprocess.run([
        blender_path,
        "--background",
        "--python",
        "quad_remesh.py",
        "--",
        os.path.abspath(original_path),
        os.path.abspath(quad_path)
    ], check=True)

    return quad_path

import os
import trimesh


def ensure_simplified_mesh(original_path, target_faces=4000):
    filename = os.path.basename(original_path)

    # Only simplify original model files
    if "_simplified" in filename:
        return original_path

    simplified_path = original_path.replace("_model.obj", "_simplified.obj")

    if os.path.exists(simplified_path):
        return simplified_path

    print(f"[SIMPLIFY] Reducing {filename} to ~{target_faces} faces")

    mesh = trimesh.load(original_path, force='mesh')

    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Loaded file is not a valid mesh")

    if len(mesh.faces) > target_faces:
        mesh = mesh.simplify_quadratic_decimation(target_faces)

    mesh.export(simplified_path)

    return simplified_path

# -------------------------------------------------
# Headset Object
# -------------------------------------------------
class Headset:
    def __init__(self, name, model_path, description_path=None):
        self.name = name

        quad_path = ensure_quadmesh(model_path)

        self.vertices, self.faces, self.edges = load_obj(quad_path)

        if description_path and os.path.exists(description_path):
            with open(description_path, "r", encoding="utf-8") as f:
                self.description = f.read()
        else:
            self.description = "No description available."


# -------------------------------------------------
# Headset Manager
# -------------------------------------------------
class HeadsetManager:
    def __init__(self, asset_dir="assets/headsets"):
        self.headsets = []
        self.load_headsets(asset_dir)

    def load_headsets(self, asset_dir):
        if not os.path.exists(asset_dir):
            print(f"[WARN] Asset directory not found: {asset_dir}")
            return

        folders = sorted(os.listdir(asset_dir))

        for folder in folders:
            folder_path = os.path.join(asset_dir, folder)

            if not os.path.isdir(folder_path):
                continue

            model_file = None
            description_file = None

            for file in os.listdir(folder_path):
                lower = file.lower()

                # Only allow ORIGINAL model files (exclude quad)
                if lower.endswith("_model.obj") and "_quad_" not in lower:
                    model_file = os.path.join(folder_path, file)

                if lower == "description.txt":
                    description_file = os.path.join(folder_path, file)

            if model_file:
                try:
                    headset = Headset(folder, model_file, description_file)
                    self.headsets.append(headset)
                    print(f"[LOADED] {folder} ({len(headset.edges)} edges)")
                except Exception as e:
                    print(f"[ERROR] Failed loading {folder}: {e}")
            else:
                print(f"[SKIP] No original *_model.obj found in {folder}")

        print(f"[INFO] Total headsets loaded: {len(self.headsets)}")

    def count(self):
        return len(self.headsets)

    def get(self, index):
        if len(self.headsets) == 0:
            return None
        return self.headsets[index % len(self.headsets)]