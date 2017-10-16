# -*- coding: utf-8 -*-

import numpy as np
from time import sleep
import pygame
from pygame.locals import *
import math
from models import Box
import sys

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
    m_y = np.dot(m_z, m_y)
    return np.dot(m_y, m_x)

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

def translation(x, y, z=0):
    m = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ])
    return m

def main():
    width = 900
    height = 700

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    color = (0.40, 0.40, 0/40)
    box1 = Box(100, 10, 200, 100, 100)
    box2 = Box(-100, 10, 200, 100, 100)

    roll = 0
    pitch = 0
    yaw = 0
    x_offset = 0
    y_offset = 0
    z_offset = 0
    fov = 80
    epsilon = 0.01
    keys = {}
    vp = viewport(0, 0, 0.1, 100, width, height)
    while True:
        screen.fill((255, 255, 255))
        # controls
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            keys[event.key] = True
        elif event.type == KEYUP:
            keys[event.key] = False
        if keys.get(K_a, False):
            x_offset -= 5
        if keys.get(K_d, False):
            x_offset += 5
        if keys.get(K_u, False):
            y_offset += 2
        if keys.get(K_j, False):
            y_offset -= 2
        if keys.get(K_s, False):
            z_offset -= 2
        if keys.get(K_w, False):
            z_offset += 2
        if keys.get(K_LEFT, False):
            yaw -= 2
        if keys.get(K_RIGHT, False):
            yaw += 2
        if keys.get(K_UP, False) and keys.get(K_LCTRL, False):
            fov += 1
        elif keys.get(K_UP, False):
            pitch += 2
        if keys.get(K_DOWN, False) and keys.get(K_LCTRL, False):
            fov -= 1
        elif keys.get(K_DOWN, False):
            pitch -= 2
        projection = perspective_projection(fov, 0.1, 100, width, height)
        t = translation(-x_offset, -y_offset, -z_offset)
        mat = t.dot(rotation(-pitch, -yaw, -roll))
        mat = mat.dot(projection)
        mat = mat.dot(vp)
        for box in (box1, box2):
            for edge in box.EDGES:
                # transformation
                p0 = box.POINTS[edge[0]].dot(mat)
                p1 = box.POINTS[edge[1]].dot(mat)
                # normalization
                if p0[3] < epsilon or p1[3] < epsilon:
                    continue
                p0 = p0 / p0[3]
                p1 = p1 / p1[3]
                # drawing
                pygame.draw.aaline(screen, color, (p0[0], p0[1]), (p1[0], p1[1]))
        # exit
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        pygame.time.delay(25)


if __name__ == "__main__":
    main()
