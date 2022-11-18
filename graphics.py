import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import random

from math_utils import *
from ui_text import *

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

def spherical2cartesian(rho, theta, phi):    
    x = math.cos(theta) * math.sin(phi) * rho
    y = math.sin(theta) * math.sin(phi) * rho
    z = math.cos(phi) * rho
    
    return [x, y, z]

def initBackground(star_num = 100):
    stars = []
    for i in range(star_num):
        rho = 200000
        theta = random.uniform(0, 3.14)
        phi = random.uniform(0, 3.14)

        rand_pos = spherical2cartesian(rho, theta, phi)
        stars.append([rand_pos[0], rand_pos[1], rand_pos[2]])

    return stars

def drawBackground(stars):
    glPushMatrix()
    glColor(1, 1, 1)
    glBegin(GL_POINTS)
    for star in stars:
        glVertex3f(star[0],star[1],star[2])
    glEnd()
    glPopMatrix()

def drawVessel(v):
    
    # here we go
    glPushMatrix()

    # change color we render with
    glColor(0.3, 0.3, 0.35)

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

    # engine plume cone
    if v.get_main_engine():
        glPushMatrix()
        glColor(0.9, 0.7, 0)

        glBegin(GL_LINES)
        
        plume_start = [0,-5,0]
        plume_start = numpy.matmul(numpy.array(plume_start), v.get_orient())
        
        plume_end_1 = [0.05*v.get_percent_thrust(), -0.15*v.get_percent_thrust(), 0]
        plume_end_1 = numpy.matmul(numpy.array(plume_end_1), v.get_orient())
        glVertex3f(plume_start[0], plume_start[1], plume_start[2])
        glVertex3f(plume_end_1[0], plume_end_1[1], plume_end_1[2])

        plume_end_2 = [-0.05*v.get_percent_thrust(), -0.15*v.get_percent_thrust(), 0]
        plume_end_2 = numpy.matmul(numpy.array(plume_end_2), v.get_orient())
        glVertex3f(plume_start[0], plume_start[1], plume_start[2])
        glVertex3f(plume_end_2[0], plume_end_2[1], plume_end_2[2])

        plume_end_3 = [0, -0.15*v.get_percent_thrust(), 0.05*v.get_percent_thrust()]
        plume_end_3 = numpy.matmul(numpy.array(plume_end_3), v.get_orient())
        glVertex3f(plume_start[0], plume_start[1], plume_start[2])
        glVertex3f(plume_end_3[0], plume_end_3[1], plume_end_3[2])

        plume_end_4 = [0, -0.15*v.get_percent_thrust(), -0.05*v.get_percent_thrust()]
        plume_end_4 = numpy.matmul(numpy.array(plume_end_4), v.get_orient())
        glVertex3f(plume_start[0], plume_start[1], plume_start[2])
        glVertex3f(plume_end_4[0], plume_end_4[1], plume_end_4[2])

        glVertex3f(plume_end_1[0], plume_end_1[1], plume_end_1[2])
        glVertex3f(plume_end_3[0], plume_end_3[1], plume_end_3[2])

        glVertex3f(plume_end_3[0], plume_end_3[1], plume_end_3[2])
        glVertex3f(plume_end_2[0], plume_end_2[1], plume_end_2[2])

        glVertex3f(plume_end_2[0], plume_end_2[1], plume_end_2[2])
        glVertex3f(plume_end_4[0], plume_end_4[1], plume_end_4[2])

        glVertex3f(plume_end_4[0], plume_end_4[1], plume_end_4[2])
        glVertex3f(plume_end_1[0], plume_end_1[1], plume_end_1[2])
        
        glEnd()
        
        glPopMatrix()

    # now get out
    glPopMatrix()

