/*
 * IntervalValued.h
 *
 *  Created on: 12/09/2010
 *      Author: Anderson
 */

#ifndef INTERVALVALUED_H_
#define INTERVALVALUED_H_

#include <vector>
#include <string>
#include <iostream>
#include "Intervalo.h"

class IntervalValued {
public:
	IntervalValued();
	virtual ~IntervalValued();
	void setCidade(std::string cidade);
	void setPais(std::string pais);
	std::string getCidade();
	std::string getPais();
	std::vector<float> CalculaPesos(Intervalo* intervaloOriginal, std::vector<Intervalo*> intervalosElementares);
	std::vector<float> OrdenaVetor(std::vector<Intervalo*> intervalosOriginais);
	int ExisteIntersecao(Intervalo* intervaloOriginal, Intervalo* intervaloElementar);
	std::vector<Intervalo*> CriaIntervalosElementares(std::vector<float> _intervalosOrdenados);
	float TamanhoIntersecao(Intervalo* intervaloOriginal, Intervalo* intervaloElementar);
	float CalculaTamanhoIntervalo(Intervalo* intervalo);
	int Contains(std::vector<float> vetorIntervalos, float limite);
	// Xj
	std::vector<Intervalo*> intervalosOriginais;
	//Conjunto de intervalos elementares (Aj)
	std::vector<Intervalo*> intervalosElementares;

private:
	std::string cidade;
	std::string pais;
};


#endif /* INTERVALVALUED_H_ */
