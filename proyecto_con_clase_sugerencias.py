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

	def __init__(self,image, board_grid):
		tk.Frame.__init__(self)
		self.grid()
		self.board_grid=board_grid
		self.cargarImagen(image)
		self.create_widgets()
		self.create_board()
		self.mostrar()

	def cargarImagen(self, image):
		image = Image.open(image)		
		self.image=image
		self.board_width=image.size[0]
		self.board_height=image.size[1]
		self.piece_width=self.board_width / self.board_grid
		self.piece_height=self.board_height / self.board_grid


	def create_widgets(self):
	    args = dict(width=self.board_width, height=self.board_height)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def create_board(self):
		self.tablero = []

		for x in xrange(self.board_grid):
 			for y in xrange(self.board_grid):
				x0 = x * self.piece_width
				y0 = y * self.piece_height
				x1 = x0 + self.piece_width
				y1 = y0 + self.piece_height
				image = ImageTk.PhotoImage(self.image.crop((x0, y0, x1, y1)))
				piece = {'id'     : None,
                         'image'  : image,
                         'pos_o'  : (x, y), 
                         'pos_p'  : get_pieces_around(self), # Posibles posiciones a las que puede cambiar
                         'pos_a'  : None,
                         'pivote' : False, # Identificar que pieza es el pivote 
                         'visible': True}



				self.tablero.append(piece)
		#self.tablero[0]['visible'] = False 

	def mostrar(self):
		random.shuffle(self.tablero) # shuffle = barajar
		index = 0
		for x in xrange(self.board_grid):
			for y in xrange(self.board_grid):
				self.tablero[index]['pos_a'] = (x, y)
				if self.tablero[index]['visible']:
					x1 = x * self.piece_width
 					y1 = y * self.piece_height
					image = self.tablero[index]['image']
					id = self.canvas.create_image(x1, y1, image=image, anchor=tk.NW)
					self.tablero[index]['id'] = id
				index += 1


	#Busca todos los movimientos validos y devuelve una lista con estos
	# Para un movimiento valido es que no se salga del rango, es decir, que si el tamaño maximo es
	# 4, si intenta moverse a la 5 o a la -1 no puede moverse y no es un movimiento valido
def get_pieces_around(self):
        pieces = {'center': None,
                  'right' : None,
                  'left'  : None,
                  'top'   : None,
                  'bottom': None}
        for piece in self.board:
            if not piece['visible']:
                pieces['center'] = piece
                break
        x0, y0 = pieces['center']['pos_a']
        for piece in self.board:
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

'''



		------ IMPORTANTE Y COSAS QUE HACER ------

			Adri guapo, tienes que meter el metodo "comprobarImagenes"
			dentro de la clase puzzle


		------                              ------

		|
		|
		|
		|
		|
	   \|/


'''
def comprobarImagenes(img_o, img_p,ancho,alto):
	#carga imagenes
	img_original = Image.open(img_o)
	img_puzzle = Image.open(img_p)
	#obtiene sus tamaños
	ancho_original, alto_original =img_original.size
	ancho_puzzle, alto_puzzle =img_puzzle.size
	#obtiene el tamaño de las piezas
	ancho_pieza_orig = ancho_original / ancho
	alto_pieza_orig = alto_original / alto
	ancho_pieza_puz = ancho_puzzle / ancho
	alto_pieza_puz = alto_puzzle / alto

	#almacena ambas imagenes en listas (lo mismo hay que cambiarlo a matriz)
	lista_original=[]
	lista_puzzle=[]

	#antes habria que comprobar que ambas imagenes son iguales en tamaño
	for x in range(0,ancho):
		for y in range(0,alto):
			x0 = x * ancho_pieza_orig
			y0 = y * alto_pieza_orig
			x1 = x0 + ancho_pieza_orig
			y1 = y0 + alto_pieza_orig
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

	if iguales==ancho*alto: #ancho por alto porque son las dimensiones de la imagen
		print ("Imagen correcta")
	else:
		print ("Imagen incorrecta")


#este era para ir pixel a pixel pero parece que no hace falta
def compararTrozo(img_original, img_puzzle):
	correcto = True
	ancho, alto = img_original.size
	aux =0
	while aux < alto:		
		for x in xrange(ancho):	
			x1 = x+1
			y1 = aux+1
			img1=img_original.crop((x, aux, x1, y1))
			img2=img_puzzle.crop((x, aux, x1, y1))
			if img1!=img2:
				correcto = False
				x=ancho
				aux=alto
		aux=aux+1
	return correcto



if __name__ == '__main__':
	#AlhambraPixelesModificado4x4
	#IntermedioAlhambra41
	
	comprobarImagenes('AlhambraInicialPuzzle4x4.png','IntermedioAlhambra41.png',1024,760)
	app = puzzle('IntermedioAlhambra41.png', 4)
	app.master.title('prueba')
	app.mainloop()


