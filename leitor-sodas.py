# *-* coding: utf-8 *-*

import re
import sys
import random
import math
#from numpy import *
import numpy as np
import pdb
from operator import itemgetter, attrgetter
from classes import *

def leitor(filename):
	f = open(filename, 'rU')
	text = f.read()
	
	# busca os individuos na base
	match = re.compile(r"\b",re.U)
	individuals = re.findall(r'([\d]+),[\s]*"([\w]+)",[\s]*"([\w|\W][^\n]+)"[\s]*', text)
	individuals_objects = []
	
	for ind in individuals:
		individual = Individual(ind[0], ind[1], ind[2])
		individuals_objects.append(individual)
		
	no_vars = re.search(r'var_nb = ([\d]+)', text)
	numero_variaveis = int(no_vars.group(1))
	print "numero_variaveis: ", numero_variaveis
	# busca a variável categórica na base
	vs = []
	var = re.search(r'VARIABLES[\s]*=[\w|\W]*RECTANGLE_MATRIX[\s]*=', text)
	
	if var:
		#busca variáveis do tipo inter_cont
		vars_cont = re.findall(r'([\d]+) ,(inter_cont) ,"" ,"[\w]+" ,"([\w|\/|\_|\(|\)]+)" ,[\d|\.]+, [\d|\.]+, [\d|\.]+, [\d|\.]+', var.group())

		#busca variáveis do tipo nominal
		vars_categ = re.search(r'([\d]+)[\s]*,[\s]*(nominal)[\s]*,[\s]*""[\s]*,[\s]*"[\w]+"[\s]*,[\s]*"([\w|\/|\_|\(|\)|\']+)"[\s]*,[\s]*[\d|\.]+[\s]*,[\s]*[\d|\.]+[\s]*,[\s]*[\d|\.]+[\s]*,[\s]*([\w|\W]+)[\n][\s]+\)', var.group())

		categ = re.search(r'[\d]+[\s]*,nominal[\w|\W]*[\n][\s]*\)', var.group())
		if categ:
			classes_re = re.findall(r'([\d]+)[\s]*,[\s]*"([\w]+)"[\s]*,[\s]*"([\w|\W][^\n]+)"[\s]*,[\d]+', categ.group())

	#variaveis = []
	#for var_cont in vars_cont:
	#	print var_cont
	#	variavel = Variavel(var_cont[0], var_cont[1])
	#	variaveis.append(variavel)

	variavel_nominal = Variavel(vars_categ.group(1), vars_categ.group(2))
	#variaveis.append(variavel_nominal)

	#for v in variaveis:
	#	print v.id, v.tipo

	# classes a priori de uma variável categórica de classe
	classes = []
	for cls in classes_re:
		classe = Classe(cls[0], cls[2])
		classes.append(classe)

	# busca os atributos de cada individuo
	atrib_individuos = re.search(r'(RECTANGLE_MATRIX[\s]*=[\w|\W]*)DIST_MATRIX[\s]*=', text)
	#print atrib_individuos.group(1)
	if atrib_individuos:		
		#|\(\d,
		atribs = re.findall(r'[\([\s]*[\d|.]+[\s]*[:|,][\s]*[\d|.]+[\s]*\)|\(\d\)|\d\)|\(\d]', atrib_individuos.group(1))
		#print atribs
		i = 1
		j = 0
		#for classific in atribs:
		for i in range(int(variavel_nominal.id)-1, len(atribs), numero_variaveis):
		#if i % int(variavel_nominal.id) == 0:
			#print "i: ", i
			classe_individuo = re.search(r'[\d]+', atribs[i])
			classe_id = classe_individuo.group()
			#print "classe_id: ", classe_id
			individuals_objects[j].set_classe_a_priori(classe_id)
			for cls in classes:
				if cls.id == classe_id:
					cls.inserir_objeto(individuals_objects[j])
			j += 1
			#i += 1


	#for classe in classes:
	#	print "\n", classe.id,
	#	for obj in classe.objetos:
	#		print obj.nome,
	
	numbers = []
	m = re.search(r'DIST_MATRIX=\s[\w|\W]+END',  text)
	if m:
		numbers = re.findall(r'[\d]+\.[\d]+', m.group())
	else:
		print "WARNING: O arquivo não contém matriz de dissimilaridades"
		
	values = []
	for i in range(len(numbers)):	
		values.append(float(numbers[i]))
		
	dissimilaridades = []	
	i=0
	n=0
	
	#Contrói uma matriz diagonal
	while i < len(individuals):
		while n < len(values):
			dissimilaridades.append(values[n:n+i+1])
			n=n+i+1
			i+=1
	
	#Preenchendo toda a matriz (tornando-a simétrica)
	col = 0
	i=0
	while i < len(individuals): 
		while col < len(dissimilaridades):
			lin = col + 1
			while lin < len(dissimilaridades):
				dissimilaridades[i].append(dissimilaridades[lin][col])
				lin+=1
			i+=1
			col+=1
	
	return dissimilaridades, individuals_objects, classes
	
	
