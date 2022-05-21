import random
import time

from math_utils import *

class terrain():
    def __init__(self, center, size, detail_level):
        self.center = center
        self.size = size
        self.detail_level = detail_level
        self.vertices = []

    def generate(self):
        def clamp(val, mnm, mxm):
            return min(max(val, mnm),mxm)

        print("Generating terrain...")
        
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

        for z in range(z_lines_num):
            for x in range(x_lines_num):
                # x + z*size[0]
                if x == 0:
                    last_y = self.center[1]

                if x+z == 0:
                    current_y = self.center[1] + random.uniform(-25, 25)
                    
                current_y = last_y + random.uniform(-25, 25)

                if z > 0:
                    while abs(current_y - self.vertices[x + (z-1)*x_lines_num][1]) > 25:
                        current_y = last_y + random.uniform(-25, 25)
                
                current_y = clamp(current_y, self.center[1] - self.size[1], self.center[1] + self.size[1])
                self.vertices.append([x_lines[x], current_y, z_lines[z]])

        self.x_lines_num = x_lines_num
        self.z_lines_num = z_lines_num

        print("Generating craters...")
        # crater generation
        num_of_craters = int(((self.size[0] * self.size[2])**0.5) / 300)

        for c in range(num_of_craters):
            cx = random.choice(x_lines)
            cz = random.choice(z_lines)
            c_width = random.uniform(150, 600)
            c_height = random.uniform(100, 250)

            for vertex in self.vertices:
                if (vertex[0] - cx)**2 + (vertex[2] - cz)**2 < c_width**2:
                    # vertex[1] = vertex[1] - abs((((vertex[0] - cx)**2 + (vertex[2] - cz)**2)**0.5 /c_width) * c_height)
                    vertex[1] = -c_height + random.uniform(-c_height/25, c_height/25)
                elif c_width**2 < (vertex[0] - cx)**2 + (vertex[2] - cz)**2 < c_width**2 * 1.3:
                    vertex[1] = vertex[1] + abs((((vertex[0] - cx)**2 + (vertex[2] - cz)**2)**0.5 /c_width) * c_height/5)

    def get_center(self):
        return self.center

    def get_closest_vertex_xz(self, xz):
        if self.vertices:

            z_lines_num = self.z_lines_num
            x_lines_num = self.x_lines_num

            x_spacing = abs(self.vertices[1][0] - self.vertices[0][0])
            z_spacing = abs(self.vertices[0][2] - self.vertices[x_lines_num + 1][2])

            rel_x = xz[0] - self.center[0]
            rel_z = xz[1] - self.center[2]

            z_ind = int(z_lines_num/2 + rel_z / z_spacing)
            x_ind = int(x_lines_num/2 + rel_x / x_spacing)

            index = z_ind * x_lines_num + x_ind

            return self.vertices[index]
            
##            result = None
##            last_dist = None
##            for vertex in self.vertices:
##                if not result or ((xz[0] - vertex[0])**2 + (xz[1] - vertex[2])**2)**0.5 < last_dist:
##                    result = vertex
##                    last_dist = ((xz[0] - vertex[0])**2 + (xz[1] - vertex[2])**2)**0.5
##
##            return result
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

            # for the edge case where we are at the edge of the terrain
            try:
                second_closest_xz = self.vertices[closest_index + x_offset + z_offset * self.x_lines_num]
            except:
                return closest_xz[1]

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
