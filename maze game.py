import random
import numpy as np
import pygame
import sys
import math
import socket
import threading
import pickle

Maze_rows = 20
Maze_cols = 20

Game = {
    "system":{
        "window width": 640,
        "window height": 480,
        "running": True,
        "background music": ("Darktown Strutters Ball.wav", "Lovable Clown Sit Com.wav", "Entire.wav", "Lucid Dreamer.wav", "Sunspots.wav")
    },
    "screen":{
        "start": True,
        "difficulty": False,
        "game": False,
        "result": False,
        "setting": False,
        "score": False,
        "room": False,
    },
    "variables":{
        "maze": np.zeros((Maze_rows, Maze_cols, 5), dtype=np.uint8),
        "seed": 0,
        "computer speed": 2,
        "historical record":{
            "easy": [],
            "normal": [],
            "hard": [],
        },
        "computer record":{
            "easy": [],
            "normal": [],
            "hard": [],
        },
        "connections":{
            "socket": [],
            "IP": [],
            "position": [],
            "color":[],
            "prepare": [],
        },
    },
    "setting":{
        "game mode": 0,
        "player number": 1,
        "connect":{
            "role": None,
            "room": None,
            "port": 6000,
        },
        "computer solver": 0,
        "difficulty": "",
    },
}

class generate_maze:
    def set_seed(self):
        if Game['variables']['seed'] == 0:
            Game['variables']['seed'] = random.randint(1111111111, 9999999999)
        random.seed(int(Game['variables']['seed']))

    def dfs(self):
        self.set_seed()
        M = np.zeros((Maze_rows,Maze_cols,5), dtype=np.uint8)
        r = 0
        c = 0
        history = [(r,c)]

        while history:
            M[r,c,4] = 1
            check = []
            if c > 0 and M[r,c-1,4] == 0:
                check.append('L')
            if r > 0 and M[r-1,c,4] == 0:
                check.append('U')
            if c < Maze_cols-1 and M[r,c+1,4] == 0:
                check.append('R')
            if r < Maze_rows-1 and M[r+1,c,4] == 0:
                check.append('D')

            if len(check):
                history.append([r,c])
                move_direction = random.choice(check)
                if move_direction == 'L':
                    M[r,c,0] = 1
                    c = c-1
                    M[r,c,2] = 1
                if move_direction == 'U':
                    M[r,c,1] = 1
                    r = r-1
                    M[r,c,3] = 1
                if move_direction == 'R':
                    M[r,c,2] = 1
                    c = c+1
                    M[r,c,0] = 1
                if move_direction == 'D':
                    M[r,c,3] = 1
                    r = r+1
                    M[r,c,1] = 1
            else:
                r,c = history.pop()

        M[0,0,0] = 1
        M[Maze_rows-1,Maze_cols-1,2] = 1
        return M

    def prim(self):
        self.set_seed()
        M = np.zeros((Maze_rows,Maze_cols,5), dtype=np.uint8)
        r = 0
        c = 0
        history = [(r,c)]

        while history:
            r,c = random.choice(history)
            M[r,c,4] = 1
            history.remove((r,c))
            check = []
            if c > 0:
                if M[r,c-1,4] == 1:
                    check.append('L')
                elif M[r,c-1,4] == 0:
                    history.append((r,c-1))
                    M[r,c-1,4] = 2
            if r > 0:
                if M[r-1,c,4] == 1:
                    check.append('U')
                elif M[r-1,c,4] == 0:
                    history.append((r-1,c))
                    M[r-1,c,4] = 2
            if c < Maze_cols-1:
                if M[r,c+1,4] == 1:
                    check.append('R')
                elif M[r,c+1,4] == 0:
                    history.append((r,c+1))
                    M[r,c+1,4] = 2
            if r < Maze_rows-1:
                if M[r+1,c,4] == 1:
                    check.append('D')
                elif  M[r+1,c,4] == 0:
                    history.append((r+1,c))
                    M[r+1,c,4] = 2

            if len(check):
                move_direction = random.choice(check)
                if move_direction == 'L':
                    M[r,c,0] = 1
                    c = c-1
                    M[r,c,2] = 1
                if move_direction == 'U':
                    M[r,c,1] = 1
                    r = r-1
                    M[r,c,3] = 1
                if move_direction == 'R':
                    M[r,c,2] = 1
                    c = c+1
                    M[r,c,0] = 1
                if move_direction == 'D':
                    M[r,c,3] = 1
                    r = r+1
                    M[r,c,1] = 1

        M[0,0,0] = 1
        M[Maze_rows-1,Maze_cols-1,2] = 1
        return M

    def Recursive_division(self, r1, r2, c1, c2, M):
        if r1 < r2 and c1 < c2:
            rm = random.randint(r1, r2-1)
            cm = random.randint(c1, c2-1)
            cd1 = random.randint(c1,cm)
            cd2 = random.randint(cm+1,c2)
            rd1 = random.randint(r1,rm)
            rd2 = random.randint(rm+1,r2)
            d = random.randint(1,4)
            if d == 1:
                M[rd2, cm, 2] = 1
                M[rd2, cm+1, 0] = 1
                M[rm, cd1, 3] = 1
                M[rm+1, cd1, 1] = 1
                M[rm, cd2, 3] = 1
                M[rm+1, cd2, 1] = 1
            elif d == 2:
                M[rd1, cm, 2] = 1
                M[rd1, cm+1, 0] = 1
                M[rm, cd1, 3] = 1
                M[rm+1, cd1, 1] = 1
                M[rm, cd2, 3] = 1
                M[rm+1, cd2, 1] = 1
            elif d == 3:
                M[rd1, cm, 2] = 1
                M[rd1, cm+1, 0] = 1
                M[rd2, cm, 2] = 1
                M[rd2, cm+1, 0] = 1
                M[rm, cd2, 3] = 1
                M[rm+1, cd2, 1] = 1
            elif d == 4:
                M[rd1, cm, 2] = 1
                M[rd1, cm+1, 0] = 1
                M[rd2, cm, 2] = 1
                M[rd2, cm+1, 0] = 1
                M[rm, cd1, 3] = 1
                M[rm+1, cd1, 1] = 1

            self.Recursive_division(r1, rm, c1, cm, M)
            self.Recursive_division(r1, rm, cm+1, c2, M)
            self.Recursive_division(rm+1, r2, cm+1, c2, M)
            self.Recursive_division(rm+1, r2, c1, cm, M)

        elif r1 < r2:
            rm = random.randint(r1, r2-1)
            M[rm,c1,3] = 1
            M[rm+1,c1,1] = 1
            self.Recursive_division(r1, rm, c1, c1, M)
            self.Recursive_division(rm+1, r2, c1, c1, M)
        elif c1 < c2:
            cm = random.randint(c1,c2-1)
            M[r1,cm,2] = 1
            M[r1,cm+1,0] = 1
            self.Recursive_division(r1, r1, c1, cm, M)
            self.Recursive_division(r1, r1, cm+1, c2, M)

    def recursive(self):
        self.set_seed()
        r1 = 0
        r2 = Maze_rows-1
        c1 = 0
        c2 = Maze_cols-1
        M = np.zeros((Maze_rows,Maze_cols,5), dtype=np.uint8)
        self.Recursive_division(r1, r2, c1, c2, M)
        M[0,0,0] = 1
        M[Maze_rows-1,Maze_cols-1,2] = 1
        return M