def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, T, matrizes, individuals):

	prototipos = []
	clusters = []
	
	# para cardinalidade q = 1:
	i = 0
	while i < c:
		prot = random.choice(individuals)
		if not prot in prototipos:
			prototipos.append(prot)
			cluster = Cluster(prot)
			clusters.append(cluster)
			i += 1
	
	#criando uma matriz com numpy
	mapa = np.array(clusters)
	# mapa.shape = (int(np.sqrt(c)), int(np.sqrt(c)))
	mapa.shape = (mapa_x, mapa_y)
	
	#define as coordenadas de cada cluster no mapa
	for i in range(len(mapa)):
		for j in range(len(mapa[i])):
			mapa[i,j].definir_ponto(i,j)
			
	#print "\nMapa\n"	
	#for cluster in mapa.flat:
	#	print cluster.point.x, cluster.point.y, cluster.prototipo.nome
		
	#print
			
	for objeto in individuals:
		#print "\nObjeto: ", objeto.nome
		criterios = {}
		for cluster in mapa.flat:
			#print "Coordenada: ", cluster.point.x, cluster.point.y, " Prototipo: ", cluster.prototipo.nome
			point1 = Point(cluster.point.x, cluster.point.y)
			criterio = calcula_criterio_init(objeto, mapa, T, matrizes, c, point1)
			#print "sum1(criterio): ", criterio
			criterios[ cluster ] = criterio
			
		#for k, v in criterios.items():
		#	print k.prototipo.nome, v
	
		
		(menor_criterio_prot, menor_criterio) = min(criterios.items(), key=lambda x: x[1])
		# print "Menor criterio para o objeto ", objeto.nome, menor_criterio_prot.prototipo.nome, menor_criterio
		
		for cluster in mapa.flat:
			if cluster.prototipo.nome == menor_criterio_prot.prototipo.nome:
				cluster.inserir_objeto(objeto)
				objeto.set_cluster(cluster)
		
	#for cluster in mapa.flat:
	#	print "\nCluster (prototipo): ", cluster.prototipo.nome 
	#	print "Objetos:"
	#	for objeto in cluster.objetos:
	#		print objeto.nome
			
	return mapa, prototipos, individuals
	
def calcula_criterio_init(obj, mapa, T, matrizes, c, point1):
	
	#print "calcula_criterio_init\n"
	denom = (2 * math.pow(T,2))
	sum1 = 0.0
	for cluster in mapa.flat:
		#print "Coordenada: ", cluster.point.x, cluster.point.y, " Prototipo: ", cluster.prototipo.nome
		point2 = Point(cluster.point.x, cluster.point.y)
		sum2 = 0
		
		for matriz in matrizes:
			diss = matriz[int(obj.id)][int(cluster.prototipo.id)]
			sum2 += diss
		
		#print "delta: ", delta(point1, point2)
		#print "sum2: ", sum2
		sum1 += ( ( math.exp ( (-1) * ( delta(point1, point2) / denom ) ) ) * sum2 )
		#print "sum1: ", sum1

	return sum1
	
