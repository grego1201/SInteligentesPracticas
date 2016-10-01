#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk


class Application(tk.Frame):

	def __init__(self,image, board_grid):
		tk.Frame.__init__(self)
		self.grid()
		self.board_grid=board_grid
		self.load_image(image)
		self.create_widgets()
		self.create_board()
		self.show()

	def load_image(self, image):
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
		self.board = []

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
				self.board.append(piece)
		self.board[0]['visible'] = False 

	def show(self):
		random.shuffle(self.board) # shuffle = barajar
		index = 0
		for x in xrange(self.board_grid):
			for y in xrange(self.board_grid):
				self.board[index]['pos_a'] = (x, y)
				if self.board[index]['visible']:
					x1 = x * self.piece_width
 					y1 = y * self.piece_height
					image = self.board[index]['image']
					id = self.canvas.create_image(x1, y1, image=image, anchor=tk.NW)
					self.board[index]['id'] = id
				index += 1
			

if __name__ == '__main__':
	app = Application('alhambra.png', 4)
	app.master.title('prueba')
	app.mainloop()

