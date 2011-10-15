#!/usr/bin/env python
# *-* coding: utf-8 *-*

class Classe:
	def __init__(self, _id, _desc):
		self.indice = _id
		self.desc = _desc
		self.objetos = []

	def inserir_objeto(self, obj):
		self.objetos.append(obj)
