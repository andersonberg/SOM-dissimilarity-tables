#!/usr/bin/env python
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
		if self.x != other.x or self.y != other.y:
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
