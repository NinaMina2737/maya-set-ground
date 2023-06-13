#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import math
from vector import Vector3

DIFFERENCE_THRESHOLD = 1e-6

class Matrix:
    def __init__(self, rows=None, cols=None, elements=None):
        if rows is None and cols is None and elements is None:
            raise ValueError("Matrix.__init__ takes either rows and columns or elements")
        if not rows is None and not cols is None:
            if not isinstance(rows, int) or not isinstance(cols, int):
                raise ValueError("Matrix.__init__ takes two integers as rows and columns")
            if rows < 1 or cols < 1:
                raise ValueError("Matrix.__init__ takes two positive integers as rows and columns")
            if not elements is None:
                raise ValueError("Matrix.__init__ takes either rows and columns or elements")
            self.rows = rows
            self.cols = cols
            self.elements = [[0 for j in range(cols)] for i in range(rows)]
        if not elements is None:
            if not isinstance(elements, list):
                raise ValueError("Matrix.__init__ takes a list of lists")
            if any(not isinstance(row, list) for row in elements):
                raise ValueError("Matrix.__init__ takes a list of lists")
            if any(not isinstance(item, (int, float)) for row in elements for item in row):
                raise ValueError("Matrix.__init__ takes a list of lists of numbers")
            if any(len(row) != len(elements[0]) for row in elements):
                raise ValueError("Matrix.__init__ takes a list of lists of the same length")
            if not rows is None or not cols is None:
                raise ValueError("Matrix.__init__ takes either rows and columns or elements")
            self.rows = len(elements)
            self.cols = len(elements[0])
            self.elements = elements

    def __str__(self):
        return '\n'.join([' '.join([str(self.elements[i][j]) for j in range(self.cols)]) for i in range(self.rows)])

    def __iter__(self):
        return iter(self.elements)

    def __add__(self, other):
        return Matrix(elements=[[self.elements[i][j] + other.elements[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __sub__(self, other):
        return Matrix(elements=[[self.elements[i][j] - other.elements[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if not self.cols == other.rows:
                raise ValueError("Matrix.__mul__ takes a matrix with the same number of rows as the number of columns of this matrix")
            return Matrix(elements=[[sum([self.elements[i][k] * other.elements[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector3):
            matrix = [
                other.elements[0],
                other.elements[1],
                other.elements[2]
            ]
            if self.rows == 4:
                matrix.append(1)
            elif self.rows != 3:
                raise ValueError("Matrix.__mul__ takes a 3x3 or 4x4 matrix")
            elements = [sum([matrix[j] * self.elements[i][j] for j in range(self.cols)]) for i in range(self.rows)]
            if self.rows == 4:
                elements = elements[:3]
            return Vector3(elements=elements)
        else:
            return Matrix(elements=[[self.elements[i][j] * other for j in range(self.cols)] for i in range(self.rows)])

    def __rmul__(self, other):
        if isinstance(other, Matrix):
            if not self.rows == other.cols:
                raise ValueError("Matrix.__rmul__ takes a matrix with the same number of columns as the number of rows of this matrix")
            return Matrix(elements=[[sum([other.elements[i][k] * self.elements[k][j] for k in range(self.cols)]) for j in range(other.cols)] for i in range(self.rows)])
        elif isinstance(other, Vector3):
            elements = [
                other.elements[0],
                other.elements[1],
                other.elements[2]
            ]
            if self.rows == 4:
                elements.append(1)
            elif self.rows != 3:
                raise ValueError("Matrix.__rmul__ takes a 3x3 or 4x4 matrix")
            elements = [sum([elements[j] * self.elements[i][j] for j in range(self.cols)]) for i in range(self.rows)]
            if self.rows == 4:
                elements = elements[:3]
            return Vector3(elements=elements)
        else:
            return Matrix(elements=[[other * self.elements[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def flatten(self):
        return [item for row in self.elements for item in row]

def euler_to_rotate_matrix(angles, rotate_order="xyz"):
    if not isinstance(angles, Vector3):
        raise ValueError("euler_to_rotate_matrix takes a Vector3 as angles")
    if not isinstance(rotate_order, (str, unicode)):
        raise ValueError("euler_to_rotate_matrix takes a string as rotate_order")
    if not rotate_order in ["xyz", "xzy", "yxz", "yzx", "zxy", "zyx"]:
        raise ValueError("euler_to_rotate_matrix takes a string in ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'] as rotate_order")
    matrix_x = Matrix(elements=[
        [1, 0, 0],
        [0, math.cos(angles.elements[0]), -math.sin(angles.elements[0])],
        [0, math.sin(angles.elements[0]), math.cos(angles.elements[0])]
        ])
    matrix_y = Matrix(elements=[
        [math.cos(angles.elements[1]), 0, math.sin(angles.elements[1])],
        [0, 1, 0],
        [-math.sin(angles.elements[1]), 0, math.cos(angles.elements[1])]
        ])
    matrix_z = Matrix(elements=[
        [math.cos(angles.elements[2]), -math.sin(angles.elements[2]), 0],
        [math.sin(angles.elements[2]), math.cos(angles.elements[2]), 0],
        [0, 0, 1]
        ])
    rotate_order_map = {"x": matrix_x, "y": matrix_y, "z": matrix_z}
    rotate_matrix = rotate_order_map[rotate_order[1]] * rotate_order_map[rotate_order[0]]
    rotate_matrix = rotate_order_map[rotate_order[2]] * rotate_matrix
    return rotate_matrix
