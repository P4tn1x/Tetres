import pygame, random, sys, os #importnem pygame, random, sys, os
from pygame import * #z pygame importuje všetko

os.chdir(os.path.dirname(os.path.abspath(__file__))) #Obrázky a hudba by sa mali dať spustiť z hocijakého miesta v PC

#Klása Button
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color): #button bude mať nejaký image, pozíciu, text, font, base_color a hovering_color
		self.image = image #image
		self.x_pos = pos[0] #x-ová pozícia
		self.y_pos = pos[1] #y-ová pozícia
		self.font = font #písmo
		self.base_color, self.hovering_color = base_color, hovering_color #štandardné a "hoverovacie" farby
		self.text_input = text_input #text, ktorý sa bude zobrazovať
		self.text = self.font.render(self.text_input, True, self.base_color) #text v inej farbe ako štandardný
		if self.image is None: #ak nebude obrázok, tak sa zobrazí text
			self.image = self.text  #text sa zobrazí ako obrázok
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #zistí pozíciu textu
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos)) #zistí pozíciu textu 

	def update(self, screen): #definicia na aktualizáciu scény
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position): #definícia na kontrolu pohybu myši
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position): #definícia na zmenu farby tlačidla
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def gamemusic():
        pygame.mixer.music.load("tetres.mp3")
        pygame.mixer.music.play(-1)

def menumusic():
    pygame.mixer.music.load("menu.mp3")
    pygame.mixer.music.play(-1)
    
def gameovermusic():
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.play(0)

pygame.init() #Pygame sa spustí

SCREEN = pygame.display.set_mode((1280, 720)) #Nastavenie veľkosti obrazovky
pygame.display.set_caption("Tetres") #Nastavenie na pomenovanie okna
menumusic()

BG = pygame.image.load("tetres.jpg") #Pozadie bude obrázok tetres2.jpg


#farby kociek
farby = [
    (0, 0, 0),   #Čierna
    (120, 37, 179), #Fialová
    (100, 179, 179), #Modrá
    (80, 34, 22), #Hnedá
    (80, 134, 22), #Zelená
    (180, 34, 22), #Žltá
    (180, 34, 122), #Purpurová
    ]   

s_width = 1280 #Šírka obrazovky
s_height = 720 #Výška obrazovky
screen = pygame.display.set_mode((s_width, s_height)) #Vytvorenie okna


class Figure: #Klása kocka
    x = 0 
    y = 0

    tvary = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], #I
        [[4, 5, 9, 10], [2, 6, 5, 9]], #Z
        [[6, 7, 9, 10], [1, 5, 6, 10]], #S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], #J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], #T
        [[1, 2, 5, 6]], #O
        ]

    def __init__(self, x, y,type,color,rotation): #Klása kocka bude mať nejakú súradnicu x, y, typ, farbu a rotáciu
        self.x = x #x-ová pozícia
        self.y = y #y-ová pozícia
        self.type = type #typ kocky
        self.color = color #farba kocky
        self.rotation = rotation #rotácia kocky
        self.type = random.randint(0, len(self.tvary) - 1) #Knižnica random nám náhodne vyberie tvar kocky
        self.color = random.randint(1, len(farby) - 1) #Knižnica random nám náhodne vyberie farbu kocky
        self.rotation = 0 #Nastavíme defaultnu rotáciu na 0

    def image(self):
        return self.tvary[self.type][self.rotation] #Ako bude kocka vyzerať

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tvary[self.type]) #Aké môže mať rotácie

