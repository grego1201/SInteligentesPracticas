#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Tkinter import *
from PIL import Image, ImageTk


def cortarImagen(ventana, imagen, ancho, alto):

	''' --- recibe una imagen, la corta y la coloca en labels ---'''
	filas = 5
	columnas = 5
	#matriz = [] #almacena en una matriz cada trozo de imagen
	coordenadas=[] #matrix de filas x columas, almacena en cada casilla las 4 coordenadas del trozo de imagen
	xSuperior = ySuperior = 0
	yInferior = alto/filas
	xInferior = ancho/columnas
	#img = Image.new("RGB",(ancho,alto),"white") #crea imagen en blanco del mismo tamaño para pegar encima los trozos

	''' Recorre la imagen de arriba a abajo, de izquierda a derecha'''
	for x in range(0,filas):
		#matriz.append([])
		coordenadas.append([])  #crea la primera fila de la matriz, vacia
		for y in range(0,columnas):
			#matriz[x].append(imagen.crop((xSuperior,ySuperior,xInferior,yInferior))) #ancho,alto
			coordenadas[x].append((xSuperior,ySuperior,xInferior,yInferior)) #introduce en la matriz
			#img.paste(imagen.crop(coordenadas[x][y]), (xSuperior,ySuperior,xInferior,yInferior))   #volver a pegar la imagen para visualizarla en el img.show()
			xSuperior=xInferior #coloca la X del primer punto, en el punto siguiente (que será) la posicion del punto anterior, ya que se recorre en el eje X
			xInferior=xInferior+(ancho/columnas) #mueve el punto inferior a la siguiente posicion
		ySuperior=yInferior #baja una posicion en el eje y, es decir, a la posicion del punto inferior
		yInferior =yInferior +(alto/filas) #baja una posicion el punto inferior
		xSuperior=0 #vuelve al origen de coordenadas en el eje x
		xInferior=ancho/columnas #coloca el x inferior 
	#img.show()   # Mostrar imagen final

	labels=[]
	photos = []
	posx=0
	posy=0
	indice=0

	for x in range (0,filas):
		for y in range(0,columnas):
			#obtiene un trozo de la imagen, lo transforma y lo almacena para posteriormente meterlo en la etiqueta
			photos.append(ImageTk.PhotoImage(imagen.crop(coordenadas[x][y])))
			#photo.append(ImageTk.PhotoImage(matriz[x][y]))
			labels.append(Label(ventana, image=photos[indice]).place(x=0+posx, y=0+posy))#crea una etiqueta con esa imagen para mostrarla
			indice = indice +1
			posx=posx+(ancho/columnas)
		posy=posy+(alto/filas)
		posx=0


	ventana.mainloop() #esto creo que establece los cambios en la ventana

	return ventana, photos, labels

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


ventana, photos, labels = cortarImagen(ventana, imagen, t1,t2) #devuelve la venta, un array de etiquetas (para moverlas y eso luego)
															  # y trozos de foto (esto ultimo lo dejamos asi y si vemos que luego no hace falta se borra)

ventana.mainloop()#esto creo que establece los cambios en la ventana