class StartScreen:
    def __init__(self, screen):
        self.button_font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)
        self.start_button = Button("Start", (Game['system']['window width']/2, Game['system']['window height']*3/7), self.button_font, 150)
        self.setting_button = Button("Setting", (Game['system']['window width']/2, Game['system']['window height']*4/7), self.button_font, 150)
        self.score_button = Button("Score", (Game['system']['window width']/2, Game['system']['window height']*5/7), self.button_font, 150)
        self.quit_button = Button("Quit", (Game['system']['window width']/2, Game['system']['window height']*6/7), self.button_font, 150)
        self.title = Text("Maze Game", (Game['system']['window width']/2, Game['system']['window height']/5), self.title_font)
        self.screen = screen
        self.clock = pygame.time.Clock()

    def run(self):
        running = Game['screen']['start']
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['start'] = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.rect.collidepoint(event.pos):
                        Game['screen']['difficulty'] = True
                        Game['screen']['start'] = False
                        running = False
                    elif self.quit_button.rect.collidepoint(event.pos):
                        Game['system']['running'] = False
                        Game['screen']['start'] = False
                        sys.exit()
                    elif self.setting_button.rect.collidepoint(event.pos):
                        Game['screen']['setting'] = True
                        Game['screen']['start'] = False
                        running = False
                    elif self.score_button.rect.collidepoint(event.pos):
                        Game['screen']['score'] = True
                        Game['screen']['start'] = False
                        running = False
            self.screen.fill((255, 255, 255))
            self.title.draw(self.screen)
            self.start_button.draw(self.screen)
            self.setting_button.draw(self.screen)
            self.score_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class DifficultyScreen:
    def __init__(self, screen):
        self.button_font = pygame.font.SysFont(None, 40)
        self.easy_button = Button("Easy", (Game['system']['window width']/4, Game['system']['window height']/2), self.button_font, 150)
        self.normal_button = Button("Normal", (Game['system']['window width']*2/4, Game['system']['window height']/2), self.button_font, 150)
        self.hard_button = Button("Hard", (Game['system']['window width']*3/4, Game['system']['window height']/2), self.button_font, 150)
        self.maze = generate_maze()
        self.screen = screen
        self.clock = pygame.time.Clock()

    def run(self):
        running = Game['screen']['difficulty']
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['difficulty'] = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.easy_button.rect.collidepoint(event.pos):
                        Game['variables']['maze'] = self.maze.recursive()
                        Game['setting']['difficulty'] = "easy"
                        Game['screen']['game'] = True
                        Game['screen']['difficulty'] = False
                        running = False
                    elif self.normal_button.rect.collidepoint(event.pos):
                        Game['variables']['maze'] = self.maze.dfs()
                        Game['setting']['difficulty'] = "normal"
                        Game['screen']['game'] = True
                        Game['screen']['difficulty'] = False
                        running = False
                    elif self.hard_button.rect.collidepoint(event.pos):
                        Game['variables']['maze'] = self.maze.prim()
                        Game['setting']['difficulty'] = "hard"
                        Game['screen']['game'] = True
                        Game['screen']['difficulty'] = False
                        running = False
            self.screen.fill((255, 255, 255))
            self.easy_button.draw(self.screen)
            self.normal_button.draw(self.screen)
            self.hard_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.time_font = pygame.font.SysFont(None, 30)
        self.seed_font = pygame.font.SysFont(None, 25)
        self.button_font = pygame.font.SysFont(None, 25)
        self.sol_button = Button("Solution", (Game['system']['window width'] - 60, Game['system']['window height'] - 30), self.button_font, 100)
        self.back_button = Button("Back to menu", (70, 30), self.button_font, 130)
        self.clock = pygame.time.Clock()

    def run(self):
        running = Game['screen']['game']
        self.generate_walls(Game['variables']['maze'])
        player = Player(self.origin_pos_x + 3, self.origin_pos_y + 3, 10, 10, (255, 0, 0), self.screen)
        computer = MazeSolver(Game['variables']['maze'])
        computer.initialize()
        computer2 = MazeSolver2(Game['variables']['maze'],self.origin_pos_x + 3, self.origin_pos_y + 3, 10, 10, (255, 0, 0), self.screen)
        computer2.initialize()
        Game['setting']['computer solver'] = 0
        pos = [self.origin_pos_x + 10.5, self.origin_pos_y + 10.5]
        direction_list = computer.direction_list()
        direction = ""
        Game['variables']['computer speed'] = 2
        d = 0
        step = 0
        game_start = False
        time_event = pygame.USEREVENT + 1
        pygame.time.set_timer(time_event, 100)
        time_elapsed = 0
        Game['variables']['computer record'][Game['setting']['difficulty']].append(99999)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['game'] = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sol_button.rect.collidepoint(event.pos):
                        Game['setting']['computer solver'] = 1
                        pos = [self.origin_pos_x + 10.5, self.origin_pos_y + 10.5]
                        d = 0
                        step = 0
                    elif self.back_button.rect.collidepoint(event.pos):
                        Game['screen']['start'] = True
                        Game['screen']['game'] = False
                        running = False
                elif event.type == pygame.KEYDOWN:
                    game_start = True
                elif event.type == time_event:
                    if game_start:
                        time_elapsed += 1

            self.screen.fill((255, 255, 255))
            for i in range(len(self.walls)):
                self.walls[i].draw()
            player.update(self.walls)
            if player.current_pos_x() >= self.origin_pos_x + (Maze_cols - 1) * 18 and player.current_pos_y() >= self.origin_pos_y + (Maze_rows - 1) * 18 + 3:
                Game['screen']['result'] = True
                Game['screen']['game'] = False
                Game['variables']['historical record'][Game['setting']['difficulty']].append(time_elapsed // 10)
                running = False

            if Game['setting']['computer solver'] == 1:
                Game['variables']['computer record'][Game['setting']['difficulty']].append(99999)
                pygame.draw.circle(self.screen, (0, 0, 255), tuple(pos), 5)
                if d < len(direction_list):
                    direction = direction_list[d]
                    step += Game['variables']['computer speed']
                    if direction == 'right':
                        pos[0] += Game['variables']['computer speed']
                    elif direction == 'left':
                        pos[0] -= Game['variables']['computer speed']
                    elif direction == 'up':
                        pos[1] -= Game['variables']['computer speed']
                    elif direction == 'down':
                        pos[1] += Game['variables']['computer speed']
                    if step == 18:
                        step = 0
                        d += 1
            if Game['setting']['computer solver'] == 0:
                
                if computer2.finaltop!=-1 and time_elapsed // 10 >= 30 :
                    pygame.draw.circle(self.screen, (0, 255, 0), tuple(pos), 5)
                    count = 9
                    d = computer2.finalpath.pop()
                    computer2.finaltop -=1
                    print(d)
                    x=d[0]
                    y=d[1]
                    pos[0]= self.origin_pos_x + 9*y
                    pos[1]= self.origin_pos_y + 9*x
                    if computer2.finaltop ==-1:    
                        Game['variables']['computer record'][Game['setting']['difficulty']].append(time_elapsed // 10)
            time_str = f"{time_elapsed // 10}" + "s"
            begin_str = f"{30-(time_elapsed // 10)}" + "s"
            computer_str=" Computer will start in : "
            t_str=" Time: "
            self.t_text = Text(t_str, (Game['system']['window width'] - 50, 70), self.time_font)
            self.t_text.draw(self.screen)
            self.time_text = Text(time_str, (Game['system']['window width'] - 50, 90), self.time_font)
            self.time_text.draw(self.screen)
            if Game['setting']['computer solver'] == 0:
                if time_elapsed // 10 < 30 :
                    self.computer_text = Text(computer_str, (Game['system']['window width'] - 170, 20), self.time_font)
                    self.computer_text.draw(self.screen)
                    self.begin_text = Text(begin_str, (Game['system']['window width'] - 35, 20), self.time_font)
                    self.begin_text.draw(self.screen)
            self.seed_text = f"seed: {Game['variables']['seed']}"
            self.seed = Text(self.seed_text,(80, Game['system']['window height'] - 20), self.seed_font)
            self.seed.draw(self.screen)
            self.sol_button.draw(self.screen)
            self.back_button.draw(self.screen)
            self.clock.tick(60)
            pygame.display.flip()

    def generate_players(self):
        self.Players = []
        for i in range(Game['setting']['player number']):
            self.Players.append(Player(self.origin_pos_x + 3, self.origin_pos_y + 10, 10, 10, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), self.screen))

    def generate_walls(self, maze):
        self.origin_pos_x = (Game['system']['window width'] - Maze_cols * 15 - (Maze_cols + 1) * 3) / 2
        self.origin_pos_y = (Game['system']['window height'] - Maze_rows * 15 - (Maze_rows + 1) * 3) / 2
        self.walls = []
        for y in range(Maze_rows):
            for x in range(Maze_cols):
                for i in range(4):
                    if maze[y, x, i] == 0:
                        if i == 0:
                            self.walls.append(Wall((self.origin_pos_x + x * 18, self.origin_pos_y + y * 18), 3, 21, (0,0,0), self.screen))
                        elif i == 1:
                            self.walls.append(Wall((self.origin_pos_x + x * 18, self.origin_pos_y + y * 18), 21, 3, (0,0,0), self.screen))
                        elif i == 2:
                            self.walls.append(Wall((self.origin_pos_x + x * 18 + 18, self.origin_pos_y + y * 18), 3, 21, (0,0,0), self.screen))
                        elif i == 3:
                            self.walls.append(Wall((self.origin_pos_x + x * 18, self.origin_pos_y + y * 18 + 18), 21, 3, (0,0,0), self.screen))

class ResultScreen:
    def __init__(self, screen):
        self.button_font = pygame.font.SysFont(None, 40)
        self.text_font = pygame.font.SysFont(None, 50)
        self.back_button = Button("Menu", (Game['system']['window width']/4, Game['system']['window height']*5/7), self.button_font, 150)
        self.retry_button = Button("Retry", (Game['system']['window width']/2, Game['system']['window height']*5/7), self.button_font, 150)
        self.quit_button = Button("Quit", (Game['system']['window width']*3/4, Game['system']['window height']*5/7), self.button_font, 150)
        self.screen = screen
        self.clock = pygame.time.Clock()

    def run(self):
        running = Game['screen']['result']
        current = f"current time : {Game['variables']['historical record'][Game['setting']['difficulty']][-1]} s"
        minimum = f"minimum time : {min(Game['variables']['historical record'][Game['setting']['difficulty']])} s"
        if Game['setting']['computer solver'] == 0:
            if Game['variables']['computer record'][Game['setting']['difficulty']][-1] != 99999:
                computer= f"computer time : {Game['variables']['computer record'][Game['setting']['difficulty']][-1]} s"
            else:
                computer= ""
            if Game['variables']['historical record'][Game['setting']['difficulty']][-1] < Game['variables']['computer record'][Game['setting']['difficulty']][-1] :
                grade = " You won!"
            elif Game['variables']['historical record'][Game['setting']['difficulty']][-1] > Game['variables']['computer record'][Game['setting']['difficulty']][-1] :
                grade = " You lose!"
            else:
                grade = " It's a tie!"
        self.current_time = Text(current, (Game['system']['window width']/2, Game['system']['window height']*2/7), self.text_font)
        self.minimum_time = Text(minimum, (Game['system']['window width']/2, Game['system']['window height']*3/7), self.text_font)
        if Game['setting']['computer solver'] == 0:
            self.computer_time = Text(computer, (Game['system']['window width']/2, Game['system']['window height']*4/7), self.text_font)
            self.finalgrade = Text(grade, (Game['system']['window width']/2, Game['system']['window height']*1/7), self.text_font)
            self.items = [self.current_time, self.minimum_time, self.computer_time,self.finalgrade ,self.back_button, self.retry_button, self.quit_button]
        else:
            self.items = [self.current_time, self.minimum_time,self.back_button, self.retry_button, self.quit_button]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['result'] = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.rect.collidepoint(event.pos):
                        Game['screen']['start'] = True
                        Game['screen']['result'] = False
                        running = False
                    elif self.quit_button.rect.collidepoint(event.pos):
                        Game['system']['running'] = False
                        Game['screen']['result'] = False
                        sys.exit()
                    elif self.retry_button.rect.collidepoint(event.pos):
                        Game['screen']['game'] = True
                        Game['screen']['result'] = False
                        running = False
            self.screen.fill((255, 255, 255))
            for i in self.items:
                i.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

class SettingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.button()

    def run(self):
        running = Game['screen']['setting']
        self.seed = ""
        seed_input = False
        room_address = ""
        room_input = False
        self.temp={
            "game mode": Game['setting']['game mode'],
            "role": None,
        }
        while running:
            seed_button = Button(self.seed, (350, Game['system']['window height']*1/7), self.font, 300)
            room_button = Button(room_address, (400, Game['system']['window height']*4/7), self.font, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['setting'] = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.single_button.rect.collidepoint(event.pos):
                        self.temp['game mode'] = 0
                    elif self.multi_button.rect.collidepoint(event.pos):
                        self.temp['game mode'] = 1
                    elif self.apply_button.rect.collidepoint(event.pos):
                        Game['setting']['game mode'] = self.temp['game mode']
                        if len(self.seed) == 0:
                            self.seed = "0"
                        Game['variables']['seed'] = int(self.seed)
                        if self.temp['game mode'] == 1:
                            Game['setting']['connect']['role'] = self.temp['role']
                            if self.temp['role'] == 1:
                                Game['setting']['connect']['room'] = room_address
                            Game['screen']['room'] = True
                            Game['screen']['setting'] = False
                            running = False
                        elif self.temp['game mode'] == 0:
                            Game['screen']['start'] = True
                            Game['screen']['setting'] = False
                            running = False
                    elif self.cancel_button.rect.collidepoint(event.pos):
                        Game['screen']['start'] = True
                        Game['screen']['setting'] = False
                        running = False
                    elif seed_button.rect.collidepoint(event.pos):
                        seed_input = ~seed_input
                        room_input = False
                    elif self.server_button.rect.collidepoint(event.pos) and self.temp['game mode'] == 1:
                        self.temp['role'] = 0
                    elif self.client_button.rect.collidepoint(event.pos) and self.temp['game mode'] == 1:
                        self.temp['role'] = 1
                    elif room_button.rect.collidepoint(event.pos) and self.temp['role'] == 1 and self.temp['game mode'] == 1:
                        room_input = ~room_input
                        seed_input = False
                if seed_input:
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                            if len(self.seed) < 10:
                                self.seed += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            self.seed = self.seed[:-1]
                if room_input:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            room_address = room_address[:-1]
                        else:
                            room_address += event.unicode
            self.screen.fill((255, 255, 255))
            if seed_input:
                seed_button.set_color((255, 0, 0))
            else:
                seed_button.set_color((0, 0, 0))
            seed_button.draw(self.screen)
            if self.temp['game mode'] == 1:
                self.server_button.draw(self.screen)
                self.client_button.draw(self.screen)
                if self.temp['role'] == 1:
                    Text("Room ID:", (150, Game['system']['window height']*4/7), self.font).draw(self.screen)
                    if room_input:
                        room_button.set_color((255, 0, 0))
                    else:
                        room_button.set_color((0, 0, 0))
                    room_button.draw(self.screen)
            if self.temp['game mode'] == 0  or self.temp['role'] == 0:
                room_input = False
            self.color_check()
            self.menu()
            self.draw_button()
            pygame.display.flip()
            self.clock.tick(60)

    def button(self):
        self.single_button = Button("Single Player", ((Game['system']['window width'] - 100)/3 + 100, Game['system']['window height']*2/7), self.font, 150)
        self.multi_button = Button("Multi Players", ((Game['system']['window width'] - 100)*2/3 + 100, Game['system']['window height']*2/7), self.font, 150)
        self.server_button = Button("Create a room", ((Game['system']['window width'] - 100)/3 + 100, Game['system']['window height']*3/7), self.font, 150)
        self.client_button = Button("Join a room", ((Game['system']['window width'] - 100)*2/3 + 100, Game['system']['window height']*3/7), self.font, 150)
        self.apply_button = Button("Apply", (Game['system']['window width'] - 100, Game['system']['window height'] - 30), self.font, 150)
        self.cancel_button = Button("Cancel", (100, Game['system']['window height'] - 30), self.font, 150)

    def draw_button(self):
        self.button_object = (self.single_button, self.multi_button, self.apply_button, self.cancel_button)
        for o in self.button_object:
            o.draw(self.screen)

    def menu(self):
        game_mode = Text("Game Mode:", (100, Game['system']['window height']*2/7), self.font)
        seed = Text("Seed:", (100, Game['system']['window height']/7), self.font)
        game_mode.draw(self.screen)
        seed.draw(self.screen)

    def color_check(self):
        if self.temp['game mode'] == 0:
            self.single_button.set_color((255, 0, 0))
            self.multi_button.set_color((0, 0, 0))
        elif self.temp['game mode'] == 1:
            self.single_button.set_color((0, 0, 0))
            self.multi_button.set_color((255, 0, 0))
        if self.temp['role'] == 0:
            self.server_button.set_color((255, 0, 0))
            self.client_button.set_color((0, 0, 0))
        elif self.temp['role'] == 1:
            self.server_button.set_color((0, 0, 0))
            self.client_button.set_color((255, 0, 0))
        else:
            self.server_button.set_color((0, 0, 0))
            self.client_button.set_color((0, 0, 0))

class ScoreScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 40)
        self.text_font = pygame.font.SysFont(None, 25)
        self.back_button = Button("Back to menu", (70, Game['system']['window height'] - 30), pygame.font.SysFont(None, 25), 130)
        self.title = [Text("Easy", (Game['system']['window width']/4, 30), self.title_font), Text("Normal", (Game['system']['window width']/2, 30), self.title_font), Text("Hard", (Game['system']['window width']*3/4, 30), self.title_font)]
        self.sidebar()

    def run(self):
        running = Game['screen']['score']
        self.number()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['score'] = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.rect.collidepoint(event.pos):
                        Game['screen']['start'] = True
                        Game['screen']['score'] = False
                        running = False

            self.screen.fill((255, 255, 255))
            for i in self.title:
                i.draw(self.screen)
            for i in self.side:
                i.draw(self.screen)
            for i in range(len(self.num)):
                for j in self.num[i]:
                    j.draw(self.screen)
            self.back_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def sidebar(self):
        ave = Text("average", (45, 80), self.text_font)
        sd = Text("SD", (45, 120), self.text_font)
        first = Text("1.", (45, 160), self.text_font)
        second = Text("2.", (45, 200), self.text_font)
        third = Text("3.", (45, 240), self.text_font)
        fourth = Text("4.", (45, 280), self.text_font)
        fifth = Text("5.", (45, 320), self.text_font)
        self.side = [ave, sd, first, second, third, fourth, fifth]
    
    def number(self):
        self.num = [[None for _ in range(7)] for _ in range(3)]
        difficulty = ['easy', 'normal', 'hard']
        for i in range(3):
            temp = sorted(Game['variables']['historical record'][difficulty[i]])
            for j in range(7):
                if j == 0:
                    self.num[i][j] = Text(self.calculate_average(temp), (Game['system']['window width']*(i + 1)/4, 80), self.text_font)
                elif j == 1:
                    self.num[i][j] = Text(self.calculate_standard_deviation(temp), (Game['system']['window width']*(i + 1)/4, 120), self.text_font)
                else:
                    try:
                        self.num[i][j] = Text(str(temp[j - 2]), (Game['system']['window width']*(i + 1)/4, 120 + (j - 1)*40), self.text_font)
                    except:
                        self.num[i][j] = Text("---", (Game['system']['window width']*(i + 1)/4, 120 + (j - 1)*40), self.text_font)

    def calculate_standard_deviation(self, lst):
        n = len(lst)
        if n < 2:
            return '---'
        mean = sum(lst) / n
        variance = sum((x - mean) ** 2 for x in lst) / (n - 1)
        return str(round(math.sqrt(variance), 2))

    def calculate_average(self, lst):
        if len(lst) > 0:
            return str(round(sum(lst) / len(lst), 2))
        else:
            return "---"

class RoomScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.code = ['l', 'f', '8', 'H', 'B', 'S', 'T', '7', 'p', 'a', 'o', 'A', 'J', 'L', 'e', '9', 'Z', 'g', 'v', 'n', 'Q', 'c', 'D', 'E', 'P', 'u', 'I', 'X', 'y', '0', 'M', 'm', 'F', 'R', 'x', 'U', 'K', 'V', '1', 't', 's', 'C', '6', 'r', 'q', '3', 'G', 'Y', 'i', '2', 'b', 'W', 'w', 'k', 'd', 'h', '5', 'O', 'N', 'z', '4', 'j']
        self.font = pygame.font.SysFont(None, 30)
        self.button()
        self.ready_text = [Text("ready", (300, 235), pygame.font.SysFont(None, 25)), Text("ready", (130, 395), pygame.font.SysFont(None, 25)), Text("ready", (300, 395), pygame.font.SysFont(None, 25))]
        for i in self.ready_text:
            i.color = (255, 255, 255)

    def run(self):
        role = Game['setting']['connect']['role']
        if role == 0:
            global server 
            server = Server()
            server.start()
        elif role == 1:
            try:
                global client
                client = Client(self.id_to_ip(Game['setting']['connect']['room']))
                client.start()
            except:
                Game['screen']['room'] = False
                Game['screen']['start'] = True
                self.screen.fill((255, 255, 255))
                Text("This room does not exist", (320, 240), pygame.font.SysFont(None, 50)).draw(self.screen)
                pygame.time.wait(10000)
        self.running = Game['screen']['room']
        self.ready = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game['system']['running'] = False
                    Game['screen']['room'] = False
                    if role == 0:
                        server.server_socket.close()
                    elif role == 1:
                        client.client_socket.close()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if role == 0:
                        if self.easy_button.rect.collidepoint(event.pos):
                            Game['setting']['difficulty'] = 'easy'
                            te = (1, 'easy')
                            server.broadcast(pickle.dumps(te))
                        elif self.normal_button.rect.collidepoint(event.pos):
                            Game['setting']['difficulty'] = 'normal'
                            te = (1, 'normal')
                            server.broadcast(pickle.dumps(te))
                        elif self.hard_button.rect.collidepoint(event.pos):
                            Game['setting']['difficulty'] = 'hard'
                            te = (1, 'hard')
                            server.broadcast(pickle.dumps(te))
                        elif self.start_button.rect.collidepoint(event.pos):
                            #if i in Game['variables']['connections']['prepare'] == 1:
                            maze = generate_maze()
                            if Game['setting']['difficulty'] == 'easy':
                                Game['variables']['maze'] = maze.recursive()
                            elif Game['setting']['difficulty'] == 'normal':
                                Game['variables']['maze'] = maze.dfs()
                            elif Game['setting']['difficulty'] == 'hard':
                                Game['variables']['maze'] = maze.prim()
                            serialize_maze = pickle.dumps(Game['variables']['maze'])
                            server.broadcast(serialize_maze)
                            server.broadcast(pickle.dumps((2)))
                            Game['screen']['game'] = True
                            Game['screen']['room'] = False
                            self.running = False

                    if role == 1:
                        if self.ready:
                            if self.undo_button.rect.collidepoint(event.pos):
                                tem = (4, 0)
                                client.send_message(pickle.dumps(tem))
                                self.ready = False
                        else:
                            if self.ready_button.rect.collidepoint(event.pos):
                                tem = (4, 1)
                                client.send_message(pickle.dumps(tem))
                                self.ready = True
            self.screen.fill((255, 255, 255))
            try:
                self.color_check()
            except Exception as e:
                print(e)
            if role == 0:
                ID = self.ip_to_id(server.ip_address)
                ID = "Room ID: " + ID
                Text(ID, (Game['system']['window width']/2, 30), self.font).draw(self.screen)
            rect = [pygame.Rect(50, 100, 160, 160), pygame.Rect(230, 100, 160, 160), pygame.Rect(50, 280, 160, 160), pygame.Rect(230, 280, 160, 160)]
            for r in rect:
                pygame.draw.rect(self.screen, (0, 0, 0), r, 1, 1)
            if role == 0:
                temp = (0, Game['variables']['connections']['IP'], Game['variables']['connections']['position'], Game['variables']['connections']['color'], Game['variables']['connections']['prepare'])
                message = pickle.dumps(temp)
                server.broadcast(message)
            for i in range(len(Game['variables']['connections']['IP'])):
                if i == 0:
                    Text(Game['variables']['connections']['IP'][i], (130, 115), pygame.font.SysFont(None, 20)).draw(self.screen)
                    pygame.draw.rect(self.screen, Game['variables']['connections']['color'][i], pygame.Rect(90, 140, 80, 80))
                elif i == 1:
                    Text(Game['variables']['connections']['IP'][i], (300, 115), pygame.font.SysFont(None, 20)).draw(self.screen)
                    pygame.draw.rect(self.screen, Game['variables']['connections']['color'][i], pygame.Rect(260, 140, 80, 80))
                elif i == 2:
                    Text(Game['variables']['connections']['IP'][i], (130, 275), pygame.font.SysFont(None, 20)).draw(self.screen)
                    pygame.draw.rect(self.screen, Game['variables']['connections']['color'][i], pygame.Rect(90, 300, 80, 80))
                elif i == 3:
                    Text(Game['variables']['connections']['IP'][i], (300, 275), pygame.font.SysFont(None, 20)).draw(self.screen)
                    pygame.draw.rect(self.screen, Game['variables']['connections']['color'][i], pygame.Rect(260, 300, 80, 80))
            self.easy_button.draw(self.screen)
            self.normal_button.draw(self.screen)
            self.hard_button.draw(self.screen)
            if role == 1:
                if self.ready:
                    self.undo_button.draw(self.screen)
                else:
                    self.ready_button.draw(self.screen)
            elif role == 0:
                self.start_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def button(self):
        self.easy_button = Button("Easy", (540, Game['system']['window height']*2/7), self.font, 150)
        self.normal_button = Button("Normal", (540, Game['system']['window height']*3/7), self.font, 150)
        self.hard_button = Button("Hard", (540, Game['system']['window height']*4/7), self.font, 150)
        self.ready_button = Button("Ready", (540, Game['system']['window height']*6/7), self.font, 150)
        self.undo_button = Button("Undo", (540, Game['system']['window height']*6/7), self.font, 150)
        self.start_button = Button("Start", (540, Game['system']['window height']*6/7), self.font, 150)

    def ip_to_id(self, ip):
        temp = ip.split(".")
        ip_num = ""
        for i in temp:
            ip_num += i
        ip_num = int(ip_num)
        ID = ""
        while ip_num != 0:
            remainder = ip_num % 62
            ID = self.code[remainder] + ID
            ip_num = ip_num // 62
        return ID
    
    def id_to_ip(self, ID):
        n = 0
        ip_num = 0
        for i in ID[::-1]:
            ip_num += self.code.index(i) * 62 ** n
            n += 1
        ip_num = str(ip_num)
        ip = ip_num[:3] + '.' + ip_num[3:6] + '.' + ip_num[6:9] + '.' + ip_num[9:]
        return ip

    def color_check(self):
        if Game['setting']['difficulty'] == 'easy':
            self.easy_button.set_color((255, 0, 0))
            self.normal_button.set_color((0, 0, 0))
            self.hard_button.set_color((0, 0, 0))
        elif Game['setting']['difficulty'] == 'normal':
            self.easy_button.set_color((0, 0, 0))
            self.normal_button.set_color((255, 0, 0))
            self.hard_button.set_color((0, 0, 0))
        elif Game['setting']['difficulty'] == 'hard':
            self.easy_button.set_color((0, 0, 0))
            self.normal_button.set_color((0, 0, 0))
            self.hard_button.set_color((255, 0, 0))
        for i in range(len(Game['variables']['connections']['prepare'])):
            if i != 0:
                if Game['variables']['connections']['prepare'][i] == 0:
                    self.ready_text[i - 1].color = (255, 255, 255)
                elif Game['variables']['connections']['prepare'][i] == 1:
                    self.ready_text[i - 1].color = (255, 0, 0)

class Player:
    def __init__(self, x, y, width, height, color, surface):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.surface = surface
        self.vel = 2

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

    def update(self, walls):
        prev_x, prev_y = self.x, self.y
        self.handle_keys()
        for wall in walls:
            if wall.contact(self.get_rect()):
                self.x, self.y = prev_x, prev_y
        if self.x < (Game['system']['window width'] - Maze_cols * 15 - (Maze_cols + 1) * 3) / 2:
            self.x = prev_x
        self.draw()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def current_pos_x(self):
        return self.x

    def current_pos_y(self):
        return self.y

class MazeSolver:
    def __init__(self, maze):
        self.M = maze
        self.maze = np.zeros((Maze_rows * 2 + 1, Maze_cols * 2 + 1), dtype = np.uint8)
        self.rows = Maze_rows * 2 + 1
        self.cols = Maze_cols * 2 + 1
        self.visited = []
        self.path = []

    def solve(self, start, end):
        self.visited.clear()
        self.path.clear()
        self._dfs(start, end)

    def _dfs(self, current, end):
        if current == end:
            return True

        row, col = current
        if (
            row < 0
            or row >= self.rows
            or col < 0
            or col >= self.cols
            or self.maze[row][col] == 1
            or current in self.visited
        ):
            return False

        self.visited.append(current)
        
        neighbors = [
            (row - 1, col),
            (row, col + 1),
            (row + 1, col),
            (row, col - 1)
        ]

        for neighbor in neighbors:
            if self._dfs(neighbor, end):
                self.path.append(current)
                return True

        return False

    def convert_maze(self):
        for y in range(Maze_rows):
            for x in range(Maze_cols):
                for i in range(4):
                    if self.M[y, x, i] == 0:
                        if i == 0:
                            self.maze[2 * y + 1, 2 * x] = 1
                            self.maze[2 * y, 2 * x] = 1
                            self.maze[2 * y + 2, 2 * x] = 1
                        elif i == 1:
                            self.maze[2 * y, 2 * x + 1] = 1
                            self.maze[2 * y, 2 * x + 2] = 1
                            self.maze[2 * y, 2 * x] = 1
                        elif i == 2:
                            self.maze[2 * y + 1, 2 * x + 2] = 1
                            self.maze[2 * y + 2, 2 * x + 2] = 1
                            self.maze[2 * y, 2 * x + 2] = 1
                        elif i == 3:
                            self.maze[2 * y + 2, 2 * x + 1] = 1
                            self.maze[2 * y + 2, 2 * x + 2] = 1
                            self.maze[2 * y + 2, 2 * x] = 1
        self.maze[1][0] = 0
        self.maze[self.rows - 2][self.cols - 1] = 0

    def revert_path(self):
        self.re_path = []
        for i in self.path[::-1]:
            if (i[0] % 2 == 1) and (i[1] % 2 == 1):
                self.re_path.append((int((i[1] - 1) / 2), int((i[0] - 1) / 2)))

    def direction_list(self):
        direction = []
        for i in range(len(self.re_path) - 1):
            if self.re_path[i + 1][0] > self.re_path[i][0]:
                direction.append('right')
            elif self.re_path[i + 1][0] < self.re_path[i][0]:
                direction.append('left')
            elif self.re_path[i + 1][1] > self.re_path[i][1]:
                direction.append('down')
            elif self.re_path[i + 1][1] < self.re_path[i][1]:
                direction.append('up')
        direction.append('end')
        return direction

    def initialize(self):
        self.convert_maze()
        self.solve((1, 0), (self.rows - 2, self.cols - 1))
        self.revert_path()

class MazeSolver2:
    def __init__(self,M,x, y, width, height, color, surface):
        self.moves = [(dx, dy) for dx, dy in zip([-1, 0, 1,0], [0,1,0,-1])]
        self.m = M
        self.mark = [[0] * 100 for _ in range(100)]
        self.finalpath = [[0] * 100 for _ in range(100)]
        self.path = [[0] * 100 for _ in range(100)]
        self.top =  -1
        self.Stack = []
        self.N = np.zeros((Maze_rows * 2 + 1,Maze_cols * 2 + 1), dtype=np.uint8)
        self.r=Maze_rows*2+1
        self.c=Maze_cols*2+1
        self.vel = 1
        self.finaltop=-1
        self.pathtop=-1
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.surface = surface
        self.original_posx=x
        self.original_posy=y
          
    def find_path(self):
        self.Stack = []
        found=0
        step=(1,1,1)
        self.top += 1
        self.pathtop += 1
        self.Stack.append(step)
        self.mark[1][1]=1
        while self.top != -1 and found != 1:
            step = self.Stack.pop()
            self.top -= 1
            i, j, d = step[0], step[1], step[2]
            while d <= 3 :
                u, v = i + self.moves[d][0], j + self.moves[d][1]
                if(u==self.r-2 and v==self.c-2):
                    self.mark[self.r-2][self.c-2]=1
                    self.finalpath.append((u+1,v+1,1))
                    self.finaltop+=1
                    self.finalpath.append((u,v+1,1))
                    self.finaltop+=1
                    self.finalpath.append((u,v,1))
                    self.finaltop+=1
                    self.finalpath.append((i,j,d))
                    self.finaltop+=1
                    found=1
                    place=self.pathtop
                    for tmp in range(place, -1, -1):
                        step= self.path.pop()
                        self.finalpath.append(step)
                        self.finaltop+=1
                    return
                if (self.N[u][v]==0) and (self.mark[u][v]==0):
                    self.mark[u][v] = 1
                    s=(i,j,d)
                    self.path.append(s)
                    self.pathtop += 1
                    step = (i, j, d+1)
                    self.top += 1
                    self.Stack.append(step)
                    i, j, d = u, v, 0
                else:
                    d = d+1

    def print_maze(self):
        for i in range(self.r):
            for j in range(self.c):
                print(str(self.N[i][j]) + " ", end="")
            print()
      

    def print_path(self):
      print()
      for i in range(self.r):
          for j in range(self.c):
            print(str(self.mark[i][j]) + " ", end="")
          print()
    
    def convert_maze(self):
        for y in range(Maze_rows):
            for x in range(Maze_cols):
                for i in range(4):
                    if self.m[y, x, i] == 0:
                        if i == 0:
                            self.N[2 * y + 1, 2 * x] = 1
                            self.N[2 * y, 2 * x] = 1
                            self.N[2 * y + 2, 2 * x] = 1
                        elif i == 1:
                            self.N[2 * y, 2 * x + 1] = 1
                            self.N[2 * y, 2 * x + 2] = 1
                            self.N[2 * y, 2 * x] = 1
                        elif i == 2:
                            self.N[2 * y + 1, 2 * x + 2] = 1
                            self.N[2 * y + 2, 2 * x + 2] = 1
                            self.N[2 * y, 2 * x + 2] = 1
                        elif i == 3:
                            self.N[2 * y + 2, 2 * x + 1] = 1
                            self.N[2 * y + 2, 2 * x + 2] = 1
                            self.N[2 * y + 2, 2 * x] = 1
        self.N[1][0]=1
        self.N[self.r-2][self.c-1]=1
        
    def initialize(self):
        self.convert_maze()
        self.find_path()

class Button:
    def __init__(self, text, pos, font, width):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect(0, 0, width, font.get_height() + 10)
        self.rect.center = pos
        self.button_font = font
        self.color = (0, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surface = self.button_font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center = self.pos)
        surface.blit(text_surface, text_rect)

    def set_color(self, color):
        self.color = color

class Text:
    def __init__(self, text, pos, font):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = (0, 0, 0)

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center = self.pos)
        surface.blit(text_surface, text_rect)