class Tetris: #Klása tetris
    level = 1 #Nastavenie úrovne hry
    score = 0 #Ukazuje skóre hry
    state = "start" #Nastavenie stavu hry 
    field = [] #Vykreslenie hracieho poľa
    height = 0 #Výška hracej plochy
    width = 0 #Šírka hracej plochy
    x = 700 #Súradnice, kde má byť hracia plocha
    y = 0 #Súradnice, kde má byť hracia plocha
    zoom = 24 #Približenie na hraciu plochu
    figure = None #Vytvorí kocku

    def __init__(self, height, width): #Klása Tetris má svoju výšku a śírku
        self.height = height #Výška hracej plochy
        self.width = width #Šírka hracej plochy
        self.field = [] #Vytvoríme pole
        self.score = 0 #Skóre je defaultne 0
        self.state = "start" #Stav je defaultne "start"
        for i in range(height): #Pre i v rozsahu výšky hracej plochy
            new_line = [] #Vytvoríme nové riadky
            for j in range(width): #Pre j v rozsahu šírky hracej plochy
                new_line.append(0) #Pridať do riadku hodnotu 0
            self.field.append(new_line) #Pridať do pola nový riadok

    def new_figure(self): #Vytvorí novú kocku
        self.figure = Figure(6, 0,"","","") #Kocka sa spawne na súradnici 6, 0
            

    def intersects(self): #Kocka sa prekrýva s hracou plochou
        intersection = False #Nastavíme, že sa kocka neprekrýva
        for i in range(4): #Pre i v rozsahu 4
            for j in range(4): #Pre j v rozsahu 4
                if i * 4 + j in self.figure.image():  #Ak sa kocka prekryva s hracou plochou
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0: 
                        intersection = True #Kocka sa prekrýva
        return intersection #Vráti True ak sa kocka prekrýva s hracou plochou

    def break_lines(self): #definicia na ničenie plných riadkov
        lines = 0 #Nastavíme, že nie je žiadny riadok plný
        for i in range(1, self.height): #Pre i v rozsahu 1 až výška hracej plochy
            zeros = 0 #Nastavíme, že nie je žiadny riadok plný
            for j in range(self.width): #Pre j v rozsahu šírky hracej plochy
                if self.field[i][j] == 0: #Ak je na riadku 0
                    zeros += 1 #Zvýšíme zeros o 1
            if zeros == 0: #Ak je riadok plný
                lines += 1 #Zvýšíme lines o 1
                for i1 in range(i, 1, -1): #Pre i1 v rozsahu i až 1
                    for j in range(self.width): #Pre j v rozsahu šírky hracej plochy
                        self.field[i1][j] = self.field[i1 - 1][j] #Zmeníme hodnotu na riadku i1 za riadok i1 - 1
        self.score += lines ** 2 #skóre sa navýši o počet riadkov ktoré boli zničene a ich mocnice (3^3), (4^4), (5^5)

    def go_space(self): #definicia na posun kocky o jedno miesto
        while not self.intersects(): #Dokiaľ sa kocka neprekrýva
            self.figure.y += 1 #Posunieme kocku o jedno miesto vyššie
        self.figure.y -= 1 #Posunieme kocku o jedno miesto nižšie
        self.freeze() #Zastavíme kocku

    def go_down(self): #definicia na posun kocky o jedno miesto dole
        self.figure.y += 1 #Posunieme kocku o jedno miesto vyššie
        if self.intersects(): #Ak sa kocka prekrýva
            self.figure.y -= 1 #Posunieme kocku o jedno miesto nižšie
            self.freeze() #Zastavíme kocku

    def freeze(self): #definicia na zastavenie kocky
        for i in range(4): #Pre i v rozsahu 4
            for j in range(4): #Pre j v rozsahu 4
                if i * 4 + j in self.figure.image(): #Ak sa kocka prekryva s hracou plochou
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color #Zmeníme hodnotu na pozícii kocky na hodnotu farby kocky
        self.break_lines() #Zničíme riadky
        self.new_figure() #Vytvoríme novú kocku
        if self.intersects(): #Ak sa kocka prekrýva
            self.state = "gameover" #Stav hry je "gameover"

    def go_side(self, dx): #definicia na posun kocky o jedno miesto vpravo alebo vľavo
        old_x = self.figure.x #Zo starej pozície kocky sa stane nová
        self.figure.x += dx #Posunieme kocku o jedno miesto vpravo alebo vľavo
        if self.intersects(): #Ak sa kocka prekrýva
            self.figure.x = old_x #Pozícia kocky sa nezmeni

    def rotate(self): #definicia na otáčanie kocky
        old_rotation = self.figure.rotation #Zo starej rotácie kocky sa stane nová
        self.figure.rotate() #Otáčame kocku
        if self.intersects(): #Ak sa kocka prekrýva
            self.figure.rotation = old_rotation #Kocka sa neotočí


#Definujeme si farby
BLACK = (0, 0, 0) #Čierna
WHITE = (255, 255, 255) #Biela
GREEN = (0,255,0) #Zelená
ORANGE = (255,165,0) #Oranžová
RED = (255,0,0) #Červená


fontGO = pygame.font.SysFont("Calibri", 50, True, False) #Definujeme si font pre texty keď hra skončí
fontEND = pygame.font.SysFont('Calibri', 130, True, False) #Definujeme si font pre text "GAME OVER"
fontMIDGAME = pygame.font.SysFont('Calibri', 70, True, False) #Definujeme si font pre texty ktoré sa ukazujú počas hry


def get_font(size):
    return pygame.font.Font("font.ttf", size) #Importneme si font


