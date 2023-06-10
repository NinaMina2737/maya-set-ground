#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math
from vector import Vector3

class Matrix:
    def __init__(self, rows=None, cols=None, data=None):
        if not rows is None and not cols is None:
            if not isinstance(rows, int) or not isinstance(cols, int):
                raise ValueError("Matrix.__init__ takes two integers as rows and columns")
            if rows < 1 or cols < 1:
                raise ValueError("Matrix.__init__ takes two positive integers as rows and columns")
            if not data is None:
                raise ValueError("Matrix.__init__ takes either rows and columns or data")
            self.rows = rows
            self.cols = cols
            self.data = [[0 for j in range(cols)] for i in range(rows)]
        if not data is None:
            if not isinstance(data, list):
                raise ValueError("Matrix.__init__ takes a list of lists")
            if any(not isinstance(row, list) for row in data):
                raise ValueError("Matrix.__init__ takes a list of lists")
            if any(not isinstance(item, (int, float)) for row in data for item in row):
                raise ValueError("Matrix.__init__ takes a list of lists of numbers")
            if any(len(row) != len(data[0]) for row in data):
                raise ValueError("Matrix.__init__ takes a list of lists of the same length")
            if not rows is None or not cols is None:
                raise ValueError("Matrix.__init__ takes either rows and columns or data")
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
        if isinstance(other, Matrix):
            if not self.cols == other.rows:
                raise ValueError("Matrix.__mul__ takes a matrix with the same number of rows as the number of columns of this matrix")
            return Matrix([[sum([self.data[i][k] * other.data[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector3):
            matrix = [
                other.data[0],
                other.data[1],
                other.data[2]
            ]
            if self.rows == 4:
                matrix.append(1)
            elif self.rows != 3:
                raise ValueError("Matrix.__mul__ takes a 3x3 or 4x4 matrix")
            elements = [sum([matrix[j] * self.data[i][j] for j in range(self.cols)]) for i in range(self.rows)]
            if self.rows == 4:
                elements = elements[:3]
            return Vector3(elements)
        else:
            return Matrix([[self.data[i][j] * other for j in range(self.cols)] for i in range(self.rows)])

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            if not self.rows == other.cols:
                raise ValueError("Matrix.__rmul__ takes a matrix with the same number of columns as the number of rows of this matrix")
            return Matrix([[sum([other.data[i][k] * self.data[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector3):
            data = [
                other.data[0],
                other.data[1],
                other.data[2]
            ]
            if self.rows == 4:
                data.append(1)
            elif self.rows != 3:
                raise ValueError("Matrix.__rmul__ takes a 3x3 or 4x4 matrix")
            elements = [sum([data[j] * self.data[i][j] for j in range(self.cols)]) for i in range(self.rows)]
            if self.rows == 4:
                elements = elements[:3]
            return Vector3(elements)
        else:
            return Matrix([[other * self.data[i][j] for j in range(self.cols)] for i in range(self.rows)])
