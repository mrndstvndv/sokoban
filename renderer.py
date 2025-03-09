from pygame.locals import *
from OpenGL.GL import *
from objects import Square, One, Two

from game import W, C, B, P, PB, CB


class Renderer:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.square = Square()
        self.one = One()
        self.two = Two()
        self.color_location = glGetUniformLocation(shader_program, "color")
        self.vertex_location = glGetUniformLocation(shader_program, "offset")

    def render_one(self, x, y):
        glUniform4f(self.color_location, 1.0, 0.0, 1.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.one.vao)
        glDrawElements(GL_TRIANGLES, self.one.square_index, GL_UNSIGNED_INT, None)

    def render_two(self, x, y):
        glUniform4f(self.color_location, 1.0, 0.0, 1.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.two.vao)
        glDrawElements(GL_TRIANGLES, self.two.square_index, GL_UNSIGNED_INT, None)

    def render_square(self, x, y):
        glUniform4f(self.color_location, 1.0, 0.0, 1.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.square.vao)
        glDrawElements(GL_TRIANGLES, self.square.square_index, GL_UNSIGNED_INT, None)

    def render_player(self, x, y):
        glUniform4f(self.color_location, 0.0, 1.0, 0.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.square.vao)
        glDrawElements(GL_TRIANGLES, self.square.square_index, GL_UNSIGNED_INT, None)

    def render_crate(self, x, y):
        glUniform4f(self.color_location, 1.0, 0.0, 0.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.square.vao)
        glDrawElements(GL_TRIANGLES, self.square.square_index, GL_UNSIGNED_INT, None)

    def render_bomb(self, x, y):
        glUniform4f(self.color_location, 0.0, 0.0, 1.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.square.vao)
        glDrawElements(GL_TRIANGLES, self.square.square_index, GL_UNSIGNED_INT, None)

    def render_level(self, level):
        self.render_two(-5.5, -4.7)

        num_rows = len(level)
        for row, r_val in enumerate(level):
            for col, obj in enumerate(r_val):
                x = col - 3.0
                y = (num_rows - 1 - row) - 3.0

                if obj == W:
                    self.render_square(x, y)
                if obj == B:
                    self.render_bomb(x, y)
                if obj == C or obj == CB:
                    self.render_crate(x, y)
                if obj == P or obj == PB:
                    self.render_player(x, y)
