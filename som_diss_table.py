#!/usr/bin/env python
# -*- coding: latin1 -*-

# som_diss_table.py
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

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, T, matrizes, soma_dissimilaridades, individuals_objects):

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

	# para cardinalidade q > 1

	#for i in range(c+1):
	#	cluster = Cluster(i+1)
	#	clusters.append(cluster)	
	#for i in range(c):
	#	for j in range(q):
	#		prot = random.choice(individuals)
	#		novo_prototipo = Individual(prot.indice, prot.id2, prot.nome)
	#		if not novo_prototipo in clusters[i].prototipos:
	#			clusters[i].prototipos.append(novo_prototipo)
	#		if not novo_prototipo in prototipos:
	#			prototipos.append(novo_prototipo)
	
	#criando uma matriz com numpy
	mapa = np.array(clusters)
	mapa.shape = (mapa_x, mapa_y)
	
	#define as coordenadas de cada cluster no mapa
	for i in range(len(mapa)):
		for j in range(len(mapa[i])):
			mapa[i,j].definir_ponto(i,j)
			
	for objeto in individuals:
		criterios = {}
		for cluster in mapa.flat:
			point1 = Point(cluster.point.x, cluster.point.y)
			criterio = calcula_criterio(objeto, mapa, T, soma_dissimilaridades, point1)
			criterios[ cluster ] = criterio
	
		
		(menor_criterio_cluster, menor_criterio) = min(criterios.items(), key=lambda x: x[1])
		#print "Menor criterio: ", menor_criterio, menor_criterio_cluster.prototipo.nome, menor_criterio_cluster.point.x, menor_criterio_cluster.point.y

		#Insere o objeto no cluster de menor critério
		mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
		objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			
	return mapa, prototipos, individuals
	
def calcula_prototipo(objeto_alvo, objetos, mapa, denom, soma_dissimilaridades, point2):

	sum1 = 0.0
	for obj in objetos:
		point1 = Point(obj.cluster.point.x, obj.cluster.point.y)
		sum2 = soma_dissimilaridades[obj.indice, objeto_alvo.indice]		
		sum1 += ( ( math.exp ( (-1.) * ( delta(point1, point2) / denom ) ) ) * sum2 )
						
	return sum1

def atualiza_prototipo(mapa, individuals, denom, soma_dissimilaridades, q):
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			somas = {}
			point2 = Point(cluster.point.x, cluster.point.y)
			for obj in individuals:
				menor_criterio_sum = calcula_prototipo(obj, individuals, mapa, denom, soma_dissimilaridades, point2)
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
	
def calcula_criterio(obj, mapa, denom, soma_dissimilaridades, point1):
	
	sum1 = 0.0
	for cluster in mapa.flat:
		point2 = Point(cluster.point.x, cluster.point.y)
		sum2 = soma_dissimilaridades[obj.indice, cluster.prototipo.indice]
		
		#for matriz in matrizes:
		#	diss = matriz[int(obj.indice),int(cluster.prototipo.indice)]
		#	sum2 += diss
		
		kernel = math.exp ( (-1.) * ( delta(point1, point2) / denom ) )
		sum1 += ( kernel  * sum2 )

	return sum1

def atualiza_particao(individuals, mapa, denom, soma_dissimilaridades):
	for objeto in individuals:
		cluster_atual = objeto.cluster
		criterios = {}
		for cluster in mapa.flat:
			point1 = Point(cluster.point.x, cluster.point.y)
			criterio = calcula_criterio(objeto, mapa, denom, soma_dissimilaridades, point1)
			criterios[ cluster ] = criterio				

		(menor_criterio_cluster, menor_criterio) = min(criterios.items(), key=lambda x: x[1])

		#sorted_criterios = sorted(criterios.items(), key=lambda x: x[1])
			
		#sorted_criterios = sorted(criterios.items(), key=itemgetter(1,0))
		#(menor_criterio_cluster, menor_criterio) = mapa[sorted_criterios[0][0].x, sorted_criterios[0][0].y], sorted_criterios[0][1]
			
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
	
def main():
	
	if len(sys.argv) != 2:
		print 'usage: ./som_diss_table.py configuration_file'
		sys.exit(1)
	
