from typing import List
from scenes.scene import Scene
from pygame.event import Event


class OptionsScene(Scene):
    def __init__(self, shader) -> None:
        super().__init__(shader)

    def render(self, events: List[Event]) -> None:
        return super().render(events)
