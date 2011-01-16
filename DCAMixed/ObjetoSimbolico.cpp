/*
 * ObjetoSimbolico.cpp
 *
 *  Created on: 22/09/2010
 *      Author: Anderson
 */

#include "ObjetoSimbolico.h"
#include <stdio.h>
#include <vector>
#include <iostream>
#include <string.h>

using namespace std;

ObjetoSimbolico::ObjetoSimbolico() {

}

void ObjetoSimbolico::ImprimeHistograma()
{
	unsigned int i, j;

	for(i = 0; i < histogramas.size(); i++)
	{
		cout << "\nVariável " << i << ":" << endl;
		for(j = 0; j < histogramas[i]->GetHistograma().size(); j++)
		{
			cout << histogramas[i]->GetHistograma()[j] << " ";
		}
	}

	cout << "\n";
}

ObjetoSimbolico* ObjetoSimbolico::ClonarObjeto()
{
	unsigned int i, x;
	ObjetoSimbolico* clone = new ObjetoSimbolico();

	for(i = 0; i < this->histogramas.size(); i++)
	{
		HistogramValued* histograma = new HistogramValued();
		std::vector<float> pesos;
		for(x = 0; x < this->histogramas[i]->GetHistograma().size(); x++)
		{
			pesos.push_back(this->histogramas[i]->GetHistograma()[x]);
		}

		histograma->SetHistograma(pesos);

		clone->histogramas.push_back(histograma);
	}

	clone->cluster = this->cluster;
	strcpy((char*)clone->cidade.c_str(), this->cidade.c_str());

	return clone;
}

//int ObjetoSimbolico::Equals(ObjetoSimbolico* objeto)
//{
//	unsigned int i, j;
//	int booleano = 0;
//
//	if(histogramas.size() == objeto->histogramas.size()){
//		for(i = 0; i < histogramas.size(); i++)
//		{
//			if(histogramas[i]->GetHistograma().size() == objeto->histogramas[i]->GetHistograma().size())
//			{
//				for(j = 0; j < histogramas[i]->GetHistograma().size(); j++)
//				{
//					if(histogramas[i]->GetHistograma()[j] != objeto->histogramas[i]->GetHistograma()[j])
//					{
//						booleano++;
//					}
//				}
//			}
//		}
//	}
//
//	return booleano;
//}

ObjetoSimbolico::~ObjetoSimbolico() {
	// TODO Auto-generated destructor stub
}
