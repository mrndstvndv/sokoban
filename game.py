from player import Player
import copy

W = 1
C = 3
B = 4
P = 5
G = 6
PB = 54
CB = 34

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