#	option = sys.argv[1]
#	if option == '--a':
#		adaptativo = True
#	elif option == '--n':
#		adaptativo = False
#	else:
#		print 'unknown option: ' + option
#		sys.exit(1)
	
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

	#Lê mais de um arquivo sodas
	for filename in filenames:
		filename_base = re.search(r'/([\w]+)[\w|\d|\W]+[\.sds]', filename)

		dissimilaridades, individuals_objects, classes_a_priori = leitor(filename)
		dissimilaridades = np.array(dissimilaridades)
		matrizes.append(dissimilaridades)

	matrizes = np.array(matrizes)
	nome_base = filename_base.group(1)

	soma_dissimilaridades = []
	for obj1 in individuals_objects:
		for obj2 in individuals_objects:
			soma_dissimilaridades.append(sum(matrizes[:,obj1.indice,obj2.indice]))

	soma_dissimilaridades = np.array(soma_dissimilaridades).reshape(len(individuals_objects), len(individuals_objects))

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
		(mapa, prototipos, individuals) = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, soma_dissimilaridades, individuals_objects)	
	
		#Iterações
		while T > t_min:
		# while t < (n_iter - 1):
			#Step 1: computation of the best prototypes
			t += 1.0
			#print 't', t
			T = t_max * math.pow( (t_min / t_max), (t / (n_iter - 1.0)) )
			denom = 2. * math.pow(T,2)

			mapa = atualiza_prototipo(mapa, individuals, denom, soma_dissimilaridades, q)
				
			#Step 2: definition of the best partition
			
			mapa, individuals = atualiza_particao(individuals, mapa, denom, soma_dissimilaridades)

		no_clusters_completos = 0

		for cluster in mapa.flat:
			text.append("\nCluster " + str(cluster.point.x) + "," + str(cluster.point.y) + " Prototipo: " + str(cluster.prototipo.nome) +
			" [" + str(len(cluster.objetos)) + " objetos]")
			text.append("Objetos: ")
			for objeto in cluster.objetos:
				text.append(str(objeto.nome) + " ")

			if len(cluster.objetos) > 0:
				no_clusters_completos += 1

		energia = calcula_energia(mapa, individuals, soma_dissimilaridades, T)
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
		#print precisao_matrix

		###########################################################
		# Cálculo do recall #
		recall_matrix =	calcula_recall(confusion_matrix, classes_a_priori, no_clusters_completos)
		#print recall_matrix

		###########################################################
		# Cálculo do f_measure #

		len_cls_priori = len(classes_a_priori)
		f_measure_matrix = calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, no_clusters_completos)
		#print f_measure_matrix

		soma2 = sum(confusion_matrix[:,:].sum(axis=0))
		f_measure = float(soma2 / no_objetos) * f_measure_matrix.max()
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
	filename_result = nome_base + "-" + str(mapa_x) + "x" + str(mapa_y) + "-" + hoje.strftime("%d%m%y") + "_01.txt"

	resultado = open(filename_result, 'w')
	resultado.writelines(text)

	#txt = ' '.join(text)
	#resultado.write(txt + '\n')
	
	resultado.close()

	print "Fim do experimento."

	# dissimilaridades_txt = []
	# for dissimilaridade in dissimilaridades:
		# dissimilaridades_txt.append(str(dissimilaridade) + " " + str(len(dissimilaridade)))
	
	# dados = open("matriz.txt", 'w')
	# text = '\n'.join(dissimilaridades_txt)
	# dados.write(text + '\n')
	# dados.close()

def calcula_energia(mapa, objetos, soma_dissimilaridades, T):
	
	denom = (2. * math.pow(T,2))
	energia = 0.
	for obj in objetos:
		point1 = Point(obj.cluster.point.x, obj.cluster.point.y)		
		sum1 = 0.0
		
		for cluster in mapa.flat:
			point2 = Point(cluster.point.x, cluster.point.y)
			sum2 = soma_dissimilaridades[obj.indice, cluster.prototipo.indice]
				
			sum1 += ( ( math.exp ( (-1.) * ( delta(point1, point2) / denom ) ) ) * sum2 )
		
		energia += sum1

	return energia

def combinacao(n):
	resultado = (n * (n - 1.)) / 2.
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
	# Cálculo do numerador
	soma1 = 0.
	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			soma1 += (combinacao(confusion_matrix[i,j]))

	x = math.pow( combinacao(no_objetos), -1)
	soma1 = soma1 - x
	soma2 = 0.
	for i in range(len(classes_a_priori)):
		soma2 += combinacao(confusion_matrix[i,:].sum())

	soma3 = 0.
	for j in range(no_clusters_completos):
		soma3 += combinacao(confusion_matrix[:,j].sum())

	numerador_cr = soma1 * soma2 * soma3

	# Cálculo do denominador
	fator1 = (((0.5) * (soma2 + soma3)) - x)

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
				f_measure_matrix[i,j] = -1.
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
