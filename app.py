#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import copy
from time import time
import resource
import signal, os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk


from pieza import pieza
from estado import estado
from frontera import frontera
from problema import problema
from espacio_estados import espacio_estados
from nodo import nodo
from datosUsuario import datosUsuario

class app(tk.Frame):

	def __init__(self,imagen_o,imagen_p, colum, fil):
		tk.Frame.__init__(self)
		self.grid()

		self.columnas=colum
		self.filas=fil

		self.estadoInicial= estado(self.filas, self.columnas)
		self.estadoObjetivo= estado(self.filas, self.columnas)
		
		if self.obtener_datos(imagen_o, imagen_p):
			self.crear_tablero_original()
			if self.comprobar_imagenes():

				self.espacioEstados=espacio_estados(self.filas,self.columnas) #necesario pasarselas para los sucesores
				self.frontera=frontera()
				self.problema=problema(self.estadoObjetivo, self.estadoInicial, self.espacioEstados)
				
				''' busqueda de solucion'''
				estrategia=self.getEstrategia()
				self.solucion,haySolucion=self.seleccionarBusqueda(estrategia)

				#saca todos los nodos de la solucion para hacer el camino a la inversa
				self.pilaEstadosSol=[]
				fichero = open('solucion.txt', 'w')
				fichero.write("")
				fichero.close()

				fichero = open('solucion.txt', 'a')

				padre=self.solucion #ultimo nodo de la solucion(estado inicial)
				print "Coste:"+str(padre.getCosto())
				print "Profundidad:"+str(padre.getProfuncidad())
				
				if haySolucion:
					while padre!=None:
						self.pilaEstadosSol.append(padre)
						if padre.getAccion()!=None:
							fichero.write(padre.getAccion() + "\n")
						padre=padre.getPadre()#coge el nodo siquiente

					fichero.close()
					self.crear_canvas()		
					self.mostrar()
					#
					self.after(0,self.mover)
				else:
					print "No hay solucion"
					exit(-1)
			else:
				print("Las imagenes no son iguales")
				exit(-1)

	def seleccionarBusqueda(self,estrategia):
		profMax=None
		tiempoInicial = time()

		node = nodo(None, self.problema.getEstadoInicial(), 0, None, 0, self.pivote,0)
		self.frontera.insertar(node)

		print "Calculando..."

		if estrategia=="iterativo":
			profMax=self.getProfMax()
			incremento=self.getIncremento()
			solucion,haySolucion=self.profundidadLimitada(estrategia, profMax, incremento)
		else:
			if estrategia=="limitada":
				profMax=self.getProfMax()
			solucion,haySolucion=self.busqueda(estrategia,profMax)

		tiempoFinal = time()
		print("Tiempo:" + str(tiempoFinal-tiempoInicial))

		return solucion,haySolucion

	def busqueda(self, estrategia, profMax=None): 
		solucion=False
		sucesores=[]
		totalNodos=1

		while solucion==False and self.frontera.isEmpty()==False:
			node=self.frontera.eliminar()
			if profMax==None or node.getProfuncidad()<profMax:
				if self.problema.esObjetivo(node.getEstado()) == True:
					solucion=True
					self.mostrarSolucion(node)
					print "nodos:"+str(totalNodos)
				else:
					sucesores=self.problema.espacioEstados.sucesores(node.getEstado(), node.getPivote())
					for i in sucesores:
						insertar=self.comprobarSiInsertar(node,i)	
						if insertar==True:
							self.insertarNodo(node, i, estrategia, node.getProfuncidad()+1)
							totalNodos+=1
							
					sucesores=[]
				
			else:
				break

		return node, solucion

	def profundidadLimitada(self,estrategia, profMax=None,incremento=None):
	    solucion = False
	    node=None
	    print incremento
	    while solucion == False and incremento <= profMax:
	        node, solucion = self.busqueda(estrategia, profMax)
	        profMax += incremento

	    return node, solucion

	def insertarNodo(self,padre ,i, estrategia, profundidad):
		valor= 0
		if estrategia == "anchura":
			valor=profundidad
		if estrategia == "profundidad" or estrategia == "limitada" or estrategia == "iterativo":
			valor=profundidad*(-1)
		if estrategia == "costo uniforme":
			valor=i['coste'] 
		if estrategia == "asterisco":
			valor = (padre.getCosto()+i['coste']) + self.problema.heuristica(i['estado'])

		self.frontera.insertar(nodo(padre, i['estado'], padre.getCosto()+i['coste'], i['movimiento'], valor, i['posPivote'], profundidad))

	def comprobarSiInsertar(self, padre,sucesor):
		insertar =True
		if (padre.getAccion()=="Up" and sucesor['movimiento']=="Down") or (padre.getAccion()=="Down" and sucesor['movimiento']=="Up"):
				insertar=False

		if (padre.getAccion()=="Right" and sucesor['movimiento']=="Left") or (padre.getAccion()=="Left" and sucesor['movimiento']=="Right"):
				insertar=False

		return insertar

	def getEstrategia(self):
		listaEstrategias=["anchura","profundidad","limitada","iterativo","costo uniforme","asterisco"]
		estrategia=""
		aux=False

		print "0-Anchura"
		print "1-Profundidad"
		print "2-Profundidad Limitada"
		print "3-Iterativo"
		print "4-Costo Uniforme"
		print "5-A*"

		while aux==False:
			eleccion=raw_input("Seleccione una estrategia de busqueda:")
			if eleccion.isdigit():
				eleccion=int(eleccion)
				if eleccion<len(listaEstrategias) and eleccion>-1:
					estrategia=listaEstrategias[eleccion]
					aux=True

		return estrategia

	def getIncremento(self):
		aux=False
		incremento=0

		while aux==False:
			incremento=raw_input("Seleccione un incremento:")
			if incremento.isdigit():
				incremento=int(incremento)
				break
				
		return incremento

	def getProfMax(self):
		aux=False
		maxima=0

		while aux==False:
			maxima=raw_input("Seleccione una profundidad máxima:")
			if maxima.isdigit():
				maxima=int(maxima)
				break
				
		return maxima

	def mostrarSolucion(self, node):
		print ("solucion encontrada con " + str(node.getValor())+" movimientos")

		padre=None
		padre=node.getPadre()
		while padre!=None:
			print (padre.getAccion())
			padre=padre.getPadre()

	def limitarMemoria(self, tamMax):
		soft, hard = resource.getrlimit(resource.RLIMIT_AS)
		resource.setrlimit(resource.RLIMIT_AS, (tamMax, hard))

	def obtener_datos(self, img_o, img_p):
		try:
			#abre las imagenes
			self.img_original=Image.open(img_o) #carga la imagen inicial (puede que no tenga espacio negro)
			self.img_puzzle= Image.open(img_p) #carga la imagen con el estado inicial

			#establece el ancho y alto del tablero
			self.ancho_tablero=self.img_original.size[0]
			self.alto_tablero=self.img_original.size[1]

			#establece el alto y ancho de las piezas
			self.ancho_pieza=self.ancho_tablero / self.columnas
			self.alto_pieza=self.alto_tablero / self.filas

			#pinta el pivote en la foto, por si no está
			self.pintarPivote()

			return True

		except:
			print("La imagen seleccionada no se encuentra en el directorio")
			return False

	def pintarPivote(self):
		#crea un lienzo en blanco
		imagen = Image.new("RGB",(self.ancho_tablero,self.alto_tablero),"white")#crea una imagen en blanco sobre la que se pegarán todas las demas
		#pinta encima la imagen inicial
		imagen.paste(self.img_original,(0,0))
		#pinta el cuadro negro
		imagen.paste(Image.new("RGB",(self.ancho_pieza, self.alto_pieza),"black"),(0,0))
		#asigna a la imagen original la nueva imagen con el cuadro negro
		self.img_original=imagen

	def crear_tablero_original(self):#modificar para adaptarlo a las clases
		self.estado_objetivo = [] #almacena el tablero conforme estaría resuelto, almacena tuplas (id,coordenadas), las coordenadas x,y simulan una matriz
		self.estado_inicial=[] #almacena el tablero conforme al estado inicial, almacena tuplas (id,coordenadas),las coordenadas x,y simulan una matriz

		self.listaImg_Original=[] #almacena la imagen original cortada en trozos, sirve para compararla con la otra imagen y para generar una imagen png nueva
		self.listaImg_Puzzle=[] #almacena la imagen del estado inicial en trozos, para compararla con la original, luego se vacia
		self.imagenes=[] #almacena los trozos igual que en listaImg_Original pero en forma PhotoImage, necesario para mostrarlos en el canvas

		contadorPivote=0
		ids=0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x0 = x * self.ancho_pieza
				y0 = y * self.alto_pieza
				x1 = x0 + self.ancho_pieza
				y1 = y0 + self.alto_pieza
				
				self.listaImg_Original.append(self.img_original.crop((x0, y0, x1, y1)))
				self.imagenes.append(ImageTk.PhotoImage(self.listaImg_Original[ids]))

				#crea una nueva pieza que almacena la id y la posicion x,y que tendrá
				pieza_o = pieza()
				pieza_o.crearPieza(ids,(x,y))
				self.estado_objetivo.append(pieza_o) 
				
				#foto estado inicial
				self.listaImg_Puzzle.append(self.img_puzzle.crop((x0, y0, x1, y1)))
				pieza_p = pieza()
				pieza_p.crearPieza(None,(x,y))
				self.estado_inicial.append(pieza_p) #crea una nueva pieza sin id, con la posicion que tendrá
				ids+=1

		#establece el pivote en el tablero original
		self.estado_objetivo[0].setPivote(True)
		self.pivote=0

	def comprobar_imagenes(self):
		iguales= 0
		#se comparan las imagenes trozo a trozo
		for x in range(0, len(self.listaImg_Original)):
			for y in range(0,len(self.listaImg_Puzzle)):	
				if self.listaImg_Original[x] == self.listaImg_Puzzle[y]: # si los dos trozos son iguales...
					iguales = iguales + 1

					self.estado_inicial[y].setId(self.estado_objetivo[x].getId())#establece a la pieza desordenada la id que corresponde con la imagen original
					self.listaImg_Puzzle[y]=[] # por si hay muchas imagenes del mismo color, para que no vuelva a comparar y asignar el id a la misma, se elimina de la lista

					if x == 0: #establece el pivote en el tablero puzzle (ya que cuando x sea 0, en el tablero original(y por tanto en la lista original) será la imagen negra)
						self.estado_inicial[y].setPivote(True)
						self.pivote=y
					break

		self.listaImg_Puzzle=[] #vacia la lista que no va a volver a utilizarse para liberar memoria

		#crea el estado inicial y el objetivo
		self.estadoInicial.crearEstado(self.estado_inicial, self.pivote)
		self.estadoInicial.setPosPivAnterior(self.pivote)#anteriormente no ha tenido otra posicion de pivote, ya que es el inicial
		self.estadoObjetivo.crearEstado(self.estado_objetivo, 0)

		#si el numero de piezas iguales coincide con el tamaño de la matriz (filas*columnas) es que las dos imagenes son iguales
		if iguales==self.columnas*self.filas:			
			return True
		else:
			return False

	def crear_canvas(self):
	    args = dict(width=self.ancho_tablero, height=self.alto_tablero)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def mostrar(self):
		index = 0

		estado_i = self.estadoInicial.getTablero()

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x1 = x * self.ancho_pieza
				y1 = y * self.alto_pieza

				#obtiene la imagen correspondiente a la id almacenada y la muestra en la posicion x,y
				image = self.imagenes[estado_i[index].getId()]
				self.pintar(x1,y1,image)

				index += 1
	def mover(self):

		node=None
	
		if len(self.pilaEstadosSol)>0:
			node=self.pilaEstadosSol.pop()	
			estado=node.getEstado()
			pivote=estado.getPivote()
			coordenadas=estado.getTablero()[pivote].getCoordenadas()
			posPivoteAnterior=estado.getPostPivAnterior()
			coordenadasAnteriores=estado.getTablero()[posPivoteAnterior].getCoordenadas()

			x= int(coordenadas[0]*self.ancho_pieza)
			y= int(coordenadas[1]*self.alto_pieza)
			self.pintar(x, y, self.imagenes[estado.getTablero()[pivote].getId()])

			x1= int(coordenadasAnteriores[0]*self.ancho_pieza)
			y1= int(coordenadasAnteriores[1]*self.alto_pieza)
			self.pintar(x1, y1, self.imagenes[estado.getTablero()[posPivoteAnterior].getId()])

			if len(self.pilaEstadosSol)>0:
				self.after(1000,self.mover)


	def pintar(self,x,y,imagen):
		self.canvas.create_image(x, y, image=imagen, anchor=tk.NW)

	def crear_imagen(self, tablero):

		imagen = Image.new("RGB",(self.ancho_tablero,self.alto_tablero),"white")#crea una imagen en blanco sobre la que se pegarán todas las demas
		indice=0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x0 = x * self.ancho_pieza
				y0 = y * self.alto_pieza

				#recorre la lista de imagenes obteniendo las imagenes en el orden que están en el tablero de ese instante, y las pega juntas
				imagen.paste(self.listaImg_Original[tablero[indice].getId()],(x0,y0))
				indice+=1

		imagen.save("imagenGenerada.png")


if __name__ == '__main__':

	datosUsuario = datosUsuario()
	imagenInicial,estadoInicial,columnas,filas= datosUsuario.obtenerDatosUsuario()

	app = app(imagenInicial,estadoInicial, int(columnas),int(filas))
	app.master.title('Puzzle')
	app.mainloop()