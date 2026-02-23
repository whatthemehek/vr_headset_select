import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import config

class Renderer:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            pygame.OPENGL | pygame.DOUBLEBUF
        )

        glEnable(GL_DEPTH_TEST)

        gluPerspective(
            60,
            config.WINDOW_WIDTH / config.WINDOW_HEIGHT,
            0.1,
            50.0
        )

        self.font = pygame.font.SysFont("Consolas", 28)

    def clear(self):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw_model(self, vertices, edges, position_x,
                scale, rotation_y=0):

        glPushMatrix()
        glTranslatef(position_x, 0, -4.2)
        glScalef(scale, scale, scale)
        glRotatef(rotation_y, 0, 1, 0)

        glDisable(GL_DEPTH_TEST)
        glLineWidth(1.5)
        glColor3f(*config.WIREFRAME_COLOR)

        glBegin(GL_LINES)
        for edge in edges:
            glVertex3fv(vertices[edge[0]])
            glVertex3fv(vertices[edge[1]])
        glEnd()

        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
    # ---------- TEXTURE TEXT RENDERING ----------
    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, config.TEXT_COLOR)
        texture_data = pygame.image.tostring(surface, "RGBA", True)
        width = surface.get_width()
        height = surface.get_height()

        # --- Switch to 2D projection ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, config.WINDOW_WIDTH,
                0, config.WINDOW_HEIGHT,
                -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # --- Create texture ---
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            texture_data
        )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # --- FIX STATE ---
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # THIS IS THE IMPORTANT LINE
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

        glColor4f(1, 1, 1, 1)  # Force white

        # --- Draw quad ---
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + width, y)
        glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
        glTexCoord2f(0, 1); glVertex2f(x, y + height)
        glEnd()

        # --- Cleanup ---
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        glDeleteTextures([texture])

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
    def update(self):
        pygame.display.flip()