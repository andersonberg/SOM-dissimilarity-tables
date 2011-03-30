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

