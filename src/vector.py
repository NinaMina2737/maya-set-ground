#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math

class Vector:
    def __init__(self, *args):
        if not all([isinstance(arg, (int, float)) for arg in args]):
            raise ValueError("Vector.__init__ takes only integers or floats")
        if not len(args) == 3:
            raise ValueError("Vector.__init__ takes 3 arguments")
        self.data = list(args)

    def __str__(self):
        return "Vector(%f, %f, %f)" % (self.data[0], self.data[1], self.data[2])

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        return Vector([self.data[i] + other.data[i] for i in range(3)])

    def __sub__(self, other):
        return Vector([self.data[i] - other.data[i] for i in range(3)])

    def __mul__(self, other):
        if len(other) != 1:
            raise ValueError("Vector.__mul__ takes a scalar")
        return Vector([self.data[i] * other for i in range(3)])

    def __div__(self, other):
        if len(other) != 1:
            raise ValueError("Vector.__div__ takes a scalar")
        return Vector([self.data[i] / other for i in range(3)])

    def __abs__(self):
        return math.sqrt(self.data[0] * self.data[0] + self.data[1] * self.data[1] + self.data[2] * self.data[2])

    def normalize(self):
        return self / abs(self)

    def dot(self, other):
        return sum([self.data[i] * other.data[i] for i in range(3)])

    def cross(self, other):
        return Vector(self.data[1] * other.data[2] - self.data[2] * other.data[1],
                      self.data[2] * other.data[0] - self.data[0] * other.data[2],
                      self.data[0] * other.data[1] - self.data[1] * other.data[0])

    def norm(self):
        return abs(self)

    def length(self):
        return abs(self)
