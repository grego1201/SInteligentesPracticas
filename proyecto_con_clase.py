#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
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

	def __init__(self,image_o,image_p, cuadricula):
		tk.Frame.__init__(self)
		self.grid()
		self.cuadricula=cuadricula
		self.comprobarImagenes(image_o,image_p,cuadricula,cuadricula) #esto habra que cambiarlo para mandarle filas y columnas metidas por el usuario
		#si fuese incorrecta en el metodo anterior tenemos que añadir aqui para que no haga lo siguiente
		#ya que no deberia mostrarla al ser incorrecta, digo yo, no sé que querrá xD
		self.cargarImagen(image_o, image_p)
		self.create_widgets()
		self.crearTablero()
		self.mostrar()

	def cargarImagen(self, image_o,image_p):
		image_o= Image.open(image_o)
		image_p= Image.open(image_p)
		self.image=image_p
		self.image_original=image_o
		self.board_width=image_p.size[0]
		self.board_height=image_p.size[1]
		#esto lo cambio cuando tenga un rato, ahora mismo toma matriz cuadrada, cuando añadamos que el usuario
		#meta el tamaño habra que cambiar cuadricula por filas y columnas, que habra que almacenar tb en self y demas
		self.piece_width=self.board_width / self.cuadricula
		self.piece_height=self.board_height / self.cuadricula


	def create_widgets(self):
	    args = dict(width=self.board_width, height=self.board_height)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def crearTablero(self):
		self.tablero = []

		for x in xrange(self.cuadricula):
 			for y in xrange(self.cuadricula):
				x0 = x * self.piece_width
				y0 = y * self.piece_height
				x1 = x0 + self.piece_width
				y1 = y0 + self.piece_height
				image = ImageTk.PhotoImage(self.image.crop((x0, y0, x1, y1)))
				piece = {'id'     : None,
                         'image'  : image,
                         'pos_o'  : (x, y),
                         #'pos_p'  : get_pieces_around(self), # Posibles posiciones a las que puede cambiar
                         'pos_a'  : None,
                         'pivote' : False, # Identificar que pieza es el pivote
                         }

				self.tablero.append(piece)


	def mostrar(self):
		#random.shuffle(self.tablero) # shuffle = barajar, no hace falta al dar el estado inigial ellos
		index = 0
		for x in xrange(self.cuadricula):
			for y in xrange(self.cuadricula):
				self.tablero[index]['pos_a'] = (x, y)
				x1 = x * self.piece_width
				y1 = y * self.piece_height
				image = self.tablero[index]['image']
				id = self.canvas.create_image(x1, y1, image=image, anchor=tk.NW)
				self.tablero[index]['id'] = id
				index += 1

	def comprobarImagenes(self,img_o, img_p,columnas,filas):
		#carga imagenes
		img_original = Image.open(img_o)
		img_puzzle = Image.open(img_p)
		#obtiene sus tamaños
		ancho_o, alto_o =img_original.size
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
				lista_original.append(img_original.crop((x0, y0, x1, y1)))
				lista_puzzle.append(img_puzzle.crop((x0, y0, x1, y1)))

				#lo comentado seria si se mete en la clase, ya que necesita el tk.Frame
				'''img1=ImageTk.PhotoImage(img_original.crop((x0, y0, x1, y1)))
				lista_original.append(img1)
				img2=ImageTk.PhotoImage(img_puzzle.crop((x0, y0, x1, y1)))
				lista_puzzle.append(img2) '''

		iguales= 0
		correctos = []
		correctos.append([])
		#se comparan las imagenes trozo a trozo
		for x in range(0, len(lista_original)):
			for y in range(0,len(lista_puzzle)):
				if (y in correctos) == False:#poda para que no busque en imagenes que ya ha mirado y están ok
					if lista_original[x] == lista_puzzle[y]:
						iguales = iguales + 1
						correctos.append(y)
						y=len(lista_puzzle)

		if iguales==columnas*filas: #numero de celdas
			print ("Imagen correcta")
		else:
			print ("Imagen incorrecta")


	#Busca todos los movimientos validos y devuelve una lista con estos
	# Para un movimiento valido es que no se salga del rango, es decir, que si el tamaño maximo es
	# 4, si intenta moverse a la 5 o a la -1 no puede moverse y no es un movimiento valido
	def get_pieces_around(self):
	        pieces = {'center': None,
	                  'right' : None,
	                  'left'  : None,
	                  'top'   : None,
	                  'bottom': None}
	        for piece in self.tablero:
	            if not piece['visible']:
	                pieces['center'] = piece
	                break
	        x0, y0 = pieces['center']['pos_a']
	        for piece in self.tablero:
	            x1, y1 = piece['pos_a']
	            if y0 == y1 and x1 == x0 + 1:
	                pieces['right'] = piece
	            if y0 == y1 and x1 == x0 - 1:
	                pieces['left'] = piece
	            if x0 == x1 and y1 == y0 - 1:
	                pieces['top'] = piece
	            if x0 == x1 and y1 == y0 + 1:
	                pieces['bottom'] = piece
	        return pieces

	'''def movimientosValidos(pieces):
		Esto no se podria resolver mirando dentro de las piezas obtenidas de la def pieces_around que recoge una lista con los las 			piezas que rodean la pieza pivote y con esta lista solo tendriamos que recorrer las que no sean none para ver los movimiento 			validos
		mov_validos=[]
			for item in xrange(pieces):
				if item == none:
					....... nada
				else:
					mov_validos.append(item)

	def movimientoCorrecto(): ===> "Esto por ahora nada no?"


	def cambioPiezas(piece1,piece2):

		piece_aux = none
		piece_aux= piece1
		piece1=piece2
		piece2=piece_aux

	'''

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
				anchoAlto = leerEntero()
			elif opcion==4:
				app = puzzle('ImagenesPrueba/'+ nombreDes,'ImagenesPrueba/'+nombreOr, anchoAlto) #el 4 es el numero de filas y columnas, tendremos que añadir algo para que las pida al usuario
				app.master.title('prueba')
				app.mainloop()
			elif opcion==5:
				break

		except:
			print "Porfavor introduzca una opcion"
