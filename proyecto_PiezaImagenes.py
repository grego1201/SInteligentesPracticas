#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import signal, os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk

'''------- 	CADA PIEZA ALMACENA IMAGEN, NO SOLO COORDENADAS, OCUPA MAS EN EJECUCION-----------'''

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
		self.obtenerDatos(image_o, image_p)
		self.creartableroOriginal()
		if self.comprobarImagenes():
			self.create_widgets()
			self.mostrar()
			self.after(1000,self.mover)
			self.after(5000, self.crearImagen)
		else:
			print("--- Las imagenes no son iguales --- ")

	def obtenerDatos(self, img_o, img_p):	
		self.img_original=Image.open(img_o)
		self.img_puzzle= Image.open(img_p)
		self.board_width=self.img_original.size[0]
		self.board_height=self.img_original.size[1]
		self.piece_width=self.board_width / self.ancho
		self.piece_height=self.board_height / self.alto

	def create_widgets(self):
	    args = dict(width=self.board_width, height=self.board_height)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def creartableroOriginal(self):
		self.tableroOriginal = []
		self.tableroPuzzle=[]

		self.listaImg_Original=[]
		self.listaImg_Puzzle=[]

		contadorPivote=0
		ids=0

		for x in xrange(self.ancho):
			for y in xrange(self.alto):
				x0 = x * self.piece_width
				y0 = y * self.piece_height
				x1 = x0 + self.piece_width
				y1 = y0 + self.piece_height

				#foto original
				if x==0 and y==0:
					self.listaImg_Original.append(Image.new("RGB",(self.piece_width,self.piece_height),"black"))#en esta se almacenan los trozos de imagenes sin tratar para comprobarlos, luego se vacia
					image = ImageTk.PhotoImage(self.listaImg_Original[ids])
				else:				
					self.listaImg_Original.append(self.img_original.crop((x0, y0, x1, y1))) 
					image = ImageTk.PhotoImage(self.listaImg_Original[ids])

				self.tableroOriginal.append(self.nuevaPieza(ids,image,(x,y)))

				#foto puzzle
				self.listaImg_Puzzle.append(self.img_puzzle.crop((x0, y0, x1, y1)))
				image2 = ImageTk.PhotoImage(self.listaImg_Puzzle[ids])
				self.tableroPuzzle.append(self.nuevaPieza(None,image2,(x,y)))
				ids+=1

		#establece el pivote en el tablero original 
		self.tableroOriginal[0]['pivote']=True
		self.pivote=0

	def comprobarImagenes(self):
		iguales= 0

		#se comparan las imagenes trozo a trozo
		for x in range(0, len(self.tableroOriginal)):
			for y in range(0,len(self.tableroPuzzle)):
					if self.listaImg_Original[x] == self.listaImg_Puzzle[y]:
						iguales = iguales + 1
						self.tableroPuzzle[y]['id']=self.tableroOriginal[x]['id']						
						if x == 0: #establece el pivote en el tablero puzzle
							self.tableroPuzzle[y]['pivote']=True
							self.pivote=y						
						break

		#self.listaImg_Original=[]
		self.listaImg_Puzzle=[]

		if iguales==self.ancho*self.alto: #numero de celdas
			return True
		else:
			return False


	def nuevaPieza(self, ids, image, coor):
		piece = {'id': ids,
		'image'  : image,
		'pos_o'  : coor,
		'pivote' : False, # Identificar que pieza es el pivote
		}

		return piece

	def mostrar(self):
		index = 0
		for x in xrange(self.ancho):
			for y in xrange(self.alto):
				x1 = x * self.piece_width
				y1 = y * self.piece_height
				image = self.tableroPuzzle[index]['image']
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
			movimiento='Up'
			coorX=self.tableroPuzzle[self.pivote]['pos_o'][0]
			coorY=self.tableroPuzzle[self.pivote]['pos_o'][1]-1
		if a ==1:
			movimiento='Down'
			coorX=self.tableroPuzzle[self.pivote]['pos_o'][0]
			coorY=self.tableroPuzzle[self.pivote]['pos_o'][1]+1
		if a ==2:
			movimiento='Left'
			coorX=self.tableroPuzzle[self.pivote]['pos_o'][0]-1
			coorY=self.tableroPuzzle[self.pivote]['pos_o'][1]
		if a ==3:
			movimiento='Right'
			coorX=self.tableroPuzzle[self.pivote]['pos_o'][0]+1
			coorY=self.tableroPuzzle[self.pivote]['pos_o'][1]

		if self.movimientosValidos(self.tableroPuzzle[self.pivote]['pos_o'],movimiento):
			
			for i in self.tableroPuzzle:		
				if i['pos_o']==(coorX,coorY):
					break
				indice2+=1

			self.cambioPiezas(self.pivote,indice2)
			x = int(self.tableroPuzzle[self.pivote]['pos_o'][0]) * self.piece_width
			y = int(self.tableroPuzzle[self.pivote]['pos_o'][1]) * self.piece_height
			aux=self.pintar(x, y, self.tableroPuzzle[self.pivote]['image'])

			x = int(self.tableroPuzzle[indice2]['pos_o'][0]) * self.piece_width
			y = int(self.tableroPuzzle[indice2]['pos_o'][1]) * self.piece_height
			aux=self.pintar(x, y, self.tableroPuzzle[indice2]['image'])

			self.pivote=indice2
			self.after(1000,self.mover)
		else:
			self.after(0,self.mover)

	def movimientosValidos(self, coor, movimiento):
		valido=True

		if (coor[0]==0 and movimiento=='Left') or (coor[0]==3 and movimiento=='Right') or (coor[1]==0 and movimiento=='Up') or (coor[1]==3 and movimiento=='Down'):
			valido=False

		return valido


	#cambia todo menos las coordenadas
	def cambioPiezas(self, id1, id2):
		aux = self.tableroPuzzle[id1]
		coor2=self.tableroPuzzle[id2]['pos_o']
		self.tableroPuzzle[id1]=self.tableroPuzzle[id2]
		self.tableroPuzzle[id1]['pos_o']=aux['pos_o']
		self.tableroPuzzle[id2]=aux
		self.tableroPuzzle[id2]['pos_o']=coor2

			
	def crearImagen(self):
		imagen = Image.new("RGB",(self.board_width,self.board_height),"white")
		indice=0
		#img2= Image.new("RGB",(self.piece_width,self.piece_height),"black")

		for x in xrange(self.ancho):
			for y in xrange(self.alto):
				x0 = x * self.piece_width
				y0 = y * self.piece_height

				imagen.paste(self.listaImg_Original[self.tableroPuzzle[indice]['id']],(x0,y0))
				indice+=1

		imagen.save("imagenGenerada.png")


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
	#IntermedioAlhambra10x5
	#Inicialalhambra10x5
	app = puzzle('Inicialalhambra10x5.png','IntermedioAlhambra10x5.png', 10,5) 
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
