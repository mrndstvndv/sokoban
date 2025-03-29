from OpenGL.GL import *
import pygame
from objects import Object, Rectangle
from scenes.gamescene import PURPLE
from scenes.scene import Scene
from config import gl
from utils import normalize


class MenuScene(Scene):
    def __init__(self, shader) -> None:
        super().__init__(shader)
        self.color_location = gl.glGetUniformLocation(shader, "color")
        self.vertex_location = gl.glGetUniformLocation(shader, "offset")
        self.rectangle = Rectangle()

    def render_obj(self, object: Object, x, y, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.vertex_location, x, y)
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(GL_TRIANGLE_FAN, object.index, gl.GL_UNSIGNED_INT, None)

    def render(self, events) -> None:
        super().render(events)

        mx, my = pygame.mouse.get_pos()
        mx, my = normalize(mx, my)

        print(f"MOUSE: {mx}, {my}")

        self.render_obj(self.rectangle, mx, my, PURPLE)

    def de_init(self) -> None:
        super().de_init()
        self.rectangle.de_init()
