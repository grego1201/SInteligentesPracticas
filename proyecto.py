#!/usr/bin/python3
#_*_ coging: uft-8 _*_
from Tkinter import *  
from PIL import Image, ImageTk


def cortarImagen(ventana,imagen, ancho, alto):
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
			matriz[x].append(imagen.crop((yini,xini,yfin,xfin))) 
			#img.paste(matriz[x][y], (yini,xini,yfin,xfin))   #este trozo es para volver a ver la imagen que este bien
			yini=yfin
			yfin=yfin+(ancho/columnas)
		xini=xfin
		xfin =xfin +(alto/filas)
		yini=0
		yfin=ancho/columnas
	#img.show()   #este trozo es para volver a ver la imagen que este bien

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
except:
	print("No se ha podido cargar la imagen")


cortarImagen(ventana, imagen, t1,t2)
  
ventana.mainloop()  