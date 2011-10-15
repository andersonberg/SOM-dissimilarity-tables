#!/usr/bin/env python
# -*- coding: latin1 -*-

# bsom.py
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
import config

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, soma_dissimilaridades, individuals_objects):

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
	
	#define as coordenadas de cada cluster no mapa
	for i in range(mapa_x):
		for j in range(mapa_y):
			mapa[i,j].definir_ponto(i,j)
	
	# Etapa de afetação		
	for objeto in individuals:
		criterios = [ (calcula_criterio(objeto, mapa, denom, soma_dissimilaridades, cluster.point), cluster) for cluster in mapa.flat ]
		(menor_criterio, menor_criterio_cluster) = min(criterios)

		# Insere o objeto no cluster de menor critério
		mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
		objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			
	return mapa, individuals
	
# Cálculo para seleção de melhor protótipo para cada cluster
def calcula_prototipo(objeto_alvo, objetos, mapa, denom, soma_dissimilaridades, point2):

	sum_1 = sum([exp(-delta(obj.cluster.point,point2) / denom) * soma_dissimilaridades[obj.indice, objeto_alvo.indice] for obj in objetos])
	return sum_1

# Seleciona o melhor protótipo para cada cluster
def atualiza_prototipo(mapa, individuals, denom, soma_dissimilaridades, q):
	prototipos = []
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			somas1 = [ (calcula_prototipo(obj, individuals, mapa, denom, soma_dissimilaridades, cluster.point), obj) for obj in individuals ]

			somas = [ (criterio,objeto) for (criterio,objeto) in somas1 if objeto not in prototipos]
			
			#se q = 1
			(menor_criterio, menor_criterio_obj) = min(somas)
			novo_prototipo = Individual(menor_criterio_obj.indice, menor_criterio_obj.id2, menor_criterio_obj.nome)
			cluster.prototipo = novo_prototipo
			prototipos.append(menor_criterio_obj)

	return mapa
	
# Calcula o critério para escolha do cluster para cada indivíduo
def calcula_criterio(obj, mapa, denom, soma_dissimilaridades, point1):

	sum_1 = sum([exp(-delta(point1, cluster.point) / denom) * soma_dissimilaridades[obj.indice, cluster.prototipo.indice] for cluster in mapa.flat])

	return sum_1

# Atualiza partição afetando cada indivíduo ao cluster mais adequado
def atualiza_particao(individuals, mapa, denom, soma_dissimilaridades):
	for objeto in individuals:
		cluster_atual = objeto.cluster

		# calcula o critério de cada cluster para o objeto em questão
		criterios = [ (calcula_criterio(objeto, mapa, denom, soma_dissimilaridades, cluster.point), cluster) for cluster in mapa.flat ]
		(menor_criterio, menor_criterio_cluster) = min(criterios)

		if menor_criterio_cluster.point != cluster_atual.point:
		#Insere o objeto no cluster de menor critério
			mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
			objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			mapa[cluster_atual.point.x, cluster_atual.point.y].remover_objeto(objeto)
			
	for cluster1 in mapa.flat:
		for cluster2 in mapa.flat:
			if cluster1.point < cluster2.point and cluster1.prototipo.nome == cluster2.prototipo.nome:
				cluster1.objetos.extend(cluster2.objetos)
				for obj in cluster2.objetos:
					obj.cluster = cluster1
				cluster2.objetos = []

	return mapa, individuals

def delta(point1, point2):
	dist = float(np.square(point1.x - point2.x) + np.square(point1.y - point2.y))
	#dist = math.fabs(point1.x - point2.x) + math.fabs(point1.y - point2.y)
	return dist

# Calcula o critério de adequação
def calcula_energia(mapa, objetos, soma_dissimilaridades, T):
	denom = (2. * math.pow(T,2))
	energia = sum([ exp(-delta(obj.cluster.point, cluster.point) / denom) * soma_dissimilaridades[obj.indice, cluster.prototipo.indice] for cluster in mapa.flat for obj in objetos ])

	return energia

