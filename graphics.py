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
    glColor(0.3, 0.3, 0.35)
    
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

def drawTerrain(t, current_ship, render_dist):
    glPushMatrix()
    glTranslatef(t.get_center()[0], t.get_center()[1], t.get_center()[2])

    glColor(0.8, 0.8, 0.8)

    glBegin(GL_POLYGON)

    # draw x lines
    for a in range(t.z_lines_num):
        for b in range(t.x_lines_num):
            # why the hell is drawing lines so bloody expensive??
            # anyway, don't draw those that are too far away
            if (abs(current_ship.get_pos()[0] - t.vertices[a*t.x_lines_num+b][0]) < 250*render_dist + current_ship.get_pos()[1] * render_dist and
                abs(current_ship.get_pos()[2] - t.vertices[a*t.x_lines_num+b][2]) < 250*render_dist + current_ship.get_pos()[1] * render_dist):
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
            if (abs(current_ship.get_pos()[0] - t.vertices[a*t.x_lines_num+b][0]) < 100 * render_dist + current_ship.get_pos()[1] * 0.625 * render_dist and
                abs(current_ship.get_pos()[2] - t.vertices[a*t.x_lines_num+b][2]) < 100 * render_dist + current_ship.get_pos()[1] * 0.625 * render_dist):
                if not b+1 == t.x_lines_num:
                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
                    glVertex3f(t.vertices[a*t.x_lines_num+b+1][0], t.vertices[a*t.x_lines_num+b+1][1], t.vertices[a*t.x_lines_num+b+1][2])

                if not a+1 == t.z_lines_num:
                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
                    glVertex3f(t.vertices[(a+1)*t.x_lines_num+b][0], t.vertices[(a+1)*t.x_lines_num+b][1], t.vertices[(a+1)*t.x_lines_num+b][2])

    glEnd()
    
    glPopMatrix()

def drawLine2D(x1, y1, x2, y2, color, camera):
    glPushMatrix()
    glTranslate(-camera.get_pos()[0],
                -camera.get_pos()[1],
                -camera.get_pos()[2])
    
    glColor(color[0], color[1], color[2])
    
    glBegin(GL_LINES)
    
    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-10) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-10) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-10) * camera.get_orient()[2][2])
    
    glVertex3f((x2) * camera.get_orient()[0][0] + (y2) * camera.get_orient()[1][0] + (-10) * camera.get_orient()[2][0],
               (x2) * camera.get_orient()[0][1] + (y2) * camera.get_orient()[1][1] + (-10) * camera.get_orient()[2][1],
               (x2) * camera.get_orient()[0][2] + (y2) * camera.get_orient()[1][2] + (-10) * camera.get_orient()[2][2])
    glEnd()
    glPopMatrix()

def drawRectangle2D(x1, y1, x2, y2, color, camera):
    drawLine2D(x1, y1, x2, y1, color, camera)
    drawLine2D(x1, y1, x1, y2, color, camera)
    drawLine2D(x2, y1, x2, y2, color, camera)
    drawLine2D(x1, y2, x2, y2, color, camera)

def drawInterface(camera, ship, autopilot):

##    # artificial horizon
##    glPushMatrix()
##    glTranslate(-camera.get_pos()[0],
##                -camera.get_pos()[1],
##                -camera.get_pos()[2])
##    
##    glColor(0.9, 0.9, 0.9)
##    
##    glBegin(GL_LINES)
##    
##    glVertex3f(5 * camera.get_orient()[0][0] + 0 * camera.get_orient()[1][0] + (-10) * camera.get_orient()[2][0],
##               0,
##               5 * camera.get_orient()[0][2] + 0 * camera.get_orient()[1][2] + (-10) * camera.get_orient()[2][2])
##    
##    glVertex3f(3 * camera.get_orient()[0][0] + 0 * camera.get_orient()[1][0] + (-10) * camera.get_orient()[2][0],
##               0,
##               3 * camera.get_orient()[0][2] + 0 * camera.get_orient()[1][2] + (-10) * camera.get_orient()[2][2])
##    glEnd()
##    glPopMatrix()
    
    # thrust setting
    percent_thrust = ship.get_percent_thrust()
    thrust_line_y = percent_thrust/100 * 3 -5
    
    drawRectangle2D(5,-2,6,-5,[1,0,1], camera)
    drawLine2D(5,thrust_line_y,6,thrust_line_y,[1,0,1], camera)

    # angular velocity display
    drawRectangle2D(6, 4, 8, 6, [1,0,0], camera)

    # centerlines
    drawLine2D(6, 5, 8, 5, [0.5,0,0], camera)
    drawLine2D(7, 4, 7, 6, [0.5,0,0], camera)
    drawLine2D(7, 6, 7, 6.5, [0.5,0,0], camera)
    
    # horiz line (moves in y direction)
    drawLine2D(6, max(min(ship.get_ang_vel()[0]/8 + 5, 5.9), 4.1),
               8, max(min(ship.get_ang_vel()[0]/8 + 5, 5.9), 4.1),
               [1,0,0], camera)
    # vert line (moves in x direction)
    drawLine2D(max(min(-ship.get_ang_vel()[1]/8 + 7, 7.9), 6.1), 4,
               max(min(-ship.get_ang_vel()[1]/8 + 7, 7.9), 6.1), 6,
               [1,0,0], camera)

    # roll
    drawRectangle2D(6, 6, 8, 6.5, [1,0,0], camera)
    drawLine2D(max(min(-ship.get_ang_vel()[2]/8 + 7,7.9),6.1), 6,
               max(min(-ship.get_ang_vel()[2]/8 + 7,7.9),6.1), 6.5, [1,0,0], camera)

    # linear velocity display
    drawRectangle2D(3, 4, 5, 6, [0,1,1], camera)

    # centerlines
    drawLine2D(3, 5, 5, 5, [0,0.5,0.5], camera)
    drawLine2D(3, 5, 5, 5, [0,0.5,0.5], camera)
    
    horizontal_vel_x = ship.get_vel()[0] * ship.get_orient()[0][0] + ship.get_vel()[2] * ship.get_orient()[0][2]
    horizontal_vel_z = ship.get_vel()[2] * ship.get_orient()[2][2] + ship.get_vel()[0] * ship.get_orient()[2][0]

    # local horizontal z
    drawLine2D(3,max(min(-horizontal_vel_z/25 + 5, 5.9), 4.1),
               5,max(min(-horizontal_vel_z/25 + 5, 5.9), 4.1),
               [0,1,1], camera)

    # local horizontal x
    drawLine2D(max(min(horizontal_vel_x/25 + 4, 4.9), 3.1), 4,
               max(min(horizontal_vel_x/25 + 4, 4.9), 3.1), 6,
               [0,1,1], camera)

    # descent speed
    drawRectangle2D(2.5, 4, 3, 6, [0,1,1], camera)
    
    # centerline
    drawLine2D(2.5, 5.5, 3, 5.5, [0,0.5,0.5], camera)

    # descent rate
    drawLine2D(2.5, max(min(ship.get_vel()[1]/10 + 5.5, 5.9), 4.1),
               3, max(min(ship.get_vel()[1]/10 + 5.5, 5.9), 4.1),
               [0,1,1], camera)

    # AP light
    if autopilot:
        drawRectangle2D(5, -1.9, 5.4, -1.5, [0,0.8,0], camera)

    if ship.get_prop_mass() < 500:
        drawRectangle2D(5.6, -1.9, 6, -1.5, [1,0,0], camera)
