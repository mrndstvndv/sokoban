from typing import List, Tuple, cast

from pygame import math
from config import gl

import numpy as np
import math
import ctypes

from utils import Vec2f


def create_object(vertices, indices_arr):
    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices_arr, dtype=np.uint32)

    VAO = gl.glGenVertexArrays(1)
    VBO = gl.glGenBuffers(1)
    EBO = gl.glGenBuffers(1)

    gl.glBindVertexArray(VAO)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    gl.glBufferData(
        gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW
    )

    # Position attribute (location = 0)
    gl.glVertexAttribPointer(
        0,
        2,
        gl.GL_FLOAT,
        gl.GL_FALSE,
        6 * ctypes.sizeof(ctypes.c_float),
        ctypes.c_void_p(0),
    )
    gl.glEnableVertexAttribArray(0)

    # Color attribute (location = 1)
    gl.glVertexAttribPointer(
        1,
        4,
        gl.GL_FLOAT,
        gl.GL_FALSE,
        6 * ctypes.sizeof(ctypes.c_float),
        ctypes.c_void_p(2 * ctypes.sizeof(ctypes.c_float)),
    )
    gl.glEnableVertexAttribArray(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    return (VAO, EBO, len(indices))


class Shape:
    def __init__(self, scale=1):
        self.vertices = []
        self.indices = []
        self.scale = scale

    def square(
        self, bottom_left, bottom_right, top_right, top_left, color=(1.0, 1.0, 1.0, 0.0)
    ):
        self.vertices += [
            bottom_left[0] * self.scale,
            bottom_left[1] * self.scale,
            *color,
            bottom_right[0] * self.scale,
            bottom_right[1] * self.scale,
            *color,
            top_right[0] * self.scale,
            top_right[1] * self.scale,
            *color,
            top_left[0] * self.scale,
            top_left[1] * self.scale,
            *color,
        ]

        start = (len(self.vertices) // 6) - 4

        self.indices += [start, start + 1, start + 2]
        self.indices += [start, start + 2, start + 3]

    def plot_pixels(self, points, size=0.1):
        size = size / 2

        if len(points[0]) == 3:
            for x, y, color in points:
                self.square(
                    (x - size, y - size),  # Bottom-left
                    (x + size, y - size),  # Bottom-right
                    (x + size, y + size),  # Top-right
                    (x - size, y + size),  # Top
                    color,
                )

        else:
            for x, y in points:
                self.square(
                    (x - size, y - size),  # Bottom-left
                    (x + size, y - size),  # Bottom-right
                    (x + size, y + size),  # Top-right
                    (x - size, y + size),  # Top
                )

    def get_bounds(self) -> Tuple[Vec2f, Vec2f] | None:
        """
        Finds the top-left (start point) and bottom-right (end point) of a given set of vertices.

        :param vertices: A list where every 6 elements represent (x, y, r, g, b, a).
        :return: (start_point, end_point) as tuples (x, y)
        """
        if not self.vertices:
            return None  # Return None if there are no vertices

        # Initialize min/max values
        min_x = float("inf")
        max_x = float("-inf")
        min_y = float("inf")
        max_y = float("-inf")

        # Iterate through the vertices, stepping by 6 to only consider (x, y)
        for i in range(0, len(self.vertices), 6):
            x, y = self.vertices[i], self.vertices[i + 1]
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        # Start point: Top-left (min_x, max_y)
        start_point = Vec2f(min_x, max_y)
        # End point: Bottom-right (max_x, min_y)
        end_point = Vec2f(max_x, min_y)

        return start_point, end_point

    def build(self):
        return create_object(self.vertices, self.indices)


class Object:
    vao = None
    ebo = None
    index = None
    shape: Shape

    def de_init(self):
        if self.vao == None:
            Exception("vao does not exist")

        if self.ebo == None:
            Exception("ebo does not exist")

        gl.glDeleteVertexArrays(1, [self.vao])
        gl.glDeleteBuffers(1, [self.ebo])


class Square(Object):
    def __init__(self):
        shape = Shape()
        shape.square(
            (-0.5, -0.5),  # Bottom-left
            (0.5, -0.5),  # Bottom-right
            (0.5, 0.5),  # Top-right
            (-0.5, 0.5),  # Top
        )
        self.vao, self.ebo, self.square_index = shape.build()


class One(Object):
    def __init__(self):
        shape = Shape()
        points = [
            (0.05, 0.45),
            (0.05, 0.35),
            (0.15, 0.35),
            (0.15, 0.45),
            (0.25, 0.45),
            (0.25, 0.35),
            (0.35, 0.45),
            (0.35, 0.35),
            (0.45, 0.45),
            (0.45, 0.35),
            (0.35, 0.25),
            (0.45, 0.25),
            (0.35, 0.15),
            (0.45, 0.15),
            (0.45, 0.05),
            (0.35, 0.05),
            (0.35, -0.05),
            (0.45, -0.05),
            (0.45, -0.15),
            (0.35, -0.15),
            (0.35, -0.25),
            (0.45, -0.25),
            (0.45, -0.35),
            (0.35, -0.35),
            (0.35, -0.45),
            (0.45, -0.45),
        ]

        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Two(Object):
    def __init__(self):
        shape = Shape()

        height = 0.5
        width = 0.5

        shape.square(
            (-width, height - 0.25),  # bottom-left
            (width, height - 0.25),  # bottom-right
            (width, height),  # top-right
            (-width, height),  # top-left
        )

        shape.square(
            (width - 0.25, 0.125),  # bottom-left
            (width, 0.125),  # bottom-right
            (width, height),  # top-right
            (width - 0.25, height),  # top-left
        )

        shape.square(
            (-width, -0.125),  # bottom-left
            (width, -0.125),  # bottom-right
            (width, 0.125),  # top-right
            (-width, 0.125),  # top-left
        )

        shape.square(
            (-width, -height),  # bottom-left
            (-width + 0.25, -height),  # bottom-right
            (-width + 0.25, -0.125),  # top-right
            (-width, -0.125),  # top-left
        )

        shape.square(
            (-width, -height),  # bottom-left
            (width, -height),  # bottom-right
            (width, -height + 0.25),  # top-right
            (-width, -height + 0.25),  # top-left
        )

        self.vao, self.ebo, self.square_index = shape.build()


class Three(Object):
    def __init__(self):
        shape = Shape()

        height = 0.5
        width = 0.5

        shape.square(
            (-width, height - 0.25),  # bottom-left
            (width, height - 0.25),  # bottom-right
            (width, height),  # top-right
            (-width, height),  # top-left
        )

        shape.square(
            (width - 0.25, 0.125),  # bottom-left
            (width, 0.125),  # bottom-right
            (width, height),  # top-right
            (width - 0.25, height),  # top-left
        )

        shape.square(
            (-width, -0.125),  # bottom-left
            (width, -0.125),  # bottom-right
            (width, 0.125),  # top-right
            (-width, 0.125),  # top-left
        )

        shape.square(
            (width - 0.25, -height),  # bottom-left
            (width, -height),  # bottom-right
            (width, -0.125),  # top-right
            (width - 0.25, -0.125),  # top-left
        )

        shape.square(
            (-width, -height),  # bottom-left
            (width, -height),  # bottom-right
            (width, -height + 0.25),  # top-right
            (-width, -height + 0.25),  # top-left
        )

        self.vao, self.ebo, self.square_index = shape.build()


class Four(Object):
    def __init__(self):
        shape = Shape()

        height = 0.5
        width = 0.5

        shape.square(
            (-width, 0.125),  # bottom-left
            (-width + 0.25, 0.125),  # bottom-right
            (-width + 0.25, height),  # top-right
            (-width, height),  # top-left
        )

        shape.square(
            (-width, -0.125),  # bottom-left
            (width, -0.125),  # bottom-right
            (width, 0.125),  # top-right
            (-width, 0.125),  # top-left
        )

        shape.square(
            (width - 0.25, -height),  # bottom-left
            (width, -height),  # bottom-right
            (width, height),  # top-right
            (width - 0.25, height),  # top-left
        )

        self.vao, self.ebo, self.square_index = shape.build()


class Five(Object):
    def __init__(self):
        shape = Shape()

        height = 0.5
        width = 0.5

        shape.square(
            (-width, height - 0.25),  # bottom-left
            (width, height - 0.25),  # bottom-right
            (width, height),  # top-right
            (-width, height),  # top-left
        )

        shape.square(
            (-width + 0.25, 0.125),  # bottom-left
            (-width, 0.125),  # bottom-right
            (-width, height),  # top-right
            (-width + 0.25, height),  # top-left
        )

        shape.square(
            (-width, -0.125),  # bottom-left
            (width, -0.125),  # bottom-right
            (width, 0.125),  # top-right
            (-width, 0.125),  # top-left
        )

        shape.square(
            (+width, -height),  # bottom-left
            (+width - 0.25, -height),  # bottom-right
            (+width - 0.25, -0.125),  # top-right
            (+width, -0.125),  # top-left
        )

        shape.square(
            (-width, -height),  # bottom-left
            (width, -height),  # bottom-right
            (width, -height + 0.25),  # top-right
            (-width, -height + 0.25),  # top-left
        )

        self.vao, self.ebo, self.square_index = shape.build()


class Six(Object):
    def __init__(self):
        shape = Shape()

        height = 0.5
        width = 0.5

        shape.square(
            (-width, height - 0.25),  # bottom-left
            (width, height - 0.25),  # bottom-right
            (width, height),  # top-right
            (-width, height),  # top-left
        )

        shape.square(
            (-width + 0.25, 0.125),  # bottom-left
            (-width, 0.125),  # bottom-right
            (-width, height),  # top-right
            (-width + 0.25, height),  # top-left
        )

        shape.square(
            (-width, -0.125),  # bottom-left
            (width, -0.125),  # bottom-right
            (width, 0.125),  # top-right
            (-width, 0.125),  # top-left
        )

        shape.square(
            (-width, -height),  # bottom-left
            (-width + 0.25, -height),  # bottom-right
            (-width + 0.25, -0.125),  # top-right
            (-width, -0.125),  # top-left
        )

        shape.square(
            (width, -height),  # bottom-left
            (width - 0.25, -height),  # bottom-right
            (width - 0.25, -0.125),  # top-right
            (width, -0.125),  # top-left
        )

        shape.square(
            (-width, -height),  # bottom-left
            (width, -height),  # bottom-right
            (width, -height + 0.25),  # top-right
            (-width, -height + 0.25),  # top-left
        )

        self.vao, self.ebo, self.square_index = shape.build()


class Seven(Object):
    def __init__(self) -> None:
        shape = Shape()
        points = [
            (-0.45, 0.45),
            (-0.45, 0.35),
            (-0.35, 0.45),
            (-0.35, 0.35),
            (-0.25, 0.45),
            (-0.25, 0.35),
            (-0.15, 0.35),
            (-0.15, 0.45),
            (0.05, 0.45),
            (-0.05, 0.45),
            (-0.05, 0.35),
            (0.05, 0.35),
            (0.15, 0.35),
            (0.15, 0.45),
            (0.25, 0.45),
            (0.25, 0.35),
            (0.35, 0.35),
            (0.35, 0.45),
            (0.45, 0.45),
            (0.45, 0.35),
            (0.35, 0.25),
            (0.45, 0.25),
            (0.35, 0.15),
            (0.45, 0.15),
            (0.45, 0.05),
            (0.35, 0.05),
            (0.35, -0.05),
            (0.45, -0.05),
            (0.45, -0.15),
            (0.35, -0.15),
            (0.35, -0.25),
            (0.45, -0.25),
            (0.45, -0.35),
            (0.35, -0.35),
            (0.35, -0.45),
            (0.45, -0.45),
        ]

        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Eight(Object):
    def __init__(self) -> None:
        shape = Shape()
        points = [
            (-0.45, 0.45),
            (-0.45, 0.35),
            (-0.45, 0.25),
            (-0.35, 0.15),
            (-0.45, 0.15),
            (-0.45, 0.05),
            (-0.45, -0.05),
            (-0.45, -0.15),
            (-0.45, -0.25),
            (-0.45, -0.35),
            (-0.45, -0.45),
            (-0.35, -0.45),
            (-0.35, -0.35),
            (-0.35, -0.25),
            (-0.35, -0.15),
            (-0.35, -0.05),
            (-0.35, 0.05),
            (-0.35, 0.25),
            (-0.35, 0.35),
            (-0.35, 0.45),
            (-0.25, 0.45),
            (-0.25, 0.35),
            (-0.15, 0.45),
            (-0.15, 0.35),
            (-0.05, 0.45),
            (-0.05, 0.35),
            (0.05, 0.45),
            (0.05, 0.35),
            (0.15, 0.45),
            (0.15, 0.35),
            (0.25, 0.45),
            (0.25, 0.35),
            (0.35, 0.45),
            (0.35, 0.35),
            (0.45, 0.45),
            (0.45, 0.35),
            (-0.25, 0.05),
            (-0.25, -0.05),
            (-0.15, 0.05),
            (-0.15, -0.05),
            (-0.05, 0.05),
            (-0.05, -0.05),
            (0.05, 0.05),
            (0.05, -0.05),
            (0.15, 0.05),
            (0.15, -0.05),
            (0.25, -0.05),
            (0.25, 0.05),
            (0.35, 0.05),
            (0.35, -0.05),
            (0.45, -0.05),
            (0.45, 0.05),
            (0.45, 0.15),
            (0.35, 0.15),
            (0.35, 0.25),
            (0.45, 0.25),
            (0.35, -0.15),
            (0.45, -0.15),
            (0.35, -0.25),
            (0.45, -0.25),
            (0.45, -0.35),
            (0.35, -0.35),
            (0.35, -0.45),
            (0.45, -0.45),
            (0.15, -0.45),
            (0.25, -0.45),
            (0.25, -0.35),
            (0.15, -0.35),
            (0.05, -0.35),
            (-0.05, -0.35),
            (-0.15, -0.35),
            (-0.25, -0.35),
            (-0.25, -0.45),
            (-0.15, -0.45),
            (-0.05, -0.45),
            (0.05, -0.45),
        ]

        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Nine(Object):
    def __init__(self) -> None:
        shape = Shape()
        points = [
            (-0.45, 0.45),
            (-0.45, 0.35),
            (-0.35, 0.35),
            (-0.35, 0.45),
            (-0.25, 0.45),
            (-0.25, 0.35),
            (-0.15, 0.45),
            (-0.15, 0.35),
            (-0.05, 0.35),
            (-0.05, 0.45),
            (0.05, 0.45),
            (0.05, 0.35),
            (0.15, 0.35),
            (0.15, 0.45),
            (0.25, 0.45),
            (0.25, 0.35),
            (0.35, 0.35),
            (0.45, 0.45),
            (0.35, 0.45),
            (0.45, 0.35),
            (0.35, 0.25),
            (0.45, 0.25),
            (0.35, 0.15),
            (0.45, 0.15),
            (0.35, 0.05),
            (0.45, 0.05),
            (0.35, -0.05),
            (0.45, -0.05),
            (0.35, -0.15),
            (0.45, -0.15),
            (0.35, -0.25),
            (0.45, -0.25),
            (0.45, -0.35),
            (0.35, -0.35),
            (0.45, -0.45),
            (0.35, -0.45),
            (-0.35, 0.25),
            (-0.45, 0.25),
            (-0.45, 0.15),
            (-0.35, 0.15),
            (-0.45, 0.05),
            (-0.35, 0.05),
            (-0.25, 0.05),
            (-0.15, 0.05),
            (-0.05, 0.05),
            (0.05, 0.05),
            (0.15, 0.05),
            (0.25, 0.05),
            (0.25, -0.05),
            (0.15, -0.05),
            (0.05, -0.05),
            (-0.05, -0.05),
            (-0.15, -0.05),
            (-0.25, -0.05),
            (-0.35, -0.05),
            (-0.45, -0.05),
        ]

        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Zero(Object):
    def __init__(self) -> None:
        shape = Shape()
        points = [
            (-0.45, 0.45),
            (-0.45, 0.35),
            (-0.45, 0.25),
            (-0.45, 0.15),
            (-0.45, 0.05),
            (-0.45, -0.05),
            (-0.45, -0.15),
            (-0.45, -0.25),
            (-0.45, -0.35),
            (-0.45, -0.45),
            (-0.35, -0.45),
            (-0.25, -0.45),
            (-0.15, -0.45),
            (-0.05, -0.45),
            (0.05, -0.45),
            (0.15, -0.45),
            (0.25, -0.45),
            (0.35, -0.45),
            (0.45, -0.45),
            (0.45, -0.35),
            (0.45, -0.25),
            (0.45, -0.15),
            (0.45, -0.05),
            (0.45, 0.05),
            (0.45, 0.15),
            (0.45, 0.25),
            (0.45, 0.35),
            (0.45, 0.45),
            (0.35, 0.45),
            (0.25, 0.45),
            (0.15, 0.45),
            (0.05, 0.45),
            (-0.05, 0.45),
            (-0.15, 0.45),
            (-0.25, 0.45),
            (-0.35, 0.45),
            (-0.35, 0.35),
            (-0.25, 0.35),
            (-0.15, 0.35),
            (-0.05, 0.35),
            (0.05, 0.35),
            (0.15, 0.35),
            (0.25, 0.35),
            (0.35, 0.35),
            (0.35, 0.25),
            (0.35, 0.15),
            (0.35, 0.05),
            (0.35, -0.05),
            (0.35, -0.15),
            (0.35, -0.25),
            (0.35, -0.35),
            (0.25, -0.35),
            (0.15, -0.35),
            (0.05, -0.35),
            (-0.05, -0.35),
            (-0.15, -0.35),
            (-0.25, -0.35),
            (-0.35, -0.35),
            (-0.35, -0.25),
            (-0.35, -0.15),
            (-0.35, -0.05),
            (-0.35, 0.05),
            (-0.35, 0.15),
            (-0.35, 0.25),
        ]

        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Pixel(Object):
    def __init__(self):
        shape = Shape()

        width = 0.5
        height = 0.5

        shape.square(
            (-width, height - 0.1),  # bottom-left
            (-width + 0.1, height - 0.1),  # bottom-right
            (-width + 0.1, height),  # top-right
            (-width, height),  # top-left
        )

        self.vao, self.ebo, self.square_index = shape.build()


class Wall(Object):
    def __init__(self):
        shape = Shape()

        points = [
            (0.35, 0.35),
            (0.35, 0.25),
            (0.15, 0.35),
            (0.05, 0.35),
            (-0.05, 0.35),
            (-0.15, 0.35),
            (-0.25, 0.35),
            (-0.35, 0.35),
            (-0.35, 0.25),
            (-0.25, 0.25),
            (-0.15, 0.25),
            (-0.05, 0.25),
            (0.05, 0.25),
            (0.15, 0.25),
            (0.35, 0.05),
            (0.25, 0.05),
            (-0.35, 0.05),
            (-0.35, -0.05),
            (0.15, 0.05),
            (0.05, 0.05),
            (-0.05, 0.05),
            (-0.15, 0.05),
            (-0.15, -0.05),
            (-0.05, -0.05),
            (0.05, -0.05),
            (0.15, -0.05),
            (0.25, -0.05),
            (0.35, -0.05),
            (0.35, -0.25),
            (0.25, -0.25),
            (0.35, -0.35),
            (0.25, -0.35),
            (0.15, -0.25),
            (0.15, -0.35),
            (-0.05, -0.25),
            (-0.05, -0.35),
            (-0.15, -0.35),
            (-0.15, -0.25),
            (-0.25, -0.25),
            (-0.25, -0.35),
            (-0.35, -0.35),
            (-0.35, -0.25),
        ]

        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Bomb(Object):
    def __init__(self):
        points = [
            (0.25, 0.35),
            (0.05, 0.35),
            (-0.05, 0.35),
            (-0.15, 0.35),
            (-0.25, 0.25),
            (-0.35, 0.15),
            (-0.35, 0.05),
            (-0.25, 0.05),
            (-0.15, 0.15),
            (-0.05, 0.25),
            (-0.05, 0.15),
            (-0.05, 0.05),
            (-0.15, -0.05),
            (-0.25, -0.05),
            (-0.15, -0.15),
            (-0.05, -0.25),
            (0.05, -0.35),
            (-0.05, -0.15),
            (-0.05, -0.05),
            (0.15, -0.25),
            (0.25, -0.15),
            (0.35, -0.05),
            (0.45, 0.05),
            (0.45, 0.15),
            (0.35, 0.25),
            (0.35, 0.05),
            (0.25, 0.05),
            (0.15, 0.05),
            (0.05, 0.05),
            (0.05, -0.05),
            (0.15, 0.25),
            (0.05, 0.25),
        ]

        shape = Shape()
        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Crate(Object):
    def __init__(self):
        points = [
            (-0.35, 0.35),
            (-0.35, 0.25),
            (-0.35, 0.05),
            (-0.35, -0.05),
            (-0.35, -0.25),
            (-0.35, -0.35),
            (-0.25, -0.35),
            (-0.15, -0.35),
            (-0.05, -0.35),
            (0.05, -0.35),
            (0.15, -0.35),
            (0.25, -0.35),
            (0.35, -0.35),
            (0.35, -0.25),
            (0.35, -0.05),
            (0.35, 0.05),
            (0.35, 0.25),
            (0.35, 0.35),
            (0.25, 0.35),
            (0.15, 0.35),
            (0.05, 0.35),
            (-0.05, 0.35),
            (-0.15, 0.35),
            (-0.25, 0.35),
            (-0.15, 0.15),
            (-0.05, 0.05),
            (-0.15, -0.05),
            (-0.05, -0.15),
            (0.05, -0.05),
            (0.15, -0.15),
            (0.15, 0.05),
            (0.05, 0.15),
        ]

        shape = Shape()
        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class Player(Object):
    def __init__(self):
        points = [
            (0.05, 0.45),
            (-0.05, 0.45),
            (-0.15, 0.35),
            (-0.05, 0.35),
            (0.05, 0.35),
            (0.15, 0.35),
            (0.15, 0.25),
            (0.15, 0.15),
            (0.05, 0.15),
            (-0.15, 0.15),
            (-0.15, -0.05),
            (-0.05, -0.05),
            (0.05, -0.05),
            (0.15, -0.05),
            (0.25, -0.05),
            (0.35, -0.15),
            (0.35, -0.25),
            (-0.25, -0.15),
            (-0.25, -0.25),
            (-0.05, -0.15),
            (-0.05, -0.25),
            (-0.05, -0.35),
            (-0.05, -0.45),
            (0.15, -0.15),
            (0.15, -0.25),
            (0.15, -0.35),
            (0.15, -0.45),
            (0.05, -0.15),
            (0.05, -0.25),
        ]

        shape = Shape()
        shape.plot_pixels(points)
        self.vao, self.ebo, self.square_index = shape.build()


class CircleGenerator:
    def __init__(self, radius, quality) -> None:
        self.radius: float = radius
        self.quality: int = quality
        self.da: float = (2.0 * np.pi) / float(quality) if quality > 0 else 0.0

    def get_point(self, n: int) -> Tuple[float, float]:
        angle = self.da * float(n)
        return self.radius * math.cos(angle), self.radius * math.sin(angle)

    def generate_circle(self) -> List[Tuple[float, float]]:
        return [self.get_point(i) for i in range(self.quality)]

    def obj(self):
        vertices = self.generate_circle()
        vertices_flat = [coord for point in vertices for coord in point]

        indices = []
        for i in range(self.quality):
            indices.append(i)

        return create_object(vertices_flat, indices)


class Circle(Object):
    def __init__(self, radius, quality) -> None:
        circle = CircleGenerator(radius, quality)

        self.vao, self.ebo, self.index = circle.obj()


class Rectangle(Object):
    def __init__(self, start: Vec2f, end: Vec2f) -> None:
        self.start = start
        self.end = end

        top_left = (start.x, start.y)
        top_right = (end.x, start.y)
        bot_right = (end.x, end.y)
        bot_left = (start.x, end.y)

        vertices = [*bot_left, *bot_right, *top_right, *top_left]

        indices = [0, 1, 2, 3, 4, 5, 6, 7]

        self.vao, self.ebo, self.index = create_object(vertices, indices)

    def in_bounds(self, pos: Vec2f) -> bool:
        return (
            pos.x >= self.start.x
            and pos.x <= self.end.x
            and pos.y <= self.start.y
            and pos.y >= self.end.y
        )
