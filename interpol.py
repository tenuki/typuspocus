

class PInterpolator:
    def __init__(self, pinicio, pfin):
        self.inicio = complex(pinicio[0],pinicio[1])
        self.fin = complex(pfin[0],pfin[1])
        
class MadamBezier(PInterpolator):
    def __init__(self, pinicio, pfin, prev=None):
        PInterpolator.__init__(self,pinicio, pfin)
        d = self.fin-self.inicio
        if 0: #prev<>None:
            self.m1 = 2*self.inicio - prev.getPrev()
        else:
            self.m1 = self.inicio + d/4    
        self.m2 = self.fin-d/4 #random here please 
        print self.inicio
        print self.m1
        print self.m2
        print self.fin
        
    def getAt(self, t):
        #t=1-t
        c = ((1-t)**3)*self.inicio + \
                3*t*((1-t)**2)*self.m1+\
                3*(t**2)*(1-t)*self.m2+\
                (t**3)*self.fin 
        print c.real, c.imag
        return c.real, c.imag
        
    def getPrev(self):
        return self.m2
        
if __name__=="__main__":
    inter = MadamBezier( (0,0), (4,4) )
    for r in range(10):
        print inter.getAt( 1.0/(r+1) )