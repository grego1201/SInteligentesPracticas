#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Tkinter import *
from PIL import Image, ImageTk


def cortarImagen(ventana,imagen, ancho, alto):
	'''im = Image.open(ruta)
	region = im.crop((0,0,x,y))
	region.save("imagenprueba.png","PNG")'''
	filas = 5
	columnas = 5
	matriz = []
	xini = yini = 0
	xfin = alto/filas
	yfin = ancho/columnas
	img = Image.new("RGB",(ancho,alto),"white")

	for x in range(0,filas):
		matriz.append([])
		for y in range(0,columnas):
			matriz[x].append(imagen.crop((yini,xini,yfin,xfin))) #ancho,alto
			img.paste(matriz[x][y], (yini,xini,yfin,xfin))   # Pegar región girada en la imagen original
			yini=yfin
			yfin=yfin+(ancho/columnas)
		xini=xfin
		xfin =xfin +(alto/filas)
		yini=0
		yfin=ancho/columnas
	img.show()   # Mostrar imagen final

	lbl2=[]
	photo = []
	posx=0
	posy=0
	indice=0
	for x in range (0,filas):
		for y in range(0,columnas):
			photo.append(ImageTk.PhotoImage(matriz[x][y]))
			lbl2.append(Label(ventana, image=photo[indice]).place(x=0+posx, y=0+posy))
			indice = indice +1
			posx=posx+(ancho/columnas)
		posy=posy+(alto/filas)
		posx=0




	ventana.mainloop()




''' -------------------------------
			    M A I N
	-------------------------------'''
ventana = Tk()
ventana.title("Prueba");

''' -- Creamos la imagen -- '''
try:
	imagen = Image.open("alhambra.png")
	photo = ImageTk.PhotoImage(imagen)
	t1,t2= imagen.size
	print(t1,t2)
	ventana.geometry(str(t1)+"x"+str(t2)+"+0+0")
	#lblImagen=Label(ventana,image=photo).place(x=0,y=0)
except:
	print("No se ha podido cargar la imagen")


'''imagen2 = imagen.crop((100,100,200,200))
photo2 = ImageTk.PhotoImage(imagen2)
lbl2=Label(ventana, image=photo2).place(x=0, y=0)
'''


cortarImagen(ventana, imagen, t1,t2)
'''imagen2 = Image.open("imagenprueba.png")
photo2 = ImageTk.PhotoImage(imagen2)
lblImagen2=Label(ventana,image=photo2).place(x=200,y=200)'''


ventana.mainloop()
