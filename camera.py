# -*- coding: utf-8 -*-

import math
import numpy as np
import pygame
from pygame.locals import *
import sys
from time import sleep

from models import Box, Rectangle
from common import perspective_projection, rotation, scale, set_up_text, translation, viewport


def main():
    width = 900
    height = 700

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    color = (0.40, 0.40, 0/40)
    box1 = Box(100, 10, 200, 80, 90)
    box2 = Box(-100, 10, 200, 85, 90)
    box3 = Box(100, 10, 300, 100, 100)
    box4 = Box(-100, 10, 300, 100, 130)
    rect = Rectangle(0, 100, 80, 300)

    roll = 0
    pitch = 0
    yaw = 0
    x_offset = 0
    y_offset = 0
    z_offset = 0
    fov = 80
    epsilon = 0.005
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
            yaw += 1
        if keys.get(K_RIGHT, False):
            yaw -= 1
        if keys.get(K_z, False):
            roll -= 1
        if keys.get(K_x, False):
            roll += 1
        if keys.get(K_UP, False) and keys.get(K_LCTRL, False):
            fov -= 1
        elif keys.get(K_UP, False):
            pitch += 2
        if keys.get(K_DOWN, False) and keys.get(K_LCTRL, False):
            fov += 1
        elif keys.get(K_DOWN, False):
            pitch -= 2
        text = set_up_text(fov, pitch, yaw, roll, x_offset, y_offset, z_offset)

        projection = perspective_projection(fov, 0.1, 100, width, height)
        t = translation(-x_offset, -y_offset, -z_offset)
        mat = t.dot(rotation(-pitch, -yaw, -roll))
        mat = mat.dot(projection)
        mat = mat.dot(vp)

        for box in (box1, box2, box3, box4, rect):
            for face in box.FACES:
                for edge in face:
                    # transformation
                    p0 = box.POINTS[box.EDGES[edge][0]].dot(mat)
                    p1 = box.POINTS[box.EDGES[edge][1]].dot(mat)
                    # normalization
                    if p0[3] < epsilon or p1[3] < epsilon:
                        continue
                    p0 = p0 / p0[3]
                    p1 = p1 / p1[3]
                    # drawing
                    pygame.draw.aaline(screen, color, (p0[0], p0[1]), (p1[0], p1[1]))
                    screen.blit(text, (420 - text.get_width() // 2, 10 - text.get_height() // 2))
        # exit
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        pygame.time.delay(15)


if __name__ == "__main__":
    main()
