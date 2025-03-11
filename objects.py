from OpenGL.GL import *
import numpy as np
import ctypes


def create_object(vertices, indices_arr):
    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices_arr, dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    # Bind and set vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Bind and set element buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Set vertex attribute pointers
    glVertexAttribPointer(
        0, 2, GL_FLOAT, GL_FALSE, 2 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    # Unbind VAO (not the EBO)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return (VAO, EBO, len(indices))


class Square:
    def __init__(self):
        shape = Shape()
        shape.square(
            (-0.5, -0.5),  # Bottom-left
            (0.5, -0.5),  # Bottom-right
            (0.5, 0.5),  # Top-right
            (-0.5, 0.5),  # Top
        )
        self.vao, self.ebo, self.square_index = shape.build()


class One:
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


class Shape:
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

    def plot_pixels(self, points):
        for x, y in points:
            self.square(
                (x - 0.05, y - 0.05),  # bottom-left
                (x + 0.05, y - 0.05),  # bottom-right
                (x + 0.05, y + 0.05),  # top-right
                (x - 0.05, y + 0.05),  # top-left
            )

    def build(self):
        return create_object(self.vertices, self.indices)


class Two:
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


class Three:
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


class Four:
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


class Five:
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


class Six:
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


class Seven:
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


class Eight:
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


class Nine:
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


class Zero:
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


class Pixel:
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


class Wall:
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


class Bomb:
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


class Crate:
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


class Player:
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
