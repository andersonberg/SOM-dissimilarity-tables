#!/usr/bin/env python
# -*- coding: latin1 -*-

# som_diss_table.py
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
	for i in range(len(mapa)):
		for j in range(len(mapa[i])):
			mapa[i,j].definir_ponto(i,j)
	
	# Etapa de afetação		
	for objeto in individuals:
		criterios = [ (calcula_criterio(objeto, mapa, denom, soma_dissimilaridades, cluster.point), cluster) for cluster in mapa.flat ]
		(menor_criterio, menor_criterio_cluster) = min(criterios)

		# Insere o objeto no cluster de menor critério
		mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
		objeto.set_cluster(mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
			
	return mapa, prototipos, individuals
	
# Cálculo para seleção de melhor protótipo para cada cluster
def calcula_prototipo(objeto_alvo, objetos, mapa, denom, soma_dissimilaridades, point2):

	sum_1 = sum([exp(-delta(obj.cluster.point,point2) / denom) * soma_dissimilaridades[obj.indice, objeto_alvo.indice] for obj in objetos])
	return sum_1

# Seleciona o melhor protótipo para cada cluster
def atualiza_prototipo(mapa, individuals, denom, soma_dissimilaridades, q):
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			somas = [ (calcula_prototipo(obj, individuals, mapa, denom, soma_dissimilaridades, cluster.point), obj) for obj in individuals ]
			
			#se q = 1
			(menor_criterio, menor_criterio_obj) = min(somas)
			novo_prototipo = Individual(menor_criterio_obj.indice, menor_criterio_obj.id2, menor_criterio_obj.nome)
			cluster.prototipo = novo_prototipo

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
	
def main():
	
#	if len(sys.argv) != 2:
#		print 'usage: ./som_diss_table.py configuration_file'
#		sys.exit(1)
	
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

	# Lê arquivo de configuração
#	conf_file = sys.argv[1]
	conf_file = raw_input("Digite o caminho do arquivo de configuração: ")
	nome_base = raw_input("Digite o nome da base: ")
	conf = open(conf_file, 'rU')

	configuracao = conf.read()
	
	# número de repetições do experimento	
	r = re.search(r'repeticoes = ([\d]+)', configuracao)
	repeticoes = int(r.group(1))
	# número de linhas no mapa
	x = re.search(r'mapa_x = ([\d]+)', configuracao)
	mapa_x = int(x.group(1))
	# número de colunas no mapa
	y = re.search(r'mapa_y = ([\d]+)', configuracao)
	mapa_y = int(y.group(1))
	# Cardinalidade
	card = re.search(r'q = ([\d]+)', configuracao)
	q = int(card.group(1))
	# T-min
	tm = re.search(r't_min = ([\d|\.]+)', configuracao)
	t_min = float(tm.group(1))
	# T-max
	tM = re.search(r't_max = ([\d|\.]+)', configuracao)
	t_max = float(tM.group(1))
	# Número de iterações
	n = re.search(r'n_iter = ([\d]+)', configuracao)
	n_iter = float(n.group(1))

	# Arquivos de dados
	f = re.search(r'files: ([\w|\W|\s]+)', configuracao)
	arquivos = f.group(1)
	filenames = arquivos.split()

	text.append("Parâmetros iniciais\n")
	text.append("\nTopologia: " + str(mapa_x) + "x" + str(mapa_y))
	text.append("\nCardinalidade (q): " + str(q))
	text.append("\nTmin: " + str(t_min) + " Tmax: " + str(t_max))
	text.append("\nNúmero de iterações: " + str(n_iter))

	# Lê mais de um arquivo sodas
	for filename in filenames:
		dissimilaridades, individuals_objects, classes_a_priori = leitor(filename)
		dissimilaridades = np.array(dissimilaridades)
		matrizes.append(dissimilaridades)

	# Cria um array de matrizes
	matrizes = np.array(matrizes)

	soma_dissimilaridades = []
	for obj1 in individuals_objects:
		for obj2 in individuals_objects:
			soma_dissimilaridades.append(sum(matrizes[:,obj1.indice,obj2.indice]))

	soma_dissimilaridades = np.array(soma_dissimilaridades).reshape(len(individuals_objects), len(individuals_objects))

	criterios_energia = []
	oercs = []

	c = mapa_x * mapa_y

	for a in range(repeticoes):

		# Etapa de inicialização

		text.append("\n\n#####################################")
		text.append("\nRepetição do experimento: " + str(a) + "\n")
	
		print "Repetição ", a
		print "..."

		# Inicialização
		T = t_max
		t = 0.0
		denom = 2. * math.pow(T,2)
		(mapa, prototipos, individuals) = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, soma_dissimilaridades, individuals_objects)	
	
		#Iterações
		while T > t_min:
		# while t < (n_iter - 1):
			#Step 1: computation of the best prototypes
			t += 1.0
			T = t_max * math.pow( (t_min / t_max), (t / (n_iter - 1.0)) )
			denom = 2. * math.pow(T,2)

			mapa = atualiza_prototipo(mapa, individuals, denom, soma_dissimilaridades, q)
				
			#Step 2: definition of the best partition
			
			mapa, individuals = atualiza_particao(individuals, mapa, denom, soma_dissimilaridades)

#			energia = calcula_energia(mapa, individuals, soma_dissimilaridades, T)
#			text.append("\n\nCritério de adequação (energia): " + str(energia))

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

		###########################################################
		# Cálculo do recall #
		recall_matrix =	calcula_recall(confusion_matrix, classes_a_priori, no_clusters_completos)

		###########################################################
		# Cálculo do f_measure #

		len_cls_priori = len(classes_a_priori)
		f_measure_matrix = calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, no_clusters_completos)
		soma2 = sum( [ confusion_matrix[i,:].sum() * f_measure_matrix[i,:].max() for i in range(len(classes_a_priori)) ] )
		f_measure = float(soma2 / no_objetos)
		text.append("\nF-measure(P,Q): " + str(f_measure))

		###########################################################
		# Cálculo do oerc (taxa de erro de classificação global) #
		oerc = calcula_oerc(confusion_matrix, no_clusters_completos, no_objetos)
		oercs.append(oerc)
		text.append("\nOERC: " + str(oerc))

	menor_criterio_energia = min(criterios_energia)
	menor_erro = min(oercs)
	text.append("\n\nMelhor repetição: " + str(criterios_energia.index(menor_criterio_energia)))
	text.append("\nMenor oerc: " + str(oercs.index(menor_erro)))

	hoje = date.today()
	filename_result = nome_base + "-" + str(mapa_x) + "x" + str(mapa_y) + "-" + hoje.strftime("%d%m%y") + "_01.txt"

	resultado = open(filename_result, 'w')
	resultado.writelines(text)
	resultado.close()

	print "Fim do experimento."

	# dissimilaridades_txt = []
	# for dissimilaridade in dissimilaridades:
		# dissimilaridades_txt.append(str(dissimilaridade) + " " + str(len(dissimilaridade)))
	
	# dados = open("matriz.txt", 'w')
	# text = '\n'.join(dissimilaridades_txt)
	# dados.write(text + '\n')
	# dados.close()

if __name__ == '__main__':
	main()