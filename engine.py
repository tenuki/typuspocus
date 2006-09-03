import pygame
from pygame.locals import *
DEBUG = 1

class Game:
    def __init__(self, x_size, y_size, framerate=30):
        pygame.init()
        self.screen_size = x_size, y_size
        self.x_size = x_size
        self.y_size = y_size
        self.screen = pygame.display.set_mode((x_size, y_size)) 
        pygame.mixer.set_reserved(3)
        self.framerate = framerate   
        self.clock = pygame.time.Clock()
        
    def run(self, scene):
        scene.run( )
        if DEBUG: print "FPS:", self.clock.get_fps()
        
    def tick(self):
        self.clock.tick(self.framerate)

   
        
class SceneExit(Exception):
    pass
    
class Scene:
    bg_color = (0,0,0)
    
    @property 
    def background(self):
        if self._background is None:
            self._background = pygame.Surface(self.game.screen.get_size()).convert()
            self._background.fill(self.bg_color)
        return self._background
        
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self._background = None
        self.init(*args, **kwargs)
        
    def init(self): pass
        
    def end(self, value=None):
        self.return_value = value
        raise SceneExit()
        
    def runScene(self, scene):
        ret = scene.run()
        if DEBUG: print "Left Scene", str(scene), "with", ret
        self.paint()
        return ret
        
    def run(self):
        if DEBUG: print "Entering Scene:", str(self)
        self.game.screen.blit(self.background, (0,0))
        self.paint()
        pygame.display.flip()
        while 1:
            self.game.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                else:
                    try:
                        self.event(event)
                    except SceneExit:
                        return self.return_value
                    
            try:
                self.loop()
            except SceneExit:
                return self.return_value
            self.update()
            pygame.display.flip()
        
    def event(self, evt):
        pass
        
    def loop(self):
        pass
        
    def update(self):
        pass
        
    def paint(self):
        pass
     
