import pygame
from pygame.locals import *
from engine import Game, Scene
from people import *
import random
peoplex,peopley = (55, 119)
filasx, filasy = (800/peoplex,600/peopley)

wardrobes = getAllWardrobes()
def buildIndividual():
    wd=random.choice(wardrobes)
    i= Individual(wd)
    i.random()
    return i

class Fila:
    sillas=None
    def __init__(self):
        if Fila.sillas is None:
            Fila.sillas = self.construirSillas()
        self.personas = [ buildIndividual().render() for x in range(filasx) ]

    def construirSillas(self):
        img = pygame.image.load('escenario/butaca.png')
        img.convert_alpha()
        base = pygame.Surface((800, peopley), 0, img)
        for x in range(filasx):
            base.blit(img, (peoplex * x, 0) )
        return base

    def render(self, surface, (dx,dy) ):
        surface.blit(Fila.sillas, (dx,dy))
        for x, persona in enumerate(self.personas):
            if random.randint(0,90)==0:
                gx = random.choice([-1,0,1])
                gy = random.choice([-1,-2,0])
            else:
                gx, gy = 0,0
            surface.blit(persona, ((x*peoplex)+dx+gx, dy+gy))


class Audiencia:
    def __init__(self):
        self.filas = [ Fila() for y in range(filasy) ]
        self.fg = pygame.image.load("escenario/foreground.png")
        self.fg.convert()

    def render(self, surface):
        for y,fila in enumerate(self.filas):
            dx = (y%2) * peoplex/2 - peoplex/2 + 6
            dy = peopley/2 * y
            fila.render(surface, (dx,dy) )
        surface.blit(self.fg, (0,0))

class AudienciaScene(Scene):
    def init(self):
        self.finalizar = False
        self.audiencia = Audiencia()

    def noop(self):
        for y in range(filasy):
            for x in range(filasx):
                some = buildIndividual()
                dx = (y%2) * peoplex/2 - peoplex/2 + 6
                self.bg.blit(some.render(),(peoplex*x+dx, peopley/2*y)) 
        
    def event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            elif evt.key == K_RETURN:
                self.finalizar = True
    def gameEvent(self):
        pass
    
    def loop(self):
        # aca updateamos el mundo cada paso
        if self.finalizar:
            self.end( )
                    
    def update(self):
        global iLayers
        self.game.screen.fill((0,0,0))
        self.audiencia.render(self.game.screen)
        
if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)
    g.run( AudienciaScene(g, "Scene1") )
