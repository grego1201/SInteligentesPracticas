#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk


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
                         'pos_a'  : None,
                         'visible': True}
				self.tablero.append(piece)
		self.tablero[0]['visible'] = False 

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

def comprobarImagenes(img_o, img_p):
	#carga imagenes
	img_original = Image.open(img_o)
	img_puzzle = Image.open(img_p)
	#obtiene sus tamaños
	ancho_original, alto_original =img_original.size
	ancho_puzzle, alto_puzzle =img_puzzle.size
	#obtiene el tamaño de las piezas
	ancho_pieza_orig = ancho_original / 4
	alto_pieza_orig = alto_original / 4
	ancho_pieza_puz = ancho_puzzle / 4
	alto_pieza_puz = alto_puzzle / 4

	#almacena ambas imagenes en listas (lo mismo hay que cambiarlo a matriz)
	lista_original=[]
	lista_puzzle=[]

	#antes habria que comprobar que ambas imagenes son iguales en tamaño
	for x in range(0,4):
		for y in range(0,4):
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

	if iguales==16: #16 porque es de 4x4

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
	comprobarImagenes('AlhambraInicialPuzzle4x4.png','IntermedioAlhambra41.png')
	#app = puzzle('alhambra.png', 5)
	#app.master.title('prueba')
	#app.mainloop()

