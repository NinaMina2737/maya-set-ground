#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math
from vector import Vector3
from matrix import Matrix

class Quaternion:
    def __init__(self, parameters=None):
        if parameters:
            if len(parameters) != 4:
                raise ValueError("Quaternion.__init__ takes a 4-element list")
            if any(not isinstance(parameter, (float, int)) for parameter in parameters):
                raise ValueError("Quaternion.__init__ takes a 4-element list of float or int")
            self.x = parameters[0]
            self.y = parameters[1]
            self.z = parameters[2]
            self.w = parameters[3]
        else:
            raise ValueError("Quaternion.__init__ takes a 4-element list or an axis and an angle")

    def __str__(self):
        return "Quaternion(%f, %f, %f, %f)" % (self.x, self.y, self.z, self.w)

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.w))

    def __mul__(self, other):
        source = other
        target = self
        if isinstance(source, Quaternion):
            x = source.x * target.w - source.y * target.z + source.z * target.y + source.w * target.x
            y = source.x * target.z + source.y * target.w - source.z * target.x + source.w * target.y
            z = -source.x * target.y + source.y * target.x + source.z * target.w + source.w * target.z
            w = -source.x * target.x - source.y * target.y - source.z * target.z + source.w * target.w
            return Quaternion(parameters=[x, y, z, w])
        else:
            raise ValueError("Quaternion.__mul__ takes a Quaternion")

    def __rmul__(self, other):
        source = self
        target = other
        if isinstance(target, Quaternion):
            x = source.x * target.w - source.y * target.z + source.z * target.y + source.w * target.x
            y = source.x * target.z + source.y * target.w - source.z * target.x + source.w * target.y
            z = -source.x * target.y + source.y * target.x + source.z * target.w + source.w * target.z
            w = -source.x * target.x - source.y * target.y - source.z * target.z + source.w * target.w
            return Quaternion(parameters=[x, y, z, w])
        else:
            raise ValueError("Quaternion.__rmul__ takes a Quaternion")

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def inverse(self):
        return Quaternion(parameters=[-self.x, -self.y, -self.z, self.w])

    def normalize(self):
        return Quaternion(parameters=[self.x / abs(self), self.y / abs(self), self.z / abs(self), self.w / abs(self)])

    def to_rotate_matrix4x4(self):
        quaternion = self
        if abs(quaternion) != 1:
            quaternion = quaternion.normalize()
        x = quaternion.x
        y = quaternion.y
        z = quaternion.z
        w = quaternion.w

        m00 = 1 - 2 * (y * y + z * z)
        m01 = 2 * (x * y + w * z)
        m02 = 2 * (x * z - w * y)
        m03 = 0.0

        m10 = 2 * (x * y - w * z)
        m11 = 1 - 2 * (x * x + z * z)
        m12 = 2 * (y * z + w * x)
        m13 = 0.0

        m20 = 2 * (x * z + w * y)
        m21 = 2 * (y * z - w * x)
        m22 = 1 - 2 * (x * x + y * y)
        m23 = 0.0

        m30 = 0.0
        m31 = 0.0
        m32 = 0.0
        m33 = 1.0

        elements = [
            [m00, m01, m02, m03],
            [m10, m11, m12, m13],
            [m20, m21, m22, m23],
            [m30, m31, m32, m33]
            ]
        return Matrix(elements=elements)

def axis_angle_to_rotate_quaternion(axis, angle):
    if not isinstance(axis, Vector3):
        raise ValueError("Quaternion.__init__ takes a Vector as axis")
    if not isinstance(angle, (int, float)):
        raise ValueError("Quaternion.__init__ takes a float or an int as angle")
    axis = axis.normalize()
    x = axis.x * math.sin(angle * 0.5)
    y = axis.y * math.sin(angle * 0.5)
    z = axis.z * math.sin(angle * 0.5)
    w = math.cos(angle * 0.5)
    return Quaternion(parameters=[x, y, z, w]).normalize()

def euler_to_rotate_quaternion(euler, order="xyz"):
    quaternion_x = Quaternion(parameters=[math.sin(euler.x * 0.5), 0, 0, math.cos(euler.x * 0.5)]).normalize()
    quaternion_y = Quaternion(parameters=[0, math.sin(euler.y * 0.5), 0, math.cos(euler.y * 0.5)]).normalize()
    quaternion_z = Quaternion(parameters=[0, 0, math.sin(euler.z * 0.5), math.cos(euler.z * 0.5)]).normalize()
    order_map = {"x": quaternion_x, "y": quaternion_y, "z": quaternion_z}
    quaternion = order_map[order[1]] * order_map[order[0]]
    quaternion = order_map[order[2]] * quaternion
    return quaternion.normalize()
