import pygame
from pygame import *
import random
import sys

#prerobit koniec hry, pridat prasknutu kocku do stredu, ESC na lavo, LSHIFT vpravo <<< HOTOVO

farby = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

tvary = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ] 



s_width = 1280
s_height = 720
play_width =  300 #meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30
screen = pygame.display.set_mode((s_width, s_height))

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height





class Figure:
    x = 0
    y = 0

    tvary = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y,type,color,rotation):
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.rotation = rotation
        self.type = random.randint(0, len(self.tvary) - 1)
        self.color = random.randint(1, len(farby) - 1)
        self.rotation = 0

    def image(self):
        return self.tvary[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tvary[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 480
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(6, 0,"","","")

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    

    #def draw_next_shape(self):
        #self.shape = tvary
        #self.shape_color = farby
        #self.shape_rotation = 0
    
        #format = self.shape[self.shape_rotation % len(self.shape)]
 
        #for i, line in enumerate(format):
            #row = list(line)
            #for j, column in enumerate(row):
                #if column == 0:
                    #pygame.draw.rect(screen, self.shape_color, (sx + j*30, sy + i*30, 30, 30), 0)


    #def draw_next_shape(self):
        #label = pygame.font.SysFont("comicsans", 30)
        #sx = top_left_x + play_width + 50
        #sy = top_left_y + play_height/2 - 100
        #format = self.figure[self.shape_rotation % len(self.shape)]
 
        #for i, y in enumerate(format):
            #y = list(y)
            #for j, x in enumerate(y):
                #if x == 0:
                    #pygame.draw.rect(screen, self.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
        #screen.blit(label, (sx + 10, sy- 30))

    #def get_shape(self):
        #global tvary, farby
 
        #return Tetris(new_figure(tvary, farby))

    #def draw_next_shape(self):
        #self.shape = tvary
        #self.shape_color = farby
        #self.shape_rotation = 0
        #x = top_left_x + play_width + 50
        #sy = top_left_y + play_height/2 - 100
        
        #format = self.shape[self.shape_rotation % len(self.shape)]

        #for i, line in enumerate(format):
            #row = list(line)
            #for j, column in enumerate(row):
                #if column == 0:
                    #pygame.draw.rect(screen, self.shape_color, (sx + j*30, sy + i*30, 30, 30), 0)

    




# Initialize the game engine
pygame.init()

# Define some farby
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


sx = 10
sy = 20
size = (1280, 720)
screen = pygame.display.set_mode(size)


pygame.display.set_caption("Tetres")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(30,14)
counter = 0

pressing_down = False
while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:      #Čo robia rôzne klávesy
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_w:
                game.rotate()
            if event.key == pygame.K_r:
                game.rotate()


            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_s:
                pressing_down = True


            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_a:
                game.go_side(-1)


            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_d:
                game.go_side(1)
            
            if event.key == pygame.K_SPACE:
                game.go_space()


            if event.key == pygame.K_g:
                game.state = "gameover"
            
            
            if event.key == pygame.K_LSHIFT  and game.state == "gameover":
                game.__init__(30,14,14,30)
            if event.key == pygame.K_RSHIFT  and game.state == "gameover":
                game.__init__(30,14,14,30)
            
            
            if event.key == pygame.K_ESCAPE and game.state == "gameover":
                pygame.quit()
                sys.exit()                  #Čo robia rôzne klávesy

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_s:
                pressing_down = False

    screen.fill(WHITE)   

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, farby[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j 
                if p in game.figure.image():
                    pygame.draw.rect(screen, farby[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])



    # koniec hry font, text a aj farby
    fontGO = pygame.font.SysFont("Calibri", 50, True, False)
    fontEND = pygame.font.SysFont('Calibri', 130, True, False)
    fontMIDGAME = pygame.font.SysFont('Calibri', 70, True, False)
    
                                                                            #GO = Game Over
    skore = fontMIDGAME.render("Score:", True, BLACK)
    skorecislo = fontMIDGAME.render(str(game.score), True, BLACK)          #fontMIDGAME = font pre text počas hry
    nextblock = fontMIDGAME.render("Ďalšia kocka:", True, BLACK) 
    dalsiakockaobraz = pygame.Surface([game.zoom * 4, game.zoom * 4])
    text_game_over = fontEND.render("Prehral si", True, BLACK)
    text_game_over1 = fontGO.render("Stlač ESC pre ukončenie", True, BLACK)
    text_game_over2 = fontGO.render("Stlač SHIFT pre novú hru", True, BLACK)

    screen.blit(skore, [100, 200])
    screen.blit(nextblock,[850,200])
    screen.blit(skorecislo, [175, 38500])
    if game.state == "gameover":  
        screen.fill(WHITE)
        kjube = pygame.image.load("crackedcube.png")
        odist = pygame.image.load("esc2.png")
        lrshift = pygame.image.load("shift2.png")
        screen.blit(kjube, (520,200))
        screen.blit(odist, (130,430))
        screen.blit(lrshift, (875,435))
        screen.blit(text_game_over, [360, 25])
        screen.blit(text_game_over1, [20, 405])
        screen.blit(text_game_over2, [740, 405])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()