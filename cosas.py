import pygame
import os
base = "escenario/cosas/"
for i in os.listdir(base):
    if i[-3:] in ["png", "bmp", "gif"]:
        locals()[i.split(".")[0]] = pygame.image.load(base + i)
        
del os
del pygame
del base