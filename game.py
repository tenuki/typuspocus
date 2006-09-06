import pygame
from pygame.locals import *
from engine import Game, Scene
from audiencia import AudienciaScene
import cosas
from motor import MainMotor, Estados
import hollow


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
    def __init__(self, hechizo, font_size = 80, font = "escenario/VeraMono.ttf", width=600):
        self.font = font =  pygame.font.Font(font,font_size)
        text = set([ t for t in hechizo ])
        self.cache = {}
        colores = [
            [(130,130,170), (0,0,255)],
            [(255,255,0),(255,0,0)],
            [(170,170,100),(255,0,0)],
            [(255,0,0),(128,0,0)],
            ]
        for t in text:
            self.cache[t] = [ hollow.textOutline(font,t,*c) for c in colores ]
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
    linebyline = False
    
    def init(self, level_number, motor):
        import sounds
        self.sounds = sounds
        self.motor = motor
        self.line_manager = LineManager(self.motor.hechizo)
        self.offset_cache = [None]*len(self.motor.hechizo)
        self.style_cache = [None]*len(self.motor.hechizo)
        self.last_cursor = 0
        self.level_number = level_number
        
        self.line_group = pygame.sprite.OrderedUpdates()
        self.line = None
        self.audiencia = AudienciaScene(self.game, self.level_number)
        self.subscenes.append( self.audiencia )
        
        pygame.time.set_timer(CLOCK_TICK, 1000)
        
        #pygame.mixer.music.load("sounds/8bp063-07-dorothys_magic_bag-rondo_alla_turka.mp3")
        #pygame.mixer.music.set_volume(0.5)
        #pygame.mixer.music.play(-1)
        
        self.tick_count = True
        
        self.state = PLAYING

        self.level_timer = Timer(self.motor.getTimeLeft())
        self.audiencia.setVoluntario(self.motor.voluntario, False)
        self.messagefont = pygame.font.Font("escenario/VeraMono.ttf",50)
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
                sound_len = 100
                timeleft = self.motor.getTimeLeft()
                total_time = self.motor._getTiempoJuego()
                tick_rate = sound_len + timeleft * (1000-sound_len)/total_time
                if self.tick_count:
                    self.sounds.tick1.play()
                else:
                    self.sounds.tick2.play()
                self.tick_count = not self.tick_count
                pygame.time.set_timer(CLOCK_TICK, tick_rate)
                print "tickrate", tick_rate
            
                
            if self.motor.cursor >= len(self.motor.hechizo):
                self.sounds.suspenso.play()
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
                self.sounds.abucheo.play()
                self.audiencia.tomateame()
                self.wintime = pygame.time.get_ticks()
                
            self.level_timer.setTimeLeft( self.motor.getTimeLeft() )
                
                
            evt = self.motor.tick()
            self.audiencia.setCalor( self.motor.calor )
            
            if evt:
                self.audiencia.gameEvent( evt )
        elif self.state == WINNING:
            if pygame.time.get_ticks() -self.wintime > 2000:
                self.state = WON
                self.audiencia.setVoluntario(None, True) 
                self.sounds.bravo.play()
        elif self.state == LOSING:
            if pygame.time.get_ticks() -self.wintime > 2000:
                self.state = LOST
                self.audiencia.setVoluntario(self.motor.voluntario_error, True)
                self.sounds.abucheo.play()   
        elif self.state == TOMATOING:
            if pygame.time.get_ticks() -self.wintime > 2000:
                self.state = TOMATO

                
                         
    def update(self):
        font = self.messagefont
            
        if self.state == PLAYING:
            #self.game.screen.blit(self.background, (0,0))
            if self.linebyline:
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
                    cursor_img = font.render("^", True, (255,255,255))
                    self.game.screen.blit(cursor_img, 
                                          (cursor_xpos,ypos+self.line_manager.height)
                                          )                    
            else:
                # paint forward
                xpos = 400
                ypos = 300
                cursor = self.motor.cursor
                print "falta == ",self.motor.hechizo[cursor:]
                for position, letter in enumerate(self.motor.hechizo[cursor:]):
                    style = self.motor.estado[position+cursor]
                    
                        
                    i = self.line_manager.get(letter, self.motor.estado[position+cursor])
                    
                    self.game.screen.blit( i, (xpos, ypos) )
                    xpos += i.get_width()
                    if xpos > 800: break
                    
                #pain backwards
                xpos = 400
                letters = [l for l in self.motor.hechizo[:cursor]]
                print "done==", self.motor.hechizo[:cursor]
                letters.reverse()
                for position, letter in enumerate(letters):
                    style = self.motor.estado[-position+cursor]
                    
                        
                    i = self.line_manager.get(letter, self.motor.estado[-1-position+cursor])
                    width = i.get_width()
                    if xpos - width < 0: break
                    xpos -= width
                    self.game.screen.blit( i, (xpos, ypos) )
                    
                    
                
            

            self.level_timer.blit( self.game.screen, (770, 50))
        if self.state in [WON, LOST, TOMATO]:
            im = font.render("[press any key]", True, (30,30,200))
            ypos = 540
            xpos = (800-im.get_width())/2
            
            self.game.screen.blit( im, (xpos, ypos) )
            
                
        
                       
