# -*- coding: utf-8 -*-

import numpy as np
from time import sleep
import pygame
from pygame.locals import *
import math
from models import Box

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

def rotation(angle_x, angle_y, angle_z):
    angle_x = math.radians(angle_x)
    m_x = np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle_x), -math.sin(angle_x), 0],
        [0, math.sin(angle_x), math.cos(angle_x), 0],
        [0, 0, 0, 1]
    ])

    angle_y = math.radians(angle_y)
    m_y = np.array([
        [math.cos(angle_y), 0, math.sin(angle_y), 0],
        [0, 1, 0, 0],
        [-math.sin(angle_y), 0, math.cos(angle_y), 0],
        [0, 0, 0, 1]
    ])

    angle_z = math.radians(angle_z)
    m_z = np.array([
        [math.cos(angle_z), -math.sin(angle_z), 0, 0],
        [math.sin(angle_z), math.cos(angle_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    m_y = np.dot(m_x, m_y)
    return np.dot(m_y, m_z)

def scale(v):
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

def translation(v):
    m = np.array([
        [1, 0, 0, v[0]],
        [0, 1, 0, v[1]],
        [0, 0, 1, v[2]],
        [0, 0, 0, 1]
    ])
    return m

def main():
    width = 900
    height = 700

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    box = Box()

    roll = 0
    pitch = 0
    yaw = 0
    while True:
        screen.fill((0, 0, 0))
        vp = viewport(0, 0, 0.1, 100, width, height)
        projection = perspective_projection(160, 0.1, 100, width, height)
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_LEFT:
            pitch -= 5
        if event.type == KEYDOWN and event.key == K_RIGHT:
            pitch += 5
        if event.type == KEYDOWN and event.key == K_UP:
            roll += 5
        if event.type == KEYDOWN and event.key == K_DOWN:
            roll -= 5
        mat = rotation(roll, pitch, yaw).dot(projection)
        mat = mat.dot(vp)
        print('pitch: {0}, roll: {1}\n\n'.format(pitch, roll))
        for edge in box.EDGES:
            # przekształcenia
            p0 = box.POINTS[edge[0]].dot(mat)
            p1 = box.POINTS[edge[1]].dot(mat)
            # normalizacja
            p0 = p0 / p0[3]
            p1 = p1 / p1[3]
            # rysowanie
            pygame.draw.line(screen, 200, (p0[0], p0[1]), (p1[0], p1[1]))
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        pygame.display.flip()
        pygame.time.delay(25)


if __name__ == "__main__":
    main()
