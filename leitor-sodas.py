# *-* coding: utf-8 *-*

import re
import sys
import random
import math
#from numpy import *
import numpy as np
import pdb
from operator import itemgetter, attrgetter

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __lt__(self, other):
		if self.x < other.x:
			return True
		elif self.x == other.x:
			if self.y < other.y:
				return True
			else:
				return False
		else:
			return False
			
	def __le__(self, other):
		if self < other or self == other:
			return True
		else:
			return False
			
	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False
			
	def __ne__(self, other):
		if self.x != other.x and self.y != other.y:
			return True
		else:
			return False
			
	def __gt__(self, other):
		if self.x > other.x:
			return True
		elif self.x == other.x:
			if self.y > other.y:
				return True
			else:
				return False
		else:
			return False
			
	def __ge__(self, other):
		if self > other or self == other:
			return True
		else:
			return False
			
	def __hash__(self):
		return id(self)

class Individual:
	def __init__(self, _id, _id2, _nome):
		self.id = _id
		self.id2 = _id2
		self.nome = _nome
		
	def set_cluster(self, cluster):
		self.cluster = cluster

class Cluster:
	def __init__(self, prototipo):
		self.prototipo = prototipo
		self.objetos = []
	
	def definir_ponto(self, x, y):
		self.point = Point(x, y)
	
	def inserir_objeto(self, obj):
		self.objetos.append(obj)
		
	def remover_objeto(self, obj):
		if obj in self.objetos:
			self.objetos.remove(obj)

class Classe:
	def __init__(self, _id, _desc):
		self.id = _id
		self.desc = _desc

class Variavel:
	def __init__(self, _id, _tipo, _desc):
		self.id = _id
		self.tipo = _tipo
		self.desc = _desc

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
		
	# busca a variável categórica na base
	vs = []
	var = re.search(r'VARIABLES[\s]*=[\w|\W]*RECTANGLE_MATRIX[\s]*=', text)
	print var.group()
	if var:
		#busca variáveis do tipo inter_cont
		vars_cont = re.findall(r'([\d]+) ,(inter_cont) ,"" ,"[\w]+" ,"([\w|\/|\_|\(|\)]+)" ,[\d|\.]+, [\d|\.]+, [\d|\.]+, [\d|\.]+', var.group())

		#busca variáveis do tipo nominal
		vars_categ = re.search(r'([\d]+)[\s]*,[\s]*(nominal)[\s]*,[\s]*""[\s]*,[\s]*"[\w]+"[\s]*,[\s]*"([\w|\/|\_|\(|\)]+)"[\s]*,[\s]*[\d|\.]+[\s]*,[\s]*[\d|\.]+[\s]*,[\s]*[\d|\.]+[\s]*,[\s]*([\w|\W]+)[\n][\s]+\)', var.group())

		categ = re.search(r'[\d]+[\s]*,nominal[\w|\W]*[\n][\s]*\)', var.group())
		if categ:
			classes_re = re.findall(r'([\d]+)[\s]*,[\s]*"([\w]+)"[\s]*,[\s]*"([\w|\W][^\n]+)"[\s]*,[\d]+', categ.group())

	variaveis = []
	for var_cont in vars_cont:
		print var_cont
		variavel = Variavel(var_cont[0], var_cont[1], var_cont[2])
		variaveis.append(variavel)
	print vars_categ.group()
#	for var_categ in vars_categ:
#		print var_categ

	for v in variaveis:
		print v.id, v.tipo, v.desc
	

	classes = []
	for cls in classes_re:
		classe = Classe(cls[0], cls[2])
		classes.append(classe)

	#for classe in classes:
	#	print classe.id, classe.desc

	# busca a classificação categórica de cada individuo
	#class_individuos = re.search(r'RECTANGLE_MATRIX[\s]*=[\w|\W]*DIST_MATRIX[\s]*=', text)
	#if class_individuos:
	#	classificacoes = re.findall(r'[\d]', class_individuos.group())
	#	for classific in classificacoes:
	#		print classific,
	
	numbers = []
	m = re.search(r'DIST_MATRIX=\s[\w|\W]+END',  text)
	if m:
		numbers = re.findall(r'[\d]+\.[\d]+', m.group())
	else:
		print "WARNING: O arquivo nao contem matriz de dissimilaridades"
		
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
			
	print "\nMapa\n"	
	for cluster in mapa.flat:
		print cluster.point.x, cluster.point.y, cluster.prototipo.nome
		
	print
			
	for objeto in individuals:
		print "\nObjeto: ", objeto.nome
		criterios = {}
		for cluster in mapa.flat:
			print "Coordenada: ", cluster.point.x, cluster.point.y, " Prototipo: ", cluster.prototipo.nome
			point1 = Point(cluster.point.x, cluster.point.y)
			criterio = calcula_criterio_init(objeto, mapa, T, matrizes, c, point1)
			print "sum1(criterio): ", criterio
			criterios[ cluster ] = criterio
			
		for k, v in criterios.items():
			print k.prototipo.nome, v
	
		
		(menor_criterio_prot, menor_criterio) = min(criterios.items(), key=lambda x: x[1])
		# print "Menor criterio para o objeto ", objeto.nome, menor_criterio_prot.prototipo.nome, menor_criterio
		
		for cluster in mapa.flat:
			if cluster.prototipo.nome == menor_criterio_prot.prototipo.nome:
				cluster.inserir_objeto(objeto)
				objeto.set_cluster(cluster)
		
	for cluster in mapa.flat:
		print "\nCluster (prototipo): ", cluster.prototipo.nome 
		print "Objetos:"
		for objeto in cluster.objetos:
			print objeto.nome
			
	return mapa, prototipos, individuals
	
def calcula_criterio_init(obj, mapa, T, matrizes, c, point1):
	
	print "calcula_criterio_init\n"
	denom = (2 * math.pow(T,2))
	sum1 = 0.0
	for cluster in mapa.flat:
		print "Coordenada: ", cluster.point.x, cluster.point.y, " Prototipo: ", cluster.prototipo.nome
		point2 = Point(cluster.point.x, cluster.point.y)
		sum2 = 0
		
		for matriz in matrizes:
			diss = matriz[int(obj.id)][int(cluster.prototipo.id)]
			sum2 += diss
		
		print "delta: ", delta(point1, point2)
		print "sum2: ", sum2
		sum1 += ( ( math.exp ( (-1) * ( delta(point1, point2) / denom ) ) ) * sum2 )
		print "sum1: ", sum1

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
	t = 0
	# c = 9
	mapa_x = 2
	mapa_y = 3
	c = mapa_x * mapa_y
	q = 1
	t_min = 0.4
	t_max = 3
	n_iter = 15
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
		
			print "\nOrdenando criterios\n"
			# sorted_criterios = sorted(criterios.items(), key=lambda x: x[1])
			
			# for criterio in sorted_criterios:
				# print criterio[0].prototipo.nome
			
			sorted_criterios = sorted(criterios.items(), key=itemgetter(1,0))
			
			print "Menor: ", mapa[sorted_criterios[0][0].x, sorted_criterios[0][0].y].prototipo.nome, sorted_criterios[0][0].x, sorted_criterios[0][0].y
			for criterio in sorted_criterios:
				print mapa[criterio[0].x, criterio[0].y].prototipo.nome, criterio[0].x, criterio[0].y, criterio[1]
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
	
	energia = calcula_energia(mapa, individuals, matrizes, T)
	
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
