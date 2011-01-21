# *-* coding: utf-8 *-*

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __lt__(self, other):
		if self.x < other.x:
			return True
		elif self.x == other.x:
			if self.y < other.y:
				return True
			else:
				return False
		else:
			return False
			
	def __le__(self, other):
		if self < other or self == other:
			return True
		else:
			return False
			
	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False
			
	def __ne__(self, other):
		if self.x != other.x and self.y != other.y:
			return True
		else:
			return False
			
	def __gt__(self, other):
		if self.x > other.x:
			return True
		elif self.x == other.x:
			if self.y > other.y:
				return True
			else:
				return False
		else:
			return False
			
	def __ge__(self, other):
		if self > other or self == other:
			return True
		else:
			return False
			
	def __hash__(self):
		return id(self)

class Individual:
	def __init__(self, _id, _id2, _nome):
		self.id = _id
		self.id2 = _id2
		self.nome = _nome
		
	def set_cluster(self, cluster):
		self.cluster = cluster

	def set_classe_a_priori(self, classe):
		self.classe_a_priori = classe

class Cluster:
	def __init__(self, prototipo):
		self.prototipo = prototipo
		self.objetos = []
	
	def definir_ponto(self, x, y):
		self.point = Point(x, y)
	
	def inserir_objeto(self, obj):
		self.objetos.append(obj)
		
	def remover_objeto(self, obj):
		if obj in self.objetos:
			self.objetos.remove(obj)

class Classe:
	def __init__(self, _id, _desc):
		self.id = _id
		self.desc = _desc
		self.objetos = []

	def inserir_objeto(self, obj):
		self.objetos.append(obj)

class Variavel:
	def __init__(self, _id, _tipo):
		self.id = _id
		self.tipo = _tipo
	
	def classe(self, classes):
		self.classes = classes