def easydiff(): #Hra na easy difficulty
    gamemusic() #Zapne sa hudba pre hru

    done = False #done je premenná ktorá sa používa na zastavenie hry, defaultne je nastavené že hra neskončila
    clock = pygame.time.Clock() #Definujeme si časovač
    fps = 25 #Definujeme si defaultný počet FPS (25)
    game = Tetris(28,14) #Hracia plocha bude mať rozmery 28x14
    counter = 0 #Definujeme si counter ktorý sa používa na zapisovanie koľko kociek je na hracej ploche
    pressing_down = False #Definujeme si premennú ktorá sa používa na zapisovanie či je stlačená klávesa "down"
    game.level = 2 #Difficulty je 2
    game.x = 700 #X-ová pozícia hraciej plochy
    game.y = 25 #Y-ová pozícia hraciej plochy

    #Main loop hry
    while not done: #Dokým done nebude True
        if game.figure is None: #Ak je kocka None
            game.new_figure() #Hra spawne novú kocku
        counter += 1 #Zvýšíme counter o 1
        if counter > 100000: #Ak je counter viac ako 100000
            counter = 0 #Counter sa vynuluje

        if counter % (fps // game.level // 2) == 0 or pressing_down: #Ak je counter deliteľný číslom počtu FPS podľa levelu a je stlačená klávesa "down"
            if game.state == "start": #Ak je stav hry "start"
                game.go_down() #Kocka začne padať
                
            

        for event in pygame.event.get(): #Prejdeme všetky udalosti
            if event.type == pygame.QUIT: #Ak je udalosť QUIT
                pygame.quit() #Program sa vypne
                sys.exit() #Program sa vypne
            if event.type == pygame.KEYDOWN: #Ak stlačíme klávesu:
                
                #Ak je stlačená klávesa "W", "R" alebo šipka hore, kocka sa otočí
                if event.key == pygame.K_UP:
                    game.rotate() 
                if event.key == pygame.K_w:
                    game.rotate()
                if event.key == pygame.K_r:
                    game.rotate()

                #Ak je stlačená klávesa "S" alebo šipka dole, kocka sa pohne o jeden riadok dole
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_s:
                    pressing_down = True

                #Ak je stlačená klávesa "A" alebo šipka vľavo, kocka sa pohne o stĺpec doľava
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_a:
                    game.go_side(-1)

                #Ak je stlačená klávesa "D" alebo šipka vpravo, kocka sa pohne o stĺpec doprava
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_d:
                    game.go_side(1)
            
                #Ak je stlačený SPACE, kocka spadne úplne nadol
                if event.key == pygame.K_SPACE:
                    game.go_space()
                                   
                    
                #Ak je stlačený SHIFT keď skončí hra, začne sa nová hra 
                if event.key == pygame.K_LSHIFT  and game.state == "gameover": 
                    game.level = 2
                    fps = 25
                    game.__init__(28,14)
                    gamemusic()
                if event.key == pygame.K_RSHIFT  and game.state == "gameover":
                    game.level = 2
                    fps = 25
                    game.__init__(28,14)
                    gamemusic()
                #Ak je stlačený ESC keď skončí hra, stane sa návrat na menu
                if event.key == pygame.K_ESCAPE and game.state == "gameover":
                    pygame.mixer.music.pause()
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)
                    main_menu()
                                    
        
            if event.type == pygame.KEYUP: #Ak pustíme hociakú klávesu
                if event.key == pygame.K_DOWN: #Ale hra zaznamenáva že ju ešte držíme
                    pressing_down = False #Držanie klávesy sa deaktivuje

            if game.state == "gameover": #Keď je stav hry "gameover"
                gameovermusic() #Zapne sa hudba pre gameover
            
            
        screen.fill(GREEN) #Pozadie sa dá na zelené    
        
        for i in range(game.height): #Pre každý riadok
            for j in range(game.width): #Pre každý stĺpec
                pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1) #Vykreslenie hracej plochy
                if game.field[i][j] > 0: #Ak je na danom mieste niečo
                    pygame.draw.rect(screen, farby[game.field[i][j]], #Vykreslenie farby
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1]) #Vykreslenie hracej plochy
        
        if game.figure is not None: #Ak je niečo na hracej ploche
            for i in range(4): #Pre každú kocku
                for j in range(4): #Pre každý stĺpec
                    p = i * 4 + j  #Počíta sa pozícia kocky
                    if p in game.figure.image(): #Ak je na pozícii kocky niečo
                        pygame.draw.rect(screen, farby[game.figure.color],  #Vykreslenie kocky na hracej ploche
                                        [game.x + game.zoom * (j + game.figure.x) + 1, #Vykreslenie kocky na hracej ploche
                                        game.y + game.zoom * (i + game.figure.y) + 1, #Vykreslenie kocky na hracej ploche
                                        game.zoom - 2, game.zoom - 2]) #Vykreslenie kocky na hracej ploche

        
        skore = fontMIDGAME.render("Score:", True, BLACK) #Definujeme text "Score"
        skorecislo = fontMIDGAME.render(str(game.score), True, BLACK) #Definujeme skóre
        efpees = fontMIDGAME.render("FPS:", True, BLACK) #Definujeme text "FPS"
        efpeescislo = fontMIDGAME.render(str(fps), True, BLACK) #Definujeme FPS
        text_game_over = fontEND.render("GAME OVER", True, BLACK) #Definujeme text "GAME OVER"
        text_game_over1 = fontGO.render("Back to lobby", True, BLACK) #Definujeme text "Back to lobby"
        text_game_over2 = fontGO.render("New Game", True, BLACK) #Definujeme text "New Game"

        screen.blit(skore, [100, 200]) #Vykreslenie textu "Score" na obrazovke
        screen.blit(skorecislo, [170, 385]) #Vykreslenie skóre na obrazovke
        screen.blit(efpees, [400, 200]) #Vykreslenie FPS na obrazovke
        screen.blit(efpeescislo, [425, 385]) #Vykreslenie FPS na obrazovke
        
        
        if game.state == "gameover":  #Ak je stav hry "gameover"
            screen.fill(WHITE) #Obrazovka sa vyplní na bielo
            kjube = pygame.image.load("crackedcube.png") #Definujeme obrázok "crackedcube"
            odist = pygame.image.load("esc.png") #Definujeme obrázok "esc"
            lrshift = pygame.image.load("shift.png") #Definujeme obázok "shift"
            
            screen.blit(kjube, (520,200)) #Vykreslíme obrázok "crackedcube"
            screen.blit(odist, (130,430)) #Vykreslíme obrázok "esc"
            screen.blit(lrshift, (875,435)) #Vykreslíme obrázok "shift"
            screen.blit(text_game_over, [300, 25]) #Vykreslíme text "GAME OVER"
            screen.blit(text_game_over1, [100, 405]) #Vykreslíme text "Back to lobby"
            screen.blit(text_game_over2, [880, 405]) #Vykreslíme text "New Game"

        pygame.display.flip() #Zmení sa scéna
        clock.tick(fps) #Čas hry pôjde podľa FPS hry

