/*
 * Cluster.h
 *
 *  Created on: 06/12/2010
 *      Author: Anderson
 */

#ifndef CLUSTER_H_
#define CLUSTER_H_

#include <vector>
#include <list>
#include "ObjetoSimbolico.h"
#include "Peso.h"

class Cluster {
public:
	Cluster();
	int id;
	std::list<ObjetoSimbolico*> objetos;
	ObjetoSimbolico* prototipo;
	Peso* pesos;
	int Contains(ObjetoSimbolico* objeto);
	int GetPosition(ObjetoSimbolico* objeto);
	virtual ~Cluster();
};

#endif /* CLUSTER_H_ */