def calcula_melhor_prototipo(objetos, mapa, T, matrizes, point2):

	somas = {}
	denom = (2 * math.pow(T,2))
	sum1 = 0.0
	for obj in objetos:	
		for cluster in mapa.flat:
			point1 = Point(obj.cluster.point.x, obj.cluster.point.y)
			sum2 = 0
			for matriz in matrizes:
				diss = matriz[int(obj.id)][int(mapa[point2.x,point2.y].prototipo.id)]
				sum2 += diss
			
			sum1 += ( ( math.exp ( (-1) * ( delta(point1, point2) / denom ) ) ) * sum2 )
					
		somas[obj] = sum1

	# print 
	# for k, v in somas.items():
		# print k.nome, v
		
	(menor_criterio_obj, menor_criterio) = min(somas.items(), key=lambda x: x[1])
						
	return menor_criterio_obj, menor_criterio
	
def calcula_cluster_vencedor(obj, mapa, T, matrizes, c, point1):
	denom = (2 * math.pow(T,2))
	sum1 = 0.0
	
	for cluster in mapa.flat:
		point2 = Point(cluster.point.x, cluster.point.y)
		sum2 = 0
		for matriz in matrizes:
			diss = matriz[int(obj.id)][int(cluster.prototipo.id)]
			sum2 += diss
			

		sum1 += ( ( math.exp ( (-1) * ( delta(point1, point2) / denom ) ) ) * sum2 )
		
	return sum1
	
def delta(point1, point2):
	dist = np.square(point1.x - point2.x) + np.square(point1.y - point2.y)
	return dist
	
def calcula_energia(mapa, objetos, matrizes, T):
	
	energia = 0
	for obj in objetos:
		point1 = Point(obj.cluster.point.x, obj.cluster.point.y)
		denom = (2 * math.pow(T,2))
		sum1 = 0.0
		
		for cluster in mapa.flat:
			point2 = Point(cluster.point.x, cluster.point.y)
			sum2 = 0
			for matriz in matrizes:
				diss = matriz[int(obj.id)][int(cluster.prototipo.id)]
				sum2 += diss
				
			sum1 += ( ( math.exp ( (-1) * ( delta(point1, point2) / denom ) ) ) * sum2 )
		
		energia += sum1

	return energia

def combinacao(n):
	resultado = (n * (n - 1)) / 2
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
	
	#for n in confusion_matrix:
	#	print n,
	

	print "\n====================================="
	print "\n\tmatriz de confusão"
	print "Classes\t\t\t Clusters"
	print "---------------------------------------"
	print "\t",
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			print cluster.prototipo.nome, "\t",
	print "Total"
	print "\n"
	i = 0
	for classe in classes_a_priori:	
		print classe.id, "\t", 
		for j in range(no_clusters_completos):
			print confusion_matrix[i,j], "\t\t\t",
		print confusion_matrix[i,:].sum(axis=0)
		i+=1
	
	print "Total", "\t", confusion_matrix.sum(axis=0)

	return confusion_matrix

# Cálculo do índice de Rand Corrigido #
def calcula_cr(confusion_matrix, classes_a_priori, no_clusters_completos, no_objetos):
	# Cálculo do numerador
	soma1 = 0
	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			soma1 += combinacao(confusion_matrix[i,j]) - math.pow( combinacao(no_objetos), -1)

	soma2 = 0
	for i in range(len(classes_a_priori)):
		soma2 += combinacao(confusion_matrix[i,:].sum(axis=0))

	soma3 = 0
	for j in range(no_clusters_completos):
		soma3 += combinacao(confusion_matrix[:,j].sum(axis=0))

	numerador_cr = soma1 * soma2 * soma3

	# Cálculo do denominador
	fator1 = ((0.5) * (soma2 + soma3)) - math.pow( combinacao(no_objetos), -1)

	denominador_cr = fator1 * soma2 * soma3

	cr = numerador_cr / denominador_cr

	print "####################"
	print "Corrected Rand index"
	print cr, "\n"

	return cr
	

