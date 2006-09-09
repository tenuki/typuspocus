import pygame
from pygame.locals import *
from engine import Game, Scene
from audiencia import AudienciaScene
import audiencia
import cosas
from motor import MainMotor, Estados
import hollow
from sounds import sounds
import time

DEBUG = 0

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
    def __init__(self, hechizo, font_size = 80, font = "escenario/MagicSchoolOne.ttf", altfont_size = 80, altfont = "escenario/VeraSe.ttf", width=600):
        self.font = pygame.font.Font(font,font_size)
        self.altfont = pygame.font.Font(altfont,altfont_size)
        text = set([ t for t in hechizo ])
        self.cache = {}
        colores = [
            [(130,130,170), (0,0,255)],
            [(255,255,0),(255,0,0)],
            [(170,170,100),(170,0,0)],
            [(255,0,0),(128,0,0)],
            ]
        for t in text:
            if t in " ,.<>:;":
                font = self.altfont
            else:
                font = self.font
            if t == " ":
                self.cache[t] = [ 
                    hollow.textOutline(font,t,*colores[0]),
                    hollow.textOutline(font,t,*colores[1]),
                    hollow.textOutline(font,"_",*colores[2]),
                    hollow.textOutline(font,"_",*colores[3])
                    ]
            else:
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
    
    def init(self, level_number, motor, laAudiencia):
        self.audiencia = laAudiencia
        self.motor = motor
        self.line_manager = LineManager(self.motor.hechizo)
        self.offset_cache = [None]*len(self.motor.hechizo)
        self.style_cache = [None]*len(self.motor.hechizo)
        self.last_cursor = 0
        self.level_number = level_number
        
        self.line_group = pygame.sprite.OrderedUpdates()
        self.line = None
        self.audiencia = AudienciaScene(self.game, self.level_number, self.audiencia)
        self.subscenes.append( self.audiencia )
        self.todasLasTeclas = ""
        
        pygame.time.set_timer(CLOCK_TICK, 1000)
        
        #pygame.mixer.music.load("sounds/8bp063-07-dorothys_magic_bag-rondo_alla_turka.mp3")
        #pygame.mixer.music.set_volume(0.5)
        #pygame.mixer.music.play(-1)
        
        self.tick_count = True
        
        self.state = PLAYING

        self.level_timer = Timer(self.motor.getTimeLeft())
        self.audiencia.setVoluntario(self.motor.voluntario, False)
        self.messagefont = pygame.font.Font("escenario/VeraMono.ttf",30)
        self.ratefont = pygame.font.Font("escenario/VeraMono.ttf",20)
        self.cursorfont = pygame.font.Font("escenario/MagicSchoolOne.ttf",100)
        self.motor.start()
        sounds.volumenDeeJay(1.0)
        
        
    def event(self, evt):
        if self.state == PLAYING:
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.end()
                
                res = None
                letra = evt.unicode #.lower()
                if letra.isalpha() or (letra and letra in " ,.<>:;"):
                    res, event = self.motor.hitLetra( letra )
                    self.checkEaster(letra)
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
                    sounds.tick1()
                else:
                    sounds.tick2()
                self.tick_count = not self.tick_count
                pygame.time.set_timer(CLOCK_TICK, tick_rate)
                if DEBUG: print "tickrate", tick_rate
            
                
            if self.motor.cursor >= len(self.motor.hechizo):
                sounds.suspenso()
                sounds.apagarVoces()
                sounds.volumenDeeJay(0.5)
                if self.motor.tuvoExito():
                    self.state = WINNING
                else:
                    self.state = LOSING
                self.wintime = pygame.time.get_ticks()
                    
          
        elif self.state in [ WON ]:
            if evt.type == KEYDOWN:
                    sounds.apagarSonidos()
                    self.end(GANO)
        elif self.state in [ LOST, TOMATO ]:
            if evt.type == KEYDOWN:
                    sounds.apagarSonidos()
                    self.end(PERDIO)
                
    
    
    
    def loop(self):
        sounds.heatDeeJay(self.motor.calor)
        # aca updateamos el mundo cada paso
        if self.state == PLAYING:
            if self.motor.getTimeLeft() <= 0:
                self.state = TOMATOING
                sounds.gritosmalaonda()
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
                sounds.gritosfelicitacion()
        elif self.state == LOSING:
            if pygame.time.get_ticks() -self.wintime > 2000:
                self.state = LOST
                self.audiencia.setVoluntario(self.motor.voluntario_error, True)
                sounds.gritosmalaonda()
        elif self.state == TOMATOING:
            if pygame.time.get_ticks() -self.wintime > 2000:
                self.state = TOMATO

                
    def checkEaster(self, letra):
        self.todasLasTeclas += letra
        if "who is your daddy" in self.todasLasTeclas:
            self.audiencia.doEasterEgg()
                         
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
                    cursor_img = self.cursorfont.render("^", True, (255,255,255))
                    self.game.screen.blit(cursor_img, 
                                          (cursor_xpos,ypos+self.line_manager.height)
                                          )                    
            else:
                # paint forward
                xpos = 400
                ypos = 300
                cursor = self.motor.cursor
                if DEBUG: print "falta == ",self.motor.hechizo[cursor:]
                for position, letter in enumerate(self.motor.hechizo[cursor:]):
                    style = self.motor.estado[position+cursor]
                    
                        
                    i = self.line_manager.get(letter, self.motor.estado[position+cursor])
                    
                    self.game.screen.blit( i, (xpos, ypos) )
                    xpos += i.get_width()
                    if xpos > 800: break
                    
                surface= self.line_manager.get(self.motor.hechizo[cursor], self.motor.estado[cursor])
                width = surface.get_width()
                height = surface.get_height()
                
                cursor_sf = hollow.textOutline(self.cursorfont, "^", (150,150,250), (0,0,0))
                self.game.screen.blit( cursor_sf, (400+width/2-cursor_sf.get_width()/2,370))
                
                
                #pain backwards
                xpos = 400
                letters = [l for l in self.motor.hechizo[:cursor]]
                if DEBUG: print "done==", self.motor.hechizo[:cursor]
                letters.reverse()
                for position, letter in enumerate(letters):
                    style = self.motor.estado[-position+cursor]
                    
                        
                    i = self.line_manager.get(letter, self.motor.estado[-1-position+cursor])
                    width = i.get_width()
                    if xpos - width < 0: break
                    xpos -= width
                    self.game.screen.blit( i, (xpos, ypos) )
                    
                    
                
            

            self.level_timer.blit( self.game.screen, (770, 50))
            rate = self.motor.getRate()
            if rate < self.motor.precision_requerida:
                color_tx = (255,0,0)
            else:
                color_tx = (0,255,0)
                
            rate_sf = hollow.textOutline( self.ratefont, "%i%%"%(int(rate*100)),  color_tx, (0,0,0) )
            self.game.screen.blit( rate_sf, (770-rate_sf.get_width()/2, 35-rate_sf.get_height()/2))
        if self.state in [WON, LOST, TOMATO]:
            im = hollow.textOutline(font, "[press any key]", (30,30,200), (255,255,255))
            ypos = 400
            xpos = (800-im.get_width())/2
            
            self.game.screen.blit( im, (xpos, ypos) )
            
            
