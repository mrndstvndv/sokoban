import pygame
from pygame.locals import *
from OpenGL.GL import *
from shaders import create_shader_program
from objects import create_square

W = 1
C = 3
B = 4
P = 5
PB = 54
CB = 34

level = [
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

level = level_2


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_player_position():
    for y, i_val in enumerate(level):
        for x, j_val in enumerate(i_val):
            if j_val == P:
                return (x, y)
    return (0, 0)


x, y = get_player_position()
player = Player(x, y)


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

    VAO, EBO, square_index = create_square()
    glUseProgram(shader_program)

    vertex_location = glGetUniformLocation(shader_program, "offset")
    color_location = glGetUniformLocation(shader_program, "color")

    clock = pygame.time.Clock()
    running = True

    def render_square(x, y):
        glUniform4f(color_location, 1.0, 0.0, 1.0, 1.0)
        glUniform2f(vertex_location, x, y)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, square_index, GL_UNSIGNED_INT, None)

    def render_player(x, y):
        glUniform4f(color_location, 0.0, 1.0, 0.0, 1.0)
        glUniform2f(vertex_location, x, y)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, square_index, GL_UNSIGNED_INT, None)

    def render_crate(x, y):
        glUniform4f(color_location, 1.0, 0.0, 0.0, 1.0)
        glUniform2f(vertex_location, x, y)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, square_index, GL_UNSIGNED_INT, None)

    def render_bomb(x, y):
        glUniform4f(color_location, 0.0, 0.0, 1.0, 1.0)
        glUniform2f(vertex_location, x, y)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, square_index, GL_UNSIGNED_INT, None)

    def move_left(x, y) -> bool:
        status = level[y][x]
        nextobj = level[y][x - 1]

        if nextobj != W and nextobj != C:
            if nextobj == B:
                level[y][x - 1] = CB
            else:
                level[y][x - 1] = C

            if status == CB:
                level[y][x] = B
            else:
                level[y][x] = 0

            return True
        return False

    def move_right(x, y) -> bool:
        status = level[y][x]
        nextobj = level[y][x + 1]

        if nextobj != W and nextobj != C:
            if nextobj == B:
                level[y][x + 1] = CB
            else:
                level[y][x + 1] = C

            if status == CB:
                level[y][x] = B
            else:
                level[y][x] = 0

            return True
        return False

    def move_up(x, y) -> bool:
        status = level[y][x]
        nextobj = level[y - 1][x]

        if nextobj != W and nextobj != C:
            if nextobj == B:
                level[y - 1][x] = CB
            else:
                level[y - 1][x] = C

            if status == CB:
                level[y][x] = B
            else:
                level[y][x] = 0

            return True

        return False

    def move_down(x, y) -> bool:
        status = level[y][x]
        nextobj = level[y + 1][x]

        if nextobj != W and nextobj != C:
            if nextobj == B:
                level[y + 1][x] = CB
            else:
                level[y + 1][x] = C

            if status == CB:
                level[y][x] = B
            else:
                level[y][x] = 0

            return True
        return False

    def move_player_left():
        status = level[player.y][player.x]
        nextobj = level[player.y][player.x - 1]

        if nextobj != W:
            if nextobj == C or nextobj == CB:
                if not move_left(player.x - 1, player.y):
                    return

            if nextobj == B or nextobj == CB:
                level[player.y][player.x - 1] = PB
            else:
                level[player.y][player.x - 1] = P

            if status == PB:
                level[player.y][player.x] = B
            else:
                level[player.y][player.x] = 0

            player.x -= 1

    def move_player_right():
        status = level[player.y][player.x]
        nextobj = level[player.y][player.x + 1]

        if nextobj != W:
            if nextobj == C or nextobj == CB:
                if not move_right(player.x + 1, player.y):
                    return

            if nextobj == B or nextobj == CB:
                level[player.y][player.x + 1] = PB
            else:
                level[player.y][player.x + 1] = P

            if status == PB:
                level[player.y][player.x] = B
            else:
                level[player.y][player.x] = 0

            player.x += 1

    def move_player_up():
        status = level[player.y][player.x]
        nextobj = level[player.y - 1][player.x]

        if nextobj != W:
            if nextobj == C or nextobj == CB:
                if not move_up(player.x, player.y - 1):
                    return

            if nextobj == B or nextobj == CB:
                level[player.y - 1][player.x] = PB
            else:
                level[player.y - 1][player.x] = P

            if status == PB:
                level[player.y][player.x] = B
            else:
                level[player.y][player.x] = 0

            player.y -= 1

    def move_player_down():
        status = level[player.y][player.x]
        nextobj = level[player.y + 1][player.x]

        if nextobj != W:
            if nextobj == C or nextobj == CB:
                if not move_down(player.x, player.y + 1):
                    return

            if nextobj == B or nextobj == CB:
                level[player.y + 1][player.x] = PB
            else:
                level[player.y + 1][player.x] = P

            if status == PB:
                level[player.y][player.x] = B
            else:
                level[player.y][player.x] = 0

            player.y += 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_player_left()
                if event.key == pygame.K_RIGHT:
                    move_player_right()
                if event.key == pygame.K_UP:
                    move_player_up()
                if event.key == pygame.K_DOWN:
                    move_player_down()

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)

        num_rows = len(level)
        for row, r_val in enumerate(level):
            for col, obj in enumerate(r_val):
                x = col - 3.0
                y = (num_rows - 1 - row) - 3.0

                if obj == 1:
                    render_square(x, y)
                if obj == B:
                    render_bomb(x, y)
                if obj == C or obj == CB:
                    render_crate(x, y)
                if obj == P or obj == PB:
                    render_player(x, y)

        glBindVertexArray(0)

        thereIsBomb = False
        for i in level:
            for j in i:
                if j == B or j == PB:
                    thereIsBomb = True
                    break

        if thereIsBomb == False:
            print("you win")
                

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
