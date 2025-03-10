from pygame.locals import *
from OpenGL.GL import *
from objects import (
    Bomb,
    Crate,
    Five,
    Pixel,
    Player,
    Square,
    One,
    Two,
    Three,
    Four,
    Six,
    Wall,
)

from game import W, C, B, P, PB, CB


def delete_object(vao, ebo):
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [ebo])


PURPLE = (1.0, 0.0, 1.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)
BROWN = (0.788, 0.549, 0.294, 1.0)
YELLOW = (0.95294118, 0.88627451, 0.69411765, 1.0)


class Renderer:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.nums = [One(), Two(), Three(), Four(), Five(), Six()]
        self.square = Square()
        self.wall = Wall()
        self.bomb = Bomb()
        self.pixel = Pixel()
        self.crate = Crate()
        self.player = Player()
        self.color_location = glGetUniformLocation(shader_program, "color")
        self.vertex_location = glGetUniformLocation(shader_program, "offset")

    def render_obj(self, object, x, y, color):
        glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(object.vao)
        glDrawElements(GL_TRIANGLES, object.square_index, GL_UNSIGNED_INT, None)

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

    def render_level(self, level, level_index):
        for index, num in enumerate(str(level_index + 1)):
            x = index - 5
            y = index - -4.7
            self.render_obj(self.nums[int(num) - 1], x, y, PURPLE)

        num_rows = len(level)
        for row, r_val in enumerate(level):
            for col, obj in enumerate(r_val):
                x = col - 3.0
                y = (num_rows - 1 - row) - 3.0

                if obj == W:
                    self.render_obj(self.wall, x, y, PURPLE)
                if obj == B:
                    self.render_obj(self.bomb, x, y, BLUE)
                if obj == C or obj == CB:
                    self.render_obj(self.crate, x, y, BROWN)
                if obj == P or obj == PB:
                    self.render_obj(self.player, x, y, YELLOW)

    def de_init(self):
        delete_object(self.square.vao, self.square.ebo)
