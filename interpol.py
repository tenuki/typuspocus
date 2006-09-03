

class PInterpolator:
    def __init__(self, pinicio, pfin):
        self.inicio = complex(pinicio[0],pinicio[1])
        self.fin = complex(pfin[0],pfin[1])
        
class MadamBezier(PInterpolator):
    def __init__(self, *args, prev=None):
        PInterpolador.__init__(*args)
        d = self.fin-self.inicio
        self.m1 = self.inicio + d/4    
        self.m2 = self.fin-d/4 #random here please 
        
    def getAt(self, t):
        c = ((1-t)**3)*self.inicio + \
                3*t*((1-t)**2)*self.m1+\
                3*(t**2)*(1-t)*self.m2+\
                (t**3)*self.fin 
        return c.real, c.imag
        
