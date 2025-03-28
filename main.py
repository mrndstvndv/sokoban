import pygame
from pygame.locals import *
from shaders import create_shader_program
from renderer import Renderer
from game import Game
from levels import levels
from config import gl, context


def main():
    pygame.init()
    display = (600, 600)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, context
    )
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gl.glViewport(0, 0, 600, 600)
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)

    shader_program = create_shader_program()
    gl.glUseProgram(shader_program)

    clock = pygame.time.Clock()
    running = True

    game = Game(levels)
    renderer = Renderer(shader_program)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.move_player(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.move_player(1, 0)
                if event.key == pygame.K_UP:
                    game.move_player(0, -1)
                if event.key == pygame.K_DOWN:
                    game.move_player(0, 1)
                if event.key == pygame.K_r:
                    game.reset_level()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glUseProgram(shader_program)

        renderer.render_level(game.current_level, game.level_index)

        gl.glBindVertexArray(0)

        if game.check_win():
            print("You win")
            if not game.next_level():
                print("Game completed!")
                running = False

        pygame.display.flip()
        clock.tick(60)

    # WARN: I do not think we are doing deinit right, macos lags when the game is running I think that python is just cpu intensive
    renderer.de_init()
    gl.glDeleteProgram(shader_program)
    pygame.quit()


if __name__ == "__main__":
    main()
