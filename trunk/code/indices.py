#!/usr/bin/env python
# -*- coding: latin1 -*-

# indices.py
# Projeto de mestrado
# Autor: Anderson Berg

import sys
from math import *
import numpy as np

# calcula binomial (n 2)
def combinacao(n):
	resultado = (n * (n - 1.)) / 2.
	return resultado

#Calcula a matrix de confusão
def calcula_confusion_matrix(mapa, classes_a_priori, no_clusters_completos):

	confusion_matrix = np.zeros( (len(classes_a_priori),no_clusters_completos), dtype=np.int32 )
	i = 0
	for classe in classes_a_priori.values():
		j = 0
		for cluster in mapa.mapa.flat:
			if len(cluster.objetos) > 0:
				for obj in cluster.objetos:
					if obj in classe.objetos:
						confusion_matrix[i,j] += 1
				j += 1
		i += 1

	return confusion_matrix

# Cálculo do índice de Rand Corrigido #
def calcula_cr(confusion_matrix, len_classes_a_priori, no_clusters_completos, no_objetos):
	# Cálculo do numerador
	x = 1.0 / combinacao(no_objetos)
	somaMK = sum([ combinacao(confusion_matrix[i,j]) for i in range(len_classes_a_priori) for j in range(no_clusters_completos) ])
	somaMK = somaMK - x
	soma2 = sum( [ combinacao(confusion_matrix[i,:].sum()) for i in range(len_classes_a_priori) ] )
	soma3 = sum( [ combinacao(confusion_matrix[:,j].sum()) for j in range(no_clusters_completos) ] )

	# Cálculo do denominador
	fator1 = ( ( (0.5) * (soma2 + soma3) ) - x)

	cr = (somaMK * soma2 * soma3) / (fator1 * soma2 * soma3)

	return cr
	
# Cálculo da precisão #
def calcula_precisao(confusion_matrix, len_classes_a_priori, no_clusters_completos):
	
	precisao_matrix = [ float(confusion_matrix[i,j]) / float(confusion_matrix[:,j].sum()) for i in range(len_classes_a_priori) for j in range(no_clusters_completos)]
	precisao_matrix = np.array(precisao_matrix).reshape(len_classes_a_priori,no_clusters_completos)

	return precisao_matrix

# Cálculo do recall #
def calcula_recall(confusion_matrix, len_classes_a_priori, no_clusters_completos):

	recall_matrix = [ float(confusion_matrix[i,j]) / float(confusion_matrix[i,:].sum()) for i in range(len_classes_a_priori) for j in range(no_clusters_completos) ]
	recall_matrix = np.array(recall_matrix).reshape(len_classes_a_priori,no_clusters_completos)

	return recall_matrix

# Cálculo do F-measure #
def calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, len_clusters_comp):

	f_measure_matrix = [ 2. * ( (precisao_matrix[i,j]*recall_matrix[i,j]) /  (precisao_matrix[i,j]+recall_matrix[i,j]) ) if precisao_matrix[i,j]+recall_matrix[i,j] != 0 else -1.0 for i in range(len_cls_priori) for j in range(len_clusters_comp) ]
	f_measure_matrix = np.array(f_measure_matrix).reshape(len_cls_priori, len_clusters_comp)

	return f_measure_matrix

# Cálculo do oerc (erro global) #
def calcula_oerc(confusion_matrix, len_clusters_comp, len_objetos):

	sumJ = sum([ confusion_matrix[:,j].max() for j in range(len_clusters_comp) ])
	resultado = 1. - (float(sumJ) / float(len_objetos))

	return resultado
