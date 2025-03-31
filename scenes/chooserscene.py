from typing import List

import pygame
from config import GOTO, LEVEL_CHOSEN
from game import Game
from scenes.menuscene import Button
from scenes.scene import Scene
from pygame.event import Event
from objects import *
import utils


class ChooserScene(Scene):
    def __init__(self, game: Game, shader, max_level: int) -> None:
        super().__init__(shader)
        self.max_level = max_level
        self.game = game

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

        buttons = []

        # Calculate the total width needed for buttons in a row (4 buttons per row)
        buttons_per_row = 4
        total_width = min(buttons_per_row, max_level + 1) * 2.0
        # Start position (left edge) to center all buttons
        start_x = -total_width / 2

        for i in range(max_level + 1):
            level = i + 1
            # Calculate row and column position
            row = i // buttons_per_row
            col = i % buttons_per_row

            # Position x based on column, y based on row (negative y for rows below the first)
            x = start_x + col * 2.0
            y = -row * 1.5  # Offset rows vertically with some spacing

            btn = Button(Vec2f(x, y), 1.0, 1.2, self.nums[level], shader)
            btn.set_on_click(lambda level=i: self.set_level(level))

            buttons.append(btn)

        self.buttons: List[Button] = buttons

        super().__init__(shader)

    def set_level(self, level_index: int):
        self.game.level_index = level_index
        self.game.reset_level()
        utils.post_event(LEVEL_CHOSEN)

    def render(self, events: List[Event]) -> None:
        gl.glClearColor(0.043, 0.541, 0.561, 1.0)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    utils.post_event(GOTO, scene="MENU")

        for btn in self.buttons:
            btn.render(events)
