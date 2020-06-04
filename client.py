'''Making a online multiplayer game in python'''
import pygame
from network import Network
import pickle

# Initializing pygame

pygame.init()

# Setting up the screen

width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

icon = pygame.image.load('C:\\Users\\pikac\\Documents\\VS Code\\rock.png')
pygame.display.set_icon(icon)

# Coding the button class

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2) - round(text.get_height() / 2)))  # This will center our text

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

# Functions

def redrawWindow(win, game, p):
    win.fill((128, 128, 128))
    background = pygame.image.load('C:\\Users\\pikac\\Documents\\VS Code\\dark.png').convert()
    win.blit(background, (0, 0))


    if not(game.connected()):
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("Waiting for player...", 1, (0, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Your move", 1, (65, 105, 225))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (165, 42, 42))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (220, 20, 60))
            text2 = font.render(move2, 1, (70, 130, 180))
        else:
            if game.p1went and p == 0:
                text1 = font.render(move1, 1, (220, 20, 60))
            elif game.p1went:
                text1 = font.render("Locked in", 1, (107, 142, 35))
            else:
                text1 = font.render("Waiting...", 1, (95, 158, 160))

            if game.p2went and p == 1:
                text2 = font.render(move2, 1, (220, 20, 60))
            elif game.p2went:
                text2 = font.render("Locked in", 1, (46, 139, 87))
            else:
                text2 = font.render("Waiting...", 1, (95, 158, 160))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button("Rock", 50, 500, (205, 133, 63)), Button("Scissors", 250, 500, (192, 192, 192)), Button("Paper", 450, 500, (221, 160, 221))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Arial", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie!", 1, (0, 0, 0))
            else:
                text = font.render("You Lost...", 1, (0, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1went:
                                n.send(btn.text)
                        else:
                            if not game.p2went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        background = pygame.image.load('C:\\Users\\pikac\\Documents\\VS Code\\dark.png').convert()
        win.blit(background, (0, 0))
        font = pygame.font.SysFont("Arial", 55)
        text = font.render("Click to play!", 1, (0, 0, 0))
        win.blit(text, (200, 325))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                run = False

    main()

# Calling the main game loop

while True:
    menu_screen()
