#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import copy
from time import time
import resource
import signal, os
import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk

MOVE_UP = "Up"
MOVE_DOWN = "Down"
MOVE_LEFT = "Left"
MOVE_RIGHT = "Right"

''' -------------- LAS PIEZAS NO ALMACENAN IMAGENES, SOLO UN ID QUE RELACIONA LA PIEZA CON UNA IMAGEN ---------------'''


''' -------- Clase puzzle, contiene la ejecucion principal ---------- '''
''' ----------------------------------------------------------------- '''
class app(tk.Frame):

	def __init__(self,imagen_o,imagen_p, columnas, filas):
		tk.Frame.__init__(self)
		self.grid()

		self.columnas=columnas
		self.filas=filas

		if self.obtener_datos(imagen_o, imagen_p):
			self.crear_tablero_original()
			if self.comprobar_imagenes():


				#padre, estado, costo, accion, valor, posPiv):
				#self.crear_canvas()
				#self.mostrar()
				#self.after(2000,self.mover) #cada 1s llama al metodo mover

				#para probar lo de los sucesores una vez


				tiempoInicial = time()
				self.limitarMemoria(1<<30) # 1 para cantidad y 30 para unidad ( 1 giga)
				listSuc=self.sucesores(self.tablero_puzzle, self.pivote)
				front = frontera()

				nodos = 0
				sum = 0
				tiempoMax = 0
				tiempoMin = 0
				media = 0
				tiempos = []
				try:
					while True:
						nodos += 1
						
						tiempoActual = time()
						front.insertar(nodo(0,listSuc[0]['estado'],listSuc[0]['coste'],listSuc[0]['movimiento'],random.randint(0,10),listSuc[0]['posPivote'])) #el padre como se identifica????? id nodo o algo asi?
						tiempoDespues = time()
						tiempoTardado = tiempoDespues - tiempoActual
						if tiempoTardado is > tiempoMax:
								tiempoMax = tiempoTardado
						elif tiempoTardado is < tiempoMin:
								tiempoMin = tiempoTardado
						tiempos.append(tiempoTardado)
					for i in xrange(tiempos):
						sum = sum + i
					media = sum/nodos
				except MemoryError:
					tiempoFin = time() - tiempoInicio
					print str(tiempoFin) + " segundos"
					print str(nodos) + "nodos creados"
					sys.stderr.write('\n\nExcepcion: Limite de memoria alcanzado\n')
					sys.exit(-1)




				#para probar a crear nodos con la lista de sucesores y meterlos en la frontera


				'''
				print("Valores de la frontera:")
				while front.isEmpty() == False:
					print(front.eliminar().getValor())
				'''

				 #self.after(5000,self.crear_imagen) #crea una imagen del puzzle para probar el metodo a los 5s
			else:
				print ("--- La imágenes no son iguales ---")



	def limitarMemoria(self, tamMax):
	    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
	    resource.setrlimit(resource.RLIMIT_AS, (tamMax, hard))

	def obtener_datos(self, img_o, img_p):
		try:
			self.img_original=Image.open(img_o) #carga la imagen inicial
			self.img_puzzle= Image.open(img_p) #carga la imagen con el estado inicial

			#establece el ancho y alto del tablero
			self.ancho_tablero=self.img_original.size[0]
			self.alto_tablero=self.img_original.size[1]

			#establece el alto y ancho de las piezas
			self.ancho_pieza=self.ancho_tablero / self.columnas
			self.alto_pieza=self.alto_tablero / self.filas

			return True
		except:
			print("La imagen seleccionada no se encuentra en el directorio")
			return False

	def crear_tablero_original(self):
		self.tablero_original = [] #almacena el tablero conforme estaría resuelto, almacena tuplas (id,coordenadas), las coordenadas x,y simulan una matriz
		self.tablero_puzzle=[] #almacena el tablero conforme al estado inicial, almacena tuplas (id,coordenadas),las coordenadas x,y simulan una matriz

		self.listaImg_Original=[] #almacena la imagen original cortada en trozos, sirve para compararla con la otra imagen y para generar una imagen png nueva
		self.listaImg_Puzzle=[] #almacena la imagen del estado inicial en trozos, para compararla con la original, luego se vacia
		self.imagenes=[] #almacena los trozos igual que en listaImg_Original pero en forma PhotoImage, necesario para mostrarlos en el canvas

		contadorPivote=0
		ids=0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x0 = x * self.ancho_pieza
				y0 = y * self.alto_pieza
				x1 = x0 + self.ancho_pieza
				y1 = y0 + self.alto_pieza

				#foto original
				if x==0 and y==0: #para la imagen 0.0 pone una en negro
					self.listaImg_Original.append(Image.new("RGB",(self.ancho_pieza,self.alto_pieza),"black"))
					self.imagenes.append(ImageTk.PhotoImage(self.listaImg_Original[ids]))
				else:
					self.listaImg_Original.append(self.img_original.crop((x0, y0, x1, y1)))
					self.imagenes.append(ImageTk.PhotoImage(self.listaImg_Original[ids]))

				self.tablero_original.append(self.nueva_pieza(ids,(x,y))) #crea una nueva pieza que almacena la id y la posicion x,y que tendrá

				''' Las ids de las piezas hacen referencia al indice de las listas de imagenes: ListaImg_Original e imagenes
					de forma que no almacenemos imagenes en cada pieza, si no solo un identificador de la imagen real, así ocupa menos
					espacio cara a la generación de estados, y en caso de querer mortrarla o crear una imagen solo hay que emplear
					esa id como indice de las listas '''


				#foto puzzle
				self.listaImg_Puzzle.append(self.img_puzzle.crop((x0, y0, x1, y1)))
				self.tablero_puzzle.append(self.nueva_pieza(None,(x,y))) #crea una nueva pieza sin id, con la posicion que tendrá
				ids+=1

		#establece el pivote en el tablero original
		self.tablero_original[0]['pivote']=True
		self.pivote=0

	def crear_canvas(self):
	    args = dict(width=self.ancho_tablero, height=self.alto_tablero)
	    self.canvas = tk.Canvas(self, **args)
	    self.canvas.grid()

	def comprobar_imagenes(self):
		iguales= 0
		''' tenemos que hacer poda, daba problemas '''
		#se comparan las imagenes trozo a trozo
		for x in range(0, len(self.listaImg_Original)):
			for y in range(0,len(self.listaImg_Puzzle)):
					if self.listaImg_Original[x] == self.listaImg_Puzzle[y]: # si los dos trozos son iguales...
						iguales = iguales + 1

						self.tablero_puzzle[y]['id']=self.tablero_original[x]['id']	#establece a la pieza desordenada la id que corresponde con la imagen original
						self.listaImg_Puzzle[y]=[] # por si hay muchas imagenes dle mismo color, para que no vuelva a comparar y asignar el id a la misma, se elimina de la lista

						if x == 0: #establece el pivote en el tablero puzzle (ya que cuando x sea 0, en el tablero original(y por tanto en la lista original) será la imagen negra)
							self.tablero_puzzle[y]['pivote']=True
							self.pivote=y

						break

		self.listaImg_Puzzle=[] #vacia la lista que no va a volver a utilizarse para liberar memoria

		#si el numero de piezas iguales coincide con el tamaño de la matriz (filas*columnas) es que las dos imagenes son iguales
		if iguales==self.columnas*self.filas:
			return True
		else:
			return False

	def nueva_pieza(self, ids, coor):
		piece = {'id': ids, 'coordenadas'  : coor, 'pivote' : False}
		return piece

	def mostrar(self):
		index = 0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x1 = x * self.ancho_pieza
				y1 = y * self.alto_pieza

				#obtiene la imagen correspondiente a la id almacenada y la muestra en la posicion x,y
				image = self.imagenes[self.tablero_puzzle[index]['id']]
				self.pintar(x1,y1,image)

				index += 1

	def pintar(self,x,y,imagen):
		self.canvas.create_image(x, y, image=imagen, anchor=tk.NW)

	def mover(self):
		indice=0
		coorX=coorY=0

		aleatorio=random.randint(0,3)
		mov=''

		if aleatorio ==0:
			mov = MOVE_UP
			coorX=self.tablero_puzzle[self.pivote]['coordenadas'][0]
			coorY=self.tablero_puzzle[self.pivote]['coordenadas'][1]-1
		if aleatorio ==1:
			mov= MOVE_DOWN
			coorX=self.tablero_puzzle[self.pivote]['coordenadas'][0]
			coorY=self.tablero_puzzle[self.pivote]['coordenadas'][1]+1
		if aleatorio ==2:
			mov= MOVE_LEFT
			coorX=self.tablero_puzzle[self.pivote]['coordenadas'][0]-1
			coorY=self.tablero_puzzle[self.pivote]['coordenadas'][1]
		if aleatorio ==3:
			mov= MOVE_RIGHT
			coorX=self.tablero_puzzle[self.pivote]['coordenadas'][0]+1
			coorY=self.tablero_puzzle[self.pivote]['coordenadas'][1]

		#comprueba si el pivote que está en x,y puede moverse a la posicion definida anteriormente
		if self.movimientos_validos(self.tablero_puzzle[self.pivote]['coordenadas'],mov):

			#busca la pieza que corresponde a la posicion a la que va a moverse el pivote
			for i in self.tablero_puzzle:
				if i['coordenadas']==(coorX,coorY):
					break
				indice+=1

			#las intercambia
			self.tablero_puzzle = self.cambiar_piezas(self.pivote, indice, self.tablero_puzzle)

			#pinta ambas piezas en la nueva posicion
			x = int(self.tablero_puzzle[self.pivote]['coordenadas'][0]) * self.ancho_pieza
			y = int(self.tablero_puzzle[self.pivote]['coordenadas'][1]) * self.alto_pieza
			aux=self.pintar(x, y, self.imagenes[ self.tablero_puzzle[self.pivote]['id']])

			x = int(self.tablero_puzzle[indice]['coordenadas'][0]) * self.ancho_pieza
			y = int(self.tablero_puzzle[indice]['coordenadas'][1]) * self.alto_pieza
			aux=self.pintar(x, y, self.imagenes[self.tablero_puzzle[indice]['id']])

			self.pivote=indice
			self.after(1000,self.mover)
		else:
			self.after(0,self.mover)

	def movimientos_validos(self, coor, movimiento):
		valido=True

		if (coor[0]==0 and movimiento==MOVE_LEFT) or (coor[0]==self.columnas-1 and movimiento==MOVE_RIGHT) or (coor[1]==0 and movimiento==MOVE_UP) or (coor[1]==self.filas-1 and movimiento==MOVE_DOWN):
			valido=False

		return valido

	def cambiar_piezas(self, id1, id2, estado):

		lista_aux=copy.deepcopy(estado) #si no se copia la lista así, lo que hace es apuntar a su zona de memoria
		aux = lista_aux[id1]
		coor2=lista_aux[id2]['coordenadas']

		lista_aux[id1]=lista_aux[id2]
		lista_aux[id1]['coordenadas']=aux['coordenadas']

		lista_aux[id2]=aux
		lista_aux[id2]['coordenadas']=coor2

		return lista_aux


	def crear_imagen(self):

		imagen = Image.new("RGB",(self.ancho_tablero,self.alto_tablero),"white")#crea una imagen en blanco sobre la que se pegarán todas las demas
		indice=0

		for x in xrange(self.columnas):
			for y in xrange(self.filas):
				x0 = x * self.ancho_pieza
				y0 = y * self.alto_pieza

				#recorre la lista de imagenes obteniendo las imagenes en el orden que están en el tablero de ese instante, y las pega juntas
				imagen.paste(self.listaImg_Original[self.tablero_puzzle[indice]['id']],(x0,y0))
				indice+=1

		imagen.save("imagenGenerada.png")

	def esObjetivo(self, estado): #determina si un estado recibido es el objetivo o no
		objetivo = True
		for i in range(0,len(estado)):
			if estado[i]['id']!=self.tablero_original[i]['id']:
				i=len(estado)
				objetivo = False

		if objetivo:
			print("Es objetivo")
		else:
			print("No es objetivo")

		return objetivo

	def sucesores(self,estado, posPiv): #devuelve los estados sucesores desde un estado dado
		#determina que movimientos puede hacer, el coste y el estado resultante de ello
		#return (acc1,estado1,costAcc1)...(accM,estadoM,costAccM)
		costeAcc = 1
		coorPivote = movimiento =  None
		lista_sucesores=[]


		coorPivote=estado[posPiv]['coordenadas']

		if(self.movimientos_validos(coorPivote,MOVE_UP)):
			movimiento=MOVE_UP
			sucesor=self.nuevo_sucesor(movimiento,(self.cambiar_piezas(posPiv,(posPiv-1),estado)),costeAcc,posPiv-1)
			lista_sucesores.append(sucesor)

		if(self.movimientos_validos(coorPivote,MOVE_DOWN)):
			movimiento=MOVE_DOWN
			sucesor=self.nuevo_sucesor(movimiento,(self.cambiar_piezas(posPiv,(posPiv+1),estado)),costeAcc,posPiv+1)
			lista_sucesores.append(sucesor)

		if(self.movimientos_validos(coorPivote,MOVE_LEFT)):
			movimiento=MOVE_LEFT
			sucesor=self.nuevo_sucesor(movimiento,(self.cambiar_piezas(posPiv,(posPiv-self.filas),estado)),costeAcc,posPiv-self.filas)
			lista_sucesores.append(sucesor)

		if(self.movimientos_validos(coorPivote,MOVE_RIGHT)):
			movimiento=MOVE_RIGHT
			sucesor=self.nuevo_sucesor(movimiento,(self.cambiar_piezas(posPiv,(posPiv+self.filas),estado)),costeAcc,posPiv+self.filas)
			lista_sucesores.append(sucesor)

		return lista_sucesores

	def nuevo_sucesor(self,movimiento,estado,coste, posPivote): #almacena también el pivote aunque no se pida para no tener que buscarlo en cada estado luego
		sucesor = {'movimiento': movimiento, 'estado'  : estado, 'coste' : coste, 'posPivote': posPivote}
		return sucesor

