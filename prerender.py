import pygame
from OpenGL.GL import *
import os

def prerender_headset(renderer, headset, output_dir, frame_count=180):

    os.makedirs(output_dir, exist_ok=True)

    for angle in range(frame_count):

        renderer.clear()

        renderer.draw_model(
            headset.vertices,
            headset.faces,
            headset.edges,
            0,
            1.4,
            angle
        )

        width, height = 400, 400

        data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)

        surface = pygame.image.fromstring(data, (width, height), "RGBA", True)

        pygame.image.save(
            surface,
            os.path.join(output_dir, f"{angle:03}.png")
        )

    print(f"[SAVED] {headset.name} frames")