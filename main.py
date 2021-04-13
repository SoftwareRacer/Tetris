# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 10:20:05 2021

@author: marco
"""

import pygame
import random

colors = [
    (0,0,0),
    (0,240,240),#4 in a row
    (0,0,240),#Reverse L
    (240,160,0),#L
    (240,240,0),#Block
    (0,240,0),#S
    (160,0,240),#T
    (240,0,0)#Reverse S
    ]

class Figure:
    x = 0
    y = 0
    
    Figures = [
            [[1,5,9,13], [4,5,6,7]], #4 in a row
            [[1,2,5,9], [0,4,5,6], [1,5,8,9], [4,5,6,10]], #Reverse L
            [[1,5,9,10], [4,5,6,8], [0,1,5,9], [2,4,5,6]], #L
            [[5,6,9,10]], #Block
            [[4,5,9,10], [2,5,6,9]], #S
            [[6,9,10,11], [1,5,6,9], [5,6,7,10], [2,5,6,10]], #T
            [[5,6,8,9], [3,5,6,8]] #Reverse S
        ]
    
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.Figures)-1)
        self.color = colors[self.type+1]
        self.rotation = 0
        
    def image(self):
        return self.Figures[self.type][self.rotation]
        
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.Figures[self.type])

class Tetris:
    height = 0
    width = 0
    field = []
    score = 0
    state = "start"
    Figure = None

    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()
        
    def new_figure(self):
        self.Figure = Figure(3, 0)
        
    def go_down(self):
        self.Figure.y += 1
        if self.intersects():
            self.Figure.y -= 1
    
    def side(self, dx):
        old_x = self.Figure.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if j + self.Figure.x > self.width - 1 or \
                        j  + self.Figure.x < 0:
                            edge = True
        if not edge:
            self.Figure.x = old_x
        if self.intersects():
            self.Figure.x = old_x
    
    def left(self):
        self.side(-1)
    
    def right(self):
        self.side(1)
    
    def down(self):
        while not self.intersects():
            self.Figure.y += 1
        self.Figure.y -= 1
        self.freeze()
    
    def rotate(self):
        old_rotation = self.Figure.rotation
        self.Figure.rotate()
        if self.intersects():
            self.Figure.rotation = old_rotation
        
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if i + self.Figure.y > self.height - 1 or \
                    i + self.Figure.y < 0 or \
                    self.field[i + self.Figure.y][j + self.Figure.x] > 0:
                        intersection = True
        return intersection
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    self.field[i + self.Figure.y][j + self.Figure.x] = self.Figure.type + 1
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "game over"
            
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
            self.score += lines ** 2
            
    
pygame.init()
screen = pygame.display.set_mode((360, 660))
pygame.display.set_caption("Tetris")
done = False
fps = 1
clock = pygame.time.Clock()
counter = 0

game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
zoom = 30

while not done:
    if game.state == "start":
        game.go_down()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True                
                
        if event.type == pygame.KEYUP:            
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False
                
        if pressing_down:
                game.down()
        if pressing_left:
                game.left()
        if pressing_right:
                game.right()
                
    screen.fill(color = WHITE)
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = GREY
                just_border = 1
            elif game.field[i][j] > 0:
                color = colors[game.field[i][j]]
                just_border = 0
            pygame.draw.rect(screen, color, [j*zoom+30, i*zoom+30, zoom, zoom], just_border)
    if game.Figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.Figure.image():
                    pygame.draw.rect(screen, game.Figure.color, [(j + game.Figure.x)*zoom+30, (i + game.Figure.y)*zoom+30, zoom, zoom])
    
    game_over_font = pygame.font.SysFont('Calibri', 65, True, False)
    text_game_over = game_over_font.render("Game Over!\nPress Esc", True, (255, 215, 0))
    
    if game.state == "game over":
        screen.blit(text_game_over, [30,250])
    
    score_font = pygame.font.SysFont('Calibri', 15, True, False)
    text_score = score_font.render("Score: " + str(game.score), True, (255, 215, 0))
    
    screen.blit(text_score, [0,0])
        
    pygame.display.flip()
    clock.tick(fps)
                
pygame.quit()