def drawTerrain(t, current_ship, render_dist):
    glPushMatrix()
    glTranslatef(t.get_center()[0], t.get_center()[1], t.get_center()[2])

    glColor(0.8, 0.8, 0.8)

    glBegin(GL_POLYGON)

    x_lines_num = t.x_lines_num
    z_lines_num = t.z_lines_num
    x_spacing = t.x_spacing
    z_spacing = t.z_spacing

    rect_render_dist = 250*render_dist + current_ship.get_pos()[1] * render_dist

    rel_x = current_ship.get_pos()[0] - t.center[0]
    rel_z = current_ship.get_pos()[2] - t.center[2]

    render_min_x = rel_x - rect_render_dist
    render_max_x = rel_x + rect_render_dist
    x_min_index = max(int(x_lines_num/2 + render_min_x/x_spacing), 0)
    x_max_index = max(int(x_lines_num/2 + render_max_x/x_spacing), x_lines_num-1)

    render_min_z = rel_z - rect_render_dist
    render_max_z = rel_z + rect_render_dist
    z_min_index = max(int(z_lines_num/2 + render_min_z/z_spacing), 0)
    z_max_index = max(int(z_lines_num/2 + render_max_z/z_spacing), z_lines_num-1)

    #print(x_min_index, x_max_index)
    #print(z_min_index, z_max_index)
    
    indices = []
    ai = 0
    for a in range(z_min_index, z_max_index):
        indices.append([])
        for b in range(x_min_index, x_max_index):
            indices[ai].append(a * x_lines_num + b)

        ai += 1

    for z in indices:
        for x in z:
            #print(x)
            try:
                glVertex3f(t.vertices[x][0], t.vertices[x][1], t.vertices[x][2])
                glVertex3f(t.vertices[x+x_lines_num][0], t.vertices[x+x_lines_num][1], t.vertices[x+x_lines_num][2])
            except:
                pass
        
    
##    for a in range(t.z_lines_num):
##        for b in range(t.x_lines_num):
##            # why the hell is drawing lines so bloody expensive??
##            # anyway, don't draw those that are too far away
##            if (abs(current_ship.get_pos()[0] - t.vertices[a*t.x_lines_num+b][0]) < 250*render_dist + current_ship.get_pos()[1] * render_dist and
##                abs(current_ship.get_pos()[2] - t.vertices[a*t.x_lines_num+b][2]) < 250*render_dist + current_ship.get_pos()[1] * render_dist):
##                if not b+1 == t.x_lines_num:
##                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
##                    #glVertex3f(t.vertices[a*t.x_lines_num+b+1][0], t.vertices[a*t.x_lines_num+b+1][1], t.vertices[a*t.x_lines_num+b+1][2])
##
##                if not a-1 < 0:
##                    glVertex3f(t.vertices[(a-1)*t.x_lines_num+b][0], t.vertices[(a-1)*t.x_lines_num+b][1], t.vertices[(a-1)*t.x_lines_num+b][2])
##                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])

    glEnd()

    glColor(0.0, 0.5, 0.0)

    for z in indices:
        glBegin(GL_LINE_STRIP)
        for x in z:
            #print(x)
            try:
                glVertex3f(t.vertices[x][0], t.vertices[x][1], t.vertices[x][2])
                glVertex3f(t.vertices[x+x_lines_num+1][0], t.vertices[x+x_lines_num+1][1], t.vertices[x+x_lines_num+1][2])
            except:
                pass
    
##    for a in range(t.z_lines_num):
##        glBegin(GL_LINE_STRIP)
##        for b in range(t.x_lines_num):
##            # why the hell is drawing lines so bloody expensive??
##            # anyway, don't draw those that are too far away
##            if (abs(current_ship.get_pos()[0] - t.vertices[a*t.x_lines_num+b][0]) < 100 * render_dist + current_ship.get_pos()[1] * 0.625 * render_dist and
##                abs(current_ship.get_pos()[2] - t.vertices[a*t.x_lines_num+b][2]) < 100 * render_dist + current_ship.get_pos()[1] * 0.625 * render_dist):
##                if not b+1 == t.x_lines_num:
##                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])
##                    #glVertex3f(t.vertices[a*t.x_lines_num+b+1][0], t.vertices[a*t.x_lines_num+b+1][1], t.vertices[a*t.x_lines_num+b+1][2])
##
##                if not a-1 < 0:
##                    glVertex3f(t.vertices[(a-1)*t.x_lines_num+b][0], t.vertices[(a-1)*t.x_lines_num+b][1], t.vertices[(a-1)*t.x_lines_num+b][2])
##                    glVertex3f(t.vertices[a*t.x_lines_num+b][0], t.vertices[a*t.x_lines_num+b][1], t.vertices[a*t.x_lines_num+b][2])

        glEnd()
    
    glPopMatrix()

