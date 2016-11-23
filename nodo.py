#!/usr/bin/env python
# -*- coding: utf-8 -*-

class nodo():
	def __init__(self, padre, estado, costo, accion, valor, posPiv):
		self.padre = padre
		self.estado = estado
		self.costo = costo
		self.accion = accion
		self.valor = valor
		self.posPiv = posPiv

	def getValor(self):
		return self.valor

	def getEstado(self):
		return self.estado

	def getCosto(self):
		return self.costo

	def getPadre(self):
		return self.padre

	def getPivote(self):
		return self.posPiv

	def getAccion(self):
		return self.accion

	def setValor(self, valor):
		self.valor = valor

	def setEstado(self, estado):
		self.estado = estado

	def setCosto(self, costo):
		self.costo = costo

	def setPadre(self, padre):
		self.padre = padre

	def setPivote(self, posicion):
		self.posPiv = posicion

	def setAccion(self, accion):
		self.accion = accion