import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

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

# 7-segment display line defs
#
#    _3_
# 1 |   | 6
#   |_4_|
# 2 |   | 7
#   |_5_| . (dot)
#

def l1():
    p1 = (0, 2)
    p2 = (0, 1)
    return [p1, p2]

def l2():
    p1 = (0, 1)
    p2 = (0, 0)
    return [p1, p2]

def l3():
    p1 = (0, 2)
    p2 = (1, 2)
    return [p1, p2]

def l4():
    p1 = (0, 1)
    p2 = (1, 1)
    return [p1, p2]

def l5():
    p1 = (0, 0)
    p2 = (1, 0)
    return [p1, p2]

def l6():
    p1 = (1, 2)
    p2 = (1, 1)
    return [p1, p2]

def l7():
    p1 = (1, 1)
    p2 = (1, 0)
    return [p1, p2]

# Number defs
def zero():
    return [l1, l2, l3, l5, l6, l7]

def one():
    return [l6, l7]

def two():
    return [l3, l6, l4, l2, l5]

def three():
    return [l3, l6, l4, l7, l5]

def four():
    return [l1, l4, l6, l7]

def five():
    return [l3, l1, l4, l7, l5]

def six():
    return [l3, l1, l4, l2, l7, l5]

def seven():
    return [l3, l6, l7]

def eight():
    return [l1, l2, l3, l4, l5, l6, l7]

def nine():
    return [l4, l1, l3, l6, l7, l5]

def minus():
    return [l4]

def dot():
    return (0, 0)

numbers = {"0": zero(),
           "1": one(),
           "2": two(),
           "3": three(),
           "4": four(),
           "5": five(),
           "6": six(),
           "7": seven(),
           "8": eight(),
           "9": nine(),
           "-": minus()}

def render_numbers(numstring, color, start_pt, cam, font_size=0.5):
    global numbers
    
    draw_start_x = start_pt[0]
    spacing = font_size * 0.5
    
    for char in numstring:
        if not char == ".":
            lines = numbers[char]
            for line in lines:
                x1 = draw_start_x + font_size * line()[0][0]
                y1 = start_pt[1] + font_size * line()[0][1]
                x2 = draw_start_x + font_size * line()[1][0]
                y2 = start_pt[1] + font_size * line()[1][1]
                drawLine2D(x1, y1, x2, y2, color, cam)

        else:
            x = draw_start_x
            y = start_pt[1]
            drawPoint2D(x, y, color, cam)

        draw_start_x += font_size + spacing

