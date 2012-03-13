#!/usr/bin/env python
# *-* coding: utf-8 *-*

import numpy
import random

class Individual:
    def __init__(self, _indice, _id2, _nome):
        self.indice = _indice
        self.id2 = _id2
        self.nome = _nome
        
        # Determina o melhor neurônio        
    def set_cluster(self, cluster):
        self.cluster = cluster

    def set_classe_a_priori(self, classe):
        self.classe_a_priori = classe

    def set_pertinencias(self, tamanho):
        r = 1.
        self.pertinencias = numpy.array([])
        for i in range(tamanho):

                        if i == tamanho-1:
                                self.pertinencias = numpy.append(self.pertinencias, 1.-r)
                                
                        else:
                                p = random.uniform(0,r)
                                self.pertinencias = numpy.append(self.pertinencias,p)
                                r = float(r - p)
    
    # Determina o segundo melhor neurônio
    def set_segundo(self, cluster):
        self.segundo = cluster
