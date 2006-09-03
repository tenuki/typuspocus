import pygame
from pygame.locals import *
from engine import Game, Scene

from motor import MainMotor, Estados

class LineManager:
    def __init__(self, hechizo, font_size = 30, font = "VeraMono.ttf", width=600):
        self.font = font =  pygame.font.Font(font,font_size)
        text = set([ t for t in hechizo ])
        self.cache = {}
        for t in text:
            self.cache[t] = (font.render(t,True,(200,200,200)),
                font.render(t,True,(255,255,255)),
                font.render(t,True,(170,170,170)),
                font.render(t,True,(255,0,0)),
                )
            self.height = self.cache[t][0].get_height()
                
        words = hechizo.split(" ")
        lines = []
        current = ""
        line_len = 0
        for word in words:
            word_len = sum([ self.get(l,0).get_width() for l in word ])
            if line_len + word_len > width:
                lines.append( current[1:]+" " )
                current = ""
                line_len = 0
                
            current += " "+word
            line_len += 1+word_len
        lines.append( current[1:]+" " )
        
        self.lines = lines            

    def get(self, letter, style):
        return self.cache[letter][style]
        
    def getLineFromCursor(self, cursor):
        offset = 0
        for line in self.lines:
            if len(line)+offset>cursor:
                return (offset,line)
            offset += len(line)
        return None
        

        
        
class Level(Scene):
    def init(self):
        self.motor = MainMotor(20)
        self.line_manager = LineManager(self.motor.hechizo)
        self.offset_cache = [None]*len(self.motor.hechizo)
        self.style_cache = [None]*len(self.motor.hechizo)
        self.last_cursor = 0
        
        self.line_group = pygame.sprite.OrderedUpdates()
        self.line = None
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
            if evt.key == K_RETURN:
                self.motor.hitLetra(" ")
    
    def loop(self):
        # aca updateamos el mundo cada paso
        pass          
    def update(self):
        self.game.screen.blit(self.background, (0,0))
        font = pygame.font.Font("VeraMono.ttf",30)
        
        cursor = self.motor.cursor
        offset, line = self.line_manager.getLineFromCursor( cursor )
        
        rectlist = []
        
        ypos = 500
        xpos = (800-sum([ self.line_manager.get(l,0).get_width() for l in line ]))/2
        cursor_xpos = xpos
        for position, letter in enumerate(line):
            style = self.motor.estado[position+offset]
            
            if position+offset == cursor:
                cursor_xpos = xpos
                
            i = self.line_manager.get(letter, self.motor.estado[position+offset])
            
            self.game.screen.blit( i, (xpos, ypos) )
            xpos += i.get_width()
            
        position = Rect(self.last_cursor,30,20,20)
        cursor_img = font.render("^", True, (255,255,255))
        self.game.screen.blit(self.background, position, position)
        self.game.screen.blit(cursor_img, (cursor_xpos,ypos+self.line_manager.height))
        self.last_cursor = cursor_xpos
        
        position = Rect(0,550,800,600)
        self.game.screen.blit(self.background, position, position)
       
        s = font.render("Score: %i / Calor: %.2f /TimeLeft: %f"%(self.motor.score, self.motor.calor, self.motor.getTimeLeft()), True, (255,255,255))
        self.game.screen.blit(s, (0,550))
        
        pygame.display.update(rectlist)
                
        
if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)
    g.run( Level(g) )