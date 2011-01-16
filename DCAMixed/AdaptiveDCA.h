/*
 * AdaptiveDCA.h
 *
 *  Created on: 27/10/2010
 *      Author: Anderson
 */

#ifndef ADAPTIVEDCA_H_
#define ADAPTIVEDCA_H_

#include <vector>
#include <string>
#include <iostream>
#include "HistogramValued.h"
#include "ObjetoSimbolico.h"
#include "Cluster.h"
#include "Peso.h"

class AdaptiveDCA {
public:
	AdaptiveDCA(int K, int single, int iteracoes);
	std::vector<Cluster*> Inicializacao(std::vector<ObjetoSimbolico*> objetos);
	void AtualizaPrototipos(std::vector<ObjetoSimbolico*> prototipos);
	float CalculaDistanciaEuclidiana(ObjetoSimbolico* objeto, ObjetoSimbolico* prototipo, int variavel);
	std::vector<Peso*> AtualizaPesos(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos, int single);
	void AtualizaParticao(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos, std::vector<Peso*> lambdas_clusters);
	float CalculaDistanciaAdaptativa(ObjetoSimbolico* objeto, ObjetoSimbolico* prototipo, std::vector<float> lambda);
	float CalculaLambdaUnico();
	ObjetoSimbolico* CalculaPrototipoGeral(std::vector<ObjetoSimbolico*> objetos);
	float CalculaSomaDosQuadradosGeral();
	float CalculaSomaQuadradosIntraClasse(std::vector<ObjetoSimbolico*> prototipos);
	float CalculaSomaQuadradosInterClasses(std::vector<ObjetoSimbolico*> prototipos);
	virtual ~AdaptiveDCA();
	int K;
	int iteracoes;
	std::vector<Cluster*> particao;
	ObjetoSimbolico* prototipoGeral;
	int test;
	int single;

	std::vector<float> ssqGlobalVariavel;
	std::vector<float> ssqGlobalCluster;
	std::vector<float> ssqGlobalClusterVariavel;

	std::vector<float> ssqIntraCluster;
	std::vector<float> ssqIntraVariavel;
	std::vector<float> ssqIntraClusterVariavel;

	std::vector<float> ssqInterCluster;
	std::vector<float> ssqInterVariavel;
	std::vector< std::vector<float> > ssqInterClusterVariavel;

	std::vector<float> cor_j;
	std::vector<float> ctr_j;

	std::vector<float> cor_jk;
	std::vector<float> ctr_jk;

private:

};

#endif /* ADAPTIVEDCA_H_ */
