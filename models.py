# -*- coding: utf-8 -*-

import numpy as np


class Box():
    def __init__(self):
        self.POINTS = (
            np.array([100, 100, 100, 1]),
            np.array([400, 100, 100, 1]),
            np.array([400, 100, 400, 1]),
            np.array([100, 100, 400, 1]),
            np.array([100, 400, 100, 1]),
            np.array([400, 400, 100, 1]),
            np.array([400, 400, 400, 1]),
            np.array([100, 400, 400, 1])
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
