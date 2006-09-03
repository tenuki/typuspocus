import pygame
from pygame.locals import *
from engine import Game, Scene
from audiencia import AudienciaScene
import cosas
from motor import MainMotor, Estados



CLOCK_TICK = pygame.USEREVENT

class Timer:
    def __init__(self, total_time):
        self.total_time = total_time
        self.time_left = total_time
        
    def setTimeLeft(self, time):
        self.time_left = time
        
    def blit(self, surface, (x, y)):
        full = 300
        width = 20
        current = (self.time_left*full)/self.total_time
        pygame.draw.rect(surface, (0,0,0), Rect(x-1,y-1,width+3,full+2))
        pygame.draw.rect(surface, (30,255,30), Rect(x,y+full-current,width,
                current
                ))
        
        
class LineManager:
    def __init__(self, hechizo, font_size = 30, font = "VeraMono.ttf", width=600):
        self.font = font =  pygame.font.Font(font,font_size)
        text = set([ t for t in hechizo ])
        self.cache = {}
        for t in text:
            self.cache[t] = (font.render(t,True,(130,130,170)),
                font.render(t,True,(255,255,255)),
                font.render(t,True,(170,170,100)),
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
        lines.append( current[1:] )
        
        self.lines = lines            

    def get(self, letter, style):
        return self.cache[letter][style]
        
    def getLineFromCursor(self, cursor):
        offset = 0
        for line in self.lines:
            if len(line)+offset>cursor:
                return (offset,line)
            offset += len(line)
        return 0,0
        

PERDIO, GANO = range(2)
PLAYING, WINNING, WON, TIMEOUT, TOMATOING, TOMATO, LOSING, LOST, DONE = range(9)

class Level(Scene):
    def init(self):
        import sounds
        self.sounds = sounds
        self.motor = MainMotor(5)
        self.line_manager = LineManager(self.motor.hechizo)
        self.offset_cache = [None]*len(self.motor.hechizo)
        self.style_cache = [None]*len(self.motor.hechizo)
        self.last_cursor = 0
        
        self.line_group = pygame.sprite.OrderedUpdates()
        self.line = None
        self.audiencia = AudienciaScene(self.game)
        self.subscenes.append( self.audiencia )
        
        pygame.time.set_timer(CLOCK_TICK, 1000)
        
        self.voluntario = cosas.reloj
        self.state = PLAYING

        self.level_timer = Timer(self.motor.getTimeLeft())
       
        self.motor.start()
        
               
        
        
        
    def event(self, evt):
        if self.state == PLAYING:
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.end()
                
                res = None
                letra = evt.unicode #.lower()
                if letra.isalpha() or (letra and letra in " ,.<>:;"):
                    res, event = self.motor.hitLetra( letra )
                if evt.key == K_BACKSPACE:
                    self.motor.hitBackspace()
                if evt.key == K_RETURN:
                    res, event = self.motor.hitLetra(" ")
                    
                if res:
                    self.audiencia.gameEvent( event )
                    
            elif evt.type == CLOCK_TICK:
                self.sounds.reloj.play()
              
            if self.motor.cursor >= len(self.motor.hechizo):
                if self.motor.tuvoExito():
                    self.state = WINNING
                else:
                    self.state = LOSING
                self.wintime = pygame.time.get_ticks()
                    
          
        elif self.state in [ WON ]:
            if evt.type == KEYDOWN:
                    self.end(GANO)
        elif self.state in [ LOST, TOMATO ]:
            if evt.type == KEYDOWN:
                    self.end(PERDIO)
                
    
    
    
    def loop(self):
        # aca updateamos el mundo cada paso
        if self.state == PLAYING:
            if self.motor.getTimeLeft() <= 0:
                self.state = TOMATOING
                self.wintime = pygame.time.get_ticks()
                
            self.level_timer.setTimeLeft( self.motor.getTimeLeft() )
                
                
            evt = self.motor.tick()
            self.audiencia.setCalor( self.motor.calor )
            
            if evt:
                self.audiencia.gameEvent( evt )
        elif self.state == WINNING:
            if pygame.time.get_ticks() -self.wintime > 5000:
                self.state = WON
                self.sounds.bravo.play()
        elif self.state == LOSING:
            if pygame.time.get_ticks() -self.wintime > 5000:
                self.state = LOST
                self.sounds.abucheo.play()   
        elif self.state == TOMATOING:
            if pygame.time.get_ticks() -self.wintime > 5000:
                self.state = TOMATO
                self.sounds.abucheo.play()
                
                         
    def update(self):
        if self.state == PLAYING:
            #self.game.screen.blit(self.background, (0,0))
            font = pygame.font.Font("VeraMono.ttf",30)
            
            cursor = self.motor.cursor
            offset, line = self.line_manager.getLineFromCursor( cursor )
            
            ypos = 540
            xpos = (800-sum([ self.line_manager.get(l,0).get_width() for l in line ]))/2
            cursor_xpos = xpos
            for position, letter in enumerate(line):
                style = self.motor.estado[position+offset]
                
                if position+offset == cursor:
                    cursor_xpos = xpos
                    
                i = self.line_manager.get(letter, self.motor.estado[position+offset])
                
                self.game.screen.blit( i, (xpos, ypos) )
                xpos += i.get_width()
                
            self.level_timer.blit( self.game.screen, (770, 50))
            cursor_img = font.render("^", True, (255,255,255))
            self.game.screen.blit(cursor_img, 
                (cursor_xpos,ypos+self.line_manager.height)
                )
                
            self.game.screen.blit(self.voluntario, 
                    ( 800/2 - self.voluntario.get_width()/2, 
                    400-self.voluntario.get_height() ) 
                    )
        elif self.state == WINNING:
            self.game.screen.blit(self.voluntario, 
                    ( 800/2 - self.voluntario.get_width()/2, 
                    400-self.voluntario.get_height() ) 
                    )
        elif self.state == LOSING:
            self.game.screen.blit(self.voluntario, 
                    ( 800/2 - self.voluntario.get_width()/2, 
                    400-self.voluntario.get_height() ) 
                    )
        elif self.state == TOMATO:
            self.game.screen.blit(self.voluntario, 
                    ( 800/2 - self.voluntario.get_width()/2, 
                    400-self.voluntario.get_height() ) 
                    )
        elif self.state == TOMATOING:
            self.game.screen.blit(self.voluntario, 
                    ( 800/2 - self.voluntario.get_width()/2, 
                    400-self.voluntario.get_height() ) 
                    )
        elif self.state == WON:
            pass 
        elif self.state == LOST:
            self.game.screen.blit(cosas.hongo, 
                    ( 800/2 - cosas.hongo.get_width()/2, 
                    400-cosas.hongo.get_height() ) 
                    )
        
           
class LevelIntro(Scene):
    def init(self, level_name):
        self.level_name = level_name
        self.font = font =  pygame.font.Font("VeraMono.ttf",50)
        
    def paint(self):
        s = self.font.render("Level "+self.level_name, True, (255,255,255))
        self.background.blit(s, (100,100))
        self.game.screen.blit(self.background, (0,0))
    
    def event(self, evt):
        if evt.type == KEYDOWN:
                self.end()

class MainMenu(Scene):
    def init(self):
        self.font = font =  pygame.font.Font("VeraMono.ttf",50)
        
    def paint(self):
        s = self.font.render("Typus Pocus", True, (255,255,255))
        self.background.blit(s, (100,100))
        self.game.screen.blit(self.background, (0,0))
        
        
    def event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            else:
                result = GANO
                count = 0
                while result == GANO:
                    count += 1
                    self.runScene( LevelIntro( self.game, str(count) ) )
                    result = self.runScene( Level(self.game) )
    

if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)

    g.run( MainMenu(g) )