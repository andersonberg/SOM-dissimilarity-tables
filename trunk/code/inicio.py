#!/usr/bin/env python
# -*- coding: latin1 -*-

# inicio.py
# Projeto de mestrado
# Autor: Anderson Berg
# 30/08/2011

from datetime import *
import os.path

DROPBOX_PATH = ''

def lerArquivoConfig():
    conf_file = raw_input("Enter the name of the configuration file (including path): ")
    nome_base = raw_input("Enter the name of the database: ")
    
    return conf_file, nome_base

def criaArquivos(conf_file, nome_base, text, mapa_x, mapa_y, repeticoes, t_max, n_iter, algoritmo):

#    conf_file = sys.argv[1]
#    nome_base = sys.argv[2]
    hoje = date.today()
    
    filename_result = DROPBOX_PATH + nome_base + algoritmo + "-" + str(mapa_x) + "x" + str(mapa_y) + "-" + hoje.strftime("%y%m%d") + "_" + str(repeticoes) + "x" + str(n_iter) + "_" + str(t_max) + ".txt"
    filename_individuos = DROPBOX_PATH + nome_base + algoritmo + "_obj_list" + "-" + hoje.strftime("%y%m%d") + "_" + str(repeticoes) + "x" + str(n_iter) + "_" + str(t_max) + ".txt"

    resultado = open(filename_result, 'w')
    resultado.writelines(text)
    resultado.close()

    file_individuos = open(filename_individuos, 'w')
    file_individuos.close()
    
    return filename_result, filename_individuos, resultado, file_individuos