class LevelIntro(Scene):
    def init(self, level_number, level_name):
        self.level_number = level_number
        self.level_name = level_name
        self.font = font =  pygame.font.Font("escenario/VeraMono.ttf",50)
        
    def paint(self):
        s = self.font.render("Level "+self.level_number, True, (255,255,255))
        self.background.blit(s, (100,100))
        s = self.font.render(self.level_name, True, (255,255,255))
        self.background.blit(s, (100,300))
        
        self.game.screen.blit(self.background, (0,0))
    
    def event(self, evt):
        if evt.type == KEYDOWN:
                self.end()

class LevelSuccess(Scene):
    def init(self, score, levelscore):
        self.score = score
        self.levelscore = levelscore
        self.font = font =  pygame.font.Font("escenario/VeraMono.ttf",50)
        
    def paint(self):
        s = self.font.render("Level Completed", True, (255,255,255))
        self.background.blit(s, (100,100))
        s = self.font.render("Points accumulated:"+str(self.levelscore), True, (255,255,255))
        self.background.blit(s, (100,300))
        s = self.font.render("New Score:"+str(self.score), True, (255,255,255))
        self.background.blit(s, (100,400))
        
        self.game.screen.blit(self.background, (0,0))
    
    def event(self, evt):
        if evt.type == KEYDOWN:
                self.end()
class GameOver(Scene):
    def init(self, score):
        self.score = score
        self.font = font =  pygame.font.Font("escenario/VeraMono.ttf",50)
        
    def paint(self):
        s = self.font.render("Game Over: Score "+str(self.score), True, (255,255,255))
        self.background.blit(s, (100,100))
        self.game.screen.blit(self.background, (0,0))
    
    def event(self, evt):
        if evt.type == KEYDOWN:
                self.end()
                
levels = [
          # title, parameters
          ("Starting out..", dict(cantidad_palabras =5)),
          ("Getting better..", dict(
                        cantidad_palabras=30, 
                        tiempo_por_caracter=0.4)
                      ),
          ("This guys want speed..", dict(
                      cantidad_palabras=40, 
                      tiempo_por_caracter=0.35, 
                      preferencia_precision=0.1) 
                      ),
          ("Perfectionism is king..", dict(
                       cantidad_palabras=40, 
                       tiempo_por_caracter=0.30, 
                       preferencia_precision=0.9
                       )),
          ("Mixed emotions..", dict(
                        cantidad_palabras=30, 
                        tiempo_por_caracter=0.25
                        )),
      ]                
class MainMenu(Scene):
    def init(self):
        self.font = font =  pygame.font.Font("escenario/VeraMono.ttf",50)
        
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
                score = 0
                futech = 0
                while result == GANO:
                    if count < len(levels):
                        subtitle = levels[count][0]
                        params = levels[count][1]
                    else:
                        if futech == 0: futech = count-1
                        subtitle = "Future tech "+str(count-futech)
                        params = dict(tiempo_por_caracter=1.0/(count-futech+4))
                    self.runScene( LevelIntro( self.game, str(count), subtitle ) )
                    l =  Level(self.game, count, MainMotor(**params)) 
                    result = self.runScene( l )
                    newscore = int(l.motor.score)
                    score += newscore
                    if result == GANO:
                        self.runScene( LevelSuccess(self.game, score, newscore))
                    count += 1

                self.runScene( GameOver( self.game, score ) )

if __name__ == "__main__":
    g = Game(800, 600, framerate = 20)

    g.run( MainMenu(g) )
