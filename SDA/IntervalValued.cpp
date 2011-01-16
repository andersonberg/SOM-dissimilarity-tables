/*
 * IntervalValued.cpp
 *
 *  Created on: 12/09/2010
 *      Author: Anderson
 */

#include "IntervalValued.h"
#include <algorithm>
#include <iostream>
#include <string.h>
#include <stdio.h>

using namespace std;

IntervalValued::IntervalValued() {
	// TODO Auto-generated constructor stub

}

//Calcula os pesos das variáveis histograma
std::vector<float> IntervalValued::CalculaPesos(Intervalo* intervaloOriginal, std::vector<Intervalo*> intervalosElementares){
	unsigned int j;
	float tamanho_inter, tamanho_intervalo;
	float peso;
	std::vector<float> pesos;

	tamanho_intervalo = CalculaTamanhoIntervalo(intervaloOriginal);
	peso = 0;
	for(j = 0; j < intervalosElementares.size(); j++)
	{
		if(ExisteIntersecao(intervaloOriginal, intervalosElementares[j]))
		{
			tamanho_inter = TamanhoIntersecao(intervaloOriginal, intervalosElementares[j]);
			if(peso < 1)
			{
				peso += (float)tamanho_inter / (float)tamanho_intervalo;
				if(peso > 1){
					peso = 1;
				}
			}
			else
			{
				peso = 1;
			}
		}
		pesos.push_back(peso);
	}

	return pesos;
}

// Ordena o vetor com todos os intervalos em ordem crescente
std::vector<float> IntervalValued::OrdenaVetor(std::vector<Intervalo*> intervalosOriginais)
{

	unsigned int i;
	std::vector<float> vetorIntervalos;
	for(i = 0; i < intervalosOriginais.size(); i++)
	{
		float limiteInf = intervalosOriginais[i]->GetLimiteInferior();
		float limiteSup = intervalosOriginais[i]->GetLimiteSuperior();

//		if(!Contains(vetorIntervalos, limiteInf))
//		{
			vetorIntervalos.push_back(limiteInf);
//		}

//		if(!Contains(vetorIntervalos, limiteSup))
//		{
			vetorIntervalos.push_back(limiteSup);
//		}
	}
	sort(vetorIntervalos.begin(), vetorIntervalos.end());

	return vetorIntervalos;
}

// A partir dos intervalos ordenados, cria os intervalos elementares
std::vector<Intervalo*> IntervalValued::CriaIntervalosElementares(std::vector<float> _intervalosOrdenados)
{
	std::vector<Intervalo*> intervalosElem;
	unsigned int i;
	for(i = 0; i < _intervalosOrdenados.size() - 1; i++)
	{
		float limInf = _intervalosOrdenados[i];
		float limSup = _intervalosOrdenados[i+1];
		Intervalo* interv = new Intervalo(limInf, limSup);
		intervalosElem.push_back(interv);
	}

	return intervalosElem;
}

// Verifica se há interseção entre um intervalo e um intervalo elementar
int IntervalValued::ExisteIntersecao(Intervalo* intervaloOriginal, Intervalo* intervaloElementar)
{
	int result = 0;

	if( (intervaloElementar->GetLimiteInferior() >= intervaloOriginal->GetLimiteInferior()
	 && intervaloElementar->GetLimiteInferior() < intervaloOriginal->GetLimiteSuperior())
	 || (intervaloElementar->GetLimiteSuperior() > intervaloOriginal->GetLimiteInferior()
     &&  intervaloElementar->GetLimiteSuperior() <= intervaloOriginal->GetLimiteSuperior()) )
	{
		result = 1;
	}

	else
	{
		result = 0;
	}

	return result;
}

// Calcula o tamanho da interseção entre intervalos
float IntervalValued::TamanhoIntersecao(Intervalo* intervaloOriginal, Intervalo* intervaloElementar)
{
	float tamanho;

	if(intervaloElementar->GetLimiteInferior() >= intervaloOriginal->GetLimiteInferior()
	   && intervaloElementar->GetLimiteInferior() < intervaloOriginal->GetLimiteSuperior()
	   && intervaloElementar->GetLimiteSuperior() >= intervaloOriginal->GetLimiteSuperior())
	{
		tamanho = intervaloOriginal->GetLimiteSuperior() - intervaloElementar->GetLimiteInferior();
	}

	else if(intervaloElementar->GetLimiteInferior() >= intervaloOriginal->GetLimiteInferior()
			&& intervaloElementar->GetLimiteInferior() < intervaloOriginal->GetLimiteSuperior()
			&& intervaloElementar->GetLimiteSuperior() > intervaloOriginal->GetLimiteInferior()
			&& intervaloElementar->GetLimiteSuperior() <= intervaloOriginal->GetLimiteSuperior())
	{
		tamanho = intervaloElementar->GetLimiteSuperior() - intervaloElementar->GetLimiteInferior();
	}

	else
	{
		tamanho = intervaloElementar->GetLimiteSuperior() - intervaloOriginal->GetLimiteInferior();
	}

	return tamanho;
}

// Calcula o tamanho de um intervalo qualquer
float IntervalValued::CalculaTamanhoIntervalo(Intervalo* intervalo)
{
	float tamanho;
	tamanho = intervalo->GetLimiteSuperior() - intervalo->GetLimiteInferior();
	return tamanho;
}

int IntervalValued::Contains(std::vector<float> vetorIntervalos, float limite)
{
	unsigned int i;
	int result = 0;
	for(i = 0; i < vetorIntervalos.size(); i++)
	{
		if(vetorIntervalos[i] == limite)
		{
			result = 1;
		}
	}

	return result;
}

IntervalValued::~IntervalValued() {
	// TODO Auto-generated destructor stub
}
