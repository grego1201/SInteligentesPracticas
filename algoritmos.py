




def profundidad(prob):
	frontera= Frontera()
	frontera.insertar(nodo(None, prob.estadoInicial, 1, None, 1, self.posPivote()))
	Solucion=False
	while frontera is not isempty():
		if esObjetivo(frontera[frontera.tamanio()-1]):	
			return solucion=True
		else:
			listaSucesores=prob.espacioEstados.sucesores(frontera[frontera.tamanio()-1].estado,frontera.[frontera.tamanio()-1].posPiv)
			for x in listaSucesores:
				nuevoNodo=nodo(frontera[frontera.tamanio()-1], x[1], 1, x[0], 1, self.posPivote())
				frontera.insertar(nuevoNodo)
	

def anchura(prob):
	frontera=Frontera()
	frontera.insert(nodo(None, prob.estadoInicial, 1, None, 1, self.posPivote()))
	solucion=False
	while frontera is not isempty()
		if esObjetivo():
		return rsolucion=True
			
		else:
			listaSucesores=prob.espacioEstados.sucesores(frontera.eliminar().estado,frontera.eliminar().posPiv)
			for x in listaSucesores:
				nuevoNodo=nodo(frontera[frontera.tamanio()-1], x[1], 1, x[0], 1, self.posPivote())
				frontera.insertar(nuevoNodo)
			
def limitada(prob,prof_max):
	frontera=Frontera()
	frontera.insert(nodo(None, prob.estadoInicial, 1, None, 1, self.posPivote()))
	solucion=False
	while prof <= porf_max and frontera is not isEmpty():
		if esObjetivo(frontera[frontera.tamanio()-1]):
			return solucion=True
		else:
			listaSucesores=prob.espacioEstados.sucesores(frontera[frontera.tamanio()-1].estado,frontera.[frontera.tamanio()-1].posPiv)
			prof+=1
			for x in listaSucesores:
				nuevoNodo=nodo(frontera[frontera.tamanio()-1], x[1], 1, x[0], 1, self.posPivote())
				frontera.insertar(nuevoNodo)


def iterativa(prof_aumentada):
	while prof_aumentada <= prof_total:
		limitada(prof_aumentada)
		prof_aumentada+=prof_aumentada
	





		
