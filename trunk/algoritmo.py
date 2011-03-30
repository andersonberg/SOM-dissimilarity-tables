import sys
from numpy import *

def inicializacao(c, q, n_iter, t_min, t_max, matrizes):
	t = 0
	prototipos = array( random.sample(matrizes, c) )
	
	
	
def main():
	args = sys.argv[1:]
	
	if not args:
		print 'usage: files'
		sys.exit(1)
		
	for filename in args: