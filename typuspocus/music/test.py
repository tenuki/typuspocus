"""
typus pocus: dynamic background music test

usage: python3 test.py
"""

import os
import random

import pygame


pygame.init()
sfiles = [
    f for f in os.listdir('.') if f.startswith('mm') and f.endswith('ogg') and f != 'mmend.ogg']
sounds = [pygame.mixer.Sound(f) for f in sfiles]
chan = pygame.mixer.Channel(0)

while True:
    if chan.get_queue():
        pygame.time.wait(200)
    else:
        rnum = random.randint(0, len(sfiles) - 1)
        print('queuing %s ...' % sfiles[rnum])
        chan.queue(sounds[rnum])