def calcula_precisao(confusion_matrix, classes_a_priori, no_clusters_completos):
	precisao_matrix = np.empty( (len(classes_a_priori),no_clusters_completos) )

	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			precisao_matrix[i,j] = float(confusion_matrix[i,j]) / float(confusion_matrix[:,j].sum(axis=0))

	return precisao_matrix

def calcula_recall(confusion_matrix, classes_a_priori, no_clusters_completos):
	recall_matrix = np.empty( (len(classes_a_priori),no_clusters_completos) )
	
	for i in range(len(classes_a_priori)):
		for j in range(no_clusters_completos):
			recall_matrix[i,j] = float(confusion_matrix[i,j]) / float(confusion_matrix[i,:].sum(axis=0))

	return recall_matrix

def calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, len_clusters_comp):

	f_measure_matrix = np.empty( (len_cls_priori, len_clusters_comp) )

	for i in range(len_cls_priori):
		for j in range(len_clusters_comp):
			result = 2 * ( (precisao_matrix[i,j]*recall_matrix[i,j]) /  (precisao_matrix[i,j]+recall_matrix[i,j]) )
			if not math.isnan(result):
				f_measure_matrix[i,j] = result
			else:
				f_measure_matrix[i,j] = -1.
			

	return f_measure_matrix	

def calcula_oerc(confusion_matrix, len_clusters_comp, len_objetos):

	array_max = confusion_matrix.max(axis=0)
	soma = float(array_max.sum())

	resultado = 1. - (float(soma) / float(len_objetos))

	return resultado
			
	
