#!/usr/bin/env python
# -*- coding: latin1 -*-

# absom.py
# Projeto de mestrado
# Autor: Anderson Berg

import re
import sys
import random
from math import *
import numpy as np
import pdb
from operator import itemgetter, attrgetter
from classes import *
from leitor_sodas import *
from indices import *
from datetime import *
import os.path
from util import *
import time
import config

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects):

	prototipos = []
	clusters = []
	individuals = []
	
	individuals.extend(individuals_objects)
	
	# para cardinalidade q = 1
	for i in range(c):
		prot = random.choice(individuals)
		novo_prototipo = Individual(prot.indice, prot.id2, prot.nome)
		if not novo_prototipo in prototipos:
			prototipos.append(novo_prototipo)
			cluster = Cluster(i, novo_prototipo)
			clusters.append(cluster)
	
	# criando uma matriz com numpy
	mapa = np.array(clusters)
	mapa.shape = (mapa_x, mapa_y)

	#Matriz de distâncias
	
	
	# define as coordenadas de cada cluster no mapa
	for i in range(mapa_x):
		for j in range(mapa_y):
			mapa[i,j].definir_ponto(i,j)

	# cria a matriz de pesos
	for cluster in clusters:
		cluster.pesos = np.ones(len(matrizes))
		for cluster2 in mapa.flat:
			cluster.deltas[cluster2.point] = delta(cluster.point, cluster2.point)

	# Etapa de afetação		
	for objeto in individuals:
		criterios = [ (calcula_criterio(objeto, mapa, denom, matrizes, cluster.point), cluster) for cluster in mapa.flat ]
		(menor_criterio, menor_criterio_cluster) = min(criterios)
		
		# Insere o objeto no cluster de menor critério
		mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
		objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			
	return mapa, individuals
	
def calcula_criterio(obj, mapa, denom, matrizes, point1):
	
	sum_1 = sum([exp(-delta(point1, cluster.point) / denom) * sum(np.array(matrizes[:,int(obj.indice),int(cluster.prototipo.indice)]) * cluster.pesos) for cluster in mapa.flat])

	return sum_1

# Atualiza partição afetando cada indivíduo ao cluster mais adequado
def atualiza_particao(individuals, mapa, denom, matrizes):

	for objeto in individuals:

		# calcula o critério de cada cluster para o objeto em questão
		criterios = [ (calcula_criterio(objeto, mapa, denom, matrizes, cluster.point), cluster) for cluster in mapa.flat ]
		(menor_criterio, menor_criterio_cluster) = min(criterios)
			
		if menor_criterio_cluster.point != objeto.cluster.point:
		#Insere o objeto no cluster de menor critério
			mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
			mapa[objeto.cluster.point.x, objeto.cluster.point.y].remover_objeto(objeto)
			objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])

	return mapa, individuals

# Cálculo para seleção de melhor protótipo para cada cluster
def calcula_prototipo(objeto_alvo, objetos, mapa, denom, matrizes, cluster):

	sum_1 = sum([exp(-(cluster.deltas[obj.cluster.point]) / denom) * sum(np.array(matrizes[:,int(objeto_alvo.indice),int(obj.indice)]) * cluster.pesos ) for obj in objetos])

	return sum_1

# Seleciona o melhor protótipo para cada cluster
def atualiza_prototipo(mapa, individuals, denom, matrizes, q):

	prototipos = []
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			somas1 = [ (calcula_prototipo(obj, individuals, mapa, denom, matrizes, cluster), obj) for obj in individuals]

			somas = [ (criterio,objeto) for (criterio,objeto) in somas1 if objeto not in prototipos]
			
			#se q = 1
			(menor_criterio, menor_criterio_obj) = min(somas)
			novo_prototipo = Individual(menor_criterio_obj.indice, menor_criterio_obj.id2, menor_criterio_obj.nome)
			cluster.prototipo = novo_prototipo
			prototipos.append(menor_criterio_obj)

	return mapa

def atualiza_pesos(objetos, mapa, denom, matrizes):

	for cluster in mapa.flat:
		for i in range (len(cluster.pesos)):
			produto = 1.0
			for matriz in matrizes:
				soma = sum( [ exp(-(cluster.deltas[objeto.cluster.point]) / denom) * matriz[int(objeto.indice)][int(cluster.prototipo.indice)] for objeto in objetos] )
				produto = produto * soma

			matriz_atual = matrizes[i]
			denominador = sum( [ exp(-(cluster.deltas[objeto.cluster.point]) / denom) * matriz_atual[int(objeto.indice)][int(cluster.prototipo.indice)] for objeto in objetos ] )
			
			cluster.pesos[i] = pow(produto, 1./len(matrizes)) / denominador

	
def calcula_energia(mapa, objetos, matrizes, T):
	
	denom = (2. * pow(T,2))
	energia = sum([ exp(-delta(obj.cluster.point, cluster.point) / denom) * sum(np.array( [matriz[int(obj.indice),int(cluster.prototipo.indice)] for matriz in matrizes] ) * cluster.pesos) for cluster in mapa.flat for obj in objetos])

	return energia

