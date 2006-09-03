

class PInterpolator:
    def __init__(self, pinicio, pfin):
        self.inicio = complex(pinicio[0],pinicio[1])
        self.fin = complex(pfin[0],pfin[1])
        
class MadamBezier(PInterpolator):
    def __init__(self, *args):
        PInterpolador.__init__(*args)
        #ix, iy = self.inicio
        #fx, fy = self.fin
        #self.m1 = ix+ (fx-ix)/4, iy+(fy-iy)/4 #random here please 
        #self.m2 = fx- (fx-ix)/4, fy-(fy-iy)/4 #random here please 
        d = self.fin-self.inicio
        self.m1 = self.inicio + d/4        
        
    def getAt(self, t):
        c = ((1-t)**3)*self.inicio + \
                3*t*((1-t)**2)*self.m1+\
                3*(t**2)*(1-t)*self.m2+\
                (t**3)*self.fin 
        return c.real, c.imag
        
