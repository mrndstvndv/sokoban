from OpenGL.GL import *
import numpy as np
import ctypes

def create_square():
    square_vertices = np.array([
        -0.5, -0.5,  # Bottom-left
         0.5, -0.5,  # Bottom-right
         0.5,  0.5,  # Top-right
        -0.5,  0.5,   # Top
    ], dtype = np.float32)

    indices = np.array([
        0, 1, 2,  # First triangle
        0, 2, 3   # Second triangle
    ], dtype = np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    # Bind and set vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, square_vertices.nbytes, square_vertices, GL_STATIC_DRAW)

    # Bind and set element buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Set vertex attribute pointers
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Unbind VAO (not the EBO)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO, EBO, len(indices)

