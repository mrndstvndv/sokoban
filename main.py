import pygame
from pygame.locals import *
from assets.text import PixelCrate
import config
from game import Game
import levels
from scenes import Scene, GameScene, MenuScene, chooserscene
from scenes.gamepixelscene import GamePixelScene
from shaders import create_shader_program
from config import DISPLAY_HEIGHT, DISPLAY_WIDTH, GOTO, gl, context
import shaders


def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, context)
    pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)

    gl.glEnable(gl.GL_BLEND);
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);

    gl.glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)

    clock = pygame.time.Clock()
    running = True

    shader = create_shader_program(
        shaders.vertex_shader_src, shaders.fragment_shader_src
    )

    game = Game(levels.levels)

    gamePixelScene: GamePixelScene = GamePixelScene(game, shader)
    gameScene: GameScene = GameScene(shader)
    menuScene: MenuScene = MenuScene(shader)

    currentScene: Scene = menuScene

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == config.LEVEL_CHOSEN:
                currentScene = gamePixelScene

            if event.type == config.BUTTON_CLICKED:
                if event.button == "play":
                    if game.load_level() != 0:
                        currentScene = chooserscene.ChooserScene(game, shader, game.load_level())
                    else:
                        currentScene = gamePixelScene

            if event.type == config.GOTO:
                if event.scene == "MENU":
                    currentScene = menuScene

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_2:
                    currentScene = menuScene
                if event.key == pygame.K_1:
                    currentScene = gameScene
                if event.key == pygame.K_3:
                    currentScene = gamePixelScene

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        currentScene.render(events)

        gl.glBindVertexArray(0)

        pygame.display.flip()
        clock.tick(60)

    gameScene.de_init()
    pygame.quit()


if __name__ == "__main__":
    main()