def main():
	args = sys.argv[1:]
	
	if not args:
		print 'usage: files'
		sys.exit(1)
	
	matrizes = []
	
	#Lê mais de um arquivo sodas
	for filename in args:
		dissimilaridades, individuals_objects, classes_a_priori = leitor(filename)
		matrizes.append(dissimilaridades)
		
	#Etapa de inicialização
	print "Parâmetros iniciais\n"
	t = 0
	# c = 9
	mapa_x = 2
	mapa_y = 3
	print "Topologia: ", mapa_x, " x ", mapa_y
	c = mapa_x * mapa_y
	q = 1
	print "Cardinalidade (q): ", q
	t_min = 0.4
	t_max = 6
	print "Tmin: ", t_min, "Tmax: ", t_max
	n_iter = 500
	T = t_max
	(mapa, prototipos, individuals) = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, T, matrizes, individuals_objects)
	
	text = []
	
	text.append("Topologia: " + str(mapa_x) + " x " + str(mapa_y))
	
	text.append("\n>>>>>> Iteracao 0 <<<<<<<<")
	for cluster in mapa.flat:
		text.append("\nCluster (prototipo): " + str(cluster.prototipo.nome) + "\n")
		text.append("Objetos:\n")
		for objeto in cluster.objetos:
			text.append(str(objeto.nome))
	
	while T > t_min:
	# while t < (n_iter - 1):
		#Step 1: computation of the best prototypes
		t += 1
		
		text.append("\n\n>>>>>>Iteracao " + str(t) + " <<<<<<<<")
		# print ">>>>>>Iteracao ", t, "<<<<<<<<"
		
		T = t_max * math.pow( (t_min / t_max), (t / (n_iter - 1)) )
		
		for cluster in mapa.flat:
			point2 = Point(cluster.point.x, cluster.point.y)
			menor_criterio_obj, menor_criterio = calcula_melhor_prototipo(individuals, mapa, T, matrizes, point2)
			if len(cluster.objetos) != 0:
				cluster.prototipo = menor_criterio_obj
				
		#Step 2: definition of the best partition
			
		for objeto in individuals:
			cluster_atual = objeto.cluster
			criterios = {}
			
			for cluster in mapa.flat:
				point1 = Point(cluster.point.x, cluster.point.y)
				criterio = calcula_cluster_vencedor(objeto, mapa, T, matrizes, c, point1)
				# criterios[ cluster ] = criterio
				
				
				criterios[ point1 ] = criterio
		
			#print "\nOrdenando criterios\n"
			# sorted_criterios = sorted(criterios.items(), key=lambda x: x[1])
			
			# for criterio in sorted_criterios:
				# print criterio[0].prototipo.nome
			
			sorted_criterios = sorted(criterios.items(), key=itemgetter(1,0))
			
			#print "Menor: ", mapa[sorted_criterios[0][0].x, sorted_criterios[0][0].y].prototipo.nome, sorted_criterios[0][0].x, sorted_criterios[0][0].y
			#for criterio in sorted_criterios:
			#	print mapa[criterio[0].x, criterio[0].y].prototipo.nome, criterio[0].x, criterio[0].y, criterio[1]
			(menor_criterio_cluster, menor_criterio) = mapa[sorted_criterios[0][0].x, sorted_criterios[0][0].y], sorted_criterios[0][1]
			
			# (menor_criterio_cluster, menor_criterio) = min(criterios.items(), key=lambda x: x[1])
			# print "Menor criterio para o objeto ", objeto.nome, menor_criterio_cluster.prototipo.nome, menor_criterio
			
			# text.append("\nMenor criterio para o objeto " + str(objeto.nome) + " " + str(menor_criterio_cluster.prototipo.nome) + " " +str(menor_criterio))
			
			if menor_criterio_cluster.prototipo.nome != cluster_atual.prototipo.nome:
				menor_criterio_cluster.inserir_objeto(objeto)
				cluster_atual.remover_objeto(objeto)
				objeto.cluster = menor_criterio_cluster
			
		for cluster1 in mapa.flat:
			for cluster2 in mapa.flat:
				if cluster1 != cluster2 and cluster1.prototipo.nome == cluster2.prototipo.nome:
					if cluster1.point < cluster2.point:
						for obj in cluster2.objetos:
							cluster1.objetos.append(obj)
							obj.cluster = cluster1
						cluster2.objetos = []

		for cluster in mapa.flat:
			# print "\nCluster (prototipo): ", cluster.prototipo.nome 
			text.append("\n\nCluster " + str(cluster.point.x) + "," + str(cluster.point.y) + " Prototipo: " + str(cluster.prototipo.nome) +
			" [" + str(len(cluster.objetos)) + " objetos]\n")
			# print "Objetos:"
			text.append("Objetos: ")
			for objeto in cluster.objetos:
				# print objeto.nome
				text.append(str(objeto.nome))

	no_clusters_completos = 0
	for cluster in mapa.flat:
		if len(cluster.objetos) > 0:
			no_clusters_completos += 1
	
	energia = calcula_energia(mapa, individuals, matrizes, T)

	print "Critério de adequação (energia): ", energia

	########################################
	#Calcula a matrix de confusão #
	confusion_matrix = calcula_confusion_matrix(mapa, classes_a_priori, no_clusters_completos)
		

	##########################################################################################
	# Cálculo do índice de Rand Corrigido #
	no_objetos = len(individuals)
	cr = calcula_cr(confusion_matrix, classes_a_priori, no_clusters_completos, no_objetos)	
	
	
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

	soma2 = 0
	for i in range(len(classes_a_priori)):
		soma2 += confusion_matrix[i,:].sum(axis=0)

	f_measure = float(soma2 / no_objetos) * f_measure_matrix.max()
	print "F-measure(P,Q): ", f_measure

	###########################################################
	# Cálculo do oerc (taxa de erro de classificação global) #
	oerc = calcula_oerc(confusion_matrix, no_clusters_completos, no_objetos)
	print "OERC: ", oerc


	text.append("\nEnergia: " + str(energia))
	
	resultado = open("resultados.txt", 'w')
	txt = ' '.join(text)
	resultado.write(txt + '\n')
	resultado.close()
	# dissimilaridades_txt = []
	# for dissimilaridade in dissimilaridades:
		# dissimilaridades_txt.append(str(dissimilaridade) + " " + str(len(dissimilaridade)))
	
	# dados = open("matriz.txt", 'w')
	# text = '\n'.join(dissimilaridades_txt)
	# dados.write(text + '\n')
	# dados.close()

if __name__ == '__main__':
	main()
