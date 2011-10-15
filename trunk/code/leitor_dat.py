# *-* coding: utf-8 *-*

import re
import sys
import random
import math
import numpy as np
import pdb
from operator import itemgetter, attrgetter

def leitor(filename):
    f = open(filename, 'rU')
    #text = f.read()
    matriz = []
    for line in f.readlines():
        atributos = line.split(' ')
        frequencies = atributos[0:len(atributos)-1]
        categoria = atributos[len(atributos)-1]

        attr_org = []
        attr_org.append(int(categoria))
        attr_org.extend([float(freq) for freq in frequencies])

        matriz.append(attr_org)

    np_matriz = np.array(matriz)
    f.close()

    return np_matriz

def velocidade(matriz):

	#definindo a matriz de velocidades (velocidade(j) = matriz[i,j] - matriz[i,j-1] / j - (j-1))
    velocidades = []
    for vetor in matriz:
        velocidades.append(vetor[0])
        for j in range(2,len(vetor)):
            velo = (vetor[j] - vetor[j-1])
            velocidades.append(velo)

    (x,y) = matriz.shape
    
    np_velocidades = np.array(velocidades).reshape(x,y-1)
	
    return np_velocidades

def aceleracao(velocidades):

    aceleracao = []
    for vetor in velocidades:
        aceleracao.append(vetor[0])
        for j in range(2, len(vetor)):
            acel = vetor[j] - vetor[j-1]
            aceleracao.append(acel)
			
    (x,y) = velocidades.shape
    np_aceleracao = np.array(aceleracao).reshape(x,y-1)
	
    return np_aceleracao
	
def main():
#    base_dados = raw_input("Digite o caminho da base de dados: ")
    base_dados = sys.argv[1]
    np_matriz = leitor(base_dados)
    np_velocidades = velocidade(np_matriz)
    np_aceleracao = aceleracao(np_velocidades)

    txt_matriz = []
    for vetor in np_matriz:
        for n in vetor:
            txt_matriz.append(str(n) + " ")
        txt_matriz.append("\n")

    txt_velocidades = []
    for vetor in np_velocidades:
        for n in vetor:
            txt_velocidades.append(str(n) + " ")
        txt_velocidades.append("\n")

    txt_aceleracao = []
    for vetor in np_aceleracao:
        for n in vetor:
            txt_aceleracao.append(str(n) + " ")
        txt_aceleracao.append("\n")


    filename_matriz = "matriz-original.dat"
    filename_velocidades = "matriz-velocidades.dat"
    filename_aceleracao = "matriz-aceleracao.dat"

    file_mat = open(filename_matriz, 'w')
    file_mat.writelines(txt_matriz)
    file_mat.close()

    file_veloc = open(filename_velocidades, 'w')
    file_veloc.writelines(txt_velocidades)
    file_veloc.close()

    file_acel = open(filename_aceleracao, 'w')
    file_acel.writelines(txt_aceleracao)
    file_acel.close()

if __name__ == '__main__':
    main()

