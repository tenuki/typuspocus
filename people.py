import os, re, random
import pygame
from pygame.locals import *
from engine import Game, Scene

Layers = None
iLayers = None

class SampleScene(Scene):
    def init(self, nombre, wardrobe):
        self.nombre = nombre
        self.goscene=False
        self.finalizar = False
        self.wardrobe = wardrobe
        
    def event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            elif evt.key == K_SPACE:
                self.goscene = True
            elif evt.key == K_RETURN:
                self.finalizar = True
    
    def loop(self):
        # aca updateamos el mundo cada paso
        if self.goscene:
            retorno = self.runScene( SampleScene(self.game, self.nombre + " hijo ") )
            self.goscene = False
            #print "devolvio", retorno
        if self.finalizar:
            self.end( self.nombre )
                    
    def update(self):
        global iLayers
        self.background = pygame.Surface( (800,600) )
        some = Individual(self.wardrobe)
        some.random()
        self.background = some.render()
        self.game.screen.blit(self.background, (0,0))
        font = pygame.font.SysFont("Times New Roman",30)
        s = font.render(self.nombre,True,(0,255,255))
        self.game.screen.blit(s, (0,0))


class Individual:
    def __init__(self, wardrobe):
        self.wardrobe=wardrobe
        self.layers={}
    
    def random(self):
        layers = self.wardrobe.getLayers()
        s = random.randint(0, len(layers))
        sl = random.sample(layers, s)
        #sl.append('body') #skip this for invisible ppl!
        sl+=['jackets']
        if not 'body' in sl:
            sl=layers
            sl.remove('body')
        
        for layer in sl:
            self.layers[layer] = random.sample(self.wardrobe.articles[layer], 1)
    
    def __repr__(self):
        return repr(self.layers)

    def render(self ): # , layerorder):
        layerorder = self.wardrobe.getLayerorder()
        order = layerorder.keys()
        order.sort()
        img = None
        #print order
        #print layerorder
        for k in order:
            layername=layerorder[k]
            #print layername
            if layername in self.layers.keys():
                #we use that layer!
                article = self.layers[layername][0]
                if img==None:
                    img = pygame.Surface( (91, 139) ) #full size
                    nx,ny = article.SnapPos()
                    img.blit(article.getImage(), article.SnapPos())
                    x,y=img.get_size()
                    
                else:
                    nimg = article.getImage()
                    x, y = article.SnapPos()
                    xsize, ysize = img.get_size()
                    img.blit(nimg, (x,y))
        return img
        


BasicFieldList = """"0"     "id"
"1"     "imageName"
"2"     "category"
"3"     "layer"
"4"     "snapPosX"
"5"     "snapPosY"
"6" "wearing"
"7" "waldrobe" """.split('\n')

class FieldSet:
    RE = re.compile(r'"(.*)"[ \t]*"(.*)".*')
    def __init__(self, fields=BasicFieldList):
        for f in fields:
            g = FieldSet.RE.match(f)
            if not g:
                raise Exception('Invalid fields "%s"'%repr(f))
            k,v=g.groups()
            setattr(self,v.lower(),int(k))

class Article:
    RE = re.compile('"(.*)" *'*7 + '.*')    
    def __init__(self, dataline, fieldset, path=''):
        self.fieldset = fieldset
        m = Article.RE.match(dataline)
        if not m : raise Exception('Invalid article data "%s"'%repr(dataline))    
        self.data = m.groups()
        self.image = None
        self.path = path
        
    def __repr__(self):
        return self.name

    def getSome(self,some):
        return self.data[getattr(self.fieldset,some)]
    def getLayer(self):
        return self.getSome('layer')
    def getName(self):
        return self.getSome('imagename')
    def getImage(self):
        if self.image==None:
            #self.image=Image.open(self.path+self.name)
            self.image=pygame.image.load(self.path+self.name)
            #print repr(self.image)
        #return self.image
        return self.image
    def SnapPos(self):
        return int(self.getSome('snapposx')),int(self.getSome('snapposy'))
    layer=property(getLayer)
    name=property(getName)
    
    def wget (self, fname):
        """fetch image"""
        os.spawnlp(os.P_WAIT, '/sw/bin/wget', 'wget', fname)

class Wardrobe:
    def __init__(self, path):
        self.articles={}
        self.parseConfig(path)
        self.parseArticles(path)
        
    def add(self, article):
        layer = article.layer
        artlist = self.articles.setdefault(layer, [])
        artlist.append(article)
        self.articles[layer]=artlist

    def getLayers(self):
        return self.articles.keys()
    
    def getLayerorder(self):
        return self.ordered
        
    def parseConfig(self,path):
        """get layers"""
        R = re.compile(r'"layer(.*)" *"(.*)".*')
        self.layers={}
        self.ordered = {}
        f = open(path+'config.txt')
        for l in f:
            if l[0]=='#': continue
            m = R.match(l)
            if m:
                k,v = m.groups()
                self.layers[v]=int(k)
                self.ordered[int(k)]=v
            #print m
            #print self.layers
            #print self.ordered
        f.close()
        #print '-----------------'
        #print self.layers
        #print self.ordered
    
    def parseArticles(self, path):
        articlelist=[]
        self.fieldlist=[]
        buscando, leyendoFields, leyendoArticles, listo = range(4)
        status = buscando
        fpath=path+r'/data/'
        f = open(path+'/articles.txt')
        for l in f:
            l = l.strip('\n')
            if status==buscando:
                self.fieldset = FieldSet() #basic default fieldset
                if l.startswith('HCDataSetFile_fields'):
                    status=leyendoFields
                    
            elif status==leyendoFields:
                if l.startswith('HCDataSetFile_data'):
                    self.fieldset = FieldSet(self.fieldlist)
                    status=leyendoArticles
                elif l.startswith('#'): pass
                elif l.startswith('"'):
                    self.fieldlist.append(l)
                    
            elif status==leyendoArticles:
                if l.startswith('"'):
                    self.add(Article(l, self.fieldset, path+'/data/'))
                elif l.startswith('#'):
                    pass
                else: status=listo
            elif status==listo:
                break
        f.close()

    
    
if __name__ == "__main__":
    #Wardrobe2 = Wardrobe('audiencia/fashion_boy/')
    #Wardrobe1 = Wardrobe('audiencia/fashion_girl/')
    #Wardrobe1 = Wardrobe('audiencia/girl/')
    #Wardrobe1 = Wardrobe('audiencia/goth/')
    Wardrobe1 = Wardrobe('audiencia/boy/')
    g = Game(800, 600, framerate = 200)
    g.run( SampleScene(g, "Scene1", Wardrobe1) )
    
    