/*
 * ListValued.cpp
 *
 *  Created on: 16/09/2010
 *      Author: Anderson
 */

#include <vector>
#include <string.h>
#include <iostream>
#include "ListValued.h"

ListValued::ListValued() {
	// TODO Auto-generated constructor stub

}

std::vector<float> ListValued::ConstruirHistograma(std::vector<char*> dominioCategorias, std::vector<char*> listaCategorias)
{
	float peso;
	peso = 0;
	unsigned int i = 0;
	unsigned int j = 0;
	std::vector<float> histograma;

	while(j < dominioCategorias.size())
	{
		if(i < listaCategorias.size() && !strcmp(listaCategorias[i], dominioCategorias[j]))
		{
			if(peso < 1)
			{
				peso += 1 / (float) listaCategorias.size();
			}
			else
			{
				peso = 1;
			}
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

ListValued::~ListValued() {
	// TODO Auto-generated destructor stub
}
