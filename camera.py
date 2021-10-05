import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from math_utils import *

class camera():
    def __init__(self, pos, orient):
        self.pos = pos
        self.orient = orient

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos):
        req_trans = [new_pos[0] - self.pos[0],
                     new_pos[1] - self.pos[1],
                     new_pos[2] - self.pos[2]]
        glTranslate(req_trans[0], req_trans[1], req_trans[2])
        self.pos = new_pos

    def move_local(self, movement):
        
        glTranslate((movement[0] * self.orient[0][0]) + (movement[1] * self.orient[1][0]) + (movement[2] * self.orient[2][0]),
                    (movement[0] * self.orient[0][1]) + (movement[1] * self.orient[1][1]) + (movement[2] * self.orient[2][1]),
                    (movement[0] * self.orient[0][2]) + (movement[1] * self.orient[1][2]) + (movement[2] * self.orient[2][2]))
        
        self.pos = [self.pos[0] + (movement[0] * self.orient[0][0]) + (movement[1] * self.orient[1][0]) + (movement[2] * self.orient[2][0]),
                    self.pos[1] + (movement[0] * self.orient[0][1]) + (movement[1] * self.orient[1][1]) + (movement[2] * self.orient[2][1]),
                    self.pos[2] + (movement[0] * self.orient[0][2]) + (movement[1] * self.orient[1][2]) + (movement[2] * self.orient[2][2])]

    def move_absolute(self, movement):

        glTranslate(movement[0], movement[1], movement[2])
        
        self.pos = [self.pos[0] + movement[0],
                    self.pos[1] + movement[1],
                    self.pos[2] + movement[2]]


    def rotate(self, rotation, about=None, rot_lock=False):

        if about:
            about_pos = [-about.get_pos()[0], -about.get_pos()[1], -about.get_pos()[2]]
        else:
            about_pos = self.pos

        if not rot_lock:
            glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
            glRotate(-rotation[0], self.orient[0][0], self.orient[0][1], self.orient[0][2])
            glTranslate(about_pos[0], about_pos[1], about_pos[2])

            glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
            glRotate(-rotation[1], self.orient[1][0], self.orient[1][1], self.orient[1][2])
            glTranslate(about_pos[0], about_pos[1], about_pos[2])

            glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
            glRotate(-rotation[2], self.orient[2][0], self.orient[2][1], self.orient[2][2])
            glTranslate(about_pos[0], about_pos[1], about_pos[2])

            self.orient = rotate_matrix(self.orient, rotation)

        elif about and rot_lock:
            glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
            glRotate(-rotation[0], about.orient[0][0], about.orient[0][1], about.orient[0][2])
            glTranslate(about_pos[0], about_pos[1], about_pos[2])

            glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
            glRotate(-rotation[1], about.orient[1][0], about.orient[1][1], about.orient[1][2])
            glTranslate(about_pos[0], about_pos[1], about_pos[2])

            glTranslate(-about_pos[0], -about_pos[1], -about_pos[2])
            glRotate(-rotation[2], about.orient[2][0], about.orient[2][1], about.orient[2][2])
            glTranslate(about_pos[0], about_pos[1], about_pos[2])

            self.orient = rotate_matrix(self.orient, rotation, about)

