/*
 * HistogramValued.h
 *
 *  Created on: 14/09/2010
 *      Author: Anderson
 */

#ifndef HISTOGRAMVALUED_H_
#define HISTOGRAMVALUED_H_

#include <vector>
#include <string>
#include <iostream>

class HistogramValued {
public:
	HistogramValued();
	std::vector<float> GetHistograma();
	void SetHistograma(std::vector<float>);
	void AdicionaPeso(float peso);
	virtual ~HistogramValued();

private:
	std::vector<float> histograma;
};

#endif /* HISTOGRAMVALUED_H_ */
