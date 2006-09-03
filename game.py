import pygame
from pygame.locals import *
from engine import Game, Scene

from motor import MainMotor, Estados

class Level(Scene):
    def init(self):
        self.motor = MainMotor(20)
        
    def event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            
            letra = evt.unicode #.lower()
            if letra.isalpha() or (letra and letra in " ,.<>:;"):
                self.motor.hitLetra( letra )
            if evt.key == K_BACKSPACE:
                self.motor.hitBackspace()
    
    def loop(self):
        # aca updateamos el mundo cada paso
        pass          
    def update(self):
        self.game.screen.blit(self.background, (0,0))
        font = pygame.font.SysFont("Times New Roman",30)
        
        xpos = 0
        ypos = 0
        cursor = self.motor.cursor
        for posicion, style in enumerate(self.motor.estado):
            letter = self.motor.hechizo[posicion]
            
            if posicion == cursor:
                cursor_xpos = xpos
            if style == None:
                s = font.render(letter,True,(200,200,200))
            else:
                if letter == " ": letter = "_"
                if style == Estados.OK_DEUNA:
                    s = font.render(letter,True,(255,255,255))
                elif style == Estados.OK_CORRG:
                    s = font.render(letter,True,(170,170,170))
                elif style == Estados.MAL:
                    s = font.render(letter,True,(255,0,0))

            
            self.game.screen.blit(s, (xpos,ypos))
            xpos += s.get_width()
            
        heigth = s.get_height()
        cursor_img = font.render("^", True, (255,255,255))
        self.game.screen.blit(cursor_img, (cursor_xpos,heigth))
        
                
        
if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)
    g.run( Level(g) )