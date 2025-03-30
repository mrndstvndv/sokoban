from typing import List, Tuple

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

    # Bind and set vertex buffer
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

    # Bind and set element buffer
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    gl.glBufferData(
        gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW
    )

    # Set vertex attribute pointers
    gl.glVertexAttribPointer(
        0,
        2,
        gl.GL_FLOAT,
        gl.GL_FALSE,
        2 * ctypes.sizeof(ctypes.c_float),
        ctypes.c_void_p(0),
    )
    gl.glEnableVertexAttribArray(0)

    # Unbind VAO (not the EBO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    return (VAO, EBO, len(indices))


class Object:
    vao = None
    ebo = None
    index = None

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


class Shape(Object):
    def __init__(self, scale=1):
        self.vertices = []
        self.indices = []
        self.scale = scale

    def square(self, bottom_left, bottom_right, top_right, top_left):
        self.vertices += [
            bottom_left[0],
            bottom_left[1],
            bottom_right[0],
            bottom_right[1],
            top_right[0],
            top_right[1],
            top_left[0],
            top_left[1],
        ]

        last_vertice_index = (len(self.vertices) // 2) - 1
        start = last_vertice_index - 3

        self.indices += [start, start + 1, start + 2]
        self.indices += [start, start + 2, start + 3]

    def plot_pixels(self, points, size=0.1):
        size = size / 2

        for x, y in points:
            self.square(
                (x - size, y - size),  # Bottom-left
                (x + size, y - size),  # Bottom-right
                (x + size, y + size),  # Top-right
                (x - size, y + size),  # Top
            )

    def build(self):
        return create_object(self.vertices, self.indices)


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
