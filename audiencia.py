import random
import math
import pygame
from pygame.locals import *
import time

from engine import Game, Scene
import people
import varitaje
import motor
import interpol
from sounds import sounds

DEBUG = 0

peoplex,peopley = (55, 119)
filasx, filasy = (800/peoplex,600/peopley)

MAXPUFFING = 10
MAXTOMATEANDO = 20

class Persona:
    def __init__(self, (dx, dy), level_number):
        self.position = (dx,dy)
        individuo = people.buildIndividual(level_number)
        self.images = map(lambda state:individuo.render(state), people.iStates)
        self.state = people.iStates[0]
        self.alive = False
        self.deltay = 0
        
    def subirse(self):
        self.deltay = - peopley/4
    def sentarse(self):
        self.deltay = 0
    def camina(self):
        self.deltay = - peopley/6

    def alive(self):
        self.alive = True
                        
    def render(self, surface, porcentaje):
        if self.alive and random.randint(0,1000)<porcentaje:
            gx = random.choice([-1,0,1])
            gy = random.choice([-1,-2,0])
        else:
            gx, gy = 0,0
        dx, dy = self.position
        
        #get random state
        surface.blit(self.images[0], (dx+gx, dy+gy+self.deltay))

class Fila:
    sillas=None
    def __init__(self, level_number,(dx,dy), people):
        self.position = (dx, dy)
        if Fila.sillas is None:
            Fila.sillas = self.construirSillas()
        self.personas = people

    def construirSillas(self):
        MAGENTO = (254,0,254)
        img = pygame.image.load('escenario/butaca.png')
        base = pygame.Surface((800, peopley))
        base.fill(MAGENTO)
        for x in range(filasx):
            base.blit(img, (peoplex * x, 0) )
        base = base.convert()
        base.set_colorkey(MAGENTO)
        return base

    def render(self, surface, porcentaje ):
        surface.blit(Fila.sillas, self.position)
        for x, persona in enumerate(self.personas):
            if persona is not None:
                persona.render(surface, porcentaje)

class EnginePersonas:
    def __init__(self, peopleSet):
        pass

class IntroEngine(EnginePersonas):
    def __init__(self, peopleSet, level_number):
        self.ps = peopleSet
        self.caminando = 0
        for y in range(filasy):
            for x in range(filasx):
                if random.random() > (level_number/5.0+0.1):
                    pass
                else:
                    self.caminando += 1
                    dx = (y%2) * peoplex/2 - peoplex/2 + 6
                    dy = peopley/2 * y                    

                    final = (x*peoplex+dx,dy)
                    if x < filasx/2:
                        tx = dx
                    else:
                        tx = filasx*peoplex+dx
                    #rtx = random.choice( [0+dx, filasx*peoplex+dx] )
                    inicial = (tx, dy )
                    p = Persona( inicial, level_number)
                    p.camina()
                    p.destpos = final
                    p.inipos = inicial
                    v = (p.destpos[0]-tx)
                    if v==0: v=1
                    p.xdir = v/abs(v)
                    p.velocidad = random.randint(20,80) * (p.xdir) 
                    peopleSet[y].append( p )
        self.startTime = time.time()

    def update(self):
        self.caminarUpdate()
        
    def caminarUpdate(self):
        dt = time.time() - self.startTime
        for persons in self.ps.values():
            for p in persons:
                npx = p.inipos[0] + p.velocidad * dt
                x,y = p.destpos
                if p.xdir>0 and (npx<p.destpos[0]):
                    x = npx
                elif p.xdir<0 and (npx>p.destpos[0]):
                    x = npx
                p.position = (x,y)
                if p.position == p.destpos:
                    self.caminando -= 1
                    p.sentarse()
                    
    def finish(self):
        for persons in self.ps.values():
            for p in persons:
                p.position = p.destpos
        
    def done(self):
        return self.caminando == 0            

class GOEngine(EnginePersonas):
    def __init__(self, peopleSet, level_number):
        self.ps = peopleSet
        for persons in self.ps.values():
            for p in persons:
                p.camina()
                p.xdir = - p.xdir
                p.velocidad = -p.velocidad
                p.inipos, p.destpos = p.destpos, p.inipos
        self.startTime = time.time()
        
    def update(self):
        self.caminarUpdate()
        
    def caminarUpdate(self):
        dt = time.time() - self.startTime
        for persons in self.ps.values():
            for p in persons:
                npx = p.inipos[0] + p.velocidad * dt
                x,y = p.destpos
                if p.xdir>0 and (npx<p.destpos[0]):
                    x = npx
                elif p.xdir<0 and (npx>p.destpos[0]):
                    x = npx
                p.position = (x,y)
                if p.position == p.destpos:
                    p.sentarse()


class GameEngine:
    def __init__(self, peopleSet, level_number):
        self.ps = peopleSet
    def finish(self):
        pass        
    def update(self):
        pass
    

