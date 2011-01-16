/*
 * FuzzyKMeans.h
 *
 *  Created on: 21/09/2010
 *      Author: Anderson
 */

#ifndef FUZZYKMEANS_H_
#define FUZZYKMEANS_H_

#include <vector>
#include <string>
#include <iostream>
#include "HistogramValued.h"
#include "ObjetoSimbolico.h"

class FuzzyKMeans {
public:
	FuzzyKMeans(int k, int m, int T, float Epsilon);
	void Inicializacao(std::vector<ObjetoSimbolico*> objetos);
	std::vector<ObjetoSimbolico*> AtualizaPrototipos(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos);
	std::vector<ObjetoSimbolico*> AtualizaPertinencias(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos);
	float AtualizaCriterio(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos);
	void IniciaFuzzyKMeans(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos);
	float criterio_parada;
	virtual ~FuzzyKMeans();

private:
	int K;
	int m;
	int T;
	float Epsilon;
};

#endif /* FUZZYKMEANS_H_ */
