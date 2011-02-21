#!/usr/bin/env python
# -*- coding: latin1 -*-

# som_diss_table_adap.py
# Projeto de mestrado
# Autor: Anderson Berg

import re
import sys
import random
import math
#from numpy import *
import numpy as np
import pdb
from operator import itemgetter, attrgetter
from classes import *
from leitor_sodas import *
from datetime import *
import os.path

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects):

	prototipos = []
	clusters = []
	individuals = []
	
	for obj in individuals_objects:
		individuals.append(obj)
	
	# para cardinalidade q = 1
	for i in range(c):
		prot = random.choice(individuals)
		novo_prototipo = Individual(prot.indice, prot.id2, prot.nome)
		if not novo_prototipo in prototipos:
			prototipos.append(novo_prototipo)
			cluster = Cluster(i, novo_prototipo)
			clusters.append(cluster)

	# cria a matriz de pesos
	for cluster in clusters:
		cluster.pesos = np.ones(len(matrizes))		
	
	#criando uma matriz com numpy
	mapa = np.array(clusters)
	mapa.shape = (mapa_x, mapa_y)
	
	#define as coordenadas de cada cluster no mapa
	for i in range(mapa_x):
		for j in range(mapa_y):
			mapa[i,j].definir_ponto(i,j)
			
	for objeto in individuals:
		criterios = {}
		for cluster in mapa.flat:
			point1 = Point(cluster.point.x, cluster.point.y)
			criterio = calcula_criterio(objeto, mapa, denom, matrizes, point1)
			criterios[ cluster ] = criterio
		
		(menor_criterio_cluster, menor_criterio) = min(criterios.items(), key=lambda x: x[1])

		#Insere o objeto no cluster de menor critério
		mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
		objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			
	return mapa, prototipos, individuals
	
def calcula_criterio(obj, mapa, denom, matrizes, point1):
	
	sum1 = 0.0
	for cluster in mapa.flat:
		point2 = Point(cluster.point.x, cluster.point.y)
		
		diss = []
		for matriz in matrizes:
			diss.append(matriz[int(obj.indice),int(cluster.prototipo.indice)])

		dissimilaridades = np.array(diss)
		produtos = dissimilaridades * cluster.pesos
		sum2 = sum(produtos)
		
		kernel = math.exp ( (-1.) * ( delta(point1, point2) / denom ) )
		sum1 += ( kernel  * sum2 )

	return sum1

def atualiza_particao(individuals, mapa, denom, matrizes):
	for objeto in individuals:
		criterios = {}
		for cluster in mapa.flat:
			point1 = Point(cluster.point.x, cluster.point.y)
			criterio = calcula_criterio(objeto, mapa, denom, matrizes, point1)
			criterios[ cluster ] = criterio				

		(menor_criterio_cluster, menor_criterio) = min(criterios.items(), key=lambda x: x[1])
			
		if menor_criterio_cluster.point != objeto.cluster.point:
		#Insere o objeto no cluster de menor critério
			mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
			mapa[objeto.cluster.point.x, objeto.cluster.point.y].remover_objeto(objeto)
			objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			
	for cluster1 in mapa.flat:
		for cluster2 in mapa.flat:
			if cluster1.point != cluster2.point and cluster1.prototipo.nome == cluster2.prototipo.nome:
				if cluster1.point < cluster2.point:
					for obj in cluster2.objetos:
						cluster1.objetos.append(obj)
						obj.cluster = cluster1
					cluster2.objetos = []

	return mapa, individuals

def calcula_prototipo(objeto_alvo, objetos, mapa, denom, matrizes, cluster):

	point2 = Point(cluster.point.x, cluster.point.y)
	sum1 = 0.0
	for obj in objetos:
		point1 = Point(obj.cluster.point.x, obj.cluster.point.y)

		diss = []
		for matriz in matrizes:
			diss.append(matriz[int(obj.indice),int(objeto_alvo.indice)])

		dissimilaridades = np.array(diss)
		produtos = dissimilaridades * cluster.pesos
		sum2 = sum(produtos)
		
		sum1 += ( ( math.exp ( (-1.) * ( delta(point1, point2) / denom ) ) ) * sum2 )
						
	return sum1

