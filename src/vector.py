#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math

class Vector3:
    def __init__(self, elements=None):
        if not elements is None:
            if not all([isinstance(element, (int, float)) for element in elements]):
                raise ValueError("Vector.__init__ takes only integers or floats")
            if not len(elements) == 3:
                raise ValueError("Vector.__init__ takes 3 elements")
        else:
            elements = [0, 0, 0]
        self.data = list(elements)
        self.x = self.data[0]
        self.y = self.data[1]
        self.z = self.data[2]

    def __str__(self):
        return "Vector(%f, %f, %f)" % (self.data[0], self.data[1], self.data[2])

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        return Vector3([self.data[i] + other.data[i] for i in range(3)])

    def __sub__(self, other):
        return Vector3([self.data[i] - other.data[i] for i in range(3)])

    def __mul__(self, other):
        if len(other) != 1:
            raise ValueError("Vector.__mul__ takes a scalar")
        return Vector3([self.data[i] * other for i in range(3)])

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError("Vector.__div__ takes a scalar")
        return Vector3([self.data[i] / other for i in range(3)])

    def __abs__(self):
        return math.sqrt(self.data[0] * self.data[0] + self.data[1] * self.data[1] + self.data[2] * self.data[2])

    def normalize(self):
        return self / abs(self)

    def dot(self, other):
        return sum([self.data[i] * other.data[i] for i in range(3)])

    def cross(self, other):
        return Vector3((self.data[1] * other.data[2] - self.data[2] * other.data[1],
                      self.data[2] * other.data[0] - self.data[0] * other.data[2],
                      self.data[0] * other.data[1] - self.data[1] * other.data[0]))

    def norm(self):
        return abs(self)

    def length(self):
        return abs(self)
