import pygame
from pygame.locals import *
from OpenGL.GL import *
from shaders import create_shader_program
from renderer import Renderer
from game import Game, W, C, B, P, PB, CB

level_1 = [
    [0, 0, W, W, W, 0, 0, 0, 0],
    [0, 0, W, B, W, 0, 0, 0, 0],
    [0, 0, W, 0, W, W, W, W, 0],
    [W, W, W, C, 0, C, B, W, 0],
    [W, B, 0, C, P, W, W, W, 0],
    [W, W, W, W, C, W, 0, 0, 0],
    [0, 0, 0, W, B, W, 0, 0, 0],
    [0, 0, 0, W, W, W, 0, 0, 0],
]

level_2 = [
    [W, W, W, W, W],
    [W, 0, 0, 0, W],
    [W, 0, C, 0, W, 0, W, W, W],
    [W, 0, C, P, W, 0, W, B, W],
    [W, W, W, C, W, W, W, B, W],
    [0, W, W, 0, 0, 0, 0, B, W],
    [0, W, 0, 0, 0, W, 0, 0, W],
    [0, W, 0, 0, 0, W, W, W, W],
    [0, W, W, W, W, W, W, W, W],
]


level_3 = [
    [0, W, W, W, W],
    [W, W, 0, 0, W],
    [W, 0, P, C, W],
    [W, W, C, 0, W, W],
    [W, W, 0, C, 0, W],
    [W, B, C, 0, 0, W],
    [W, B, B, CB, B, W],
    [W, W, W, W, W, W],
]

level_4 = [
    [0, W, W, W, W],
    [0, W, 0, 0, W, W, W],
    [0, W, 0, 0, 0, 0, W],
    [W, W, W, C, W, P, W, W],
    [W, B, W, 0, W, 0, 0, W],
    [W, B, C, 0, 0, W, 0, W],
    [W, B, 0, 0, 0, C, 0, W],
    [W, W, W, W, W, W, W, W],
]

levels = [level_1, level_2, level_3, level_4]

def main():
    pygame.init()
    display = (600, 600)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glViewport(0, 0, 600, 600)
    glClearColor(0.0, 0.0, 0.0, 0.0)

    shader_program = create_shader_program()
    glUseProgram(shader_program)

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

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)
        
        renderer.render_level(game.current_level)
        
        glBindVertexArray(0)

        if game.check_win():
            print("You win")
            if not game.next_level():
                print("Game completed!")
                running = False

        pygame.display.flip()
        clock.tick(60)

    delete_object(VAO, EBO)
    glDeleteProgram(shader_program)
    pygame.quit()


def delete_object(VAO, EBO):
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [EBO])


if __name__ == "__main__":
    main()