def normaldiff(): #Hra na normal difficulty
    gamemusic() #Zapne sa hudba pre hru
    
    done = False #done je premenná ktorá sa používa na zastavenie hry, defaultne je nastavené že hra neskončila
    clock = pygame.time.Clock() #Definujeme si časovač
    fps = 50 #Definujeme si defaultný počet FPS (50)
    game = Tetris(26,14) #Hracia plocha bude mať rozmery 26x14
    counter = 0 #Definujeme si counter ktorý sa používa na zapisovanie koľko kociek je na hracej ploche
    pressing_down = False #Definujeme si premennú ktorá sa používa na zapisovanie či je stlačená klávesa "down"
    game.level = 4 #Úroveň hry je 4
    game.x = 700 #X-ová pozícia hracej plochy
    game.y = 50 #Y-ová pozícia hracej plochy


    #Main loop hry
    while not done: #Dokým done nebude True
        if game.figure is None: #Ak je kocka None
            game.new_figure() #Hra spawne novú kocku
        counter += 1 #Zvýšíme counter o 1
        if counter > 100000: #Ak je counter viac ako 100000
            counter = 0 #Counter sa vynuluje

        if counter % (fps // game.level // 2) == 0 or pressing_down: #Ak je counter deliteľný číslom počtu FPS podľa levelu a je stlačená klávesa "down"
            if game.state == "start": #Ak je stav hry "start"
                game.go_down() #Kocka začne padať
                
            

        for event in pygame.event.get(): #Prejdeme všetky udalosti
            if event.type == pygame.QUIT: #Ak je udalosť QUIT
                pygame.quit() #Program sa vypne
                sys.exit() #Program sa vypne
            if event.type == pygame.KEYDOWN: #Ak stlačíme klávesu:
                
                #Ak je stlačená klávesa "W", "R" alebo šipka hore, kocka sa otočí
                if event.key == pygame.K_UP:
                    game.rotate() 
                if event.key == pygame.K_w:
                    game.rotate()
                if event.key == pygame.K_r:
                    game.rotate()

                #Ak je stlačená klávesa "S" alebo šipka dole, kocka sa pohne o jeden riadok dole
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_s:
                    pressing_down = True

                #Ak je stlačená klávesa "A" alebo šipka vľavo, kocka sa pohne o stĺpec doľava
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_a:
                    game.go_side(-1)

                #Ak je stlačená klávesa "D" alebo šipka vpravo, kocka sa pohne o stĺpec doprava
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_d:
                    game.go_side(1)
            
                #Ak je stlačený SPACE, kocka spadne úplne nadol
                if event.key == pygame.K_SPACE:
                    game.go_space()   
                    
                #Ak je stlačený SHIFT keď skončí hra, začne sa nová hra 
                if event.key == pygame.K_LSHIFT  and game.state == "gameover": 
                    game.level = 4
                    fps = 50
                    game.__init__(26,14)
                    gamemusic()
                if event.key == pygame.K_RSHIFT  and game.state == "gameover":
                    game.level = 4
                    fps = 50
                    game.__init__(26,14)
                    gamemusic()
                
                #Ak je stlačený ESC keď skončí hra, stane sa návrat na menu
                if event.key == pygame.K_ESCAPE and game.state == "gameover":
                    pygame.mixer.music.pause()
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)
                    main_menu()
                                    
        
            if event.type == pygame.KEYUP: #Ak pustíme hociakú klávesu
                if event.key == pygame.K_DOWN: #Ale hra zaznamenáva že ju ešte držíme
                    pressing_down = False #Držanie klávesy sa deaktivuje

            if game.state == "gameover": #Ak je stav hry "gameover"
                gameovermusic() #Zapne sa hudba gameover
            
            
        screen.fill(ORANGE) #Pozadie sa dá na orandžové     
        
            

        for i in range(game.height): #Pre každý riadok
            for j in range(game.width): #Pre každý stĺpec
                pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1) #Vykreslenie hracej plochy
                if game.field[i][j] > 0: #Ak je na danom mieste niečo
                    pygame.draw.rect(screen, farby[game.field[i][j]], #Vykreslenie farby
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1]) #Vykreslenie hracej plochy
        
        if game.figure is not None: #Ak je niečo na hracej ploche
            for i in range(4): #Pre každú kocku
                for j in range(4): #Pre každý stĺpec
                    p = i * 4 + j  #Počíta sa pozícia kocky
                    if p in game.figure.image(): #Ak je na pozícii kocky niečo
                        pygame.draw.rect(screen, farby[game.figure.color],  #Vykreslenie kocky na hracej ploche
                                        [game.x + game.zoom * (j + game.figure.x) + 1, #Vykreslenie kocky na hracej ploche
                                        game.y + game.zoom * (i + game.figure.y) + 1, #Vykreslenie kocky na hracej ploche
                                        game.zoom - 2, game.zoom - 2]) #Vykreslenie kocky na hracej ploche

        
        skore = fontMIDGAME.render("Score:", True, BLACK) #Definujeme text "Score"
        skorecislo = fontMIDGAME.render(str(game.score), True, BLACK) #Definujeme skóre
        efpees = fontMIDGAME.render("FPS:", True, BLACK) #Definujeme text "FPS"
        efpeescislo = fontMIDGAME.render(str(fps), True, BLACK) #Definujeme FPS
        text_game_over = fontEND.render("GAME OVER", True, BLACK) #Definujeme text "GAME OVER"
        text_game_over1 = fontGO.render("Back to lobby", True, BLACK) #Definujeme text "Back to lobby"
        text_game_over2 = fontGO.render("New Game", True, BLACK) #Definujeme text "New Game"

        screen.blit(skore, [100, 200]) #Vykreslenie textu "Score" na obrazovke
        screen.blit(skorecislo, [170, 385]) #Vykreslenie skóre na obrazovke
        screen.blit(efpees, [400, 200]) #Vykreslenie FPS na obrazovke
        screen.blit(efpeescislo, [425, 385]) #Vykreslenie FPS na obrazovke
        
        
        if game.state == "gameover":  #Ak je stav hry "gameover"
            screen.fill(WHITE) #Obrazovka sa vyplní na bielo
            kjube = pygame.image.load("crackedcube.png") #Definujeme obrázok "crackedcube"
            odist = pygame.image.load("esc.png") #Definujeme obrázok "esc"
            lrshift = pygame.image.load("shift.png") #Definujeme obázok "shift"
            
            screen.blit(kjube, (520,200)) #Vykreslíme obrázok "crackedcube"
            screen.blit(odist, (130,430)) #Vykreslíme obrázok "esc"
            screen.blit(lrshift, (875,435)) #Vykreslíme obrázok "shift"
            screen.blit(text_game_over, [300, 25]) #Vykreslíme text "GAME OVER"
            screen.blit(text_game_over1, [100, 405]) #Vykreslíme text "Back to lobby"
            screen.blit(text_game_over2, [880, 405]) #Vykreslíme text "New Game"

        pygame.display.flip() #Zmení sa scéna
        clock.tick(fps) #Čas hry pôjde podľa FPS hry
    
