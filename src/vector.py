#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math

DIFFERENCE_THRESHOLD = 1e-6

class Vector3:
    def __init__(self, elements=None):
        if not elements is None:
            if not all([isinstance(element, (int, float)) for element in elements]):
                raise ValueError("Vector.__init__ takes only integers or floats")
            if not len(elements) == 3:
                raise ValueError("Vector.__init__ takes 3 elements")
        else:
            elements = [0, 0, 0]
        self.elements = list(elements)
        self.x = self.elements[0]
        self.y = self.elements[1]
        self.z = self.elements[2]

    def __str__(self):
        return "Vector(%f, %f, %f)" % (self.elements[0], self.elements[1], self.elements[2])

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __add__(self, other):
        vector = Vector3([self.elements[i] + other.elements[i] for i in range(3)])
        vector.make_zero()
        return vector

    def __sub__(self, other):
        vector = Vector3([self.elements[i] - other.elements[i] for i in range(3)])
        vector.make_zero()
        return vector

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError("Vector.__mul__ takes a scalar")
        vector = Vector3([self.elements[i] * other for i in range(3)])
        vector.make_zero()
        return vector

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError("Vector.__div__ takes a scalar")
        vector = Vector3([self.elements[i] / other for i in range(3)])
        vector.make_zero()
        return vector

    def __abs__(self):
        return math.sqrt(self.elements[0] * self.elements[0] + self.elements[1] * self.elements[1] + self.elements[2] * self.elements[2])

    def make_zero(self):
        self.elements = [0 if abs(element) < DIFFERENCE_THRESHOLD else element for element in self.elements]
        self.x = self.elements[0]
        self.y = self.elements[1]
        self.z = self.elements[2]

    def normalize(self):
        vector = self / abs(self)
        vector.make_zero()
        return vector

    def dot(self, other):
        return sum([self.elements[i] * other.elements[i] for i in range(3)])

    def cross(self, other):
        vector = Vector3((self.elements[1] * other.elements[2] - self.elements[2] * other.elements[1],
                      self.elements[2] * other.elements[0] - self.elements[0] * other.elements[2],
                      self.elements[0] * other.elements[1] - self.elements[1] * other.elements[0]))
        vector.make_zero()
        return vector

    def norm(self):
        return abs(self)

    def length(self):
        return abs(self)
