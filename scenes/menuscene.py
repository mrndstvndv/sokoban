from math import remainder
from typing import Callable, List, Tuple
from OpenGL.GL import *
import pygame
from pygame.event import Event
from assets.text import Options, Play
import config
from game import PB
from objects import Object, Rectangle
from scenes.gamescene import PURPLE
from scenes.scene import Scene
from config import gl
from utils import Vec2f, normalize
import utils


class Button:
    on_click: Callable[[], None]

    def __init__(
        self, position: Vec2f, scale: float, max_scale: float, obj: Object, shader
    ) -> None:
        self.obj = obj
        self.initial_scale = scale
        self.current_scale = scale
        self.max_scale = max_scale
        self.color_location = gl.glGetUniformLocation(shader, "color")
        self.offset_location = gl.glGetUniformLocation(shader, "offset")
        self.scale_location = gl.glGetUniformLocation(shader, "scale")
        self.position = position
        self.bounds = self.get_bounds()

    def get_bounds(self):
        shape_bounds: Tuple[Vec2f, Vec2f] | None = self.obj.shape.get_bounds()

        if shape_bounds == None:
            Exception("Bounds not found")

        start, end = shape_bounds

        return (
            Vec2f(start.x + self.position.x, start.y + self.position.y),
            Vec2f(end.x + self.position.x, end.y + self.position.y),
        )

    def set_position(self, pos: Vec2f):
        self.position = pos
        self.bounds = self.get_bounds()

    def render_obj_old(self, object: Object, scale, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.offset_location, *self.position)
        gl.glUniform1f(self.scale_location, scale)
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(GL_TRIANGLES, object.index, gl.GL_UNSIGNED_INT, None)

    def in_bounds(self, pos: Vec2f) -> bool:
        shape_bounds: Tuple[Vec2f, Vec2f] | None = self.bounds

        start, end = shape_bounds

        return (
            pos.x >= start.x and pos.x <= end.x and pos.y <= start.y and pos.y >= end.y
        )

    def set_on_click(self, callback: Callable[[], None]) -> None:
        self.on_click = callback

    def render(self, events: List[Event]):
        self.render_obj_old(self.obj, self.current_scale, (1.0, 1.0, 1.0, 1.0))

        mx, my = pygame.mouse.get_pos()
        mouse_pos = normalize(mx, my)

        in_bounds = self.in_bounds(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if in_bounds:
                    self.current_scale = 1.0
            elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:
                if in_bounds:
                    self.on_click()
            else:
                if self.in_bounds(mouse_pos):
                    if self.current_scale < self.max_scale:
                        self.current_scale += 0.1
                else:
                    if self.current_scale > 1:
                        self.current_scale -= 0.1


class MenuScene(Scene):
    max_scale = 1.1
    current_scale = 1
    load = False

    def __init__(self, shader) -> None:
        super().__init__(shader)
        self.color_location = gl.glGetUniformLocation(shader, "color")
        self.offset_location = gl.glGetUniformLocation(shader, "offset")
        self.scale_location = gl.glGetUniformLocation(shader, "scale")
        self.rectangle = Rectangle(Vec2f(-4.0, 1.0), Vec2f(4.0, -1.0))
        self.pbtn = Button(Vec2f(0.0, 1.25), 1.0, 1.1, Play(), shader)
        self.obtn = Button(Vec2f(0.0, -1.25), 1.0, 1.1, Options(), shader)
        self.pbtn.set_on_click(
            lambda: utils.post_event(config.BUTTON_CLICKED, button="play")
        )
        self.obtn.set_on_click(lambda: print("play button clicked!"))

    def render_obj(self, object: Object, scale, color):
        gl.glUniform4f(self.color_location, color[0], color[1], color[2], color[3])
        gl.glUniform2f(self.offset_location, 0.0, 0.0)
        gl.glUniform1f(self.scale_location, scale)
        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(GL_TRIANGLE_FAN, object.index, gl.GL_UNSIGNED_INT, None)

    def render(self, events) -> None:
        super().render(events)
        gl.glClearColor(1.0, 1.0, 0.0, 1.0)

        self.pbtn.render(events)
        self.obtn.render(events)

        # self.render_obj_old(self.a, self.current_scale * 20, (1.0, 1.0, 1.0, 1.0))

    def de_init(self) -> None:
        super().de_init()
        self.rectangle.de_init()
