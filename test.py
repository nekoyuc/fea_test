import os
import json
from mesh_processors import mesh_processing as mp
from mesh_processors import modify_inp as mi
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import Obj

file = "500099.stl"
inpath = "Thingi10K/viz_experiment/"
outpath = "Thingi10K/viz_experiment/"
#mp(file, inpath, outpath)
#mi(outpath + file.replace(".stl", ".inp"))

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)

    # Import obj file
    obj = Obj("test2.obj", [], [], [])

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
    glEnable(GL_COLOR_MATERIAL)  # Enable color material

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glRotatef(1, 3, 1, 1)

        glBegin(GL_TRIANGLES)
        for face in obj.face:
            for i in range(3):
                glVertex3fv(obj.vert[face[i][0] - 1])
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

main()