''' -------- Clase nodo -------- '''
''' ---------------------------- '''
class nodo():
	def __init__(self, padre, estado, costo, accion, valor, posPiv):
		self.padre = padre
		self.estado = estado
		self.costo = costo
		self.accion = accion
		self.valor = valor
		self.posPiv = posPiv

	def getValor(self):
		return self.valor

	def getEstado(self):
		return self.estado

	def getCosto(self):
		return self.costo

	def getPadre(self):
		return self.padre

	def getPivote(self):
		return self.posPiv

	def getAccion(self):
		return self.accion


''' -------- Clase frontera -------- '''
''' -------------------------------- '''
class frontera():
	def __init__(self):
		self.frontera=[]

	def isEmpty(self):
		if len(self.frontera) is 0 :
			return True
		else:
			return False

	def insertar(self,nodo):
		self.frontera.append(nodo)
		# ordenamos los nodos por valor
		self.frontera.sort(key=lambda nodo: nodo.valor)

	def eliminar(self):
		return self.frontera.pop(0)


''' --- Main --- '''
''' ------------ '''
def leer_entero():
	while True:
		try:
			num = input("Introduzca el numero: ")
			return num
		except:
			print "Porfavor introduzca un numero"


if __name__ == '__main__':

	#Alhambra 4x4
		#AlhambraInicialPuzzle4x4.png
		#IntermedioAlhambra41.png
		#AlhambraPixelesModificado4x4.png
	#Alhambra 10x5
		#Inicialalhambra10x5
		#IntermedioAlhambra10x5
	#Blanco 10x10
		#InicialBlanco10x10.png
		#IntermedioBlanco10x10.png

	app = app('AlhambraInicialPuzzle4x4.png','IntermedioAlhambra41.png', 4,4)
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
