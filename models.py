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

class Line():
    def __init__(self):
        self.POINTS = (
            np.array([80, 80, 80, 1]),
            np.array([80, 80, 400, 1])
        )
