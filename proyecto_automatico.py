#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import signal, os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk



'''
		------ IMPORTANTE Y COSAS QUE HACER ------
			Acordarse de la poda cuando hagamos el backtracking
			Para probar el movimiento le añadimos un temporizador (1-2 segundos),
				movemos una pieza y volvemos a generar el puzzle para comprobar
				que se ha movido
			Buscar el tamaño de la imagen y recomendar en cuanto dividirlo
			Cambiar nombre variables y ponerlo bonito
			Documentacion
		------ IMPORTANTE Y COSAS QUE HACER ------
		------ Decisiones ------
			Si el usuario introduce unas dimesiones que no son posibles (no son divisibles)
				le decimos que no es posible realizarlo con esos numeros con las dimensiones
				originales pero que reduciremos el tamaño para que sea posible
			Al generar las piezas les ponemos un campo en el que identificaremos si es la pieza
				pivote o no, de este modo solo comprobaremos los movimientos posibles si la pieza es pivote
			Usamos la libreria PIL y TKinter dado que fue la que mas sencilla nos parecio y la que
				menos problemas nos dio a la hora de instalarla y usarla.
		------ Decisiones ------
'''



class puzzle(tk.Frame):

	def __init__(self,image_o,image_p, ancho, alto):
		tk.Frame.__init__(self)
		self.grid()
		self.ancho=ancho
		self.alto=alto
		self.comprobarImagenes(image_o,image_p,ancho,alto) #esto habra que cambiarlo para mandarle filas y columnas metidas por el usuario
		#si fuese incorrecta en el metodo anterior tenemos que añadir aqui para que no haga lo siguiente
		#ya que no deberia mostrarla al ser incorrecta, digo yo, no sé que querrá xD
		self.obtenerMedidas()
		self.create_widgets()
		self.crearTablero()
		self.mostrar()
		self.after(1000,self.mover)

	def obtenerMedidas(self):
		self.board_width=self.img_puzzle.size[0]
		self.board_height=self.img_puzzle.size[1]
		#esto lo cambio cuando tenga un rato, ahora mismo toma matriz cuadrada, cuando añadamos que el usuario
		#meta el tamaño habra que cambiar cuadricula por filas y columnas, que habra que almacenar tb en self y demas
		self.piece_width=self.board_width / self.ancho
		self.piece_height=self.board_height / self.alto


	def create_widgets(self):
	    args = dict(width=self.board_width, height=self.board_height)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def crearTablero(self):
		self.tablero = []
		contadorPivote=0

		for x in xrange(self.ancho):
			for y in xrange(self.alto):
				x0 = x * self.piece_width
				y0 = y * self.piece_height
				x1 = x0 + self.piece_width
				y1 = y0 + self.piece_height
				image = ImageTk.PhotoImage(self.img_puzzle.crop((x0, y0, x1, y1)))
				piece = {'id'     : None,
					'image'  : image,
					'pos_o'  : (x, y),
					#'pos_p'  : get_pieces_around(self), # Posibles posiciones a las que puede cambiar
					'pos_a'  : None,
				 	'pivote' : False, # Identificar que pieza es el pivote
				 	}
				if contadorPivote < self.pivote:
					contadorPivote+=1
				else:
					piece['pivote']=True

				self.tablero.append(piece)

	def mostrar(self):
		#random.shuffle(self.tablero) # shuffle = barajar, no hace falta al dar el estado inigial ellos
		index = 0
		for x in xrange(self.ancho):
			for y in xrange(self.alto):
				#self.tablero[index]['pos_a'] = (x, y)
				x1 = x * self.piece_width
				y1 = y * self.piece_height
				image = self.tablero[index]['image']
				self.tablero[index]['id']= self.pintar(x1,y1,image)
				index += 1

	def pintar(self,x,y,imagen):
		id = self.canvas.create_image(x, y, image=imagen, anchor=tk.NW)
		return id
			
	def mover(self):
		indice1=indice2=0
		coorX=coorY=0

		a=random.randint(0,3)
		movimiento=''
		
		if a ==0:
			movimiento='Up'
			coorX=self.tablero[self.pivote]['pos_o'][0]
			coorY=self.tablero[self.pivote]['pos_o'][1]-1
		if a ==1:
			movimiento='Down'
			coorX=self.tablero[self.pivote]['pos_o'][0]
			coorY=self.tablero[self.pivote]['pos_o'][1]+1
		if a ==2:
			movimiento='Left'
			coorX=self.tablero[self.pivote]['pos_o'][0]-1
			coorY=self.tablero[self.pivote]['pos_o'][1]
		if a ==3:
			movimiento='Right'
			coorX=self.tablero[self.pivote]['pos_o'][0]+1
			coorY=self.tablero[self.pivote]['pos_o'][1]

		if self.movimientosValidos(self.tablero[self.pivote]['pos_o'],movimiento):
			
			for i in self.tablero:		
				if i['pos_o']==(coorX,coorY):
					break
				indice2+=1

			self.cambioPiezas(self.pivote,indice2)
			x = int(self.tablero[self.pivote]['pos_o'][0]) * self.piece_width
			y = int(self.tablero[self.pivote]['pos_o'][1]) * self.piece_height
			aux=self.pintar(x, y, self.tablero[self.pivote]['image'])

			x = int(self.tablero[indice2]['pos_o'][0]) * self.piece_width
			y = int(self.tablero[indice2]['pos_o'][1]) * self.piece_height
			aux=self.pintar(x, y, self.tablero[indice2]['image'])

			self.pivote=indice2
			self.after(1000,self.mover)
		else:
			self.after(0,self.mover)

	def movimientosValidos(self, coor, movimiento):
		valido=True

		if (coor[0]==0 and movimiento=='Left') or (coor[0]==3 and movimiento=='Right') or (coor[1]==0 and movimiento=='Up') or (coor[1]==3 and movimiento=='Down'):
			valido=False

		return valido


	def comprobarImagenes(self,img_o, img_p,columnas,filas):
		#carga imagenes
		self.img_original = Image.open(img_o)
		self.img_puzzle = Image.open(img_p)

		#obtiene sus tamaños
		ancho_o, alto_o =self.img_original.size

		#obtiene el tamaño de las piezas
		ancho_pieza = ancho_o/ columnas
		alto_pieza = alto_o / filas

		#almacena ambas imagenes en listas (lo mismo hay que cambiarlo a matriz)
		lista_original=[]
		lista_puzzle=[]

		#antes habria que comprobar que ambas imagenes son iguales en tamaño
		for x in range(0,columnas):
			for y in range(0,filas):
				x0 = x * ancho_pieza
				y0 = y * alto_pieza
				x1 = x0 + ancho_pieza
				y1 = y0 + alto_pieza
				lista_original.append(self.img_original.crop((x0, y0, x1, y1)))
				lista_puzzle.append(self.img_puzzle.crop((x0, y0, x1, y1)))

		iguales= 0

		#se comparan las imagenes trozo a trozo
		for x in range(0, len(lista_original)):
			for y in range(0,len(lista_puzzle)):
					if lista_original[x] == lista_puzzle[y]:
						iguales = iguales + 1
						if x == 0: #si x es 0 en la original es la negra, el pivote, asi que almacena en que posicion está en el puzzle para luego
							self.pivote=y
						lista_puzzle.pop(y)
						break


		if iguales==columnas*filas: #numero de celdas
			print ("Imagen correcta")
		else:
			print ("Imagen incorrecta")


		#vacia las listas para que no se queden por ahi en memoria, no se si hara falta
		lista_puzzle=[]
		lista_original=[]

	#cambia todo menos las coordenadas
	def cambioPiezas(self, id1, id2):
		aux = self.tablero[id1]
		coor2=self.tablero[id2]['pos_o']
		self.tablero[id1]=self.tablero[id2]
		self.tablero[id1]['pos_o']=aux['pos_o']
		self.tablero[id2]=aux
		self.tablero[id2]['pos_o']=coor2


