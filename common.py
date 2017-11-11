import math
import numpy as np
import pygame


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


def set_up_text(fov, pitch, yaw, roll, x_offset, y_offset, z_offset):
    font = pygame.font.SysFont("arial", 28)
    text = font.render(
        "FOV= {0}, Pitch= {1}, Yaw= {2}, Roll= {3}, X= {4}, Y={5}, Z={6}".format(
            fov, pitch, yaw, roll, x_offset, y_offset, z_offset),
        True,
        (0, 128, 150)
    )
    return text


def map_triangle_to_xy(triangle):
    return (p[:2] for p in triangle)


def subdivide_triangle(triangle):
    p0 = (triangle[0] + triangle[1]) / 2
    p1 = (triangle[1] + triangle[2]) / 2
    p2 = (triangle[2] + triangle[0]) / 2

    return (triangle[0], p0, p2), (triangle[1], p0, p1), (triangle[2], p1, p2), (p0, p1, p2)
