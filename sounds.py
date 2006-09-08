import pygame
import os
import random

class Sounds:
    def init(self):
        pygame.mixer.set_reserved(3)
        self.canalMusica = pygame.mixer.Channel(0)
        self.canalAmbiente = pygame.mixer.Channel(1)
        self.canalPalabras = pygame.mixer.Channel(2)

        for s in ["genteunpocobien", "gentetranquila", "genteunpocomal"]:
            self.sonidoEnCanal(s, self.canalAmbiente)

        for s in ["arenga", "puteada"]:
            self.multiplesEnCanal(s, self.canalPalabras)

        for s in ["tick1", "tick2", "suspenso", "bravo.wav", "bu.wav"]:
            self.sonidoSuelto(s)

    def buildSonido(self, s):
        if "." not in s:
            s += ".ogg"
        return pygame.mixer.Sound("sounds/"+s)


    def multiplesEnCanal(self, s, canal):
        sonidos = [ self.buildSonido(n) for n in os.listdir("sounds") if n.startswith(s) and "." in n ]
        def play():
            canal.queue(random.choice(sonidos))
            canal.fadeout(50)
        setattr(self, s, play)
        
    def sonidoEnCanal(self, s, canal):
        sonido = self.buildSonido(s)
        def play():
            canal.queue(sonido)
            canal.fadeout(50)

        if s.endswith(".wav"):
            s = s[:-4]
        
        setattr(self, s, play)
            
    def sonidoSuelto(self, s):
        sonido = self.buildSonido(s)
        if s.endswith(".wav"):
            s = s[:-4]
        setattr(self, s, sonido.play)

sounds = Sounds()

if __name__ == "__main__":
    pygame.init()
    sounds.init()
    print dir(sounds)
