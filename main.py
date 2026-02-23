import pygame
import time
import config
from headset_manager import HeadsetManager
from renderer import Renderer

def main():
    manager = HeadsetManager()
    renderer = Renderer()

    index = 0
    show_description = False
    rotation = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index += 1
                if event.key == pygame.K_LEFT:
                    index -= 1
                if event.key == pygame.K_RETURN:
                    show_description = not show_description

        rotation += config.ROTATION_SPEED * 60 * dt

        renderer.clear()

        center = manager.get(index)
        left = manager.get(index - 1)
        right = manager.get(index + 1)

        # Draw models
        renderer.draw_model(
            center.vertices,
            center.faces,
            center.edges,
            0,
            config.CENTER_SCALE,
            rotation
        )

        renderer.draw_model(
            left.vertices,
            left.faces,
            left.edges,
            -config.MODEL_SPACING,
            config.SIDE_SCALE,
            0
        )

        renderer.draw_model(
            right.vertices,
            right.faces,
            right.edges,
            config.MODEL_SPACING,
            config.SIDE_SCALE,
            0
        )

        # UI Text
        renderer.draw_text(center.name,
                           config.WINDOW_WIDTH // 2 - 80,
                           40)

        if show_description:
            renderer.draw_text(center.description[:200],
                               50,
                               config.WINDOW_HEIGHT - 80)

        renderer.update()

    pygame.quit()

if __name__ == "__main__":
    main()