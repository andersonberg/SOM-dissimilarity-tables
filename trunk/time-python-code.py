import timeit

ti = timeit.Timer("som_diss_table_adap.atualiza_prototipo(mapa, individuals, denom, matrizes, q)", "import som_diss_table_adap \nimport math \n(matrizes, text, nome_base, mapa_x, mapa_y, repeticoes, q, t_min, t_max, n_iter, dissimilaridades, individuals_objects, classes_a_priori) = som_diss_table_adap.setup() \nc=mapa_x*mapa_y \nT=t_max \ndenom=2. * math.pow(T,2) \n(mapa, prototipos, individuals) = som_diss_table_adap.inicializacao(c, q, mapa_x, mapa_y, t_min, t_max, denom, matrizes, individuals_objects)")