def harddiff(): #Hra na hard difficulty
    gamemusic() #Zapne sa hudba pre hru
    
    done = False #done je premenná ktorá sa používa na zastavenie hry, defaultne je nastavené že hra neskončila
    clock = pygame.time.Clock() #Definujeme si časovač
    fps = 75 #Definujeme si defaultný počet FPS (75)
    game = Tetris(20,14) #Hracia plocha bude mať rozmery 20x14
    counter = 0 #Definujeme si counter ktorý sa používa na zapisovanie koľko kociek je na hracej ploche
    pressing_down = False #Definujeme si premennú ktorá sa používa na zapisovanie či je stlačená klávesa "down"
    game.level = 6 #Úroveň hry je 6
    game.x = 700 #X-ová pozícia hracej plochy
    game.y = 100 #Y-ová pozícia hracej plochy
    
    #Main loop hry
    while not done: #Dokým done nebude True
        if game.figure is None: #Ak je kocka None
            game.new_figure() #Hra spawne novú kocku
        counter += 1 #Zvýšíme counter o 1
        if counter > 100000: #Ak je counter viac ako 100000
            counter = 0 #Counter sa vynuluje

        if counter % (fps // game.level // 2) == 0 or pressing_down: #Ak je counter deliteľný číslom počtu FPS podľa levelu a je stlačená klávesa "down"
            if game.state == "start": #Ak je stav hry "start"
                game.go_down() #Kocka začne padať
                
            

        for event in pygame.event.get(): #Prejdeme všetky udalosti
            if event.type == pygame.QUIT: #Ak je udalosť QUIT
                pygame.quit() #Program sa vypne
                sys.exit() #Program sa vypne
            if event.type == pygame.KEYDOWN: #Ak stlačíme klávesu:
                
                #Ak je stlačená klávesa "W", "R" alebo šipka hore, kocka sa otočí
                if event.key == pygame.K_UP:
                    game.rotate() 
                if event.key == pygame.K_w:
                    game.rotate()
                if event.key == pygame.K_r:
                    game.rotate()

                #Ak je stlačená klávesa "S" alebo šipka dole, kocka sa pohne o jeden riadok dole
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_s:
                    pressing_down = True

                #Ak je stlačená klávesa "A" alebo šipka vľavo, kocka sa pohne o stĺpec doľava
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_a:
                    game.go_side(-1)

                #Ak je stlačená klávesa "D" alebo šipka vpravo, kocka sa pohne o stĺpec doprava
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_d:
                    game.go_side(1)
            
                #Ak je stlačený SPACE, kocka spadne úplne nadol
                if event.key == pygame.K_SPACE:
                    game.go_space()   
                    
                #Ak je stlačený SHIFT keď skončí hra, začne sa nová hra 
                if event.key == pygame.K_LSHIFT  and game.state == "gameover": 
                    game.level = 6
                    fps = 75
                    game.__init__(20,14)
                    gamemusic()
                if event.key == pygame.K_RSHIFT  and game.state == "gameover":
                    game.level = 6
                    fps = 75
                    game.__init__(20,14)
                    gamemusic()
                #Ak je stlačený ESC keď skončí hra, stane sa návrat na menu
                if event.key == pygame.K_ESCAPE and game.state == "gameover":
                    pygame.mixer.music.pause()
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)
                    main_menu()
                                    
        
            if event.type == pygame.KEYUP: #Ak pustíme hociakú klávesu
                if event.key == pygame.K_DOWN: #Ale hra zaznamenáva že ju ešte držíme
                    pressing_down = False #Držanie klávesy sa deaktivuje

            if game.state == "gameover": #Ak je stav hry "gameover"
                gameovermusic() #Zapne sa hudba gameover
            
            
        screen.fill(RED) #Pozadie sa dá na červené     
        
            

        for i in range(game.height): #Pre každý riadok
            for j in range(game.width): #Pre každý stĺpec
                pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1) #Vykreslenie hracej plochy
                if game.field[i][j] > 0: #Ak je na danom mieste niečo
                    pygame.draw.rect(screen, farby[game.field[i][j]], #Vykreslenie farby
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1]) #Vykreslenie hracej plochy
        
        if game.figure is not None: #Ak je niečo na hracej ploche
            for i in range(4): #Pre každú kocku
                for j in range(4): #Pre každý stĺpec
                    p = i * 4 + j  #Počíta sa pozícia kocky
                    if p in game.figure.image(): #Ak je na pozícii kocky niečo
                        pygame.draw.rect(screen, farby[game.figure.color],  #Vykreslenie kocky na hracej ploche
                                        [game.x + game.zoom * (j + game.figure.x) + 1, #Vykreslenie kocky na hracej ploche
                                        game.y + game.zoom * (i + game.figure.y) + 1, #Vykreslenie kocky na hracej ploche
                                        game.zoom - 2, game.zoom - 2]) #Vykreslenie kocky na hracej ploche

        
        skore = fontMIDGAME.render("Score:", True, BLACK) #Definujeme text "Score"
        skorecislo = fontMIDGAME.render(str(game.score), True, BLACK) #Definujeme skóre
        efpees = fontMIDGAME.render("FPS:", True, BLACK) #Definujeme text "FPS"
        efpeescislo = fontMIDGAME.render(str(fps), True, BLACK) #Definujeme FPS
        text_game_over = fontEND.render("GAME OVER", True, BLACK) #Definujeme text "GAME OVER"
        text_game_over1 = fontGO.render("Back to lobby", True, BLACK) #Definujeme text "Back to lobby"
        text_game_over2 = fontGO.render("New Game", True, BLACK) #Definujeme text "New Game"

        screen.blit(skore, [100, 200]) #Vykreslenie textu "Score" na obrazovke
        screen.blit(skorecislo, [170, 385]) #Vykreslenie skóre na obrazovke
        screen.blit(efpees, [400, 200]) #Vykreslenie FPS na obrazovke
        screen.blit(efpeescislo, [425, 385]) #Vykreslenie FPS na obrazovke
        
        
        if game.state == "gameover":  #Ak je stav hry "gameover"
            screen.fill(WHITE) #Obrazovka sa vyplní na bielo
            kjube = pygame.image.load("crackedcube.png") #Definujeme obrázok "crackedcube"
            odist = pygame.image.load("esc.png") #Definujeme obrázok "esc"
            lrshift = pygame.image.load("shift.png") #Definujeme obázok "shift"
            
            screen.blit(kjube, (520,200)) #Vykreslíme obrázok "crackedcube"
            screen.blit(odist, (130,430)) #Vykreslíme obrázok "esc"
            screen.blit(lrshift, (875,435)) #Vykreslíme obrázok "shift"
            screen.blit(text_game_over, [300, 25]) #Vykreslíme text "GAME OVER"
            screen.blit(text_game_over1, [100, 405]) #Vykreslíme text "Back to lobby"
            screen.blit(text_game_over2, [880, 405]) #Vykreslíme text "New Game"

        pygame.display.flip() #Zmení sa scéna
        clock.tick(fps) #Čas hry pôjde podľa FPS hry
    
