#!/usr/bin/env python
# *-* coding: utf-8 *-*

from Point import *
import numpy as np

class Cluster:
	def __init__(self, _indice):
		self.indice = _indice
		self.prototipos = []
#		self.prototipo = _prototipo
		self.objetos = []
		self.pesos = []
		self.deltas = {}
	
	def definir_ponto(self, x, y):
		self.point = Point(x, y)
	
	def inserir_objeto(self, obj):
		self.objetos.append(obj)
		
	def remover_objeto(self, obj):
		if obj in self.objetos:
			self.objetos.remove(obj)

	def __eq__(self, other):
		if self.point.x == other.point.x and self.point.y == other.point.y and self.prototipo.nome == other.prototipo.nome:
			return True
		else:
			return False
			
	def __ne__(self, other):
		if self.prototipo.nome != other.prototipo.nome and self.point.x != other.point.x and self.point.y != other.point.y:
			return True
		else:
			return False

	def __hash__(self):
		return id(self)

	def matriz_pesos(self, tamanho):
		self.pesos = np.ones(tamanho)

