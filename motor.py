# -*- coding: utf-8 -*-

import random

PALABRAS = "Nuestro objetivo es nuclear a los usuarios de Python, de manera de centralizar la comunicacion a nivel nacional. Pretendemos llegar a usuarios y empresas, promover el uso de Python, intercambiar informacion, compartir experiencias y en general, ser el marco de referencia local en el uso y difusion de esta tecnologia.".split()

class Estados:
    (OK_DEUNA, OK_CORRG, MAL) = range(3)
    

class MainMotor(object):
    '''Clase que maneja el motor del juego.

    Se lo arranca con el start.
    '''
    def __init__(self, cant):
        self.hechizo = " ".join([random.choice(PALABRAS) for x in range(cant)])
        self.largohech = len(self.hechizo)
        self.estado = [None] * self.largohech
        self.cursor = 0
        self.cant_bs = 0

    def hitLetra(self, letra):
        if self.cursor > self.largohech:
            return (None, self.estado, None, None, None)

        print "Estado viejo", self.estado
        if self.hechizo[self.cursor] == letra:
            if self.estado[self.cursor] is None:
                res = Estados.OK_DEUNA
            else:
                res = Estados.OK_CORRG
        else:
            res = Estados.MAL

        self.estado[self.cursor] = res
        self.cursor += 1
        print "Estado nuevo", self.estado

        score = self.getScore()
        calor = self.getCalor()
        eventos = self.getEventos()
        return (res, self.estado, score, calor, eventos)

    def hitBackspace(self):
        if self.cursor > 0:
            self.cursor -= 1
        self.cant_bs = +1
        return

    def getScore(self):
        score = 0

        # puntaje de las letras
        for st in self.estado:
            if st == Estados.OK_DEUNA:
                score += 2
            if st == Estados.OK_CORRG:
                score += 1
        print "Score por letras", score

        # penalizamos los backspaces
        score -= self.cant_bs * 1
        print "Score por bs", score

        # damos mas puntos por palabras todas bien escritas
        ini = fin = 0
        for pal in self.hechizo.split():
            largopal = len(pal)
            fin += largopal
            if self.estado[ini:fin] == [Estados.OK_DEUNA]*largopal:
                score += largopal
            fin += 1
            ini += largopal + 1
        print "Score por palabra", score
        return score

    def start(self):
        # FIXME
        return

    def getCalor(self):
        # FIXME
        return None
    def getEventos(self):
        # FIXME
        return None