Foreground = None #= pygame.image.load("escenario/foreground.png")

def test():
    global Foreground
    Foreground = pygame.image.load("escenario/foreground.png")
    Foreground.convert()
    

class IntermediateScene(Scene):
    def update(self):
        self.audiencia.engine.update()
        self.game.screen.fill((0,0,0))
        surface = self.game.screen.subsurface(pygame.Rect(0,0,800,525))
        self.audiencia.render(surface, abs(self.calor)*100)
        surface.blit(self.fg, (0,0))
                       
class LevelIntro(Scene):
    def init(self, level_number, level_name, audiencia):
        test()
        self.level_number = level_number
        self.audiencia = audiencia
        self.level_name = level_name
        self.font = font =  pygame.font.Font("escenario/VeraMono.ttf",50)
        
    def update(self):
        self.audiencia.update()
        s = self.font.render("Level "+self.level_number, True, (255,255,255))
        self.background.blit(s, (100,100))
        self.audiencia.render(self.background, 100) #abs(self.calor)*100)
        self.background.blit(Foreground, (0,0))
        s = self.font.render(self.level_name, True, (255,255,255))
        self.background.blit(s, (100,300))
        self.game.screen.blit(self.background, (0,0))
    
    def event(self, evt):
        if evt.type == KEYDOWN:
                self.end()

