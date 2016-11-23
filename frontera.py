#!/usr/bin/env python
# -*- coding: utf-8 -*-

class frontera():
	def __init__(self):
		self.frontera=sortedcontainers.SortedListWithKey(key=lambda nodo: nodo.valor)

	def isEmpty(self):
		if len(self.frontera) is 0 :
			return True
		else:
			return False

	def insertar(self,nodo):
		self.frontera.add(nodo)

	def eliminar(self):
		return self.frontera.pop(0)

	def getFrontera(self):
		return self.frontera
		
	def setFrontera(self, frontera):
		self.frontera = frontera