#!/usr/bin/env python
# *-* coding: utf-8 *-*

import numpy as np
from math import *
from Cluster import *
from Individual import *
from Point import *
from util import *
import pickle
import os.path

class Mapa:
    ''' Define a distribuição dos clusters no mapa '''
    def __init__(self, objetos, nlinhas, ncolunas, q, nome_base, a):
    
        self.m = 2.
        self.objetos = objetos

        nome_arquivo = 'mapa_%s_%d.dat' % (nome_base, a)
        if not os.path.exists(nome_arquivo):

            clusters = []
            c = nlinhas*ncolunas

            # Criando os clusters e determinando os protótipos
            for i in range(c):
                cluster = Cluster(i)
                for j in range(q):
                    prot = random.choice(objetos)
                    novo_prototipo = Individual(prot.indice, prot.id2, prot.nome)
                    if not novo_prototipo in cluster.prototipos:
                        cluster.prototipos.append(novo_prototipo)
                clusters.append(cluster)

            #Cria uma matriz numpy
            self.mapa = np.array(clusters)
            self.mapa.shape = (nlinhas, ncolunas)

            # Define as coordenadas dos clusters no mapa
            for i in range(nlinhas):
                for j in range(ncolunas):
                    self.mapa[i,j].definir_ponto(i,j)

            # Armazena o mapa em arquivo
            arquivo_mapa = nome_arquivo
            f = open(arquivo_mapa, 'wb')
            pickle.dump(self.mapa, f)
            f.close()

        else:
            f = open(nome_arquivo, 'rb')
            self.mapa = pickle.load(f)


    def calcula_criterio_adaptativo(self, obj, denom, matrizes, point1):
        '''Calcula critério para seleção de melhor cluster para um objeto'''
    
        soma = 0.

        for cluster in self.mapa.flat:
            exponencial = np.exp( np.divide(-delta(point1, cluster.point), denom) )

            somatorio_p = np.sum( [ np.sum([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes ] * cluster.pesos )

            soma += exponencial * somatorio_p
        return soma
        
    def calcula_criterio_batch(self, obj, denom, matrizes, point1):
        soma = 0.
        for cluster in self.mapa.flat:
            exponencial = np.exp( np.divide(-delta(point1, cluster.point), denom) )

            somatorio_p = np.sum( [ np.sum([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes ] )

            soma += exponencial * somatorio_p

        return soma
        
    def calcula_criterio_fuzzy(self, obj, denom, matrizes, point1):
        soma = 0.
        for cluster in self.mapa.flat:
            exponencial = np.exp( -delta(point1, cluster.point) / denom )

            somatorio_p = np.sum( [ np.sum([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes ] )

            soma += exponencial * pow(obj.pertinencias[cluster.indice], self.m) * somatorio_p

        return soma
        
    def calcula_criterio_soma(self, obj, denom, matrizes, point1):

        soma = np.sum([np.exp( -delta(point1, cluster.point)/denom ) * np.sum(np.array([ np.sum([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes] ) * (cluster.pesos**self.m) ) for cluster in self.mapa.flat])
        return soma
        
    def atualiza_particao(self, denom, matrizes, metodo):
        '''Atualiza a partição, afetando cada indivíduo ao cluster mais adequado'''
        #tic = time.time()
        for objeto in self.objetos:

            #calcula o critério de cada cluster para o objeto em questão
            criterios = [ (metodo(objeto, denom, matrizes, cluster.point), cluster) for cluster in self.mapa.flat ]
            (menor_criterio, menor_criterio_cluster) = min(criterios)

            if menor_criterio_cluster.point != objeto.cluster.point:
                #Insere o objeto no cluster de menor critério
                self.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y].inserir_objeto(objeto)
                self.mapa[objeto.cluster.point.x, objeto.cluster.point.y].remover_objeto(objeto)
                objeto.set_cluster(self.mapa[menor_criterio_cluster.point.x, menor_criterio_cluster.point.y])

        for cluster1 in self.mapa.flat:
            for cluster2 in self.mapa.flat:
                if cluster1.point < cluster2.point and cluster1.prototipos == cluster2.prototipos:
                    cluster1.objetos.extend(cluster2.objetos)
                    for obj in cluster2.objetos:
                        obj.cluster = cluster1
                    cluster2.objetos = []
        #toc = time.time()
        #print "atualiza particao time: ", toc - tic

    def calcula_prototipo_adaptativo(self, objeto_alvo, denom, matrizes, cluster):
        '''Cálculo para seleção do melhor protótipo de cada cluster'''

        sum_1 = np.sum([np.exp(-delta(obj.cluster.point, cluster.point) / denom) * np.sum(np.array( [matriz[int(objeto_alvo.indice),int(obj.indice)] for matriz in matrizes ])  * cluster.pesos ) for obj in self.objetos])
        
        return sum_1
            
    def calcula_prototipo_batch(self, objeto_alvo, denom, matrizes, cluster):
        sum_1 = np.sum([np.exp(-delta(obj.cluster.point, cluster.point) / denom) * np.sum(np.array( [matriz[int(objeto_alvo.indice), int(obj.indice)] for matriz in matrizes ] ) ) for obj in self.objetos])

        return sum_1
        
    def calcula_prototipo_fuzzy(self, objeto_alvo, denom, matrizes, cluster):
        sum_1 = np.sum([np.exp(-delta(obj.cluster.point, cluster.point) / denom) * pow(obj.pertinencias[cluster.indice], self.m) * np.sum(np.array( [matriz[int(objeto_alvo.indice), int(obj.indice)] for matriz in matrizes ] ) ) for obj in self.objetos])

        return sum_1
        
    def calcula_prototipo_soma(self, objeto_alvo, denom, matrizes, cluster):

        sum_1 = np.sum([np.exp(-delta(obj.cluster.point, cluster.point) / denom) * np.sum(np.array( [matriz[int(objeto_alvo.indice),int(obj.indice)] for matriz in matrizes ])  * (cluster.pesos**self.m) ) for obj in self.objetos])
					
        return sum_1


    def atualiza_prototipo(self, denom, matrizes, q, metodo):
        '''Seleciona os melhores protótipo para cada cluster'''
        #tic = time.time()
        prototipos = []
        for cluster in self.mapa.flat:
            if len(cluster.objetos) > 0:
                cluster.prototipos = []
                somas1 = [ (metodo(obj, denom, matrizes, cluster), obj) for obj in self.objetos]
                somas = [ (criterio,objeto) for (criterio,objeto) in somas1 if objeto not in prototipos]
            
                somas = sorted(somas)
            
               #(menor_criterio, menor_criterio_obj) = min(somas)
                for i in range(q):
                    (menor_criterio, menor_criterio_obj) = somas[i]
                    novo_prototipo = Individual(menor_criterio_obj.indice, menor_criterio_obj.id2, menor_criterio_obj.nome)
                    cluster.prototipos.append(novo_prototipo)
                    prototipos.append(menor_criterio_obj)
                
        #toc = time.time()
        #print "atualiza prototipo time: ", toc - tic

    def atualiza_pesos(self, denom, matrizes):
        ''' Atualiza matriz de pesos '''
        #tic = time.time()
        for cluster in self.mapa.flat:
            for i in range (len(cluster.pesos)):
                produto = 1.0
                for matriz in matrizes:
                    soma = np.sum( [ exp(-delta(objeto.cluster.point, cluster.point) / denom) * np.sum([matriz[int(objeto.indice)][int(prototipo.indice)] for prototipo in cluster.prototipos ] ) for objeto in self.objetos] )
                    produto = produto * soma

                matriz_atual = matrizes[i]
                denominador = np.sum( [ exp(-delta(objeto.cluster.point, cluster.point) / denom) * np.sum([matriz_atual[int(objeto.indice)][int(prototipo.indice)] for prototipo in cluster.prototipos ]) for objeto in self.objetos ] )
                cluster.pesos[i] = pow(produto, 1./len(matrizes)) / denominador

        #toc = time.time()
        #print "atualiza pesos time: ", toc - tic

    def calcula_energia_adaptativo(self, matrizes, T):
        '''Calcula critério de adequação'''
        denom = (2. * pow(T,2))
        energia = np.sum([ np.exp(-delta(obj.cluster.point, cluster.point) / denom) * np.sum(np.array( [np.sum ([matriz[int(obj.indice),int(prototipo.indice)] for prototipo in cluster.prototipos ] ) for matriz in matrizes] ) * cluster.pesos) for cluster in self.mapa.flat for obj in self.objetos])
        
        return energia
        
    def calcula_energia_batch(self, matrizes, T):
        denom = (2. * pow(T,2))
        energia = np.sum([ np.exp(-delta(obj.cluster.point, cluster.point) / denom) * np.sum(np.array( [np.sum ([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos ] ) for matriz in matrizes])) for cluster in self.mapa.flat for obj in self.objetos ])

        return energia
        
    def calcula_energia_fuzzy(self, matrizes, T):
        denom = (2. * pow(T,2))
        energia = np.sum([ np.exp(-delta(obj.cluster.point, cluster.point) / denom) * pow(obj.pertinencias[cluster.indice], self.m) * np.sum(np.array( [np.sum ([matriz[int(obj.indice), int(prototipo.indice)] for prototipo in cluster.prototipos ] ) for matriz in matrizes])) for cluster in self.mapa.flat for obj in self.objetos ])

        return energia
        
    def calcula_energia_soma(self, matrizes, T):
	
        denom = (2. * pow(T,2))
        energia = np.sum([ np.exp(-delta(obj.cluster.point, cluster.point) / denom) * np.sum(np.array( [np.sum ([matriz[int(obj.indice),int(prototipo.indice)] for prototipo in cluster.prototipos ] ) for matriz in matrizes] ) * (cluster.pesos**self.m)) for cluster in self.mapa.flat for obj in self.objetos])

        return energia

    def atualiza_pesos_global(self, denom, matrizes):
        #tic = time.time()
        pesos = []
        for j in range(len(matrizes)):
            produto = 1.0
            for matriz in matrizes:
                soma1 = np.sum([np.sum( [np.exp(-(delta(objeto.cluster.point, cluster.point)) / denom) * np.sum([matriz[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos]) for objeto in self.objetos]) for cluster in self.mapa.flat])
                produto = produto * soma1

            matriz_atual = matrizes[j]

            denominador = np.sum([np.sum([np.exp(-(delta(objeto2.cluster.point, cluster2.point)) / denom) * np.sum([matriz_atual[int(objeto2.indice),int(prototipo2.indice)] for prototipo2 in cluster2.prototipos]) for objeto2 in self.objetos]) for cluster2 in self.mapa.flat])                 
            
            pesos.append(pow(produto, 1./len(matrizes)) / denominador)
                
        #toc = time.time()
        #print "atualiza pesos time: ", toc - tic
        return np.array(pesos)
        
        
    def atualiza_pesos_soma_global(self, denom, matrizes):

        pesos = []
        for j in range(len(matrizes)):
            matriz_atual = matrizes[j]
            numerador = np.sum([np.sum([np.exp(-(delta(objeto2.cluster.point, cluster2.point)) / denom) * np.sum([matriz_atual[int(objeto2.indice),int(prototipo2.indice)] for prototipo2 in cluster2.prototipos]) for objeto2 in self.objetos]) for cluster2 in self.mapa.flat])

            soma = 0.0
            for matriz in matrizes:
                denominador = np.sum([np.sum( [np.exp(-(delta(objeto.cluster.point, cluster.point)) / denom) * np.sum([matriz[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos]) for objeto in self.objetos]) for cluster in self.mapa.flat])
                soma += pow((numerador / denominador), (1./(self.m-1.)))

            
            pesos.append(pow(soma, -1.))
            
        return np.array(pesos)
       
    def atualiza_pesos_soma(self, denom, matrizes):

        for cluster in self.mapa.flat:
            for j in range (len(cluster.pesos)):
                
                matriz_atual = matrizes[j]
                numerador = np.sum( [ np.exp(-delta(objeto.cluster.point, cluster.point) / denom) * np.sum([matriz_atual[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos ]) for objeto in self.objetos ] )

                soma = 0.0
                for matriz in matrizes:
                    denominador = np.sum( [ np.exp(-delta(objeto.cluster.point, cluster.point) / denom) * np.sum([matriz[int(objeto.indice),int(prototipo.indice)] for prototipo in cluster.prototipos]) for objeto in self.objetos ] )
                    soma += pow((numerador / denominador), (1./(self.m-1.)))

                cluster.pesos[j] = pow(soma, -1)
                
                
                
    def atualiza_pertinencias(self, denom, matrizes):

        fator = 1/(self.m-1)
        flag = True
        for objeto in self.objetos:
            for cluster in self.mapa.flat:
                # Verifica se o objeto é protótipo do cluster
                prototipos = [p.nome for p in cluster.prototipos]
                if objeto.nome in prototipos:
                    objeto.pertinencias[::] = 0.
                    objeto.pertinencias[cluster.indice] = 1.
                    break
                else:        
                    soma = 0.
                    numerador = np.exp(-delta(cluster.point, objeto.cluster.point) / denom) * np.sum([np.sum([matriz[int(objeto.indice)][int(prototipo.indice)] for prototipo in cluster.prototipos]) for matriz in matrizes])
                    # if flag:
                        # print
                        # print "objeto: ", objeto.nome
                        #print "numerador: ", numerador

                    for cluster2 in self.mapa.flat:
                        # Verifica se o objeto é protótipo do cluster
                        prototipos2 = [p.nome for p in cluster2.prototipos]
                        if objeto.nome in prototipos2:
                            objeto.pertinencias[::] = 0.
                            objeto.pertinencias[cluster2.indice] = 1.
                            break
                                
                        else:
                            exponen2 = np.exp(-delta(cluster2.point, objeto.cluster.point) / denom)
                            soma2 = np.sum([np.sum([matriz[int(objeto.indice)][int(prototipo2.indice)] for prototipo2 in cluster2.prototipos]) for matriz in matrizes])
                            denominador = exponen2 * soma2
                            soma += pow(numerador/denominador, fator)
                            # if flag:
                                # print "cluster > ", cluster2.point.x, cluster2.point.y
                                # print "cluster objeto > ", objeto.cluster.point.x, objeto.cluster.point.y 
                                # print "delta > ", -delta(cluster2.point, objeto.cluster.point) 
                                # print "exponen2 > ", exponen2
                                # print "soma2 > ", soma2
                                # print "denominador > ", denominador
                                # print "soma: ", soma
                    # flag = False
                    objeto.pertinencias[cluster.indice] = 1./soma
                