def goddiff(): #Hra na god difficulty
    gamemusic() #Zapne sa hudba pre hru
    
    done = False #done je premenná ktorá sa používa na zastavenie hry, defaultne je nastavené že hra neskončila
    clock = pygame.time.Clock() #Definujeme si časovač
    fps = 190 #Definujeme si defaultný počet FPS (190)
    game = Tetris(25,12) #Hracia plocha bude mať rozmery 25x14
    counter = 0 #Definujeme si counter ktorý sa používa na zapisovanie koľko kociek je na hracej ploche
    pressing_down = False #Definujeme si premennú ktorá sa používa na zapisovanie či je stlačená klávesa "down"
    game.level = 12 #Úroveň hry je 12
    game.x = 700 #X-ová pozícia hracej plochy
    game.y = 50 #Y-ová pozícia hracej plochy
    
    #Main loop hry
    while not done: #Dokým done nebude True
        if game.figure is None: #Ak je kocka None
            game.new_figure() #Hra spawne novú kocku
        counter += 1 #Zvýšíme counter o 1
        if counter > 100000: #Ak je counter viac ako 100000
            counter = 0 #Counter sa vynuluje

        if counter % (fps // game.level // 2) == 0 or pressing_down: #Ak je counter deliteľný číslom počtu FPS podľa levelu a je stlačená klávesa "down"
            if game.state == "start": #Ak je stav hry "start"
                game.go_down() #Kocka začne padať
                
            

        for event in pygame.event.get(): #Prejdeme všetky udalosti
            if event.type == pygame.QUIT: #Ak je udalosť QUIT
                pygame.quit() #Program sa vypne
                sys.exit() #Program sa vypne
            if event.type == pygame.KEYDOWN: #Ak stlačíme klávesu:
                
                #Ak je stlačená klávesa "W", "R" alebo šipka hore, kocka sa otočí
                if event.key == pygame.K_UP:
                    game.rotate() 
                if event.key == pygame.K_w:
                    game.rotate()
                if event.key == pygame.K_r:
                    game.rotate()

                #Ak je stlačená klávesa "S" alebo šipka dole, kocka sa pohne o jeden riadok dole
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_s:
                    pressing_down = True

                #Ak je stlačená klávesa "A" alebo šipka vľavo, kocka sa pohne o stĺpec doľava
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_a:
                    game.go_side(-1)

                #Ak je stlačená klávesa "D" alebo šipka vpravo, kocka sa pohne o stĺpec doprava
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_d:
                    game.go_side(1)
            
                #Ak je stlačený SPACE, kocka spadne úplne nadol
                if event.key == pygame.K_SPACE:
                    game.go_space()   
                    
                #Ak je stlačený SHIFT keď skončí hra, začne sa nová hra 
                if event.key == pygame.K_LSHIFT  and game.state == "gameover": 
                    game.level = 12
                    fps = 190
                    game.__init__(25,14)
                    gamemusic()
                if event.key == pygame.K_RSHIFT  and game.state == "gameover":
                    game.level = 12
                    fps = 190
                    game.__init__(25,14)
                    gamemusic()
                #Ak je stlačený ESC keď skončí hra, stane sa návrat na menu
                if event.key == pygame.K_ESCAPE and game.state == "gameover":
                    pygame.mixer.music.pause()
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)
                    main_menu()
                                    
        
            if event.type == pygame.KEYUP: #Ak pustíme hociakú klávesu
                if event.key == pygame.K_DOWN: #Ale hra zaznamenáva že ju ešte držíme
                    pressing_down = False #Držanie klávesy sa deaktivuje

            if game.state == "gameover": #Ak je stav hry "gameover"
                gameovermusic() #Zapne sa hudba gameover
            
            
        screen.fill(WHITE) #Pozadie sa dá na červené     
        
        
        for i in range(game.height): #Pre každý riadok
            for j in range(game.width): #Pre každý stĺpec
                pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1) #Vykreslenie hracej plochy
                if game.field[i][j] > 0: #Ak je na danom mieste niečo
                    pygame.draw.rect(screen, farby[game.field[i][j]], #Vykreslenie farby
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1]) #Vykreslenie hracej plochy
        
        if game.figure is not None: #Ak je niečo na hracej ploche
            for i in range(4): #Pre každú kocku
                for j in range(4): #Pre každý stĺpec
                    p = i * 4 + j  #Počíta sa pozícia kocky
                    if p in game.figure.image(): #Ak je na pozícii kocky niečo
                        pygame.draw.rect(screen, farby[game.figure.color],  #Vykreslenie kocky na hracej ploche
                                        [game.x + game.zoom * (j + game.figure.x) + 1, #Vykreslenie kocky na hracej ploche
                                        game.y + game.zoom * (i + game.figure.y) + 1, #Vykreslenie kocky na hracej ploche
                                        game.zoom - 2, game.zoom - 2]) #Vykreslenie kocky na hracej ploche

        
        skore = fontMIDGAME.render("Score:", True, BLACK) #Definujeme text "Score"
        skorecislo = fontMIDGAME.render(str(game.score), True, BLACK) #Definujeme skóre
        efpees = fontMIDGAME.render("FPS:", True, BLACK) #Definujeme text "FPS"
        efpeescislo = fontMIDGAME.render(str(fps), True, BLACK) #Definujeme FPS
        text_game_over = fontEND.render("GAME OVER", True, BLACK) #Definujeme text "GAME OVER"
        text_game_over1 = fontGO.render("Back to lobby", True, BLACK) #Definujeme text "Back to lobby"
        text_game_over2 = fontGO.render("New Game", True, BLACK) #Definujeme text "New Game"

        screen.blit(skore, [100, 200]) #Vykreslenie textu "Score" na obrazovke
        screen.blit(skorecislo, [170, 385]) #Vykreslenie skóre na obrazovke
        screen.blit(efpees, [400, 200]) #Vykreslenie FPS na obrazovke
        screen.blit(efpeescislo, [425, 385]) #Vykreslenie FPS na obrazovke
        
        
        if game.state == "gameover":  #Ak je stav hry "gameover"
            screen.fill(WHITE) #Obrazovka sa vyplní na bielo
            kjube = pygame.image.load("crackedcube.png") #Definujeme obrázok "crackedcube"
            odist = pygame.image.load("esc.png") #Definujeme obrázok "esc"
            lrshift = pygame.image.load("shift.png") #Definujeme obázok "shift"
            
            screen.blit(kjube, (520,200)) #Vykreslíme obrázok "crackedcube"
            screen.blit(odist, (130,430)) #Vykreslíme obrázok "esc"
            screen.blit(lrshift, (875,435)) #Vykreslíme obrázok "shift"
            screen.blit(text_game_over, [300, 25]) #Vykreslíme text "GAME OVER"
            screen.blit(text_game_over1, [100, 405]) #Vykreslíme text "Back to lobby"
            screen.blit(text_game_over2, [880, 405]) #Vykreslíme text "New Game"

        pygame.display.flip() #Zmení sa scéna
        clock.tick(fps) #Čas hry pôjde podľa FPS hry

