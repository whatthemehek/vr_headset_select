import numpy as np


import numpy as np


def load_obj(path):
    vertices = []
    faces = []

    with open(path, "r") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.strip().split()
                vertices.append(tuple(map(float, parts[1:4])))

            elif line.startswith("f "):
                parts = line.strip().split()[1:]
                face_indices = [int(p.split("/")[0]) - 1 for p in parts]
                faces.append(face_indices)

    vertices = np.array(vertices)

    # ---- AUTO CENTER ----
    min_vals = vertices.min(axis=0)
    max_vals = vertices.max(axis=0)
    center = (min_vals + max_vals) / 2.0
    vertices = vertices - center

    # ---- AUTO SCALE ----
    size = np.max(max_vals - min_vals)
    if size > 0:
        vertices = vertices / size

    # ---- GENERATE UNIQUE EDGES FROM FACES ----
    edges = set()

    for face in faces:
        for i in range(len(face)):
            a = face[i]
            b = face[(i + 1) % len(face)]
            edge = tuple(sorted((a, b)))
            edges.add(edge)

    edges = list(edges)

    return vertices, edges

import numpy as np
from scipy.spatial import ConvexHull

import numpy as np
from scipy.spatial import ConvexHull

import numpy as np

import numpy as np

import numpy as np


def generate_surface_grid(vertices, triangles, slices=14):
    rings = []

    min_vals = vertices.min(axis=0)
    max_vals = vertices.max(axis=0)

    # --- Horizontal rings (Y planes) ---
    ys = np.linspace(min_vals[1], max_vals[1], slices)
    for y in ys:
        segments = intersect_plane(vertices, triangles, axis=1, value=y)
        loops = stitch_segments(segments)
        for loop in loops:
            if len(loop) > 4:
                rings.append(np.array(loop))

    # --- Vertical rings (Z planes) ---
    zs = np.linspace(min_vals[2], max_vals[2], slices)
    for z in zs:
        segments = intersect_plane(vertices, triangles, axis=2, value=z)
        loops = stitch_segments(segments)
        for loop in loops:
            if len(loop) > 4:
                rings.append(np.array(loop))

    return rings


def intersect_plane(vertices, triangles, axis, value):
    segments = []

    for tri in triangles:
        v0, v1, v2 = vertices[list(tri)]

        points = []
        for a, b in [(v0, v1), (v1, v2), (v2, v0)]:
            if (a[axis] - value) * (b[axis] - value) < 0:
                t = (value - a[axis]) / (b[axis] - a[axis])
                p = a + t * (b - a)
                points.append(p)

        if len(points) == 2:
            segments.append((points[0], points[1]))

    return segments


def stitch_segments(segments, tolerance=1e-4):
    loops = []
    segments = segments.copy()

    while segments:
        a, b = segments.pop(0)
        loop = [a, b]

        extended = True
        while extended:
            extended = False
            for i, (p1, p2) in enumerate(segments):
                if np.linalg.norm(loop[-1] - p1) < tolerance:
                    loop.append(p2)
                    segments.pop(i)
                    extended = True
                    break
                elif np.linalg.norm(loop[-1] - p2) < tolerance:
                    loop.append(p1)
                    segments.pop(i)
                    extended = True
                    break

        loops.append(loop)

    return loops