#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as cmds
import math
import traceback
import vector
reload(vector)
from vector import Vector3
import matrix
reload(matrix)
from matrix import Matrix
import quaternion
reload(quaternion)
from quaternion import Quaternion

DIFFERENCE_THRESHOLD = 1e-6

def get_normal():
    # get selected components
    selection = cmds.ls(selection=True, flatten=True)
    # check if the selection is one or three components
    if len(selection) != 1 and len(selection) != 3:
        cmds.warning('Please select one or three components')
        return

    face = None
    vertices = None
    if len(selection) == 1:
        if not ".f" in selection[0]:
            cmds.warning('Please select face')
            return
        face = selection[0]
    elif len(selection) == 3:
        if not all([".vtx" in s for s in selection]):
            cmds.warning('Please select vertices')
            return
        vertices = selection

    normal = None
    if not vertices is None:
        if not face is None:
            cmds.warning("Please specify vertices or face")
            return
        if not all([".vtx" in s for s in vertices]):
            cmds.warning("Please specify vertices")
            return
        if len(vertices) != 3:
            cmds.warning("Please specify three vertices")
            return
        # get each vertex positions
        vertex_positions_list = [cmds.pointPosition(vertex, world=True) for vertex in vertices]
        # get each vector from the first vertex
        vectors = [Vector3(elements=vertex_positions_list[i]) - Vector3(elements=vertex_positions_list[0]) for i in range(1, len(vertex_positions_list))]
        # get cross product vector of the vectors
        normal = vectors[0].cross(vectors[1])
    if not face is None:
        if not vertices is None:
            cmds.warning("Please specify vertices or face")
            return
        if not ".f" in face:
            cmds.warning("Please specify face")
            return
        face_normal = cmds.polyInfo(face, faceNormals=True)[0].split(":")[1].split()
        face_normal = Vector3(elements=(float(face_normal[0]), float(face_normal[1]), float(face_normal[2])))
        # make sure the face normal is freezed
        face_object = face.split(".")[0]
        rotate_x = cmds.getAttr(face_object + ".rotateX") / 180 * math.pi
        rotate_y = cmds.getAttr(face_object + ".rotateY") / 180 * math.pi
        rotate_z = cmds.getAttr(face_object + ".rotateZ") / 180 * math.pi
        euler_angles = Vector3(elements=(rotate_x, rotate_y, rotate_z))
        rotate_matrix = matrix.euler_to_rotate_matrix(euler_angles)
        print("rotate_matrix", rotate_matrix)
        face_normal = rotate_matrix * face_normal
        print("face_normal", face_normal)
        normal = face_normal
        vertices = cmds.polyListComponentConversion(face, toVertex=True)
    # normalize the normal
    normal = normal.normalize()

    # get each vertex normals
    vertex_normals_list = [cmds.polyNormalPerVertex(vertex, query=True, xyz=True) for vertex in vertices]
    # make each vertex normal to vector
    vertex_normal_vectors_list = [[Vector3(elements=(vertex_normals[i], vertex_normals[i+1], vertex_normals[i+2])) for i in range(0, len(vertex_normals), 3)] for vertex_normals in vertex_normals_list]
    # get averages of each vertex normal vectors
    vertex_normal_average_vectors = []
    for vertex_normal_vectors in vertex_normal_vectors_list:
        average_vector = Vector3(elements=(0, 0, 0))
        for vertex_normal_vector in vertex_normal_vectors:
            average_vector += vertex_normal_vector
        average_vector /= len(vertex_normal_vectors)
        vertex_normal_average_vectors.append(average_vector)
    # get average of the vertex normal average vectors
    vertex_normal_average_vector = Vector3(elements=(0, 0, 0))
    for average_vector in vertex_normal_average_vectors:
        vertex_normal_average_vector += average_vector
    vertex_normal_average_vector /= len(vertex_normal_average_vectors)
    # make the average vector to unit vector
    vertex_normal_average_vector = vertex_normal_average_vector.normalize()

    # check if the normal is same direction as the average vector of the vertex normals
    dot_product = normal.dot(vertex_normal_average_vector)
    print("before_normal", normal)
    if abs(dot_product) < DIFFERENCE_THRESHOLD:
        dot_product = 0
    if dot_product < 0:
        normal *= -1
    print("after_normal", normal)
    return normal

def set_ground(source_normal=None, target_normal=None):
    source_normal = Vector3(elements=source_normal)
    target_normal = Vector3(elements=target_normal)
    source_normal = source_normal.normalize()
    target_normal = target_normal.normalize()
    print("source_normal", source_normal)
    print("target_normal", target_normal)
    rotate_axis = source_normal.cross(target_normal).normalize()
    print("rotate_axis", rotate_axis)
    dot_product = source_normal.dot(target_normal)
    print("dot_product", dot_product)
    cosine_rotate_angle = dot_product / (source_normal.length() * target_normal.length())
    print("cosine_rotate_angle", cosine_rotate_angle)
    rotate_angle = math.acos(cosine_rotate_angle)
    print("rotate_angle", rotate_angle)
    rotate_quaternion = quaternion.axis_angle_to_rotate_quaternion(rotate_axis, rotate_angle)
    print("rotate_quaternion", rotate_quaternion)
    rotate_matrix = rotate_quaternion.to_rotate_matrix4x4()
    print("rotate_matrix", rotate_matrix)
    object_shape = cmds.ls(selection=True, objectsOnly=True)[0]
    print("object_shape", object_shape)
    object = cmds.listRelatives(object_shape, parent=True)[0]
    print("object", object)
    cmds.xform(object, relative=True, matrix=rotate_matrix.flatten())
