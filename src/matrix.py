#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math
from .vector import Vector

class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = [[0 for j in range(cols)] for i in range(rows)]

    def __init__(self, m00, m01, m02, m03,
                       m10, m11, m12, m13,
                       m20, m21, m22, m23,
                       m30, m31, m32, m33):
        self.rows = 4
        self.cols = 4
        self.data = [[m00, m01, m02, m03],
                     [m10, m11, m12, m13],
                     [m20, m21, m22, m23],
                     [m30, m31, m32, m33]]

    def __str__(self):
        return '\n'.join([' '.join([str(self.data[i][j]) for j in range(self.cols)]) for i in range(self.rows)])

    def __iter__(self):
        return iter(self.data)

    def __add__(self, other):
        return Matrix([[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __sub__(self, other):
        return Matrix([[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix([[sum([self.data[i][k] * other.data[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector):
            return Vector([sum([self.data[i][j] * other.data[j] for j in range(self.cols)]) for i in range(self.rows)])
        else:
            return Matrix([[self.data[i][j] * other for j in range(self.cols)] for i in range(self.rows)])
