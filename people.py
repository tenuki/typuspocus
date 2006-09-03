import os, re, random
import pygame
from pygame.locals import *
from engine import Game, Scene

class SampleScene(Scene):
    def init(self, nombre):
        self.nombre = nombre
        self.goscene=False
        self.finalizar = False
        
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
            print "devolvio", retorno
        if self.finalizar:
            self.end( self.nombre )
                    
    def update(self):
        self.background = Surface( (800,600) )
    
        self.game.screen.blit(self.background, (0,0))
        font = pygame.font.SysFont("Times New Roman",30)
        s = font.render(self.nombre,True,(0,255,255))
        self.game.screen.blit(s, (0,0))


class Individual:
    def __init__(self, wardrobe):
        self.wardrobe=wardrobe
        self.layers={}
    
    def random(self):
        layers = self.wardrobe.layers()
        s = random.randint(0, len(layers))
        sl = random.sample(layers, s)
        sl.append('body') #skip this for invisible ppl!
        
        for layer in sl:
            self.layers[layer] = \
                random.sample(self.wardrobe.articles[layer], 1)
    
    def __repr__(self):
        return repr(self.layers)

    def render(self, layerorder):
        order = layerorder.keys()
        order.sort()
        print order
        img = None
        for k in order:
            layername=layerorder[k]
            print layername
            if layername in self.layers.keys():
                #we use that layer!
                print layername
                print self.layers
                article = self.layers[layername][0]
                if img==None:
                    nx,ny = article.SnapPos()
                    img = article.getImage()
                    x,y=img.size
                    
                elif 0:
                    nimg = article.getImage()
                    print dir(article)
                    x, y = article.SnapPos()
                    xsize, ysize = img.size
                    img.paste(nimg, (x,y,xsize, ysize))
        base.show()
        


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
    def __init__(self):
        self.articles={}
        
    def add(self, article):
        layer = article.layer
        artlist = self.articles.setdefault(layer, [])
        artlist.append(article)
        self.articles[layer]=artlist

    def layers(self):
        return self.articles.keys()
        
        
def parseConfig():
    """get layers"""
    R = re.compile(r'"layer(.*)" *"(.*)".*')
    layers={}
    ordered = {}
    f = open('config.txt')
    for l in f:
        if l[0]=='#': continue
        m = R.match(l)
        if m:
            k,v = m.groups()
            layers[v]=int(k)
            ordered[int(k)]=v
    f.close()
    return layers, ordered

def parseArticles():
    articlelist=[]
    fieldlist=[]
    wardrobe=Wardrobe()
    buscando, leyendoFields, leyendoArticles, listo = range(4)
    status = buscando
    path=r'data/'
    f = open('articles.php')
    for l in f:
        l = l.strip('\n')
        if status==buscando:
            fieldset = FieldSet() #basic default fieldset
            if l.startswith('HCDataSetFile_fields'):
                status=leyendoFields
                
        elif status==leyendoFields:
            if l.startswith('HCDataSetFile_data'):
                fieldset = FieldSet(fieldlist)
                status=leyendoArticles
            elif l.startswith('#'): pass
            elif l.startswith('"'):
                fieldlist.append(l)
                
        elif status==leyendoArticles:
            if l.startswith('"'):
                wardrobe.add(Article(l, fieldset, path))
            elif l.startswith('#'):
                pass
            else: status=listo
        elif status==listo:
            break
    f.close()
    return wardrobe, fieldset
    
    
if __name__=="__main__":
    layers, ilayers = parseConfig()
    wardrobe, fset= parseArticles()
    print wardrobe.articles
    i = Individual(wardrobe)
    i.random()
    print i
    i.render(ilayers)

    
    
    if 0:    
        path=r'http://www.stortroopers.com/fashion_boy/data/images/articles/'
        elements = getDataSet()
        for e in elements:
            print e[ImageName]
            wget(path + e[ImageName])

if __name__ == "__main__":
    g = Game(800, 600, framerate = 200)
    g.run( SampleScene(g, "Scene1") )
    
    