class LevelSuccess(Scene):
    def init(self, score, levelscore, xaudiencia):
        self.score = score
        self.audiencia = xaudiencia
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
    def init(self, score, laaudiencia):
        self.score = score
        self.font = font =  pygame.font.Font("escenario/VeraMono.ttf",50)
        self.audiencia = laaudiencia
        
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
      
      
class Menu:
    def __init__(self, font, font_selected, opts, margin=0, normal_color=(255,255,255), selected_color=(255,255,255), selected_border_color=None, normal_border_color=None):
        self.font = font
        self.font_selected = font_selected
        if selected_border_color == None:
            selected_border_color = (0,0,0)
        if normal_border_color == None:
            normal_border_color = (0,0,0)
        self.margin = margin
        self.color = color
        self.opts = opts
        self.selected = 0
        self.selected_img = []
        self.unselected_img = []
        
        line_step = 0
        for text in self.opts:
            sel = hollow.textOutline(font_selected, text, selected_color, selected_border_color )
            unsel = hollow.textOutline(font, text, normal_color, normal_border_color )
            self.selected_img.append( sel )
            self.unselected_img.append( unsel )
            line_step = max(max(sel.get_height(), unsel.get_height())+self.margin, line_step)
            
        self.line_step = line_step
            
                
    def blit(self, surface, center_x, start_y):
        for i in range(len(self.opts)):
            
            if i == self.selected:
                img = self.selected_img[i]
            else:
                img = self.unselected_img[i]
                
            x = center_x-img.get_width()/2
            y = start_y + self.line_step * i - img.get_height()/2
            
            surface.blit( img, (x,y) )
            
    def next(self):
        self.selected = (self.selected + 1)%len(self.opts)
        
    def prev(self):
        self.selected = (self.selected - 1)%len(self.opts)     
        
    def set_mouse(self, x, y):
        i = self.get_mouse_over(x,y)
        if i is not None and  i != self.selected:
            self.selected = i
            return True        
    
    def get_mouse_over(self, x, y):
        for i in range(len(self.opts)):
            img = self.selected_img[i]
                
            tx = 0-img.get_width()/2
            ty = 0 + self.line_step * i - img.get_height()/2
            
            if tx <= x <= tx+img.get_width():
                if ty+10 <= y <= ty+img.get_height()-10:
                    return i
        return None
        
    def click_mouse(self, x, y):
        i = self.get_mouse_over(x,y)
        if i is not None:
            return i      
            
class Credits(Scene):
    sections = [
        ["magic by", "dr kapanga"],
        ["rabbits by", "fu man chu"],
        ]
        
    BEGIN, HIT, RETREAT, HANDOUT, DONE, LOOP = range(6)
    
    hand_start = -647,-200
    hand_end = -300,250
    puff_position = 400,250
    begin_duration = 1.5
    hit_duration = 0.0
    retreat_duration = 1.5
    handout_duration = 4
    done_duration = 0
    loop_duration = 5
    
    def init(self, font, color=(255,255,255), outline_color=(0,0,0)):
        self.section_imgs = []
        for section in self.sections:
            lines = []
            for line in section:
                img = hollow.textOutline(font, line, color, outline_color)
                lines.append( line )
            self.section_imgs.append( lines )
            
        self.section_number = 0
        self.state = self.BEGIN
        self.state_start = time.time()
        self.hand_pos = None
        self.hand_img = None
        self.puff_img = None
        self.puff_pos = None
        self.text = None
        
        self.hand = pygame.image.load("escenario/manos/mano1.png").convert_alpha()
        self.hand2 = pygame.image.load("escenario/manos/mano2.png").convert_alpha()
        
    def event(self, evt):
        if evt.type == KEYDOWN:
            self.end()
                
                
    def loop(self):
        if self.state == self.BEGIN:
            if time.time() - self.state_start >= self.begin_duration:
                self.state = self.HIT
                self.state_start = time.time()          
            else:
                p = (1-(time.time()-self.state_start)/self.begin_duration)**2
                
                sx, sy = self.hand_start
                ex, ey = self.hand_end
                nx = sx + (ex-sx)*p
                ny = sy + (ey-sy)*p
                
                self.hand_pos = nx, ny
                self.hand_img = self.hand
            
        elif self.state == self.HIT:
            if time.time() - self.state_start >= self.hit_duration:
                self.state = self.RETREAT
                self.state_start = time.time()
        elif self.state == self.RETREAT:
            if time.time() - self.state_start >= self.retreat_duration:
                self.state = self.HANDOUT
                self.state_start = time.time()
            else:
                p = (time.time()-self.state_start)/self.begin_duration
                
                sx, sy = self.hand_start
                ex, ey = self.hand_end
                nx = ex - (ex-sx)*p
                ny = ey - (ey-sy)*p
                
                self.hand_pos = nx, ny
                self.hand_img = self.hand2
                
        elif self.state == self.HANDOUT:
            if time.time() - self.state_start >= self.handout_duration:
                self.state = self.DONE
                self.state_start = time.time()
            else:
                self.hand_pos = None
        elif self.state == self.DONE:
            if time.time() - self.state_start >= self.done_duration:
                self.state = self.BEGIN
                self.state_start = time.time()
            else:
                self.hand_pos = None
        elif self.state == self.LOOP:
            if time.time() - self.state_start >= self.begin_duration:
                self.state = self.BEGIN
                self.state_start = time.time()
            else:
                self.hand_pos = None
                    
    def update(self):
        self.game.screen.blit(self.background, (0,0))
        
        if self.text:
            pass
        if self.puff_img:
            pass
        if self.hand_pos:
            self.game.screen.blit(self.hand_img, self.hand_pos )
        
