import pygame
import os
import random

VOLUMEN_MUSICA = 0.5

class Sounds:
    def init(self):
        pygame.mixer.set_reserved(3)
        self.canalMusica = pygame.mixer.Channel(0)
        self.canalMusica.set_volume(VOLUMEN_MUSICA)
        self.canalAmbiente = pygame.mixer.Channel(1)
        self.canalPalabras = pygame.mixer.Channel(2)

        for s in ["genteunpocobien", "gentetranquila", "genteunpocomal"]:
            self.sonidoEnCanal(s, self.canalAmbiente)

        for s in ["arenga", "puteada"]:
            self.multiplesEnCanal(s, self.canalPalabras)

        for s in ["tick1", "tick2", "suspenso", "bravo.wav", "bu.wav"]:
            self.sonidoSuelto(s)

        self.musicfiles = [f for f in os.listdir('music') if f.startswith('mm') and f.endswith('ogg') and f != 'mmend.ogg']
        self.musicparts = [pygame.mixer.Sound('music/' + f) for f in self.musicfiles]

    def randomDeeJay(self):
        if not self.canalMusica.get_queue():
            rnum = random.randint(0, len(self.musicparts) - 1)
            #print 'queuing %s ...' % self.musicfiles[rnum]
            self.canalMusica.queue(self.musicparts[rnum])

    def silenciarDeeJay(self):
        self.canalMusica.fadeout(500)

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
