import math
import numpy
from pyquaternion import Quaternion

lunar_gravity = 1.625 # m/s^2

def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

def vector_scale(vect, scalar):
    return [vect[0] * scalar, vect[1] * scalar, vect[2] * scalar]

def vector_add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]

def vector_mag(vect):
    return (vect[0]**2 + vect[1]**2 + vect[2]**2)**0.5

def vector_negative(vect):
    return [-sign(vect[0]) * vect[0],
            -sign(vect[1]) * vect[1],
            -sign(vect[2]) * vect[2]]

# rotate an orientation matrix
def rotate_matrix(orientation_matrix, rotation, base_object=None):
    # orientation matrix is a 3x3 matrix, rotation is a list of three angles in degrees
    orientation_matrix = numpy.array(orientation_matrix)

    if not base_object:
            
        if rotation[0]:
            rotator = Quaternion(axis=orientation_matrix[0], angle=math.radians(rotation[0]))
            orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

        if rotation[1]:
            rotator = Quaternion(axis=orientation_matrix[1], angle=math.radians(rotation[1]))
            orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

        if rotation[2]:
            rotator = Quaternion(axis=orientation_matrix[2], angle=math.radians(rotation[2]))
            orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

    else:

        if rotation[0]:
            rotator = Quaternion(axis=base_object.get_orient()[0], angle=math.radians(rotation[0]))
            orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

        if rotation[1]:
            rotator = Quaternion(axis=base_object.get_orient()[1], angle=math.radians(rotation[1]))
            orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

        if rotation[2]:
            rotator = Quaternion(axis=base_object.get_orient()[2], angle=math.radians(rotation[2]))
            orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

    return orientation_matrix.tolist()

