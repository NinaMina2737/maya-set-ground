#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math
from vector import Vector3
from matrix import Matrix

class Quaternion:
    def __init__(self, parameters=None, axis=None, angle=None, euler=None, rotate_order="xyz"):
        if parameters:
            if len(parameters) != 4:
                raise ValueError("Quaternion.__init__ takes a 4-element list")
            if any(not isinstance(parameter, float) and not isinstance(parameter, int) for parameter in parameters):
                raise ValueError("Quaternion.__init__ takes a 4-element list of float or int")
            self.x = parameters[0]
            self.y = parameters[1]
            self.z = parameters[2]
            self.w = parameters[3]
        elif axis and angle:
            if not isinstance(axis, Vector3):
                raise ValueError("Quaternion.__init__ takes a Vector as axis")
            if not isinstance(angle, float) or not isinstance(angle, int):
                raise ValueError("Quaternion.__init__ takes a float or an int as angle")
            axis = axis.normalize()
            self.x = axis.x * math.sin(angle / 2)
            self.y = axis.y * math.sin(angle / 2)
            self.z = axis.z * math.sin(angle / 2)
            self.w = math.cos(angle / 2)
        elif euler:
            if not isinstance(euler, Vector3):
                raise ValueError("Quaternion.__init__ takes a Vector as euler")
            if not isinstance(rotate_order, (str, unicode)):
                raise ValueError("Quaternion.__init__ takes a string as rotate_order")
            if not len(rotate_order) == 3:
                raise ValueError("Quaternion.__init__ takes a 3-character string as rotate_order")
            if not all(character in "xyz" for character in rotate_order):
                raise ValueError("Quaternion.__init__ takes a 3-character string as rotate_order")
            euler = euler / 2
            quaternion_x = Quaternion(parameters=[math.sin(euler.x), 0, 0, math.cos(euler.x)])
            quaternion_y = Quaternion(parameters=[0, math.sin(euler.y), 0, math.cos(euler.y)])
            quaternion_z = Quaternion(parameters=[0, 0, math.sin(euler.z), math.cos(euler.z)])
            axis_map = {"x": quaternion_x, "y": quaternion_y, "z": quaternion_z}
            quaternion = axis_map[rotate_order[0]] * axis_map[rotate_order[1]] * axis_map[rotate_order[2]]
            self.x = quaternion.x
            self.y = quaternion.y
            self.z = quaternion.z
            self.w = quaternion.w
        else:
            raise ValueError("Quaternion.__init__ takes a 4-element list or an axis and an angle")

    def __str__(self):
        return "Quaternion(%f, %f, %f, %f)" % (self.x, self.y, self.z, self.w)

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.w))

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z
            z = self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            return Quaternion(parameters=[x, y, z, w])
        else:
            raise ValueError("Quaternion.__mul__ takes a Quaternion")

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def inverse(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def to_rotate_matrix(self):
        m00 = 1 - 2 * self.y * self.y - 2 * self.z * self.z
        m01 = 2 * self.x * self.y - 2 * self.z * self.w
        m02 = 2 * self.x * self.z + 2 * self.y * self.w
        m03 = 0
        m10 = 2 * self.x * self.y + 2 * self.z * self.w
        m11 = 1 - 2 * self.x * self.x - 2 * self.z * self.z
        m12 = 2 * self.y * self.z - 2 * self.x * self.w
        m13 = 0
        m20 = 2 * self.x * self.z - 2 * self.y * self.w
        m21 = 2 * self.y * self.z + 2 * self.x * self.w
        m22 = 1 - 2 * self.x * self.x - 2 * self.y * self.y
        m23 = 0
        m30 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        data = [
            [m00, m01, m02, m03],
            [m10, m11, m12, m13],
            [m20, m21, m22, m23],
            [m30, m31, m32, m33]
            ]
        return Matrix(data=data)
