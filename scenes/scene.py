from typing import List

from pygame.event import Event
from config import gl
from objects import CircleGenerator
from shaders import create_shader_program


class Scene:
    shader = None

    def __init__(self, shader) -> None:
        self.shader = shader

    def render(self, events: List[Event]) -> None:
        gl.glUseProgram(self.shader)

    def de_init(self) -> None:
        if self.shader != None:
            gl.glDeleteProgram(self.shader)