def play(): #Obrazovka pre výber difficulty
    while True: #Keď stlačíme button PLAY
        PLAY_MOUSE_POS = pygame.mouse.get_pos() #Zistíme si pozíciu myši a zadáme ju pod premennú PLAY_MOUSE_POS

        SCREEN.fill("black") #Vyplníme obrazovku na čierno

        PLAY_TEXT = get_font(45).render("Choose a difficulty:", True, "White") #Definujeme text "Choose a difficulty:"
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100)) #Definujeme pozíciu textu "Choose a difficulty:"
        SCREEN.blit(PLAY_TEXT, PLAY_RECT) #Na obrazovku vykreslíme text "Choose a difficulty:"

        EASY_DIFF = Button(image=None, pos=(200,260), text_input="EASY", font=get_font(75), base_color="White", hovering_color="Green") #Definujeme tlačidlo "EASY"
        NORMAL_DIFF = Button(image=None, pos=(650,260), text_input="NORMAL", font=get_font(75), base_color="White", hovering_color="Orange") #Definujeme tlačidlo "NORMAL"
        HARD_DIFF = Button(image=None, pos=(1100,260), text_input="HARD", font=get_font(75), base_color="White", hovering_color="Red") #Definujeme tlačidlo "HARD"
        GOD_DIFF = Button(image=None, pos=(1100,700), text_input="GOD", font=get_font(75), base_color="#070000", hovering_color="White") #Definujeme tlačidlo "GOD"
        
        
        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green") #Definujeme tlačidlo "BACK"

        for button in [EASY_DIFF,NORMAL_DIFF,HARD_DIFF,GOD_DIFF,PLAY_BACK]: #Pre buttony EASY,NORMAL,HARD,GOD a BACK
            button.changeColor(PLAY_MOUSE_POS) #Zmeníme farbu tlačidiel podľa pozície myši
            button.update(SCREEN) #Po stlačeni buttnu sa zmení obrazovka podľa jeho funkcie



        for event in pygame.event.get(): #Pre každú udalosť
            if event.type == pygame.QUIT: #Ak vypneme hru
                pygame.quit() #Knižnice sa vypnú
                sys.exit()    #Knižnice sa vypnú
            if event.type == pygame.MOUSEBUTTONDOWN: #Ak stláčame myš
                if EASY_DIFF.checkForInput(PLAY_MOUSE_POS): #Ak je myš na tlačidle EASY
                    easydiff() #Spustíme easydiff()
                if NORMAL_DIFF.checkForInput(PLAY_MOUSE_POS): #Ak je myš na tlačidle NORMAL
                    normaldiff() #Spustíme normaldiff()
                if HARD_DIFF.checkForInput(PLAY_MOUSE_POS): #Ak je myš na tlačidle HARD
                    harddiff() #Spustíme harddiff()
                if GOD_DIFF.checkForInput(PLAY_MOUSE_POS): #Ak je myš na tlačidle GOD
                    goddiff() #Spustíme goddiff()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS): #Ak je myš na tlačidle BACK
                    main_menu() #Spustíme main_menu()

        
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def ovladanie(): #Button na ovládanie
    while True: #Keď stlačíme button "KEYBINDS"
        OVLADANIE_MOUSE_POS = pygame.mouse.get_pos() #Definujeme pozíciu myši

        SCREEN.fill("#a6a6a6") #Obrazovka sa vyplní na bielo
        BG1 = pygame.image.load("keybinds.png") #Definujeme obrázok "keybinds"
        SCREEN.blit(BG1, (0,0)) #Vykreslíme obrázok "keybinds" ako pozadie
        OVLADANIE_BACK = Button(image=None, pos=(640, 100), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Red") #Definujeme button "BACK",

        OVLADANIE_BACK.changeColor(OVLADANIE_MOUSE_POS) #Zmeníme farbu buttonu "BACK" podľa pozície myši
        OVLADANIE_BACK.update(SCREEN) #Keď stlačíme button KEYBINDS tak sa zmení scéna

        for event in pygame.event.get(): #Pre každú udalosť
            if event.type == pygame.QUIT: #Ak manuálne vypneme hru
                pygame.quit() #Program as vypne
                sys.exit() #Program sa vypne
            if event.type == pygame.MOUSEBUTTONDOWN: #Ak stlačíme tlačítko myši
                if OVLADANIE_BACK.checkForInput(OVLADANIE_MOUSE_POS): #Ak je myš na pozícii buttonu "BACK" 
                    main_menu() #Vrátime sa do main menu

        pygame.display.update() #Zmení sa scéna
    
def main_menu(): #hlavné menu
    while True: #Pokiaľ sme na main menu
        SCREEN.blit(BG, (0, 0)) #Pozadie bude obrázok "tetres" 

        MENU_MOUSE_POS = pygame.mouse.get_pos() #zisťuje pozíciu myši

        MENU_TEXT = get_font(100).render("TETRES", True, "#000000") #text na hlavnom menu
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100)) #pozícía textu na hlavnom menu

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(640, 300), #play tlačítko bude mať nejaký obrázok "Play Rect", pozíciu, text, font, farbu a farbu pod myškou 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="Green")
        OVLADANIE_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(640,425), #ovladanie tlačitko bude mať nejaký obrázok "Play Rect", pozíciu, text, font, farbu a farbu pod myškou 
                            text_input="KEYBINDS", font=get_font(40),base_color="#d7fcd4", hovering_color="Red")
        QUIT_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(640, 550), #quit tlačítko bude mať nejaký obrázok "Play Rect", pozíciu, text, font, farbu a farbu pod myškou 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="Blue")

        SCREEN.blit(MENU_TEXT, MENU_RECT) #Vykreslíme text na hlavnom menu

        for button in [PLAY_BUTTON, OVLADANIE_BUTTON,QUIT_BUTTON]: #Pre každý button na hlavnom menu
            button.changeColor(MENU_MOUSE_POS) #Zmeníme farbu buttonu keď je nad ním kurzor
            button.update(SCREEN) #Zmeníme scénu
        
        for event in pygame.event.get(): #Pre každú udalosť na main menu
            #ak klikneme na tlačidlo pre ukončenie hry, tak sa vypne
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit()
            #ak klikneme tlačitko na myši nad buttonami PLAY, KEYBINDS alebo QUIT, tak sa spustí ich cyklus
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OVLADANIE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ovladanie()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update() #Zmení sa scéna

main_menu() #Spustíme hlavné menu