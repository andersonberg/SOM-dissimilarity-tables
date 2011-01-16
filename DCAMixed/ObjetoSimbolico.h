/*
 * ObjetoSimbolico.h
 *
 *  Created on: 22/09/2010
 *      Author: Anderson
 */

#ifndef OBJETOSIMBOLICO_H_
#define OBJETOSIMBOLICO_H_

#include <vector>
#include <string>
#include <iostream>
#include "HistogramValued.h"

class ObjetoSimbolico {
public:
	ObjetoSimbolico();
	virtual ~ObjetoSimbolico();
	void ImprimeHistograma();
	ObjetoSimbolico* ClonarObjeto();
//	int Equals(ObjetoSimbolico*);
	std::vector<HistogramValued*> histogramas;
	std::vector<float> pertinencias;
	int cluster;
	std::string cidade;
};

#endif /* OBJETOSIMBOLICO_H_ */
