from math import remainder
from OpenGL.GL import *
import pygame
from assets.text import A
from objects import Object, Rectangle
from scenes.gamescene import PURPLE
from scenes.scene import Scene
from config import gl
from utils import Vec2f, normalize


class MenuScene(Scene):
    max_scale = 1.1
    current_scale = 1

    def __init__(self, shader) -> None:
        super().__init__(shader)
        self.color_location = gl.glGetUniformLocation(shader, "color")
        self.offset_location = gl.glGetUniformLocation(shader, "offset")
        self.scale_location = gl.glGetUniformLocation(shader, "scale")
        self.rectangle = Rectangle(Vec2f(-4.0, 1.0), Vec2f(4.0, -1.0))
        self.a = A()

    def render_obj(self, object: Object, scale, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.offset_location, 0.0, 0.0)
        gl.glUniform1f(self.scale_location, scale)
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(GL_TRIANGLE_FAN, object.index, gl.GL_UNSIGNED_INT, None)

    def render_obj_old(self, object: Object, scale, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.offset_location, 0.0, 0.0)
        gl.glUniform1f(self.scale_location, scale)
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(GL_TRIANGLES, object.index, gl.GL_UNSIGNED_INT, None)

    def render(self, events) -> None:
        super().render(events)

        mx, my = pygame.mouse.get_pos()
        mouse_pos = normalize(mx, my)

        print(f"MOUSE: {mouse_pos.x}, {mouse_pos.y}")

        if self.rectangle.in_bounds(mouse_pos):
            print("in bounds")
            if self.current_scale < self.max_scale:
                self.current_scale += 0.1
        else:
            if self.current_scale > 1:
                self.current_scale -= 0.1

        self.render_obj(self.rectangle, self.current_scale, PURPLE)

        self.render_obj_old(self.a, self.current_scale*4.5, (1.0, 1.0, 1.0, 1.0))

    def de_init(self) -> None:
        super().de_init()
        self.rectangle.de_init()
