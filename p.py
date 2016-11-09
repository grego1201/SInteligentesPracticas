#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
import resource
import sys

def limitarMemoria(tamMax):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (tamMax, hard))

def juntList(A,B):
    A.append(B)
    return A


tiempoInicio = time()
limitarMemoria(1<<30) # 1 para cantidad y 30 para unidad ( 1 giga)
cont = 1
A=[]
B=[]

for i in range(0,10000000):
    A.append(i)
    B.append(i)

print "listas creadas"
while True:
    try:
        juntList(A,B)
    except MemoryError:
        tiempoFin = time() - tiempoInicio
        print str(tiempoFin) + " segundos"
        sys.stderr.write('\n\nExcepcion: Limite de memoria alcanzado\n')
        sys.exit(-1)
