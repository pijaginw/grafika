# -*- coding: utf-8 -*-

import numpy as np


class Box():
    def __init__(self, x, y, z, a, h, subdivision):
        self.POINTS = [
            np.array([x-a/2, y, z-a/2, 1]),  # 0
            np.array([x+a/2, y, z-a/2, 1]),  # 1
            np.array([x+a/2, y, z+a/2, 1]),  # 2
            np.array([x-a/2, y, z+a/2, 1]),  # 3
            np.array([x-a/2, y+h, z-a/2, 1]),  # 4
            np.array([x+a/2, y+h, z-a/2, 1]),  # 5
            np.array([x+a/2, y+h, z+a/2, 1]),  # 6
            np.array([x-a/2, y+h, z+a/2, 1])  # 7
        ]

        self.TRIANGLES = [
            (0, 1, 5),
            (0, 4, 5),
            (0, 1, 3),
            (0, 3, 4),
            (1, 2, 6),
            (1, 5, 6),
            (1, 2, 3),
            (2, 6, 7),
            (2, 3, 7),
            (3, 4, 7),
            (4, 5, 6),
            (4, 6, 7)
        ]

        for i in range(subdivision):
            subdivide(self)

def subdivide(model):
    triangles = []
    for triangle in model.TRIANGLES:
        model.POINTS.append((model.POINTS[triangle[0]] + model.POINTS[triangle[1]]) / 2)
        model.POINTS.append((model.POINTS[triangle[1]] + model.POINTS[triangle[2]]) / 2)
        model.POINTS.append((model.POINTS[triangle[2]] + model.POINTS[triangle[0]]) / 2)
        p0_i = len(model.POINTS) - 3
        p1_i = p0_i + 1
        p2_i = p1_i + 1
        triangles.append((p0_i, p1_i, p2_i))
        triangles.append((triangle[0], p0_i, p2_i))
        triangles.append((triangle[1], p0_i, p1_i))
        triangles.append((triangle[2], p1_i, p2_i))
    model.TRIANGLES = triangles


class Rectangle():
    def __init__(self, x, z, a, b, subdivision):
        self.POINTS = [
            np.array([x-a/2, 0, z, 1]),
            np.array([x-a/2, 0, z+b, 1]),
            np.array([x+a/2, 0, z+b, 1]),
            np.array([x+a/2, 0, z, 1])
        ]

        self.TRIANGLES = [
            (0, 1, 2),
            (0, 2, 3)
        ]
        
        for i in range(subdivision):
            subdivide(self)