def drawPoint2D(x, y, color, camera):
    glPushMatrix()

    glTranslate(-camera.get_pos()[0],
                -camera.get_pos()[1],
                -camera.get_pos()[2])
    
    glColor(color[0], color[1], color[2])

    glBegin(GL_POINTS)

    x1 = x * 100
    y1 = y * 100

    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])

    glEnd()
    
    glPopMatrix()

def drawLine2D(x1, y1, x2, y2, color, camera):
    glPushMatrix()
    glTranslate(-camera.get_pos()[0],
                -camera.get_pos()[1],
                -camera.get_pos()[2])
    
    glColor(color[0], color[1], color[2])
    
    glBegin(GL_LINES)

    x1 = x1 * 100
    y1 = y1 * 100
    x2 = x2 * 100
    y2 = y2 * 100
    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    
    glVertex3f((x2) * camera.get_orient()[0][0] + (y2) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x2) * camera.get_orient()[0][1] + (y2) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x2) * camera.get_orient()[0][2] + (y2) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    glEnd()
    glPopMatrix()

def drawRectangle2D(x1, y1, x2, y2, color, camera):
    drawLine2D(x1, y1, x2, y1, color, camera)
    drawLine2D(x1, y1, x1, y2, color, camera)
    drawLine2D(x2, y1, x2, y2, color, camera)
    drawLine2D(x1, y2, x2, y2, color, camera)

def drawNumbers(camera, ship, autopilot, terrain, at_descent_rate):

    # Velocity
    vel_x = "VX " + str(round(ship.get_vel()[0], 3))
    vel_y = "VY " + str(round(ship.get_vel()[1], 3))
    vel_z = "VZ " + str(round(ship.get_vel()[2], 3))
    
    render_AN(vel_x, (0,1,1), (4.45, 3.2), camera, font_size=0.1)
    render_AN(vel_y, (0,1,1), (4.45, 2.7), camera, font_size=0.1)
    render_AN(vel_z, (0,1,1), (4.45, 2.2), camera, font_size=0.1)

    # Altitude
    if ship.get_alt_quick(terrain) > 50:
        alt = "ALT " + str(round(ship.get_alt_quick(terrain), 3))
    else:
        alt = "ALT " + str(round(ship.get_alt(terrain), 3))
    render_AN(alt, (0,1,0), (4.45, 0), camera, font_size=0.1)

    # AP descent rate cmd
    adr = "APDR " + str(round(at_descent_rate, 1))
    render_AN(adr, (1,0,1), (8, 2.7), camera, font_size=0.1)

    # Propellant
    prop = "PROP " + str(round(ship.get_prop_mass(), 1))
    render_AN(prop, (0.75,0,1), (4.45, -5.3), camera, font_size=0.1)

