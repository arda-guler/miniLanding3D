import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import random

from math_utils import *

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1000,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(1000,0,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1000)
    glEnd()

def drawVessel(v):

    # change color we render with
    glColor(0.2, 0.2, 1)
    
    # here we go
    glPushMatrix()

    # put us in correct position
    glTranslatef(v.get_pos()[0], v.get_pos()[1], v.get_pos()[2])

    # actually render model now, with triangles
    for mesh in v.model.mesh_list:
        glBegin(GL_POLYGON)
        for face in mesh.faces:
            for vertex_i in face:
                vertex_i = v.model.vertices[vertex_i]
                vertex_i = numpy.matmul(numpy.array(vertex_i), v.get_orient())
                vertex_i = [vertex_i[0], vertex_i[1], vertex_i[2]]
                glVertex3f(vertex_i[0], vertex_i[1], vertex_i[2])
        glEnd()

    # now get out
    glPopMatrix()

def drawTerrain(t, current_ship):
    glPushMatrix()
    glTranslatef(t.get_center()[0], t.get_center()[1], t.get_center()[2])

    glColor(0.8, 0.8, 0.8)

    glBegin(GL_POLYGON)

    # draw x lines
    for a in range(t.z_lines_num):
        for b in range(t.x_lines_num):
            # why the hell is drawing lines so bloody expensive??
            # anyway, don't draw those that are too far away
            if (abs(current_ship.get_pos()[0] - t.vertices[a*t.x_lines_num+b][0]) < 500 + current_ship.get_pos()[1] * 2 and
                abs(current_ship.get_pos()[2] - t.vertices[a*t.x_lines_num+b][2]) < 500 + current_ship.get_pos()[1] * 2):
                if not b+1 == t.x_lines_num:
                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
                    glVertex3f(t.vertices[a*t.x_lines_num+b+1][0], t.vertices[a*t.x_lines_num+b+1][1], t.vertices[a*t.x_lines_num+b+1][2])

                if not a+1 == t.z_lines_num:
                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
                    glVertex3f(t.vertices[(a+1)*t.x_lines_num+b][0], t.vertices[(a+1)*t.x_lines_num+b][1], t.vertices[(a+1)*t.x_lines_num+b][2])

    glEnd()

    glColor(0.0, 0.5, 0.0)
    glBegin(GL_LINES)
    # draw x lines
    for a in range(t.z_lines_num):
        for b in range(t.x_lines_num):
            # why the hell is drawing lines so bloody expensive??
            # anyway, don't draw those that are too far away
            if (abs(current_ship.get_pos()[0] - t.vertices[a*t.x_lines_num+b][0]) < 200 + current_ship.get_pos()[1] * 1.25 and
                abs(current_ship.get_pos()[2] - t.vertices[a*t.x_lines_num+b][2]) < 200 + current_ship.get_pos()[1] * 1.25):
                if not b+1 == t.x_lines_num:
                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
                    glVertex3f(t.vertices[a*t.x_lines_num+b+1][0], t.vertices[a*t.x_lines_num+b+1][1], t.vertices[a*t.x_lines_num+b+1][2])

                if not a+1 == t.z_lines_num:
                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
                    glVertex3f(t.vertices[(a+1)*t.x_lines_num+b][0], t.vertices[(a+1)*t.x_lines_num+b][1], t.vertices[(a+1)*t.x_lines_num+b][2])

    glEnd()
    
    glPopMatrix()
