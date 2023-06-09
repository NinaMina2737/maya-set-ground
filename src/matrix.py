#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math
from .vector import Vector

class Matrix:
    def __init__(self, rows=4, cols=4, data=None, translation=None, rotation=None, scale=None):
        if data is None:
            self.rows = rows
            self.cols = cols
            self.data = [[0 for j in range(cols)] for i in range(rows)]
        else:
            if not isinstance(data, list):
                raise ValueError("Matrix.__init__ takes a list of lists")
            if any(not isinstance(row, list) for row in data):
                raise ValueError("Matrix.__init__ takes a list of lists")
            if any(not isinstance(item, (int, float)) for row in data for item in row):
                raise ValueError("Matrix.__init__ takes a list of lists of numbers")
            self.rows = len(data)
            self.cols = len(data[0])
            self.data = data

    def __str__(self):
        return '\n'.join([' '.join([str(self.data[i][j]) for j in range(self.cols)]) for i in range(self.rows)])

    def __iter__(self):
        return iter(self.data)

    def __add__(self, other):
        return Matrix([[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __sub__(self, other):
        return Matrix([[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __mul__(self, other):
        if not self.cols == other.rows:
            raise ValueError("Matrix.__mul__ takes a matrix with the same number of rows as the number of columns of this matrix")
        if isinstance(other, Matrix):
            return Matrix([[sum([self.data[i][k] * other.data[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector):
            return Vector([sum([self.data[i][j] * other.data[j] for j in range(self.cols)]) for i in range(self.rows)])
        else:
            return Matrix([[self.data[i][j] * other for j in range(self.cols)] for i in range(self.rows)])

    def __rmul__(self, other):
        if not self.rows == other.cols:
            raise ValueError("Matrix.__rmul__ takes a matrix with the same number of columns as the number of rows of this matrix")
        if isinstance(other, Matrix):
            return Matrix([[sum([other.data[i][k] * self.data[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector):
            return Vector([sum([other.data[j] * self.data[i][j] for j in range(self.cols)]) for i in range(self.rows)])
        else:
            return Matrix([[other * self.data[i][j] for j in range(self.cols)] for i in range(self.rows)])
