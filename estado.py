#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Moviemientos posibles '''
MOVE_UP = "Up"
MOVE_DOWN = "Down"
MOVE_LEFT = "Left"
MOVE_RIGHT = "Right"

class estado():
	def __init__(self, estado, filas, columnas, pivote):
		self.estado=estado
		self.filas=filas
		self.columnas=columnas
		self.pivote=pivote


	def getEstado(self):
		return self.estado

	def setEstado(self, estado):
		self.estado = estado

	def sucesores(self):
		movimientos = self.movimientos_validos(self.pivote)
		hijos = []
		for i in movimientos:
			hijos.append([i, self.gEstado(i), 1])
		return hijos

	def movimientos_validos(self, pivote):
		movimientos = []

		if pivote[0]>0:
			movimientos.append(MOVE_LEFT)
		if pivote[0]<self.columnas:
			movimientos.append(MOVE_RIGHT)
		if pivote[1]>0:
			movimientos.append(MOVE_UP)
		if pivote[1]<self.filas:
			movimientos.append(MOVE_DOWN)

		return movimientos



	def gEstado(self, movimiento):
		cambio = self.obtenerCoordenadas(movimiento)
		estado2 = self.estado[:]
		estado2[self.pivote] = self.estado[cambio]
		estado2[cambio] = 0
		return estado(estado2, self.filas, self.columnas, cambio)



    def esObjetivo(self):
        for i in range(1, len(self.estado)):
            if self.estado[i-1] > self.estado[i]:
                return False
        return True
