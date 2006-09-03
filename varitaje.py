import pygame
import random
import interpol

boundsRect = pygame.Rect(0,200,700,400)

class Varitaje:
    def __init__(self):
        self.pos = (400,450)
        self.l = {False:((000,300),(300,600)),
                    True: ((300,300),(700,600)) }
        self.last = True
        self.step = 0
        self.max = 30
        self.prev = None
        self.inter = None
        self.points = []
        
    def generatePoint(self):
        where = self.l[self.last]
        self.last = not self.last
        inicio, fin = where
        rand = random.randint(inicio[0],fin[0]),random.randint(inicio[1],fin[1])
        self.points.append(rand)
        
    def nextpos(self):
        r=pygame.Rect( pygame.mouse.get_pos(), (1,1) )
        return r.clamp(boundsRect).center
        if len(self.points)<5: 
            for i in range(5): 
                self.generatePoint()
        if self.step%self.max==0:
            self.step=0
            self.inter = interpol.MadamBezier( 
                            self.pos, self.points.pop(0), self.inter )
        self.step+=1
        interpos = self.inter.getAt( 3.03 * (self.step-1) )
        print interpos
        return interpos

if __name__ == "__main__":
    pass
