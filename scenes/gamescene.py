import pygame
from pygame.locals import *
import pygame
from config import gl
import levels
from objects import (
    Bomb,
    Crate,
    Eight,
    Five,
    Nine,
    Zero,
    Pixel,
    Player,
    Seven,
    Square,
    One,
    Two,
    Three,
    Four,
    Six,
    Wall,
)

from game import W, C, B, P, PB, CB, Game
from scenes.scene import Scene
from shaders import create_shader_program
import shaders


def delete_object(vao, ebo):
    gl.glDeleteVertexArrays(1, [vao])
    gl.glDeleteBuffers(1, [ebo])


PURPLE = (1.0, 0.0, 1.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)
BROWN = (0.788, 0.549, 0.294, 1.0)
YELLOW = (0.95294118, 0.88627451, 0.69411765, 1.0)


class GameScene(Scene):
    def __init__(self, shader_program):
        super().__init__(shader_program)
        self.nums = [
            Zero(),
            One(),
            Two(),
            Three(),
            Four(),
            Five(),
            Six(),
            Seven(),
            Eight(),
            Nine(),
        ]
        self.square = Square()
        self.wall = Wall()
        self.bomb = Bomb()
        self.pixel = Pixel()
        self.crate = Crate()
        self.player = Player()
        self.color_location = gl.glGetUniformLocation(shader_program, "color")
        self.vertex_location = gl.glGetUniformLocation(shader_program, "offset")
        self.scale_location = gl.glGetUniformLocation(shader_program, "scale")
        self.game = Game(levels.levels)

    def render_obj(self, object, x, y, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.vertex_location, x, y)
        gl.glUniform1f(self.scale_location, 1.0)
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES, object.square_index, gl.GL_UNSIGNED_INT, None
        )

    def render_square(self, x, y):
        gl.glUniform4f(self.color_location, 1.0, 0.0, 1.0, 1.0)
        gl.glUniform2f(self.vertex_location, x, y)
        gl.glBindVertexArray(self.square.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES, self.square.square_index, gl.GL_UNSIGNED_INT, None
        )

    def render_player(self, x, y):
        gl.glUniform4f(self.color_location, 0.0, 1.0, 0.0, 1.0)
        gl.glUniform2f(self.vertex_location, x, y)
        gl.glBindVertexArray(self.square.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES, self.square.square_index, gl.GL_UNSIGNED_INT, None
        )

    def render_crate(self, x, y):
        gl.glUniform4f(self.color_location, 1.0, 0.0, 0.0, 1.0)
        gl.glUniform2f(self.vertex_location, x, y)
        gl.glBindVertexArray(self.square.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES, self.square.square_index, gl.GL_UNSIGNED_INT, None
        )

    def render_bomb(self, x, y):
        gl.glUniform4f(self.color_location, 0.0, 0.0, 1.0, 1.0)
        gl.glUniform2f(self.vertex_location, x, y)
        gl.glBindVertexArray(self.square.vao)
        gl.glDrawElements(
            gl.GL_TRIANGLES, self.square.square_index, gl.GL_UNSIGNED_INT, None
        )

    def render_level(self, level, level_index):
        for index, num in enumerate(str(level_index + 1)):
            x = (index * 1.15)
            y = 9
            self.render_obj(self.nums[int(num)], x, y, PURPLE)

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
                    color = BROWN
                    if obj == CB:
                        color = BLUE

                    self.render_obj(self.crate, x, y, color)
                if obj == P or obj == PB:
                    self.render_obj(self.player, x, y, YELLOW)

    def render(self, events):
        super().render(events)

        gl.glClearColor(0.0, 0.0, 0.0, 0.0)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.game.move_player(-1, 0)
                if event.key == pygame.K_RIGHT:
                    self.game.move_player(1, 0)
                if event.key == pygame.K_UP:
                    self.game.move_player(0, -1)
                if event.key == pygame.K_DOWN:
                    self.game.move_player(0, 1)
                if event.key == pygame.K_r:
                    self.game.reset_level()

        self.render_level(self.game.current_level, self.game.level_index)

        if self.game.check_win():
            print("You win")
            if not self.game.next_level():
                print("Game completed!")

    def de_init(self):
        super().de_init()
        self.square.de_init()
        self.wall.de_init()
        self.bomb.de_init()
        self.pixel.de_init()
        self.crate.de_init()
        self.player.de_init()
        for num in self.nums:
            num.de_init()