class Audiencia:
    def __init__(self, level_number):
        people.resetRandom(level_number)
        self.personas = {}
        for y in range(filasy):
            self.personas[y]=[]
        self.level = level_number
        self.engine = IntroEngine(self.personas, level_number)

        self.filas = []
        for y in range(filasy):
            dx = (y%2) * peoplex/2 - peoplex/2 + 6
            dy = peopley/2 * y
            self.filas.append(Fila(level_number,(dx,dy), self.personas[y]))
    def update(self):
        self.engine.update()    
    def doGame(self):
        self.engine.finish()
        self.engine = GameEngine(self.personas, self.level)
    def doGameOver(self):
        self.engine.finish()
        self.engine = GOEngine(self.personas, self.level)
    def doWin(self):
        self.engine.finish()
        self.engine = GOEngine(self.personas, self.level)
    
    def getRandomPersonPosition(self):
        fila = random.randrange(filasy)
        dx = (fila%2) * peoplex/2 - peoplex/2 + 6
        dx += random.randrange(filasx)* peoplex
        dy = peopley/2 * fila
        return (dx+peoplex/2, dy+20)

    def render(self, surface, porcentaje):
        for fila in self.filas:
            fila.render(surface, porcentaje)

class AudienciaScene(Scene):
    def init(self, level_number, audiencia):
        self.finalizar = False
        self.audiencia = audiencia #Audiencia(level_number)
        self.voluntario = None
        self.lastbravo = time.time()
        self.calor = 0
        self.level_number = level_number
        self.fg = pygame.image.load("escenario/foreground.png").convert_alpha()
        self.varitaje = varitaje.Varitaje()
        self.mano = pygame.image.load("escenario/manos/mano1.png").convert_alpha()
        self.puffing = 0
        self.nubes = [ pygame.image.load("escenario/nube/nube%d.png"%(n+1)).convert_alpha() for n in range(5) ]
        self.tomate = pygame.image.load("escenario/tomates/tomate.png").convert_alpha()
        self.tomate_aplastado = pygame.image.load("escenario/tomates/tomate_aplastado.png").convert_alpha()

        self.tomateando = None

        pygame.mixer.set_reserved(2)
        self.channel = pygame.mixer.Channel(0)
        self.channelVoces = pygame.mixer.Channel(1)

    def event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            elif evt.key == K_RETURN:
                self.finalizar = True
                
    def gameEvent(self, evt):
        Threshold=0.20
        aLittleProb = 0.1 
        
        channel=None
        
        if evt == motor.Eventos.PALOK:
            sounds.arenga()
        elif evt == motor.Eventos.PALMAL:
            sounds.puteada()
        elif evt == motor.Eventos.OK_DEUNA:
            r = random.random()
            if self.calor>r:
                if time.time()-self.lastbravo>1.5:
                    self.lastbravo = time.time()            
                    sounds.bravo()
        elif evt == motor.Eventos.MAL:
            sounds.bu()

            
        if channel:
            cabs = abs(self.calor)
            r = random.random()
            if (cabs>Threshold) or (r<aLittleProb): 
                channel.set_volume(cabs,cabs)
            else:
                channel.stop()
        
    def setCalor(self, calor):
        self.calor = calor
    
    def loop(self):
        # aca updateamos el mundo cada paso
        if self.finalizar:
            self.end( )
                    
    def update(self):
        self.audiencia.update()
        self.game.screen.fill((0,0,0))
        surface = self.game.screen.subsurface(pygame.Rect(0,0,800,525))
        self.audiencia.render(surface, abs(self.calor)*100)
        surface.blit(self.fg, (0,0))

        if self.voluntario != None:
            surface.blit(self.voluntario, self.voluntario.get_rect(midbottom=(400,370)))

        if self.puffing > 1:
            self.puffing -= 1
            n = int( len(self.nubes) * (1 - self.puffing/float(MAXPUFFING)) )
            if DEBUG: print n, len(self.nubes)
            nube = self.nubes[n]
            surface.blit(nube, nube.get_rect(midbottom=(400,420)))

        if self.tomateando is not None:
            if self.tomateando > 0:
                self.tomateando -= 1

                rotacion = (float(self.tomateando)/MAXTOMATEANDO)*180
                scale = math.sqrt(1.0/(1+float(self.tomateando)))**3
                imagen = pygame.transform.rotozoom(self.tomate,rotacion,scale)

                p = self.tomateMB.getAt( 1.0-0.1*self.tomateando )
                surface.blit(imagen, imagen.get_rect(center=p))
        else:
            surface.blit(self.mano, self.mano.get_rect(center=self.varitaje.nextpos()))

        if self.tomateando == 0:
            imagen = self.tomate_aplastado
            surface.blit(imagen, imagen.get_rect(center=surface.get_rect().center))

    def doEasterEgg(self):
        self.mano = pygame.image.load("escenario/manos/mano-easteregg.png").convert_alpha()

    def setVoluntario(self, voluntario, hacerPuff):
        """cambia el voluntario. Si hacerPuff es true, entonces baja la varita y hace aparecer el humito"""
        self.voluntario = voluntario
        if hacerPuff:
            self.puffing = MAXPUFFING
            if DEBUG: print "------------MaxPuffing-------------"

    def tomateame(self):
        self.tomateando = MAXTOMATEANDO
        self.tomateMB = interpol.MadamBezier(
                            self.audiencia.getRandomPersonPosition(),(400,300)) 
        
if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)
    g.run( AudienciaScene(g, 10) )
