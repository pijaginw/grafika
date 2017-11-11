# -*- coding: utf-8 -*-

import math
import numpy as np
import pygame
from pygame.locals import *
import sys
from time import sleep

from models import Box, Rectangle
from common import (
    map_triangle_to_xy,
    perspective_projection,
    rotation,
    scale,
    set_up_text,
    translation,
    viewport
)


STEP = 5

def get_z(triangle):
    return (triangle[0][2] + triangle[1][2] + triangle[2][2]) / 3


def main():
    width = 900
    height = 700

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    color = (0.40, 0.40, 0/40)
    box1 = Box(100, 10, 200, 80, 90, 3)
    box2 = Box(-100, 10, 200, 85, 90, 3)
    box3 = Box(100, 10, 300, 100, 100, 3)
    box4 = Box(-100, 10, 300, 100, 130, 3)
    rect = Rectangle(0, 100, 80, 300, 3)

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
            x_offset -= STEP
        if keys.get(K_d, False):
            x_offset += STEP
        if keys.get(K_u, False):
            y_offset += STEP
        if keys.get(K_j, False):
            y_offset -= STEP
        if keys.get(K_s, False):
            z_offset -= STEP
        if keys.get(K_w, False):
            z_offset += STEP
        if keys.get(K_LEFT, False):
            yaw += STEP
        if keys.get(K_RIGHT, False):
            yaw -= STEP
        if keys.get(K_z, False):
            roll -= STEP
        if keys.get(K_x, False):
            roll += STEP
        if keys.get(K_UP, False) and keys.get(K_LCTRL, False):
            fov -= STEP
        elif keys.get(K_UP, False):
            pitch += STEP
        if keys.get(K_DOWN, False) and keys.get(K_LCTRL, False):
            fov += STEP
        elif keys.get(K_DOWN, False):
            pitch -= STEP
        text = set_up_text(fov, pitch, yaw, roll, x_offset, y_offset, z_offset)

        projection = perspective_projection(fov, 0.1, 100, width, height)
        t = translation(-x_offset, -y_offset, -z_offset)
        mat = t.dot(rotation(-pitch, -yaw, -roll))
        mat = mat.dot(projection)
        mat = mat.dot(vp)

        transformed_triangles = []
        for box in (box1, box2, box3, box4, rect):
            transformed_points = [point.dot(mat) for point in box.POINTS]
            for triangle in box.TRIANGLES:
                p0 = transformed_points[triangle[0]]
                p1 = transformed_points[triangle[1]]
                p2 = transformed_points[triangle[2]]

                if p0[3] < epsilon or p1[3] < epsilon or p2[3] < epsilon:
                    continue

                p0 = p0 / p0[3]
                p1 = p1 / p1[3]
                p2 = p2 / p2[3]

                transformed_triangles.append((p0, p1, p2))

        for p0, p1, p2 in sorted(transformed_triangles, key=get_z, reverse=True):
            # drawing
            pygame.draw.polygon(screen, 0xFFFF66, [p0[:2], p1[:2], p2[:2]])
            pygame.draw.aalines(screen, (0, 255, 0), True, [p0[:2], p1[:2], p2[:2]], 0)
            screen.blit(text, (420 - text.get_width() // 2, 10 - text.get_height() // 2))

        # exit
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        pygame.time.delay(15)


if __name__ == "__main__":
    main()
