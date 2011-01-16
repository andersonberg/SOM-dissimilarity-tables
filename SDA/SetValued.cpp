/*
 * SetValued.cpp
 *
 *  Created on: 14/09/2010
 *      Author: Anderson
 */

#include <vector>
#include <string.h>
#include <iostream>
#include "SetValued.h"

using namespace std;

SetValued::SetValued() {
	// TODO Auto-generated constructor stub

}

float SetValued::CalculaPeso(unsigned int tamanho)
{
    float peso = 1 / (float) tamanho;
    return peso;
}

std::vector<float> SetValued::ConstruirHistograma(float peso, std::vector<char*> dominioCategorias, std::vector<char*> listaCategorias)
{
	unsigned int i = 0;
	unsigned int j = 0;
	unsigned int x;
	std::vector<float> histograma;

	for(x = 0; x < dominioCategorias.size(); x++){
		histograma.push_back(0.0);
	}

	while(j < dominioCategorias.size())
	{
		if(i < listaCategorias.size() && !strcmp(listaCategorias[i], dominioCategorias[j]))
		{
			histograma[j] = peso;
			i++;
		}
		else
		{
			histograma[j] = 0.0;
		}
		j++;
	}

	return histograma;
}

SetValued::~SetValued() {
	// TODO Auto-generated destructor stub
}
