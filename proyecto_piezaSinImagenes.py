#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import signal, os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk

MOVE_UP = "Up"
MOVE_DOWN = "Down"
MOVE_LEFT = "Left"
MOVE_RIGHT = "Right"

''' -------------- EN ESTE LAS PIEZAS NO ALMACENAN IMAGENES, SOLO COORDENADAS ---------------'''

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

	def __init__(self,imagen_o,imagen_p, columnas, filas):
		tk.Frame.__init__(self)
		self.grid()
		self.columnas=columnas
		self.filas=filas
		self.obtener_datos(imagen_o, imagen_p)
		self.crear_tablero_original()
		if self.comprobar_imagenes():
			self.create_widgets()
			self.mostrar()
			self.after(1000,self.mover)
			self.after(5000,self.crear_imagen) #crea una imagen del puzzle para probar el metodo
		else:
			print ("--- La imágenes no son iguales ---")

	def obtener_datos(self, img_o, img_p):	
		self.img_original=Image.open(img_o)
		self.img_puzzle= Image.open(img_p)
		self.ancho_tablero=self.img_original.size[0]
		self.alto_tablero=self.img_original.size[1]
		self.ancho_pieza=self.ancho_tablero / self.columnas
		self.alto_pieza=self.alto_tablero / self.filas

	def create_widgets(self):
	    args = dict(width=self.ancho_tablero, height=self.alto_tablero)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def crear_tablero_original(self):
		self.tablero_original = []
		self.tablero_puzzle=[]

		self.listaImg_Original=[]
		self.listaImg_Puzzle=[]
		self.imagenes=[]

		contadorPivote=0
		ids=0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x0 = x * self.ancho_pieza
				y0 = y * self.alto_pieza
				x1 = x0 + self.ancho_pieza
				y1 = y0 + self.alto_pieza

				#foto original
				if x==0 and y==0:
					self.listaImg_Original.append(Image.new("RGB",(self.ancho_pieza,self.alto_pieza),"black"))#en esta se almacenan los trozos de imagenes sin tratar para comprobarlos, luego se vacia
					self.imagenes.append(ImageTk.PhotoImage(self.listaImg_Original[ids]))#se almacenan todos los trozos aptos para mostrar
				else:				
					self.listaImg_Original.append(self.img_original.crop((x0, y0, x1, y1))) #en esta se almacenan los trozos de imagenes sin tratar para comprobarlos, luego se vacia
					self.imagenes.append(ImageTk.PhotoImage(self.listaImg_Original[ids]))#se almacenan todos los trozos aptos para mostrar

				self.tablero_original.append(self.nueva_pieza(ids,(x,y))) #almacena la id y la posicion x,y en la matriz

				#foto puzzle
				self.listaImg_Puzzle.append(self.img_puzzle.crop((x0, y0, x1, y1)))#en esta se almacenan los trozos de imagenes sin tratar para comprobarlos, luego se vacia
				self.tablero_puzzle.append(self.nueva_pieza(None,(x,y)))
				ids+=1

				''' tanto el tablero original como el puzzle(estado inicial) almacenan solo ids y posiciones x,y, para mostrar se cogen las imagenes
				de self.imagenes y se muestran '''

		#establece el pivote en el tablero original 
		self.tablero_original[0]['pivote']=True
		self.pivote=0

	def comprobar_imagenes(self):
		iguales= 0

		#se comparan las imagenes trozo a trozo
		for x in range(0, len(self.listaImg_Original)):
			for y in range(0,len(self.listaImg_Puzzle)):
					if self.listaImg_Original[x] == self.listaImg_Puzzle[y]:
						iguales = iguales + 1
						self.tablero_puzzle[y]['id']=self.tablero_original[x]['id']	
						self.listaImg_Puzzle[y]=[] # por si hay muchas imagenes dle mismo color, para que no vuelva a comparar y asignar el id a la misma
						if x == 0: #establece el pivote en el tablero puzzle
							self.tablero_puzzle[y]['pivote']=True
							self.pivote=y						
						break

		self.listaImg_Puzzle=[]

		if iguales==self.columnas*self.filas: #numero de celdas
			return True
		else:
			return False	


	def nueva_pieza(self, ids, coor):
		piece = {'id': ids,
		'pos_o'  : coor,
		'pivote' : False, # Identificar que pieza es el pivote
		}

		return piece

	def mostrar(self):
		index = 0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x1 = x * self.ancho_pieza
				y1 = y * self.alto_pieza
				#print(self.tablero_puzzle[index]['id'])
				image = self.imagenes[self.tablero_puzzle[index]['id']]

				self.pintar(x1,y1,image)
				index += 1

	def pintar(self,x,y,imagen):
		self.canvas.create_image(x, y, image=imagen, anchor=tk.NW)
	

	def mover(self):
		indice1=indice2=0
		coorX=coorY=0

		a=random.randint(0,3)
		movimiento=''

		if a ==0:
			movimiento= MOVE_UP
			coorX=self.tablero_puzzle[self.pivote]['pos_o'][0]
			coorY=self.tablero_puzzle[self.pivote]['pos_o'][1]-1
		if a ==1:
			movimiento= MOVE_DOWN
			coorX=self.tablero_puzzle[self.pivote]['pos_o'][0]
			coorY=self.tablero_puzzle[self.pivote]['pos_o'][1]+1
		if a ==2:
			movimiento= MOVE_LEFT
			coorX=self.tablero_puzzle[self.pivote]['pos_o'][0]-1
			coorY=self.tablero_puzzle[self.pivote]['pos_o'][1]
		if a ==3:
			movimiento= MOVE_RIGHT
			coorX=self.tablero_puzzle[self.pivote]['pos_o'][0]+1
			coorY=self.tablero_puzzle[self.pivote]['pos_o'][1]

		if self.movimientos_validos(self.tablero_puzzle[self.pivote]['pos_o'],movimiento):
			
			for i in self.tablero_puzzle:		
				if i['pos_o']==(coorX,coorY):
					break
				indice2+=1

			self.cambiar_piezas(self.pivote,indice2)
			x = int(self.tablero_puzzle[self.pivote]['pos_o'][0]) * self.ancho_pieza
			y = int(self.tablero_puzzle[self.pivote]['pos_o'][1]) * self.alto_pieza
			aux=self.pintar(x, y, self.imagenes[ self.tablero_puzzle[self.pivote]['id']])

			x = int(self.tablero_puzzle[indice2]['pos_o'][0]) * self.ancho_pieza
			y = int(self.tablero_puzzle[indice2]['pos_o'][1]) * self.alto_pieza
			aux=self.pintar(x, y, self.imagenes[self.tablero_puzzle[indice2]['id']])

			self.pivote=indice2
			self.after(1000,self.mover)
		else:
			self.after(0,self.mover)

	def movimientos_validos(self, coor, movimiento):
		valido=True

		if (coor[0]==0 and movimiento==MOVE_LEFT) or (coor[0]==3 and movimiento==MOVE_RIGHT) or (coor[1]==0 and movimiento==MOVE_UP) or (coor[1]==3 and movimiento==MOVE_DOWN):
			valido=False

		return valido


	#cambia todo menos las coordenadas
	def cambiar_piezas(self, id1, id2):
		aux = self.tablero_puzzle[id1]
		coor2=self.tablero_puzzle[id2]['pos_o']
		self.tablero_puzzle[id1]=self.tablero_puzzle[id2]
		self.tablero_puzzle[id1]['pos_o']=aux['pos_o']
		self.tablero_puzzle[id2]=aux
		self.tablero_puzzle[id2]['pos_o']=coor2

	def crear_imagen(self):
		imagen = Image.new("RGB",(self.ancho_tablero,self.alto_tablero),"white")
		indice=0
		

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x0 = x * self.ancho_pieza
				y0 = y * self.alto_pieza

				imagen.paste(self.listaImg_Original[self.tablero_puzzle[indice]['id']],(x0,y0))
				indice+=1

		imagen.save("imagenGenerada.png")

def leer_entero():
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
	#IntermedioAlhambra10x5
	#Inicialalhambra10x5
	app = puzzle('AlhambraInicialPuzzle4x4.png','IntermedioAlhambra41.png', 4,4) 
	app.master.title('prueba')
	app.mainloop()

'''
	while True:

		try:

			opcion = input("Introduzca la opción que desea: \n\
			1 --> Introducir nombre imagen desordenada \n\
			2 --> Introducir nombre imagen original\n\
			3 --> Introducir columnas y altura \n\
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
				print "Introduzca el columnas"
				columnas = leer_entero()
				print "Introduzca el filas"
				filas = leer_entero()
			elif opcion==4:
				app = puzzle('AlhambraInicialPuzzle4x4.png','intermedioAlhambra41.png', 4,4) #el 4 es el numero de filas y columnas, tendremos que añadir algo para que las pida al usuario
				app.master.title('prueba')
				app.mainloop()
				break
			elif opcion==5:
				break

		except:
			print "Porfavor introduzca una opcion"'''