def leerEntero():
	while True:
		try:
			num = input("Introduzca el numero: ")
			return num
		except:
			print "Porfavor introduzca un numero"


#la clase puzzle es toda la aplicacion, esto solo es el main para lanzarla
if __name__ == '__main__':
	#AlhambraPixelesModificado4x4
	#IntermedioAlhambra41
	app = puzzle('AlhambraInicialPuzzle4x4.png','intermedioAlhambra41.png', 4,4) 
	app.master.title('prueba')
	app.mainloop()

'''
	while True:

		try:

			opcion = input("Introduzca la opción que desea: \n\
			1 --> Introducir nombre imagen desordenada \n\
			2 --> Introducir nombre imagen original\n\
			3 --> Introducir ancho y altura \n\
			4 --> Cargar imagen \n\
			5 --> Salir\n\
			")

			if (opcion > 6 or opcion < 1):
				break

			if opcion==1:
				nombreDes = raw_input("Introduzca el nombre del fichero: \n")
			elif opcion==2:
				nombreOr = raw_input("Introduzca el nombre del fichero: \n")
			elif opcion==3:
				print "Introduzca el ancho"
				ancho = leerEntero()
				print "Introduzca el alto"
				alto = leerEntero()
			elif opcion==4:
				app = puzzle('AlhambraInicialPuzzle4x4.png','intermedioAlhambra41.png', 4,4) #el 4 es el numero de filas y columnas, tendremos que añadir algo para que las pida al usuario
				app.master.title('prueba')
				app.mainloop()
				break
			elif opcion==5:
				break

		except:
			print "Porfavor introduzca una opcion"'''
