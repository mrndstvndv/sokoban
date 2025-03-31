from typing import List
from assets import text
from assets.text import *
from game import P, PB, W, B, C, CB, Game
import levels
import pygame
from objects import Object, Rectangle, Square
from scenes.scene import Scene
from pygame.event import Event
from OpenGL.GL import *
from config import gl
from utils import Vec2f


class GamePixelScene(Scene):
    def __init__(self, shader) -> None:
        super().__init__(shader)
        self.color_location = gl.glGetUniformLocation(shader, "color")
        self.offset_location = gl.glGetUniformLocation(shader, "offset")
        self.scale_location = gl.glGetUniformLocation(shader, "scale")
        self.opacity_location = gl.glGetUniformLocation(shader, "opacity")
        self.crate = PixelCrate()
        self.wall = PixelWall()
        self.walltd = WallTopDown()
        self.wallld = WallLeftDown()
        self.walllr = WallLeftRight()
        self.walldr = WallDownRight()
        self.walld = WallDown()
        self.wallt = WallTop()
        self.wallr = WallLeft()
        self.walll = WallRight()
        self.walltr = WallTopRight()
        self.walllt = WallLeftTop()
        self.walltdr = WallTopDownRight()
        self.walltlr = WallTopLeftRight()
        self.walldlr = WallDownLeftRight()
        self.walltdl = WallTopDownLeft()
        self.walltl = WallTopLeft()
        self.bomb = PixelBomb()
        self.grass = PixelGrass()
        self.player = PixelPlayer()
        self.game = Game(levels.levels)
        start, end = self.crate.shape.get_bounds()
        self.width = end.x - start.x

    def render_obj_old(self, object: Object, position, scale, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.offset_location, *position)
        gl.glUniform1f(self.scale_location, scale)
        gl.glUniform1f(self.opacity_location, color[3])
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, object.index, gl.GL_UNSIGNED_INT, None)

    def render(self, events: List[Event]) -> None:
        num_rows = len(self.game.current_level)

        gl.glClearColor(0.043, 0.541, 0.561, 1.0)

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

        for row, r_val in enumerate(self.game.current_level):
            for col, obj in enumerate(r_val):
                # Center the level and reverse columns to fix orientation
                x = (col - 2.0) * self.width
                y = ((num_rows - 1 - row) - num_rows / 2) * self.width

                if obj == W:
                    top = self.game.current_level[row - 1][col] if row > 0 else None
                    down = (
                        self.game.current_level[row + 1][col]
                        if row < num_rows - 1
                        else None
                    )
                    left = self.game.current_level[row][col - 1] if col > 0 else None
                    right = (
                        self.game.current_level[row][col + 1]
                        if col < len(r_val) - 1
                        else None
                    )

                    if top == W and down == W and right == W:
                        self.render_obj_old(
                            self.walltdr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif top == W and left == W and right == W:
                        self.render_obj_old(
                            self.walltlr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif top == W and down == W and left == W:
                        self.render_obj_old(
                            self.walltdl, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif down == W and left == W and right == W:
                        self.render_obj_old(
                            self.walldlr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif top == W and left == W:
                        self.render_obj_old(
                            self.walltl, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif top == W and down == W:
                        self.render_obj_old(
                            self.walltd, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif left == W and down == W:
                        self.render_obj_old(
                            self.wallld, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif left == W and right == W:
                        self.render_obj_old(
                            self.walllr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif down == W and right == W:
                        self.render_obj_old(
                            self.walldr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif top == W and right == W:
                        self.render_obj_old(
                            self.walltr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif left == W and top == W:
                        self.render_obj_old(
                            self.walllt, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif down == W:
                        self.render_obj_old(
                            self.walld, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif top == W:
                        self.render_obj_old(
                            self.wallt, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif left == W:
                        self.render_obj_old(
                            self.walll, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    elif right == W:
                        self.render_obj_old(
                            self.wallr, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )
                    else:
                        self.render_obj_old(
                            self.wall, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0)
                        )

                if obj == C:
                    self.render_obj_old(self.crate, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0))

                if obj == CB:
                    self.render_obj_old(self.bomb, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0))
                    self.render_obj_old(self.crate, (x, y), 1.0, (1.0, 1.0, 1.0, 0.8))

                if obj == B:
                    self.render_obj_old(self.bomb, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0))

                if obj == P:
                    self.render_obj_old(self.player, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0))

                if obj == PB:
                    self.render_obj_old(self.bomb, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0))
                    self.render_obj_old(self.player, (x, y), 1.0, (1.0, 1.0, 1.0, 1.0))

        if self.game.check_win():
            print("You win")
            if not self.game.next_level():
                print("Game completed!")
