import random

from math_utils import *

class terrain():
    def __init__(self, center, size, detail_level):
        self.center = center
        self.size = size
        self.detail_level = detail_level
        self.vertices = []

    def generate(self):
        # divide area into horizontal slits
        x_lines_num = int(self.size[0] * self.detail_level)
        x_lines = []

        x_pos_iterator = self.center[0] - self.size[0]/2
        for i in range(x_lines_num):
            x_lines.append(x_pos_iterator)
            x_pos_iterator += self.size[0]/x_lines_num

        z_lines_num = int(self.size[2] * self.detail_level)
        z_lines = []

        z_pos_iterator = self.center[2] - self.size[2]/2
        for i in range(z_lines_num):
            z_lines.append(z_pos_iterator)
            z_pos_iterator += self.size[2]/z_lines_num

        # create terrain vertices, x and z have set places, y (height) is random
        for a in range(len(z_lines)):
            for b in range(len(x_lines)):
                current_vertex = [x_lines[b],
                                  self.center[1] + random.uniform(-self.size[1], self.size[1]),
                                  z_lines[a]]
                self.vertices.append(current_vertex)

        self.x_lines_num = x_lines_num
        self.z_lines_num = z_lines_num

    def get_center(self):
        return self.center

    def get_closest_vertex_xz(self, xz):
        if self.vertices:
            result = None
            last_dist = None
            for vertex in self.vertices:
                if not result or ((xz[0] - vertex[0])**2 + (xz[1] - vertex[2])**2)**0.5 < last_dist:
                    result = vertex
                    last_dist = ((xz[0] - vertex[0])**2 + (xz[1] - vertex[2])**2)**0.5

            return result
        else:
            return -1
            
    def get_height_at_pos(self, xz):
        if not self.vertices:
            return -1
        else:
            closest_xz = self.get_closest_vertex_xz(xz)

            if abs(xz[0] - closest_xz[0]) > 2 * abs(xz[1] - closest_xz[2]):
                x_offset = sign(closest_xz[0] - xz[0])
                z_offset = 0
            elif 2 * abs(xz[0] - closest_xz[0]) < abs(xz[1] - closest_xz[2]):
                x_offset = 0
                z_offset = sign(closest_xz[2] - xz[1])
            else:
                x_offset = sign(closest_xz[0] - xz[0])
                z_offset = sign(closest_xz[2] - xz[1])

            # hold tight, some terrible interpolation is about to happen!
            closest_index = self.vertices.index(closest_xz)
            second_closest_xz = self.vertices[closest_index + x_offset + z_offset * self.x_lines_num]

            y_closest = closest_xz[1]
            y_second_closest = second_closest_xz[1]

            dist_to_closest = ((closest_xz[0] - xz[0])**2 + (closest_xz[2] - xz[1])**2)**0.5

            total_dist = ((closest_xz[0] - second_closest_xz[0])**2 + (closest_xz[2] - second_closest_xz[1])**2)**0.5
            interpolated_y = y_closest + dist_to_closest * (y_second_closest - y_closest)/total_dist

            return interpolated_y

    def estimate_height_at_pos(self, xz):
        # basically a faster version of getting height, without interpolation
        if not self.vertices:
            return -1
        else:
            closest_xz = self.get_closest_vertex_xz(xz)
            return closest_xz[1]
