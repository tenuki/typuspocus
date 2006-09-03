import pygame
from pygame.locals import *
from engine import Game, Scene

from motor import MainMotor, Estados

class Level(Scene):
    def init(self):
        self.motor = MainMotor(20)
        text = set([ t for t in self.motor.hechizo ])
        self.cache = {}
        self.offset_cache = [None]*len(self.motor.hechizo)
        self.style_cache = [None]*len(self.motor.hechizo)
        self.last_cursor = 0
        font = pygame.font.SysFont("Times New Roman",30)
        for t in text:
            self.cache[t] = (font.render(t,True,(200,200,200)),
                font.render(t,True,(255,255,255)),
                font.render(t,True,(170,170,170)),
                font.render(t,True,(255,0,0)),
                )
        self.motor.start()
        
        
        
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
        #self.game.screen.blit(self.background, (0,0))
        font = pygame.font.SysFont("Times New Roman",30)
        
        xpos = 0
        ypos = 0
        cursor = self.motor.cursor
        for position, style in enumerate(self.motor.estado):
            letter = self.motor.hechizo[position]
            
            if position == cursor:
                cursor_xpos = xpos
            if self.style_cache[position] != style:
                s = self.cache[letter][style]
            
                self.game.screen.blit(s, (xpos,ypos))
                xpos += s.get_width()
                self.style_cache[position]=style
                self.offset_cache[position] = s.get_width()
            else:
                xpos += self.offset_cache[position]
            
        
        position = Rect(self.last_cursor,30,20,20)
        cursor_img = font.render("^", True, (255,255,255))
        self.game.screen.blit(self.background, position, position)
        self.game.screen.blit(cursor_img, (cursor_xpos,30))
        self.last_cursor = cursor_xpos
        
        position = Rect(0,550,800,600)
        self.game.screen.blit(self.background, position, position)
       
        s = font.render("Score: %i / Calor: %.2f /TimeLeft: %f"%(self.motor.score, self.motor.calor, self.motor.getTimeLeft()), True, (255,255,255))
        self.game.screen.blit(s, (0,550))
        
                
        
if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)
    g.run( Level(g) )