import interpol
import pygame

boundsRect = pygame.Rect(0,200,700,400)

class Varitaje:
    def nextpos(self):
        r=pygame.Rect( pygame.mouse.get_pos(), (1,1) )
        return r.clamp(boundsRect).center

if __name__ == "__main__":
    pass
