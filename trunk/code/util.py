#!/usr/bin/env python
# -*- coding: latin1 -*-

# util.py
# Projeto de mestrado
# Autor: Anderson Berg

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
import indices
from datetime import *
import os.path

def delta(point1, point2):
    dist = float(math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))
    #dist = math.fabs(point1.x - point2.x) + math.fabs(point1.y - point2.y)
    return dist

def setup():
    text = []

    #Lê arquivo de configuração
#       conf_file = sys.argv[1]
    conf_file = raw_input("Enter the path of the configuration file: ")
    nome_base = raw_input("Enter the name of the database: ")
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

#       text.append("--Parâmetros iniciais--\n")
    text.append("\n# Topology: " + str(mapa_x) + "x" + str(mapa_y))
    text.append("\n# Cardinality (q): " + str(q))
    text.append("\n# Tmin: " + str(t_min) + "\n# Tmax: " + str(t_max))
    text.append("\n# Number of iterations: " + str(n_iter))

    matrizes = []
    #Lê mais de um arquivo sodas
    for filename in filenames:
        dissimilaridades, individuals_objects, classes_a_priori = leitor(filename)
        dissimilaridades = np.array(dissimilaridades, dtype=np.float32)
        matrizes.append(dissimilaridades)

    matrizes = np.array(matrizes)

    return matrizes, text, nome_base, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, individuals_objects, classes_a_priori


def imprime_matriz_confusao(confusion_matrix, mapa, classes_a_priori, no_clusters_completos):
    text = []
    text.append("\n=====================================")
    text.append("\n\tConfusion Matrix")
    text.append("\nClasses\t\t\t Clusters")
    text.append("\n---------------------------------------\n")
    text.append("\t")
    for cluster in mapa.mapa.flat:
        if len(cluster.objetos) > 0:
            text.append("%s,%s\t" % (str(cluster.point.x), str(cluster.point.y)) )
    text.append( "Total")
    text.append( "\n")
    i = 0
    for classe in classes_a_priori.values():        
        text.append("\n%s\t" % str(classe.indice) )
        for j in range(no_clusters_completos):
            text.append("%s\t " % str(confusion_matrix[i,j]))
        text.append(str(confusion_matrix[i,:].sum(axis=0)))
        i+=1
    
    text.append("\nTotal\t" + str(confusion_matrix.sum(axis=0)))

    return text
    
def imprime_clusters(mapa):
    text = []
    text.append("\n----------Partition----------")
    for cluster in mapa.mapa.flat:
        text.append("\nCluster (%s,%s)" % ( str(cluster.point.x),str(cluster.point.y) ) )
        text.append("\nPrototypes: [" )
        for prototipo in cluster.prototipos:
            text.append( "%s, " % str(prototipo.nome))
        text[-1] = text[-1][:-2]
        text.append("]")
        text.append("\nNumber of elements: %s" % str(len(cluster.objetos)))
        text.append("\nElements: ")
        for objeto in cluster.objetos:
            text.append("%s, " % str(objeto.nome))
        text[-1] = text[-1][:-2]

        text.append("\n")

    return text

def imprime_matriz_pesos(mapa):
    '''Imprime a matriz de pesos'''
    text = []
    text.append("\n\nMatriz de pesos:")
    for cluster in mapa.mapa.flat:
        lista_pesos_str = [str(peso) for peso in cluster.pesos ]
        text.append("\nCluster (%s,%s):" % (str(cluster.point.x) , str(cluster.point.y) ) )
        for peso in lista_pesos_str:
            text.append(" %s" % peso)
    
    return text

def imprime_pertinencias(mapa):
    '''Imprime a lista de pertinências de cada objeto'''
    text = []
    text.append("\n\nPertinências:")
    for obj in mapa.objetos:
        lista_pert = [str(pert) for pert in obj.pertinencias]
        text.append("\nObjeto %s: " % obj.nome)
        for pert in lista_pert:
            text.append("%s " % pert)
        text.append(" %s" % str(np.sum(obj.pertinencias)))
                            
    return text
        
def calcula_indices(mapa, classes_a_priori, no_clusters_completos, adap=True):
    text = []
    ########################################
    #Calcula a matrix de confusão #
    confusion_matrix = indices.calcula_confusion_matrix(mapa, classes_a_priori, no_clusters_completos)
    text.extend(imprime_matriz_confusao(confusion_matrix, mapa, classes_a_priori, no_clusters_completos))

    if adap:
        #Imprime a matriz de pesos
        text.extend(imprime_matriz_pesos(mapa))

    ##########################################################################################
    # Cálculo do índice de Rand Corrigido #
    no_objetos = len(mapa.objetos)
    
    cr = indices.calcula_cr(confusion_matrix, len(classes_a_priori), no_clusters_completos, len(mapa.objetos))     
    text.append("\n\nCorrected Rand index: " + str(cr))

    ##########################################################
    # Cálculo da precisão #
    precisao_matrix = indices.calcula_precisao(confusion_matrix, len(classes_a_priori), no_clusters_completos)

    ###########################################################
    # Cálculo do recall #
    recall_matrix = indices.calcula_recall(confusion_matrix, len(classes_a_priori), no_clusters_completos)

    ###########################################################
    # Cálculo do f_measure #

    len_cls_priori = len(classes_a_priori)
    f_measure_matrix = indices.calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, no_clusters_completos)
    soma2 = sum( [ confusion_matrix[i,:].sum() * f_measure_matrix[i,:].max() for i in range(len(classes_a_priori)) ] )
    f_measure = float(soma2 / no_objetos)
    text.append("\nF-measure(P,Q): " + str(f_measure))

    ###########################################################
    # Cálculo do oerc (taxa de erro de classificação global) #
    oerc = indices.calcula_oerc(confusion_matrix, no_clusters_completos, no_objetos)

    text.append("\nOERC: " + str(oerc))
    
    ###########################################################
    # C�lculo do erro topogr�fico
    erro_topografico = indices.calcula_topographic_error(mapa)
    text.append("\nErro Topogr�fico: %s" % erro_topografico)

    return text, oerc