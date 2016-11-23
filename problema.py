#!/usr/bin/env python
# -*- coding: utf-8 -*-

class problema():
	def __init__(self):
		self.estadoInicial = None
		self.estadoObjetivo = None

		
	def esObjetivo(self, estado): #determina si un estado recibido es el objetivo o no
		objetivo = True
		for i in range(0,len(estado)):
			if estado[i]['id']!=self.estadoObjetivo[i]['id']:
				i=len(estado)
				objetivo = False

		if objetivo:
			print("Es objetivo")
		else:
			print("No es objetivo")

		return objetivo