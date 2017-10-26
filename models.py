# -*- coding: utf-8 -*-

import numpy as np


class Box():
    def __init__(self, x, y, z, a, h):
        self.POINTS = (
            np.array([x-a/2, y, z-a/2, 1]),
            np.array([x+a/2, y, z-a/2, 1]),
            np.array([x+a/2, y, z+a/2, 1]),
            np.array([x-a/2, y, z+a/2, 1]),
            np.array([x-a/2, y+h, z-a/2, 1]),
            np.array([x+a/2, y+h, z-a/2, 1]),
            np.array([x+a/2, y+h, z+a/2, 1]),
            np.array([x-a/2, y+h, z+a/2, 1])
        )

        self.EDGES = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (4, 5),
            (5, 1),
            (5, 6),
            (6, 7),
            (7, 4),
            (6, 2),
            (7, 3)
        ]

        # indexes of edges in self.EDGES
        self.FACES = [
            [0, 1, 2, 3],
            [1, 6, 7, 10],
            [5, 7, 8, 9],
            [4, 9, 11, 3],
            [4, 5, 6, 0],
            [2, 10, 8, 11]

        ]

class Rectangle():
    def __init__(self, x, z, a, b):
        self.POINTS = (
            np.array([x-a/2, 0, z, 1]),
            np.array([x-a/2, 0, z+b, 1]),
            np.array([x+a/2, 0, z+b, 1]),
            np.array([x+a/2, 0, z, 1])
        )

        self.EDGES = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0)
        ]

        self.FACES = [
            [0, 1, 2, 3]
        ]