def atualiza_prototipo(mapa, individuals, denom, matrizes, q):
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			somas = {}

			for obj in individuals:
				menor_criterio_sum = calcula_prototipo(obj, individuals, mapa, denom, matrizes, cluster)
				somas[obj] = menor_criterio_sum
			
			#se q > 1
			#sorted_criterios = sorted(criterios.items(), key=lambda x: x[1])
			#cluster.prototipos = []
			#for i in range(q):
			#	novo_prototipo = Individual(sorted_criterios[i].indice, sorted_criterios[i].id2, sorted_criterios[i].nome)
			#	cluster.prototipos.append(novo_prototipo)
			
			#se q = 1
			(menor_criterio_obj, menor_criterio) = min(somas.items(), key=lambda x: x[1])
			novo_prototipo = Individual(menor_criterio_obj.indice, menor_criterio_obj.id2, menor_criterio_obj.nome)
			cluster.prototipo = novo_prototipo

	return mapa

def delta(point1, point2):
	dist = float(np.square(point1.x - point2.x) + np.square(point1.y - point2.y))
	#dist = math.fabs(point1.x - point2.x) + math.fabs(point1.y - point2.y)
	return dist

def atualiza_pesos(objetos, mapa, denom, matrizes):

	for cluster in mapa.flat:
		for i in range (len(cluster.pesos)):
			produto = 1.
			for matriz in matrizes:
				soma = 0.
				for objeto in objetos:
					soma += math.exp ( (-1.) * ( delta(objeto.cluster.point, cluster.point) / denom ) ) * matriz[int(objeto.indice),int(cluster.prototipo.indice)]  
				produto *= soma
			numerador = math.pow(produto, 1./len(matrizes))
			matriz_atual = matrizes[i]
			itemindex = np.where(matrizes==matriz)
			denominador = 0.

			for objeto in objetos:
				denominador += math.exp ( (-1.) * ( delta(objeto.cluster.point, cluster.point) / denom ) ) * matriz_atual[int(objeto.indice),int(cluster.prototipo.indice)]
			
			if denominador != 0:
				cluster.pesos[i] = numerador/denominador
	
