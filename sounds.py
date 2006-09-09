import pygame
import os
import random
DEBUG = 1

VOLUMEN_MUSICA = 0.3

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

        self.music_groups  = [
            ['mmjaz1', 'mmjaz2', 'mmjaz3', 'mmjaz4', 'mmlala1', 'mmlala2', 'mmlala3', 'mmlala4'],
            ['mmbas1', 'mmbas2', 'mmin1', 'mmin2', 'mmin3', 'mmin4', 'mmin5', 'mmin6', 'mmin7', 'mmin8'],
            ['mmdnza1', 'mmdnza2', 'mmdnza3', 'mmdnza4', 'mmdnzb1', 'mmdnzb2', 'mmdnzb3', 'mmdnzb4', 'mmdnzb5', 'mmdnzb6', 'mmdnzb7'],
            ]
        self.music_parts = [[pygame.mixer.Sound('music/%s.ogg' % fname) for fname in group] for group in self.music_groups]
        self.music_part_count = len(self.music_parts)
        
        self.musicfiles = [f for f in os.listdir('music') if f.startswith('mm') and f.endswith('ogg')]
        self.musicparts = [pygame.mixer.Sound('music/' + f) for f in self.musicfiles]
        self.music_end  = pygame.mixer.Sound('music/music_end.ogg')
                            

    def randomDeeJay(self):
        if not self.canalMusica.get_queue():
            rnum = random.randint(0, len(self.musicparts) - 1)
            #print 'queuing %s ...' % self.musicfiles[rnum]
            self.canalMusica.queue(self.musicparts[rnum])

    def heatDeeJay(self, calor):
        if not self.canalMusica.get_queue():
            group_idx = int((calor + 1) / 2.1 * self.music_part_count)
            print 'calor: %.2f; music_group: %d' % (calor, group_idx)
            self.canalMusica.queue(random.choice(self.music_parts[group_idx]))

    def silenciarDeeJay(self):
        #self.canalMusica.stop()
        #self.canalMusica.play(self.music_end)
        self.canalMusica.fadeout(50)

    def buildSonido(self, s):
        if "." not in s:
            s += ".ogg"
        if DEBUG: print "Loading sound:", s
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
