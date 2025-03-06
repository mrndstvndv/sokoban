import pygame
import copy
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


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self, levels):
        self.levels = levels
        self.level_index = 0
        self.current_level = copy.deepcopy(self.levels[self.level_index])
        self.player = self.init_player()
    
    def init_player(self):
        x, y = self.get_player_position(self.current_level)
        return Player(x, y)
    
    def get_player_position(self, level):
        for y, row in enumerate(level):
            for x, cell in enumerate(row):
                if cell == P or cell == PB:
                    return (x, y)
        return (0, 0)
    
    def reset_level(self):
        self.current_level = copy.deepcopy(self.levels[self.level_index])
        self.player = self.init_player()
    
    def next_level(self):
        self.level_index += 1
        if self.level_index < len(self.levels):
            self.reset_level()
            return True
        return False
    
    def check_win(self):
        for row in self.current_level:
            for cell in row:
                if cell == B or cell == PB:
                    return False
        return True
    
    def move_object(self, x, y, dx, dy):
        status = self.current_level[y][x]
        nextobj = self.current_level[y+dy][x+dx]
        
        if nextobj != W and nextobj != C and nextobj != CB:
            if nextobj == B:
                self.current_level[y+dy][x+dx] = CB
            else:
                self.current_level[y+dy][x+dx] = C
                
            if status == CB:
                self.current_level[y][x] = B
            else:
                self.current_level[y][x] = 0
                
            return True
        return False
    
    def move_player(self, dx, dy):
        status = self.current_level[self.player.y][self.player.x]
        nextobj = self.current_level[self.player.y+dy][self.player.x+dx]
        
        if nextobj != W:
            if nextobj == C or nextobj == CB:
                if not self.move_object(self.player.x+dx, self.player.y+dy, dx, dy):
                    return
            
            if nextobj == B or nextobj == CB:
                self.current_level[self.player.y+dy][self.player.x+dx] = PB
            else:
                self.current_level[self.player.y+dy][self.player.x+dx] = P
                
            if status == PB:
                self.current_level[self.player.y][self.player.x] = B
            else:
                self.current_level[self.player.y][self.player.x] = 0
                
            self.player.x += dx
            self.player.y += dy


class Renderer:
    def __init__(self, shader_program, VAO, square_index):
        self.shader_program = shader_program
        self.VAO = VAO
        self.square_index = square_index
        self.vertex_location = glGetUniformLocation(shader_program, "offset")
        self.color_location = glGetUniformLocation(shader_program, "color")
    
    def render_square(self, x, y):
        glUniform4f(self.color_location, 1.0, 0.0, 1.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.square_index, GL_UNSIGNED_INT, None)
    
    def render_player(self, x, y):
        glUniform4f(self.color_location, 0.0, 1.0, 0.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.square_index, GL_UNSIGNED_INT, None)
    
    def render_crate(self, x, y):
        glUniform4f(self.color_location, 1.0, 0.0, 0.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.square_index, GL_UNSIGNED_INT, None)
    
    def render_bomb(self, x, y):
        glUniform4f(self.color_location, 0.0, 0.0, 1.0, 1.0)
        glUniform2f(self.vertex_location, x, y)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.square_index, GL_UNSIGNED_INT, None)
    
    def render_level(self, level):
        num_rows = len(level)
        for row, r_val in enumerate(level):
            for col, obj in enumerate(r_val):
                x = col - 3.0
                y = (num_rows - 1 - row) - 3.0
                
                if obj == W:
                    self.render_square(x, y)
                if obj == B:
                    self.render_bomb(x, y)
                if obj == C or obj == CB:
                    self.render_crate(x, y)
                if obj == P or obj == PB:
                    self.render_player(x, y)


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

    clock = pygame.time.Clock()
    running = True
    
    game = Game(levels)
    renderer = Renderer(shader_program, VAO, square_index)

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