def main():
	
	if len(sys.argv) != 2:
		print 'usage: ./som_diss_table_adap.py configuration_file'
		sys.exit(1)
	
	matrizes = []
	text = []

	#Lê arquivo de configuração
	conf_file = sys.argv[1]
	conf = open(conf_file, 'rU')

	configuracao = conf.read()
	
	#número de repetições do experimento	
	r = re.search(r'repeticoes = ([\d]+)', configuracao)
	repeticoes = int(r.group(1))
	#número de linhas no mapa
	x = re.search(r'mapa_x = ([\d]+)', configuracao)
	mapa_x = int(x.group(1))
	#número de colunas no mapa
	y = re.search(r'mapa_y = ([\d]+)', configuracao)
	mapa_y = int(y.group(1))
	#Cardinalidade
	card = re.search(r'q = ([\d]+)', configuracao)
	q = int(card.group(1))
	#T-min
	tm = re.search(r't_min = ([\d|\.]+)', configuracao)
	t_min = float(tm.group(1))
	#T-max
	tM = re.search(r't_max = ([\d|\.]+)', configuracao)
	t_max = float(tM.group(1))
	#Número de iterações
	n = re.search(r'n_iter = ([\d]+)', configuracao)
	n_iter = float(n.group(1))

	#Arquivos de dados
	f = re.search(r'files: ([\w|\W|\s]+)', configuracao)
	arquivos = f.group(1)
	filenames = arquivos.split()

	text.append("Parâmetros iniciais\n")
	text.append("\nTopologia: " + str(mapa_x) + "x" + str(mapa_y))
	text.append("\nCardinalidade (q): " + str(q))
	text.append("\nTmin: " + str(t_min) + " Tmax: " + str(t_max))
	text.append("\nNúmero de iterações: " + str(n_iter))
	text.append("\n*Modelo adaptativo")

	#Lê mais de um arquivo sodas
	for filename in filenames:
		filename_base = re.search(r'/([\w]+)[\w|\d|\W]+[\.sds]', filename)

		dissimilaridades, individuals_objects, classes_a_priori = leitor(filename)
		dissimilaridades = np.array(dissimilaridades)
		matrizes.append(dissimilaridades)

	matrizes = np.array(matrizes)
	nome_base = filename_base.group(1)

	criterios_energia = []
	oercs = []

	c = mapa_x * mapa_y

	for a in range(repeticoes):

		#Etapa de inicialização

		text.append("\n\n#####################################")
		text.append("\nRepetição do experimento: " + str(a) + "\n")
	
		print "Repetição ", a
		print "..."

		#Inicialização
		T = t_max
		t = 0.0
		denom = 2. * math.pow(T,2)
		(mapa, prototipos, individuals) = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects)	
	
		while T > t_min:
		# while t < (n_iter - 1):
			#Step 1: computation of the best prototypes
			t += 1.0
			#print 't', t
			T = t_max * math.pow( (t_min / t_max), (t / (n_iter - 1.0)) )
			denom = 2. * math.pow(T,2)

			mapa = atualiza_prototipo(mapa, individuals, denom, matrizes, q)

			#Step 2: computation of the best weights
			atualiza_pesos(individuals, mapa, denom, matrizes)
				
			#Step 3: definition of the best partition
			
			mapa, individuals = atualiza_particao(individuals, mapa, denom, matrizes)

		for cluster in mapa.flat:
			text.append("\nCluster " + str(cluster.point.x) + "," + str(cluster.point.y) + " Prototipo: " + str(cluster.prototipo.nome) +
			" [" + str(len(cluster.objetos)) + " objetos]")
			text.append("Objetos: ")
			for objeto in cluster.objetos:
				text.append(str(objeto.nome) + " ")

		no_clusters_completos = 0
		for cluster in mapa.flat:
			if len(cluster.objetos) > 0:
				no_clusters_completos += 1

		energia = calcula_energia(mapa, individuals, matrizes, T)
		criterios_energia.append(energia)

		text.append("\n\nCritério de adequação (energia): " + str(energia))

		########################################
		#Calcula a matrix de confusão #
		confusion_matrix = calcula_confusion_matrix(mapa, classes_a_priori, no_clusters_completos)

		text.append("\n=====================================")
		text.append("\n\tmatriz de confusão")
		text.append("\nClasses\t\t\t Clusters")
		text.append("\n---------------------------------------\n")
		text.append("\t")
		for cluster in mapa.flat:
			if len(cluster.objetos) > 0:
				text.append(str(cluster.point.x) + "," + str(cluster.point.y) + "\t")
		text.append( "Total")
		text.append( "\n")
		i = 0
		for classe in classes_a_priori:	
			text.append("\n" + str(classe.id) + "\t")
			for j in range(no_clusters_completos):
				text.append(str(confusion_matrix[i,j]) + "\t" + " ")
			text.append(str(confusion_matrix[i,:].sum(axis=0)))
			i+=1
	
		text.append("\nTotal" + "\t" + str(confusion_matrix.sum(axis=0)))
	

		##########################################################################################
		# Cálculo do índice de Rand Corrigido #
		no_objetos = len(individuals)
		
		cr = calcula_cr(confusion_matrix, classes_a_priori, no_clusters_completos, no_objetos)	
		text.append("\nCorrected Rand index: " + str(cr) + "\n")

		##########################################################
		# Cálculo da precisão #
		precisao_matrix = calcula_precisao(confusion_matrix, classes_a_priori, no_clusters_completos)
		#print "precisao_matrix"
		#print precisao_matrix

		###########################################################
		# Cálculo do recall #
		recall_matrix =	calcula_recall(confusion_matrix, classes_a_priori, no_clusters_completos)
		#print "recall_matrix"
		#print recall_matrix

		###########################################################
		# Cálculo do f_measure #

		len_cls_priori = len(classes_a_priori)
		f_measure_matrix = calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, no_clusters_completos)

		sum2 = sum(confusion_matrix[:,:].sum(axis=0))

		f_measure = float(sum2 / no_objetos) * f_measure_matrix.max()
		
		text.append("\nF-measure(P,Q): " + str(f_measure))

		###########################################################
		# Cálculo do oerc (taxa de erro de classificação global) #
		oerc = calcula_oerc(confusion_matrix, no_clusters_completos, no_objetos)
		oercs.append(oerc)
		text.append("\nOERC: " + str(oerc))

	menor_criterio_energia = min(criterios_energia)
	maior_criterio_energia = max(criterios_energia)
	menor_erro = min(oercs)
	text.append("\n\nMelhor repetição: " + str(criterios_energia.index(menor_criterio_energia)))
	text.append("\nMaior critério: " + str(criterios_energia.index(maior_criterio_energia)))
	text.append("\nMenor oerc: " + str(oercs.index(menor_erro)))

	hoje = date.today()
	filename_result = nome_base + "-" + str(mapa_x) + "x" + str(mapa_y) + "-" + hoje.strftime("%d%m%y") + "_adaptativo_01.txt"

	resultado = open(filename_result, 'w')
	resultado.writelines(text)

	#txt = ' '.join(text)
	#resultado.write(txt + '\n')
	
	resultado.close()

	print "Fim do experimento."

