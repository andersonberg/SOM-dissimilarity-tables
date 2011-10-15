#!/usr/bin/env python
#-*-coding:latin1-*-

# gui_bsom.py
# Projeto de mestrado
# Autor: Anderson Berg

from bsom import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import pango
import config
import time
from datetime import *

class Main:
	def __init__(self):
		self.tree = gtk.glade.XML('gui_bsom.glade', 'main')
		callbacks = {
				"on_btnRun_clicked" : self.btnRun,
				"on_main_destroy":gtk.main_quit
				}
		self.tree.signal_autoconnect(callbacks)


	def btnRun(self, widget):

		self.configChooser = self.tree.get_widget("configfilechooser")
		self.conf_file = self.configChooser.get_filename()

		self.enResult = self.tree.get_widget("enResult")
		self.filename_result = self.enResult.get_text()

		self.enObjects = self.tree.get_widget("enObjects")
		self.filename_individuos = self.enObjects.get_text()

		self.txt = self.tree.get_widget("textview1")
		self.txtbuffer = self.txt.get_buffer()

		self.run()


	def run(self):
		
		matrizes, text, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, individuals_objects, classes_a_priori = config.config(self.conf_file)
		hoje = date.today()

		resultado = open(self.filename_result, 'w')
		resultado.writelines(text)
		resultado.close()

		file_individuos = open(self.filename_individuos, 'w')
		file_individuos.close()

		text = []
		criterios_energia = []
		oercs = []

		soma_dissimilaridades = []
		for obj1 in individuals_objects:
			for obj2 in individuals_objects:
				soma_dissimilaridades.append(sum(matrizes[:,obj1.indice,obj2.indice]))

		soma_dissimilaridades = np.array(soma_dissimilaridades).reshape(len(individuals_objects), len(individuals_objects))

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
			denom = 2. * pow(T,2)
			(mapa, individuals) = inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, soma_dissimilaridades, individuals_objects)
	
			while T > t_min:
			# while t < (n_iter - 1):
				#Step 1: computation of the best prototypes
				t += 1.0

				print 'Iteração', t
				T = t_max * pow( (t_min / t_max), (t / (n_iter - 1.0)) )
				denom = 2. * pow(T,2)

				mapa = atualiza_prototipo(mapa, individuals, denom, soma_dissimilaridades, q)
				
				#Step 2: definition of the best partition
				mapa, individuals = atualiza_particao(individuals, mapa, denom, soma_dissimilaridades)


			#Imprime os clusters finais		
			text.extend(imprime_clusters(mapa))

			no_clusters_completos = 0
			for cluster in mapa.flat:
				if len(cluster.objetos) > 0:
					no_clusters_completos += 1

			energia = calcula_energia(mapa, individuals, soma_dissimilaridades, T)
			criterios_energia.append(energia)

			text.append("\n\nCritério de adequação (energia): " + str(energia))

			########################################
			#Calcula a matrix de confusão #
			confusion_matrix = calcula_confusion_matrix(mapa, classes_a_priori, no_clusters_completos)
			text.extend(imprime_matriz_confusao(confusion_matrix, mapa, classes_a_priori, no_clusters_completos))

			##########################################################################################
			# Cálculo do índice de Rand Corrigido #
			no_objetos = len(individuals)
		
			cr = calcula_cr(confusion_matrix, len(classes_a_priori), no_clusters_completos, no_objetos)	
			text.append("\n\nCorrected Rand index: " + str(cr))

			##########################################################
			# Cálculo da precisão #
			precisao_matrix = calcula_precisao(confusion_matrix, len(classes_a_priori), no_clusters_completos)

			###########################################################
			# Cálculo do recall #
			recall_matrix =	calcula_recall(confusion_matrix, len(classes_a_priori), no_clusters_completos)

			###########################################################
			# Cálculo do f_measure #

			len_cls_priori = len(classes_a_priori)
			f_measure_matrix = calcula_f_measure(precisao_matrix, recall_matrix, len_cls_priori, no_clusters_completos)
			soma2 = sum( [ confusion_matrix[i,:].sum() * f_measure_matrix[i,:].max() for i in range(len(classes_a_priori)) ] )
			f_measure = float(soma2 / no_objetos)
			text.append("\nF-measure(P,Q): " + str(f_measure))

			###########################################################
			# Cálculo do oerc (taxa de erro de classificação global) #
			oerc = calcula_oerc(confusion_matrix, no_clusters_completos, no_objetos)
			oercs.append(oerc)
			text.append("\nOERC: " + str(oerc))

			resultado = open(self.filename_result, 'a')
			resultado.writelines(text)
			resultado.close()
			text = []

			list_individuos = []

			list_individuos.append("\n\n#####################################")
			list_individuos.append("\n# Repetição do experimento: " + str(a) + "\n")

			for ind in individuals:
			        list_individuos.append(str(ind.nome) + "  " + str(ind.classe_a_priori.indice) + "  " + str(ind.cluster.indice) + "\n")

			file_individuos = open(self.filename_individuos, 'a')
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

		resultado = open(self.filename_result, 'a')
		resultado.writelines(text)	
		resultado.close()

		enditer = self.txtbuffer.get_end_iter()
		self.txtbuffer.insert(enditer, "Fim do experimento.")
		print "Fim do experimento."


if __name__ == '__main__':
	absom_gui = Main()
	gtk.main()
