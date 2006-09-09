import random
import math

import pygame
from pygame.locals import *

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
        
    def render(self, surface, porcentaje):
        if random.randint(0,1000)<porcentaje:
            gx = random.choice([-1,0,1])
            gy = random.choice([-1,-2,0])
        else:
            gx, gy = 0,0
        dx, dy = self.position
        
        #get random state
        #surface.blit(random.choice(self.images), (dx+gx, dy+gy))
        surface.blit(self.images[0], (dx+gx, dy+gy))

class Fila:
    sillas=None
    def __init__(self, level_number,(dx,dy)):
        self.position = (dx, dy)
        if Fila.sillas is None:
            Fila.sillas = self.construirSillas()
        self.personas = []
        for x in range(filasx):
            if random.random() > (level_number/5.0+0.1):
                self.personas.append(None)
            else:
                self.personas.append( Persona((dx+x*peoplex,dy), level_number) )

    def construirSillas(self):
        MAGENTO = (254,0,254)
        img = pygame.image.load('escenario/butaca.png')
        base = pygame.Surface((800, peopley))
        base.fill(MAGENTO)
        for x in range(filasx):
            base.blit(img, (peoplex * x, 0) )
        base.convert()
        base.set_colorkey(MAGENTO)
        return base

    def render(self, surface, porcentaje ):
        surface.blit(Fila.sillas, self.position)
        for x, persona in enumerate(self.personas):
            if persona is not None:
                persona.render(surface, porcentaje)


class Audiencia:
    def __init__(self, level_number):
        people.resetRandom(level_number)
        self.filas = []
        for y in range(filasy):
            dx = (y%2) * peoplex/2 - peoplex/2 + 6
            dy = peopley/2 * y
            self.filas.append(Fila(level_number,(dx,dy)))

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
    def init(self, level_number):
        self.finalizar = False
        self.audiencia = Audiencia(level_number)
        self.voluntario = None
        self.calor = 0
        self.level_number = level_number
        self.fg = pygame.image.load("escenario/foreground.png")
        self.fg.convert()
        self.varitaje = varitaje.Varitaje()
        self.mano = pygame.image.load("escenario/manos/mano1.png")
        self.mano.convert()
        self.puffing = 0
        self.nubes = [ pygame.image.load("escenario/nube/nube%d.png"%(n+1)) for n in range(5) ]
        for img in self.nubes:
            img.convert()

        self.tomate = pygame.image.load("escenario/tomates/tomate.png")
        self.tomate.convert()
        self.tomate_aplastado = pygame.image.load("escenario/tomates/tomate_aplastado.png")
        self.tomate_aplastado.convert()

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
        self.mano = pygame.image.load("escenario/manos/mano-easteregg.png")
        self.mano.convert()

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