def drawInterface(camera, ship, autopilot, terrain, at_descent_rate, thrust_update_cmd, rot_damp):

    drawNumbers(camera, ship, autopilot, terrain, at_descent_rate)

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
    
    if thrust_update_cmd:
        thrust_ap_percent = max(min(ship.get_percent_thrust() + (thrust_update_cmd / ship.get_max_thrust()) * 100, 100), 0)
        thrust_ap_line_y = thrust_ap_percent/100 * 3 -5

        # left chevron (>)
        drawLine2D(6.8, thrust_ap_line_y + 0.2, 7, thrust_ap_line_y, [0.85, 0, 0.85], camera)
        drawLine2D(6.8, thrust_ap_line_y - 0.2, 7, thrust_ap_line_y, [0.85, 0, 0.85], camera)

        # right chevron (<)
        drawLine2D(8.2, thrust_ap_line_y + 0.2, 8, thrust_ap_line_y, [0.85, 0, 0.85], camera)
        drawLine2D(8.2, thrust_ap_line_y - 0.2, 8, thrust_ap_line_y, [0.85, 0, 0.85], camera)

        #drawLine2D(4.9, thrust_ap_line_y, 6.1, thrust_ap_line_y, [0.75, 0, 0.75], camera)
        
    drawLine2D(7,thrust_line_y,8,thrust_line_y,[1,0,1], camera)
    drawRectangle2D(7,-2,8,-5,[1,0,1], camera)

    # angular velocity display
    drawRectangle2D(8, 4, 10, 6, [1,0,0], camera)
    if rot_damp:
        drawLine2D(8, 4, 10, 6, [1,0,0], camera)
        drawLine2D(8, 6, 10, 4, [1,0,0], camera)

    # centerlines
    drawLine2D(8, 5, 10, 5, [0.5,0,0], camera)
    drawLine2D(9, 4, 9, 6, [0.5,0,0], camera)
    drawLine2D(9, 6, 9, 6.5, [0.5,0,0], camera)
    
    # horiz line (moves in y direction)
    drawLine2D(8, max(min(ship.get_ang_vel()[0]/8 + 5, 5.9), 4.1),
               10, max(min(ship.get_ang_vel()[0]/8 + 5, 5.9), 4.1),
               [1,0,0], camera)
    # vert line (moves in x direction)
    drawLine2D(max(min(-ship.get_ang_vel()[1]/8 + 9, 9.9), 8.1), 4,
               max(min(-ship.get_ang_vel()[1]/8 + 9, 9.9), 8.1), 6,
               [1,0,0], camera)

    # roll
    drawRectangle2D(8, 6, 10, 6.5, [1,0,0], camera)
    drawLine2D(max(min(-ship.get_ang_vel()[2]/8 + 9,9.9),8.1), 6,
               max(min(-ship.get_ang_vel()[2]/8 + 9,9.9),8.1), 6.5, [1,0,0], camera)

    # linear velocity display
    drawRectangle2D(5, 4, 7, 6, [0,1,1], camera)

    # centerlines
    drawLine2D(5, 5, 7, 5, [0,0.5,0.5], camera)
    drawLine2D(5, 5, 7, 5, [0,0.5,0.5], camera)
    
    horizontal_vel_x = ship.get_vel()[0] * ship.get_orient()[0][0] + ship.get_vel()[2] * ship.get_orient()[0][2]
    horizontal_vel_z = ship.get_vel()[2] * ship.get_orient()[2][2] + ship.get_vel()[0] * ship.get_orient()[2][0]

    # local horizontal z
    drawLine2D(5,max(min(-horizontal_vel_z/25 + 5, 5.9), 4.1),
               7,max(min(-horizontal_vel_z/25 + 5, 5.9), 4.1),
               [0,1,1], camera)

    # local horizontal x
    drawLine2D(max(min(horizontal_vel_x/25 + 6, 6.9), 5.1), 4,
               max(min(horizontal_vel_x/25 + 6, 6.9), 5.1), 6,
               [0,1,1], camera)

    # descent speed
    drawRectangle2D(4.5, 4, 5, 6, [0,1,1], camera)
    
    # centerline
    drawLine2D(4.5, 5.5, 5, 5.5, [0,0.5,0.5], camera)

    # descent rate
    drawLine2D(4.5, max(min(ship.get_vel()[1]/10 + 5.5, 5.9), 4.1),
               5, max(min(ship.get_vel()[1]/10 + 5.5, 5.9), 4.1),
               [0,1,1], camera)

    # AP light
    if autopilot:
        drawRectangle2D(7, -1.9, 7.4, -1.5, [0,0.8,0], camera)

    if ship.get_prop_mass() < 500:
        drawRectangle2D(7.6, -1.9, 8, -1.5, [1,0,0], camera)
