# -*- coding: utf-8 -*-

import numpy as np
from time import sleep
import pygame
from pygame.locals import *
import math

class Box():
    def __init__(self):
        self.POINTS = (
            np.array([200, 100, 200, 1]),
            np.array([200, 100, 200, 1]),
            np.array([300, 100, 100, 1]),
            np.array([200, 100, 100, 1]),
            np.array([200, 200, 200, 1]),
            np.array([300, 200, 200, 1]),
            np.array([300, 200, 100, 1]),
            np.array([200, 200, 100, 1])
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

def perspective_projection(fov, zNear, zFar, w, h):
    ar = w / h
    fov = np.radians(fov)
    yscale = 1 / math.tan(fov / 2)
    xscale = yscale / ar
    a = zFar / (zFar - zNear)
    b = - zNear * zFar / (zFar - zNear)
    m = np.array([
        [xscale,      0,  0,  0],
        [0,      yscale,  0,  0],
        [0,           0,  a,  1],
        [0,           0,  b,  0]
    ])
    return m

def rotation_x(angle):
    angle = math.radians(angle)
    m = np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), -math.sin(angle), 0],
        [0, math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return m

def rotation_y(angle):
    angle = math.radians(angle)
    m = np.array([
        [math.cos(angle), 0, math.sin(angle), 0],
        [0, 1, 0, 0],
        [-math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    return m

def rotation_z(angle):
    angle = math.radians(angle)
    m = np.array([
        [math.cos(angle), -math.sin(angle), 0, 0],
        [math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return m

def scale(p, v):
    m = np.array([
        [v[0],    0,    0,    0],
        [0,    v[1],    0,    0],
        [0,       0, v[2],    0],
        [0,       0,    0,    1]
    ])
    return m

def viewport(x, y, n, f, w, h):
    m = np.array([
        [w/2, 0, 0, 0],
        [0, -h/2, 0, 0],
        [0, 0, f-n, 0],
        [x + w/2, h/2 + y, n, 1]
    ])
    return m

def main():
    width = 900
    height = 700

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    box = Box()

    while True:
        vp = viewport(0, 0, 0.1, 100, width, height)
        projection = perspective_projection(160, 0.1, 100, width, height)
        mat = projection.dot(vp)
        for edge in box.EDGES:
            # przekształcenia
            p0 = box.POINTS[edge[0]].dot(mat)
            p1 = box.POINTS[edge[1]].dot(mat)
            # normalizacja
            p0 = p0 / p0[3]
            p1 = p1 / p1[3]
            # rysowanie
            pygame.draw.line(screen, 200, (p0[0], p0[1]), (p1[0], p1[1]))
            pygame.time.delay(25)
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        pygame.display.flip()
        pygame.time.delay(25)


if __name__ == "__main__":
    main()