class MainMenu(Scene):
    def init(self):
        self._background = pygame.image.load("escenario/screens/menu.png").convert()
        self.font = font =  pygame.font.Font("escenario/MagicSchoolOne.ttf",90)
        self.menu = Menu(
                 pygame.font.Font("escenario/MagicSchoolOne.ttf",50),
                 pygame.font.Font("escenario/MagicSchoolOne.ttf",70),
                 ["History Mode", "Freestyle", "Hiscores", "Credits", "Quit"],
                 margin = -40,
                 normal_color = (173,148,194),
                 selected_color = (244,232,255),
                 )
        
    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.menu.blit(self.game.screen, 400, 180)
        
    def event(self, evt):
        if evt.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            x -= 400
            y -= 180
            if self.menu.set_mouse(x,y):
                sounds.pasa()
                self.paint()
        elif evt.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            x -= 400
            y -= 180
            sel = self.menu.click_mouse(x,y)
            if sel is not None:
                sounds.enter()
                self.do_action(sel)
        elif evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            elif evt.key == K_DOWN:
                self.menu.next()
                sounds.pasa()
                self.paint()
            elif evt.key == K_UP:
                self.menu.prev()
                sounds.pasa()
                self.paint()
            elif evt.key in [K_RETURN, K_SPACE]:
                sel = self.menu.selected
                sounds.enter()
                self.do_action(sel)
                
    def do_action(self, sel):
        if sel == 0: # history
            self.play_freestyle()
        elif sel == 1: # freestyle
            self.play_freestyle()
        elif sel == 2: # hiscores
            self.hiscores()
        elif sel == 3: # credits
            self.runScene( Credits( self.game, self.font ) )
        elif sel == 4: #quit            
            self.end()
                    
    def play_history(self):
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

    def play_freestyle(self):
            result = GANO
            count = 0
            score = 0
            futech = 0
            while result == GANO:
                laAudiencia = audiencia.Audiencia(level_number=count)
                if count < len(levels):
                    subtitle = levels[count][0]
                    params = levels[count][1]
                else:
                    if futech == 0: futech = count-1
                    subtitle = "Future tech "+str(count-futech)
                    params = dict(tiempo_por_caracter=1.0/(count-futech+4))
                self.runScene( 
                        LevelIntro( self.game, str(count), subtitle, laAudiencia ) )
                l =  Level(self.game, count, MainMotor(**params), laAudiencia) 
                laAudiencia.doGame()
                result = self.runScene( l )
                newscore = int(l.motor.score)
                score += newscore
                if result == GANO:
                    laAudiencia.doWin()
                    self.runScene( 
                        LevelSuccess(self.game, score, newscore, laAudiencia))
                count += 1
            laAudiencia.doGameOver()
            self.runScene( GameOver( self.game, score, laAudiencia ) )

def main():
    g = Game(800, 525, framerate = 20, title = "Typus Pocus")

    g.run( MainMenu(g) )
    
if __name__ == "__main__":
    main()
