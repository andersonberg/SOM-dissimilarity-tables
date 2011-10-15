#!/usr/bin/env python
# -*- coding: latin1 -*-

# som_fuzz.py
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
from Mapa import *
from leitor_sodas import *
from indices import *
from datetime import *
import os.path
from util import *
import config
import inicio

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects):

    prototipos = []
    individuals = []
    
    individuals.extend(individuals_objects)
    
    mapa = Mapa(individuals, mapa_x, mapa_y, q)

    for cluster in mapa.mapa.flat:
        for cluster2 in mapa.mapa.flat:
                cluster.deltas[cluster2.point] = delta(cluster.point, cluster2.point)

    for obj in mapa.objetos:
        obj.set_pertinencias(mapa_x*mapa_y)
    
    # Etapa de afetação             
    for objeto in mapa.objetos:
        criterios = [ (mapa.calcula_criterio_fuzzy(objeto, denom, matrizes, cluster.point), cluster) for cluster in mapa.mapa.flat ]
        (menor_criterio, menor_criterio_cluster) = min(criterios)

        # Insere o objeto no cluster de menor critério
        mapa.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
        objeto.set_cluster(mapa.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
                    
    return mapa
        
        
def main():

    conf_file, nome_base = inicio.lerArquivoConfig()
    matrizes, text, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, individuals_objects, classes_a_priori = config.config(conf_file)
    filename_result, filename_individuos, resultado, file_individuos = inicio.criaArquivos(conf_file, nome_base, text, mapa_x, mapa_y, repeticoes, t_max, n_iter, "_fuzzy")

    text = []

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
        mapa = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects)

        #Iterações
        while T > t_min:
        # while t < (n_iter - 1):
            #Step 1: computation of the best prototypes
            t += 1.0
            T = t_max * math.pow( (t_min / t_max), (t / (n_iter - 1.0)) )
            denom = 2. * math.pow(T,2)
            
            mapa.atualiza_prototipo(denom, matrizes, q, mapa.calcula_prototipo_fuzzy)
                    
            #Step 2: definition of the best fuzzy partition

            mapa.atualiza_pertinencias(denom, matrizes)

            #Step 3: definition of the best partition
            mapa.atualiza_particao(denom, matrizes, mapa.calcula_criterio_fuzzy)

        no_clusters_completos = 0

        #Imprime os clusters finais             
        text.extend(imprime_clusters(mapa))

        no_clusters_completos = 0
        for cluster in mapa.mapa.flat:
            if len(cluster.objetos) > 0:
                    no_clusters_completos += 1

        energia = mapa.calcula_energia_fuzzy(matrizes, T)
        criterios_energia.append(energia)

        text.append("\n\nCritério de adequação (energia): " + str(energia))

        text.extend(imprime_pertinencias(mapa))

        texto, oerc = calcula_indices(mapa, classes_a_priori, no_clusters_completos, adap=False)
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

    menor_criterio_energia = min(criterios_energia)
    menor_erro = min(oercs)
    text.append("\n\nMelhor repetição: " + str(criterios_energia.index(menor_criterio_energia)))
    text.append("\nMenor oerc: " + str(oercs.index(menor_erro)))

    resultado = open(filename_result, 'a')
    resultado.writelines(text)      
    resultado.close()

    print "Fim do experimento."


# def calcula_criterio(mapa, obj, denom, matrizes, point1, m):
    # '''Calcula critério para seleção de melhor cluster para um objeto'''

    # soma = 0.
    # for cluster in mapa.mapa.flat:
        # exponencial = np.exp( -delta(point1, cluster.point)/ denom )

        # somatorio_p = pow(obj.pertinencias[cluster.indice], m) * np.sum([ np.sum([ matrizes[j, int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos ]) for j in range(len(matrizes))])

        # soma += exponencial * somatorio_p

    # return soma

# def calcula_prototipo(mapa, objeto_alvo, denom, matrizes, cluster, m):
    # '''Cálculo para seleção do melhor protótipo de cada cluster'''
            
    # soma = np.sum([np.exp(-delta(cluster.point, obj.cluster.point) / denom) * pow(obj.pertinencias[cluster.indice], m) * np.sum([matriz[int(objeto_alvo.indice), int(obj.indice)] for matriz in matrizes]) for obj in mapa.objetos])

    # return soma

# def atualiza_pertinencias(mapa, denom, matrizes, m):

    # fator = 1/(m-1)
    # for objeto in mapa.objetos:
        # for cluster in mapa.mapa.flat:
            # prototipos = [p.nome for p in cluster.prototipos]
            # if objeto.nome in prototipos:
                # objeto.pertinencias[::] = 0.
                # objeto.pertinencias[cluster.indice] = 1.
                # break
            # else:        
                # soma = 0.
                # numerador = np.exp(-delta(cluster.point, objeto.cluster.point) / denom) * np.sum([np.sum([matriz[int(objeto.indice)][int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes])

                # for cluster2 in mapa.mapa.flat:
                    # prototipos2 = [p.nome for p in cluster2.prototipos]
                    # if objeto.nome in prototipos2:
                        # objeto.pertinencias[::] = 0.
                        # objeto.pertinencias[cluster2.indice] = 1.
                        # break
                            
                    # else:
                        # exponen2 = np.exp(-delta(cluster2.point, objeto.cluster.point) / denom)
                        # soma2 = np.sum([np.sum([matriz[int(objeto.indice)][int(prototipo2.indice)] for prototipo2 in cluster2.prototipos]) for matriz in matrizes])
                        # denominador = exponen2 * soma2
                        # soma += pow(numerador/denominador, fator)

                # objeto.pertinencias[cluster.indice] = 1./soma


# def calcula_energia(mapa, matrizes, T):
    # '''Calcula critério de adequação'''
    # denom = (2. * pow(T,2))
    # energia = np.sum([np.exp(-delta(obj.cluster.point, cluster.point) / denom) * obj.pertinencias[cluster.indice] * np.sum( [matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos for matriz in matrizes ]  ) for cluster in mapa.mapa.flat for obj in mapa.objetos])
    # return energia


if __name__ == '__main__':
    main()
