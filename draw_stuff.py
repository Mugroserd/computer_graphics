import numpy as np
from PIL import Image, ImageDraw

import objects_definition as od


def line_brezenhem(start: od.Point, end: od.Point, draw: ImageDraw, color=(255, 0, 0)):
    """
     Draws line from start to end 2D Point via Brezenhem algorithm ( without gradient subline )
    :param start: starting line 2D point
    :param end: ending line 2D point
    :param draw: drawing tool from Pillow module
    :param color: base painting color ( optional, red is default)
    """

    # decompose point
    x0, y0 = (start.x, start.y)
    x1, y1 = (end.x, end.y)

    # reverse coordinates if y axis part of line longer thar x axis
    steeps = np.abs(x0 - x1) < np.abs(y0 - y1)
    if steeps:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    derror = np.abs(dy / dx)
    error = 0
    y = y0
    for i in np.arange(x0, x1, 1):
        # Draw base line
        draw.point([i, y] if not steeps else [y, i], fill=color)
        error += derror
        if error > 0.5:
            y += 1 if y1 > y0 else -1
            error -= 1


def line_vu(start: od.Point, end: od.Point, draw: ImageDraw, color=(255, 0, 0)):
    """
         Draws line from start to end 2D Point via Vu algorithm ( with gradient subline )
        :param start: starting line 2D point
        :param end: ending line 2D point
        :param draw: drawing tool from Pillow module
        :param color: base painting color ( optional, red is default )
        """
    # decompose point
    x0, y0 = start.x, start.y
    x1, y1 = end.x, end.y

    # reverse coordinates if y axis part of line longer thar x axis
    steeps = np.abs(x0 - x1) < np.abs(y0 - y1)
    if steeps:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    dx = x1 - x0
    dy = y1 - y0
    if dx < 0:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    derror = np.abs(dy / dx)
    error = 0
    y = y0
    sy = 1 if y1 > y0 else -1

    for i in np.arange(x0, x1, 1):

        base_color = tuple([int(i * (1 - error)) for i in list(color)])
        add_color = tuple([int(i * error) for i in list(color)])
        # Draw base line with subline
        draw.point([i, y] if not steeps else [y, i], fill=base_color)
        draw.point([i, y + sy] if not steeps else [y + sy, i], fill=add_color)

        error += derror
        if error > 1:
            y += sy
            error -= 1


def draw_pixel(point: od.Point, z_buffer, draw: ImageDraw, color=(255, 0, 0)):
    """
    Draws pixel, if it's z depth is lower then previous points
    """
    if point.third < z_buffer[point.first, point.second]:
        draw.point([point.first, point.second], fill=color)
        z_buffer[point.first, point.second] = point.third
