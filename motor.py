# -*- coding: utf-8 -*-

from __future__ import division
import random, time
import cosas
PALABRAS = "Nuestro objetivo es nuclear a los usuarios de Python, de manera de centralizar la comunicacion a nivel nacional. Pretendemos llegar a usuarios y empresas, promover el uso de Python, intercambiar informacion, compartir experiencias y en general, ser el marco de referencia local en el uso y difusion de esta tecnologia.".split()

class Estados:
    (VIRGEN, OK_DEUNA, OK_CORRG, MAL) = range(4)

class Eventos:
    (VIRGEN, OK_DEUNA, OK_CORRG, MAL, PALOK, PALMAL, INACT5, INACT10) = range(8)
    descrip = {PALOK:   "Se escribio una palabra completamente correcta",
               PALMAL:  "Se escribio una palabra completamente mal",
               INACT5:  "Hace 5 segundos que no se escribe nada",
               INACT10: "Hace 10 segundos que no se escribe nada",
              }
    

class MainMotor(object):
    '''Clase que maneja el motor del juego.

    Se lo arranca con el start().
    Cuando el usr presiona una tecla, hitLetra(), cuando hace backspace, hitBackspace()
    '''

    porcentajeRequerido = 0.50
    tiempoExtra = 10
    voluntario = cosas.reloj
    voluntario_error = cosas.hongo
    
    def __init__(self, cant):
        self.LPS = 3.0
        (self.hechizo, self.indpals) = self._armaHechizo(cant)
        self.largohech = len(self.hechizo)
        self.cursor = 0
        self.cant_bs = 0
        self.startTime = None
        self.tiempoJuego = self._getTiempoJuego()
        # calculamos el puntaje maximo con un estado 100% ok, y luego reseteamos
        self.estado = [Estados.OK_DEUNA] * self.largohech
        self.puntajeMax = self._getScore()
        self.score = 0
        self.estado = [Estados.VIRGEN] * self.largohech
        self.calor = 0
        self.tiempoUltTecla = 0

    def _armaHechizo(self, cant):
        '''Arma el hechizo y un indice que es un dict, donde la clave es la
        posicion de la ultima letra de cada palabra y el valor es una tupla
        con los dos extremos de la palabra.
        '''
        base = 0
        palabras = []
        indice = {}
        for i in range(cant):
            pal = random.choice(PALABRAS)
            largo = len(pal)
            palabras.append(pal)
            indice[base+largo-1] = (base, base+largo)
            base += largo + 1
        return (" ".join(palabras), indice)
        
    def hitLetra(self, letra):
        '''Recibe la letra que apretó el usuario y devuelve...

        - Si esa letra estuvo bien o mal
        - El estado completo de la frase
        - El puntaje total
        - El calor del público
        - Una lista de eventos
        '''
        if self.startTime is None:
            raise ValueError("Todavia no se hizo el start de la sesion!")
        if self.cursor > self.largohech:
            return (None, self.estado, None, None, None)

#        print "Estado viejo", self.estado
        if self.hechizo[self.cursor] == letra:
            if self.estado[self.cursor] in (Estados.VIRGEN, Estados.OK_DEUNA):
                res = Estados.OK_DEUNA
            else:
                res = Estados.OK_CORRG
        else:
            res = Estados.MAL
        self.estado[self.cursor] = res
#        print "Estado nuevo", self.estado

        # evento? nos fijamos si completamos una palabra
        evento = None
        if self.cursor in self.indpals:
            (ini, fin) = self.indpals[self.cursor]
            if self.estado[ini:fin] == [Estados.OK_DEUNA]*(fin-ini):
                evento = Eventos.PALOK
            if self.estado[ini:fin] == [Estados.MAL]*(fin-ini):
                evento = Eventos.PALMAL
        else:
            evento = self.estado[self.cursor]

        # actualizamos las variables
        self._getScore()
        self._getCalor()
        self.tiempoUltTecla = time.time()
        self.cursor += 1
        return (res, evento)

    def hitBackspace(self):
        '''El usuario apretó el backspace.'''
        if self.cursor > 0:
            self.cursor -= 1
        self.cant_bs = +1
        self.tiempoUltTecla = time.time()
        return

    def _getScore(self):
        '''Calcula el puntaje total según el estado.'''
        score = 0

        # puntaje de las letras
        for st in self.estado:
            if st == Estados.OK_DEUNA:
                score += 2
            if st == Estados.OK_CORRG:
                score += 1
#        print "Score por letras", score

        # penalizamos los backspaces
        score -= self.cant_bs * 1
#        print "Score por bs", score

        # damos mas puntos por palabras todas bien escritas
        ini = fin = 0
        for pal in self.hechizo.split():
            largopal = len(pal)
            fin += largopal
            if self.estado[ini:fin] == [Estados.OK_DEUNA]*largopal:
                score += largopal
            fin += 1
            ini += largopal + 1
#        print "Score por palabra", score
        self.score = score
        return score

    def start(self):
        self.startTime = time.time()
        return

    def tick(self):
        # actualizamos el calor del publico
        self._getCalor()

        # evento? vemos si hace rato que no tocamos una tecla
        inactivo = time.time() - self.tiempoUltTecla
        if inactivo > 10:
            return Eventos.INACT10
        if inactivo > 5:
            return Eventos.INACT5
        return

    def getTimeLeft(self):
        '''Antes del start, devuelve el tiempo total, después devuelve
        el que falta para terminar.
        '''
        if self.startTime is None:
            return self.tiempoJuego
        falta = self.startTime + self.tiempoJuego - time.time()
        return falta

    def _getTiempoJuego(self):
        '''Devuelve el tiempo que tiene el usuario para completar el hechizo.'''
        # la hacemos fácil, un segundo por letra
        return self.largohech/self.LPS + self.tiempoExtra

    def tuvoExito(self):
        acertados = 0
        for st in self.estado:
            if st == Estados.OK_DEUNA or st == Estados.OK_CORRG:
                acertados += 1
        porcentaje = float(acertados)/len(self.estado)
        #print acertados, "/", len(self.estado)
        return porcentaje >= self.porcentajeRequerido

    def _getCalor(self):
        '''Devuelve cuan activo está el público.
        Es un float, entre -1 (super enojado) y 1 (super alegre).
        0 es neutro.
        '''
        # algoritmo para el calor del público:
        #   Es una suma algebraica de los siguientes floats entre 0 y 1:
        #     - porcentaje de puntos logrados sobre el total posible a ese momento, y le restamos 3 para que
        #       se balancee penalizando los errores (por letra, el rango de puntos es de -2 a 1)
        #     - tiempo pasado sobre el total de tiempo posible (en contra)
        #     - cantidad de backspaces sobre el total de letras (en contra, ojo que puede dar >1)
        calor = 0
        porc_tiempopasado = (time.time() - self.startTime) / self.tiempoJuego
        punt_almomento = self.puntajeMax * porc_tiempopasado
        valor1 = ((self.score / punt_almomento) * 3) - 3 
        calor += valor1
        calor -= self.cant_bs / self.largohech
        calor *= porc_tiempopasado

        # sanity check
        if calor > 1:
            calor = 1
        if calor < -1:
            calor = -1
        self.calor = calor
        #print "Hace Calor...", porc_tiempopasado, punt_almomento, valor1, calor, self.tuvoExito()
        return calor
