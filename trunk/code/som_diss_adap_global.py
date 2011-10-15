#!/usr/bin/env python
# -*- coding: latin1 -*-

# som_diss_adap_global.py
# Projeto de mestrado
# Autor: Anderson Berg

import re
import sys
import random
from math import *
import numpy as np
import pdb
from operator import itemgetter, attrgetter
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

def inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects, pesos):

        prototipos = {}
#       clusters = []
        individuals = []
        
        individuals.extend(individuals_objects)
        
        mapa = Mapa(individuals, mapa_x, mapa_y, q)

        # cria a matriz de deltas
        for cluster in mapa.mapa.flat:
                cluster.pesos = pesos
                for cluster2 in mapa.mapa.flat:
                        cluster.deltas[cluster2.point] = delta(cluster.point, cluster2.point)

        # Etapa de afetação           
        for objeto in mapa.objetos:
                criterios = [ (mapa.calcula_criterio_adaptativo(objeto, denom, matrizes, cluster.point), cluster) for cluster in mapa.mapa.flat ]
                (menor_criterio, menor_criterio_cluster) = min(criterios)
                
                # Insere o objeto no cluster de menor critério
                mapa.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
                objeto.set_cluster(mapa.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])
                        
        return mapa

# def atualiza_pesos(mapa, denom, matrizes):
# #     tic = time.time()
        # pesos = []
        # for j in range(len(matrizes)):
                # produto = 1.0
                # for matriz in matrizes:
                        
                        # soma1 = np.sum([np.sum( [np.exp(-(delta(objeto.cluster.point, cluster.point)) / denom) * np.sum([matriz[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos]) for objeto in mapa.objetos]) for cluster in mapa.mapa.flat])
                        # produto = produto * soma1

                # matriz_atual = matrizes[j]

                # denominador = np.sum([np.sum([np.exp(-(delta(objeto2.cluster.point, cluster2.point)) / denom) * np.sum([matriz_atual[int(objeto2.indice),int(prototipo2.indice)] for prototipo2 in cluster2.prototipos]) for objeto2 in mapa.objetos]) for cluster2 in mapa.mapa.flat])                       
                
                # pesos.append(pow(produto, 1./len(matrizes)) / denominador)
                
# #     toc = time.time()
# #     print "atualiza pesos time: ", toc - tic

#       return np.array(pesos)
        
#def calcula_energia(mapa, objetos, matrizes, T, pesos):
        
#       denom = (2. * pow(T,2))
#       energia = sum([ exp(-delta(obj.cluster.point, cluster.point) / denom) * sum(np.array( [matriz[int(obj.indice),int(cluster.prototipo.indice)] for matriz in matrizes] ) * pesos) for cluster in mapa.flat for obj in objetos])

#       return energia

def main():

        conf_file, nome_base = inicio.lerArquivoConfig()
        matrizes, text, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, individuals_objects, classes_a_priori = config.config(conf_file)
        filename_result, filename_individuos, resultado, file_individuos = inicio.criaArquivos(conf_file, nome_base, text, mapa_x, mapa_y, repeticoes, t_max, n_iter, "_adaptativo_global")

        text = []
        text.append("\n*Modelo adaptativo")
        criterios_energia = []
        oercs = []

        c = mapa_x * mapa_y

        for a in range(repeticoes):

                #Etapa de inicialização

                text.append("\n\n#####################################")
                text.append("\n# Repetição do experimento: " + str(a) + "\n")
        
                print "Repetição ", a
                print "..."

                #Inicialização
                T = t_max
                t = 0.0

                # cria a matriz de pesos
                pesos = np.ones(len(matrizes))

#               text.append("\nVetor de pesos inicial\n")
#               text.extend([ str(peso) for peso in pesos ])

                denom = 2. * pow(T,2)
                mapa = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects, pesos)   
        
                while T > t_min:
                # while t < (n_iter - 1):
                        #Step 1: computation of the best prototypes
                        t += 1.0
                        print 'Iteração', t
                        T = t_max * pow( (t_min / t_max), (t / (n_iter - 1.0)) )
                        denom = 2. * pow(T,2)

                        mapa.atualiza_prototipo(denom, matrizes, q, mapa.calcula_prototipo_adaptativo)

                        #Step 2: computation of the best weights
                        pesos = mapa.atualiza_pesos_global(denom, matrizes)
                        for cluster in mapa.mapa.flat:
                                cluster.pesos = pesos
                                
                        #Step 3: definition of the best partition
                        
                        mapa.atualiza_particao(denom, matrizes, mapa.calcula_criterio_adaptativo)

                #Imprime os clusters finais             
                text.extend(imprime_clusters(mapa))

                no_clusters_completos = 0
                for cluster in mapa.mapa.flat:
                        if len(cluster.objetos) > 0:
                                no_clusters_completos += 1
                        
                energia = mapa.calcula_energia_adaptativo(matrizes, T)
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
        while(criterios_ordenados[it] < 1.0):
                it += 1

        #menor_criterio_energia = min(criterios_energia)
        menor_criterio_energia = criterios_ordenados[it]
        menor_erro = min(oercs)
        text.append("\n\nMelhor repetição: " + str(criterios_energia.index(menor_criterio_energia)))
        text.append("\nMenor oerc: " + str(oercs.index(menor_erro)))

        resultado = open(filename_result, 'a')
        resultado.writelines(text)      
        resultado.close()

        print "Fim do experimento."

if __name__ == '__main__':
        main()
