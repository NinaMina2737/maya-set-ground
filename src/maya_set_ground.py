#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as cmds
import math
import traceback
from vector import Vector

def get_normal(face=None, vertices=None):
    if face is None and vertices is None:
        return None
    if face is not None:
        if vertices is not None:
            cmds.warning('Both face and vertices are given, use face only or vertices only')
        # get vertices of the face
        vertices = cmds.polyListComponentConversion(face, toVertex=True)
        # flatten the list
        vertices = cmds.ls(vertices, flatten=True)
    elif vertices is not None:
        if face is not None:
            cmds.warning('Both face and vertices are given, use face only or vertices only')
    # get each vertex normals
    vertex_normals_list = [cmds.polyNormalPerVertex(vertex, query=True, xyz=True) for vertex in vertices]
    # print(vertex_normals_list)
    # make each vertex normal to vector
    for vertex_normals in vertex_normals_list:
        for i in range(0, len(vertex_normals), 3):
            print(type(vertex_normals[i]))
    vertex_normal_vectors_list = [[Vector(vertex_normals[i], vertex_normals[i+1], vertex_normals[i+2]) for i in range(0, len(vertex_normals), 3)] for vertex_normals in vertex_normals_list]
    # get averages of each vertex normal vectors
    vertex_normal_vector_averages = []
    for vertex_normal_vectors in vertex_normal_vectors_list:
        average_vector = Vector(0, 0, 0)
        for vertex_normal_vector in vertex_normal_vectors:
            average_vector += vertex_normal_vector
        average_vector /= len(vertex_normal_vectors)
        vertex_normal_vector_averages.append(average_vector)
    # get average normal vector of the face
    normal = Vector(0, 0, 0)
    for vertex_normal_vector_average in vertex_normal_vector_averages:
        normal += vertex_normal_vector_average
    normal /= len(vertex_normal_vector_averages)
    return normal

def set_ground():
    face = cmds.ls(selection=True)
    normal = get_normal(face=face)
    print(normal)
