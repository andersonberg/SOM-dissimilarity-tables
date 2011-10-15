#!/usr/bin/env python
# -*- coding: latin1 -*-

# config.pyx
# Projeto de mestrado
# Autor: Anderson Berg

from __future__ import division
import re
import sys
import random
from math import *
import numpy as np
import pdb
from operator import itemgetter, attrgetter
from Point import *
from Individual import *
from Cluster import *
from Classe import *
from Variavel import *
from leitor_sodas import *
from indices import *
from datetime import *
import os.path
cimport numpy as np
cimport cython

DTYPE = np.float
ctypedef np.float_t DTYPE_t

@cython.boundscheck(False)
def config(filename):
	text = []

	#Lê arquivo de configuração
#	conf_file = sys.argv[1]
	conf = open(filename, 'rU')
	
	configuracao = conf.read()
	
	#número de repetições do experimento	
	r = re.search(r'repeticoes = ([\d]+)', configuracao)
	cdef int repeticoes = int(r.group(1))
	#número de linhas no mapa
	x = re.search(r'mapa_x = ([\d]+)', configuracao)
	cdef int mapa_x = int(x.group(1))
	#número de colunas no mapa
	y = re.search(r'mapa_y = ([\d]+)', configuracao)
	cdef int mapa_y = int(y.group(1))
	#Cardinalidade
	card = re.search(r'q = ([\d]+)', configuracao)
	cdef int q = int(card.group(1))
	#T-min
	tm = re.search(r't_min = ([\d|\.]+)', configuracao)
	cdef float t_min = float(tm.group(1))
	#T-max
	tM = re.search(r't_max = ([\d|\.]+)', configuracao)
	cdef float t_max = float(tM.group(1))
	#Número de iterações
	n = re.search(r'n_iter = ([\d]+)', configuracao)
	cdef float n_iter = float(n.group(1))

	#Arquivos de dados
	f = re.search(r'files: ([\w|\W|\s]+)', configuracao)
	arquivos = f.group(1)
	filenames = arquivos.split()

	text.append("# Topology: " + str(mapa_x) + "x" + str(mapa_y))
	text.append("\n# Cardinality (q): " + str(q))
	text.append("\n# Tmin: " + str(t_min) + "\n# Tmax: " + str(t_max))
	text.append("\n# Number of iterations: " + str(n_iter))


	dissimilaridades0, individuals_objects0, classes_a_priori0 = leitor(filenames[0])
	dissimilaridades0 = np.array(dissimilaridades0)
	cdef int tam = len(filenames)
	cdef int nlin = dissimilaridades0.shape[0]
	cdef int ncol = dissimilaridades0.shape[1]

	cdef np.ndarray[DTYPE_t, ndim=3] matrizes_c = np.zeros([tam,nlin,ncol], dtype=DTYPE)
#	cdef float matrizes_c[tam][nlin][ncol]

	cdef unsigned int nmatrix, i_lin, j_col, a, b
	cdef DTYPE_t valor

	#Lê mais de um arquivo sodas
	for nmatrix in range (len(filenames)):
		dissimilaridades, individuals_objects, classes_a_priori = leitor(filenames[nmatrix])
		dissimilaridades = np.array(dissimilaridades)
		a = <unsigned int> dissimilaridades.shape[0]
		b = <unsigned int> dissimilaridades.shape[1]
		for i_lin in range(a):
			for j_col in range(b):
				valor = dissimilaridades[i_lin][j_col]
				matrizes_c[nmatrix, i_lin, j_col] = valor

	return matrizes_c, text, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, individuals_objects, classes_a_priori