class Wall:
    def __init__(self, pos, width, height, color, surface):
        self.color = color
        self.surface = surface
        self.pos = pos
        self.width, self.height = width, height

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.pos, (self.width, self.height)))

    def contact(self, player):
        wall = pygame.Rect(self.pos, (self.width, self.height))
        return wall.colliderect(player)


class Server:
    def __init__(self):
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)
        self.server_socket = None
        self.connect_accept = True

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, Game['setting']['connect']['port']))
        self.server_socket.listen(5)
        Game['variables']['connections']['socket'].append(self.server_socket)
        Game['variables']['connections']['IP'].append(self.server_socket.getsockname()[0])
        Game['variables']['connections']['position'].append((0, 0))
        Game['variables']['connections']['color'].append((255, 0, 0))
        Game['variables']['connections']['prepare'].append(1)
        print("Server started. Waiting for connections...")
        threading.Thread(target = self.connect).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(8192)
                i = Game['variables']['connections']['socket'].index(client_socket)
                if message:
                    received_tuple = pickle.loads(message)
                    if len(received_tuple) == 2 and received_tuple[0] == 4:
                        Game['variables']['connections']['prepare'][i] = received_tuple[1]
                
                else:
                    Game['variables']['connections']['socket'].pop(i)
                    Game['variables']['connections']['ID'].pop(i)
                    Game['variables']['connections']['position'].pop(i)
                    Game['variables']['connections']['color'].pop(i)
                    client_socket.close()
                    break
            except Exception as e:
                print("Error handling client:", e)
                Game['variables']['connections']['socket'].pop(i)
                Game['variables']['connections']['ID'].pop(i)
                Game['variables']['connections']['position'].pop(i)
                Game['variables']['connections']['color'].pop(i)
                client_socket.close()
                break

    def broadcast(self, message):
        for client_socket in Game['variables']['connections']["socket"]:
            if client_socket != self.server_socket:
                try:
                    client_socket.send(message)
                except Exception as e:
                    print("Error broadcasting message:", e)
    
    def connect(self):
        n = 0
        color = [(255, 165, 0), (255, 255, 0), (0, 255, 0)]
        while self.connect_accept:
            client_socket, address = self.server_socket.accept()
            print("New connection:", address)
            Game['variables']['connections']['socket'].append(client_socket)
            Game['variables']['connections']['IP'].append(client_socket.getsockname()[0])
            Game['variables']['connections']['position'].append((0, 0))
            Game['variables']['connections']['color'].append(color[n])
            Game['variables']['connections']['prepare'].append(0)
            n += 1
            threading.Thread(target=self.handle_client, args = (client_socket,)).start()
            if n == 2:
                self.connect_accept = False