def calcula_energia(mapa, objetos, matrizes, T):
	
	denom = (2. * math.pow(T,2))
	energia = 0.
	for obj in objetos:
		point1 = Point(obj.cluster.point.x, obj.cluster.point.y)	
		sum1 = 0.0
		
		for cluster in mapa.flat:
			point2 = Point(cluster.point.x, cluster.point.y)

			diss = []
			for matriz in matrizes:
				diss.append(matriz[int(obj.indice),int(cluster.prototipo.indice)])

			dissimilaridades = np.array(diss)
			produtos = dissimilaridades * cluster.pesos
		
			sum1 += ( ( math.exp ( (-1.) * ( delta(point1, point2) / denom ) ) ) * sum(produtos) )
		
		energia += sum1

	return energia

def combinacao(n):
	resultado = (n * (n - 1)) / 2.
	return resultado

#Calcula a matrix de confusão
def calcula_confusion_matrix(mapa, classes_a_priori, no_clusters_completos):

	confusion_matrix = np.zeros( (len(classes_a_priori),no_clusters_completos), dtype=np.int32 )
	i = 0
	for classe in classes_a_priori:
		j = 0
		for cluster in mapa.flat:
			if len(cluster.objetos) > 0:
				for obj in classe.objetos:
					if obj in cluster.objetos:
						confusion_matrix[i,j] += 1
				j += 1
		i += 1

	return confusion_matrix

# Cálculo do índice de Rand Corrigido #
def calcula_cr(confusion_matrix, classes_a_priori, no_clusters_completos, no_objetos):

	x = math.pow( combinacao(no_objetos), -1)
	# Cálculo do numerador
	soma1 = 0.
	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			soma1 += combinacao(confusion_matrix[i,j])

	soma1 = soma1 - x

	soma2 = 0.
	for i in range(len(classes_a_priori)):
		soma2 += combinacao(confusion_matrix[i,:].sum())

	soma3 = 0.
	for j in range(no_clusters_completos):
		soma3 += combinacao(confusion_matrix[:,j].sum())

	numerador_cr = soma1 * soma2 * soma3

	# Cálculo do denominador
	fator1 = (((0.5) * (soma2 + soma3))) - x

	denominador_cr = fator1 * soma2 * soma3

	cr = numerador_cr / denominador_cr

	return cr
	
# Cálculo da precisão #
def calcula_precisao(confusion_matrix, classes_a_priori, no_clusters_completos):
	precisao_matrix = np.empty( (len(classes_a_priori),no_clusters_completos) )

	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			precisao_matrix[i,j] = float(confusion_matrix[i,j]) / float(confusion_matrix[:,j].sum())

	return precisao_matrix

# Cálculo do recall #
def calcula_recall(confusion_matrix, classes_a_priori, no_clusters_completos):
	recall_matrix = np.empty( (len(classes_a_priori),no_clusters_completos) )
	
	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			recall_matrix[i,j] = float(confusion_matrix[i,j]) / float(confusion_matrix[i,:].sum())

	return recall_matrix

# Cálculo do F-measure #
def calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, len_clusters_comp):

	f_measure_matrix = np.empty( (len_cls_priori, len_clusters_comp) )

	for i in range(len_cls_priori):
		for j in range(len_clusters_comp):
			if precisao_matrix[i,j] == 0 and recall_matrix[i,j] == 0:
				f_measure_matrix[i,j] = 0.
			else:
				result = 2. * ( (precisao_matrix[i,j]*recall_matrix[i,j]) /  (precisao_matrix[i,j]+recall_matrix[i,j]) )
				f_measure_matrix[i,j] = result			

	return f_measure_matrix

# Cálculo do oerc (erro global) #
def calcula_oerc(confusion_matrix, len_clusters_comp, len_objetos):

	array_max = confusion_matrix.max(axis=0)
	soma = float(array_max.sum())

	resultado = 1. - (float(soma) / float(len_objetos))

	return resultado

if __name__ == '__main__':
	main()