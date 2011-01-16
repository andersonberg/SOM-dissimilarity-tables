/*
 * HistogramValued.cpp
 *
 *  Created on: 14/09/2010
 *      Author: Anderson
 */

#include <vector>
#include "HistogramValued.h"

HistogramValued::HistogramValued() {
	// TODO Auto-generated constructor stub

}

std::vector<float> HistogramValued::GetHistograma()
{
	return histograma;
}

void HistogramValued::AdicionaPeso(float peso)
{
	histograma.push_back(peso);
}

void HistogramValued::SetHistograma(std::vector<float> _histograma)
{
	histograma = _histograma;
}

HistogramValued::~HistogramValued() {
	// TODO Auto-generated destructor stub
}