class Client:
    def __init__(self, ip_address):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_address, 6000))

    def start(self):
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, message):
        self.client_socket.send(message)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(8192)
                receive_tuple = pickle.loads(message)
                
                if len(receive_tuple) == 5 and receive_tuple[0] == 0:
                    Game['variables']['connections']['IP'] = receive_tuple[1]
                    Game['variables']['connections']['position'] = receive_tuple[2]
                    Game['variables']['connections']['color'] = receive_tuple[3]
                    Game['variables']['connections']['prepare'] = receive_tuple[4]
                elif len(receive_tuple) == 2 and receive_tuple[0] == 1:
                    Game['setting']['difficulty'] = receive_tuple[1]
                elif len(receive_tuple) > 10:
                    print(receive_tuple)
                    Game['variables']['maze'] = receive_tuple
                    Game['screen']['room'] = False
                    Game['screen']['game'] = True
                    room_screen.running = False
            except Exception as e:
                print("Error receiving message:", e)
                break


pygame.init()

window = pygame.display.set_mode((Game['system']['window width'], Game['system']['window height']))

pygame.mixer.music.load(Game['system']['background music'][random.randint(0, 4)])
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

start_screen = StartScreen(window)
difficulty_screen = DifficultyScreen(window)
game_screen = GameScreen(window)
result_screen = ResultScreen(window)
setting_screen = SettingScreen(window)
score_screen = ScoreScreen(window)
room_screen = RoomScreen(window)

current_screen = start_screen

while Game['system']['running']:
    current_screen.run()

    if Game['screen']['start']:
        current_screen = start_screen
    elif Game['screen']['difficulty']:
        current_screen = difficulty_screen
    elif Game['screen']['game']:
        current_screen = game_screen
    elif Game['screen']['result']:
        current_screen = result_screen
        Game['variables']['seed'] = 0
    elif Game['screen']['setting']:
        current_screen = setting_screen
    elif Game['screen']['score']:
        current_screen = score_screen
    elif Game['screen']['room']:
        current_screen = room_screen

pygame.quit()