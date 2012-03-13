#!/usr/bin/env python
# -*- coding: latin1 -*-

# som_diss_table_adap_sum.py
# Projeto de mestrado
# Autor: Anderson Berg

import sys
import random
from math import *
import numpy as np
from leitor_sodas import *
from indices import *
from datetime import *
import os.path
from util import *
import time
import config
from Point import *
from Individual import *
from Cluster import *
from Classe import *
from Variavel import *
from Mapa import *
import inicio

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects, nome_base, a):

    prototipos = []
    individuals = []

    individuals.extend(individuals_objects)

    mapa = Mapa(individuals,  mapa_x, mapa_y, q, nome_base, a)

    #valor de m
    mapa.m = 2.0

    # cria a matriz de pesos e array de distancias
    for cluster in mapa.mapa.flat:
        cluster.matriz_pesos(len(matrizes))
        for cluster2 in mapa.mapa.flat:
                cluster.deltas[cluster2.point] = delta(cluster.point, cluster2.point)

    # Etapa de afetação
    for objeto in mapa.objetos:
        criterios = [ (mapa.calcula_criterio_soma(objeto, denom, matrizes, cluster.point), cluster) for cluster in mapa.mapa.flat ]
        (menor_criterio, menor_criterio_cluster) = min(criterios)

        # Insere o objeto no cluster de menor critério
        mapa.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
        objeto.set_cluster(mapa.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])

    return mapa

# def calcula_criterio(obj, mapa, denom, matrizes, point1, m):

    # sum_1 = np.exp( -delta(point1, cluster.point)/denom ) * np.sum(np.array([ np.sum([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes] ) * (cluster.pesos**m) )

    # return sum_1

# Cálculo para seleção de melhor protótipo para cada cluster
# def calcula_prototipo(objeto_alvo, objetos, mapa, denom, matrizes, cluster, m):

    # sum_1 = np.sum([np.exp(-(cluster.deltas[obj.cluster.point]) / denom) * np.sum(np.array( [matriz[int(objeto_alvo.indice),int(obj.indice)] for matriz in matrizes ])  * (cluster.pesos**m) ) for obj in self.objetos])

    # return sum_1

# Seleciona o melhor protótipo para cada cluster
# def atualiza_prototipo(mapa, individuals, denom, matrizes, q, m):
    # for cluster in mapa.flat:
        # if len(cluster.objetos) > 0:

            # somas = [ (calcula_prototipo(obj, individuals, mapa, denom, matrizes, cluster, m), obj) for obj in individuals ]

            # #se q = 1
            # (menor_criterio, menor_criterio_obj) = min(somas)
            # novo_prototipo = Individual(menor_criterio_obj.indice, menor_criterio_obj.id2, menor_criterio_obj.nome)
            # cluster.prototipo = novo_prototipo

    # return mapa

# def delta(point1, point2):
    # dist = float(math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))
    # #dist = math.fabs(point1.x - point2.x) + math.fabs(point1.y - point2.y)
    # return dist

# def atualiza_pesos(objetos, mapa, denom, matrizes, m):

    # for cluster in mapa.flat:
        # for j in range (len(cluster.pesos)):

            # matriz_atual = matrizes[j]
            # numerador = np.sum( [ np.exp(-delta(objeto.cluster.point, cluster.point) / denom) * np.sum([matriz_atual[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos ]) for objeto in objetos ] )

            # soma = 0.0
            # for matriz in matrizes:
                # denominador = np.sum( [ np.exp(-delta(objeto.cluster.point, cluster.point) / denom) * np.sum([matriz[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos]) for objeto in objetos ] )
                # soma += pow((numerador / denominador), (1./(m-1.)))

            # cluster.pesos[j] = pow(soma, -1)

def main():

#   if len(sys.argv) != 2:
#       print 'usage: ./som_diss_table_adap.py configuration_file'
#       sys.exit(1)


    conf_file, nome_base = inicio.lerArquivoConfig()
    matrizes, text, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, individuals_objects, classes_a_priori = config.config(conf_file)
    filename_result, filename_individuos, resultado, file_individuos = inicio.criaArquivos(conf_file, nome_base, text, mapa_x, mapa_y, repeticoes, t_max, n_iter, "_somatorio")

    text = []
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
        denom = 2. * pow(T,2)
        mapa = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects, nome_base, a)

        while T > t_min:
        # while t < (n_iter - 1):
            #Step 1: computation of the best prototypes
            t += 1.0
            #print 't', t
            T = t_max * pow( (t_min / t_max), (t / (n_iter - 1.0)) )
            denom = 2. * pow(T,2)

            mapa.atualiza_prototipo(denom, matrizes, q, mapa.calcula_prototipo_soma)

            #Step 2: computation of the best weights
            mapa.atualiza_pesos_soma(denom, matrizes)

            #Step 3: definition of the best partition

            mapa.atualiza_particao(denom, matrizes, mapa.calcula_criterio_soma)

        no_clusters_completos = 0
        #Imprime os clusters finais
        text.extend(imprime_clusters(mapa))
        for cluster in mapa.mapa.flat:
            if len(cluster.objetos) > 0:
                no_clusters_completos += 1

        energia = mapa.calcula_energia_soma(matrizes, T)
        criterios_energia.append(energia)

        text.append("\n\nCritério de adequação (energia): " + str(energia))

        texto, oerc = calcula_indices(mapa, classes_a_priori, no_clusters_completos)
        oercs.append(oerc)
        text.extend(texto)

        resultado = open(filename_result, 'a')
        resultado.writelines(text)
        resultado.close()
        text = []

        list_individuos = []
        list_individuos.append("\n\n#####################################")
        list_individuos.append("\n# Repetição do experimento: " + str(a) + "\n")

        for ind in mapa.objetos:
                list_individuos.append(str(ind.nome) + "  " + str(ind.classe_a_priori.indice) + "  " + str(ind.cluster.indice) + "\n")

        file_individuos = open(filename_individuos, 'a')
        file_individuos.writelines(list_individuos)
        file_individuos.close()

    criterios_ordenados = sorted(criterios_energia)
    it = 0
#    while(criterios_ordenados[it] < 1.0):
#        it += 1

    menor_criterio_energia = criterios_ordenados[it]
    media_criterios = np.mean(criterios_energia)
    menor_erro = min(oercs)
    text.append("\n\nMelhor repetição: " + str(criterios_energia.index(menor_criterio_energia)))
    text.append("\nMenor oerc: " + str(oercs.index(menor_erro)))
    text.append("\nM�dia dos crit�rios: %s" % media_criterios)

    resultado = open(filename_result, 'a')
    resultado.writelines(text)
    resultado.close()

    print "Fim do experimento."

if __name__ == '__main__':
    main()

