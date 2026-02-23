import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

gluPerspective(45, 800/600, 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    pygame.display.flip()

pygame.quit()