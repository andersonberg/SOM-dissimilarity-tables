/*
 * Cluster.h
 *
 *  Created on: 22/08/2011
 *      Author: Anderson
 */

using namespace std;

#ifndef CLUSTER_H_
#define CLUSTER_H_

#include <string>
#include <list>
#include <math.h>
#include <iostream>

class Cluster {
public:
	Cluster(int indice);
	virtual ~Cluster();

	void definirPonto(int x, int y);
	void inserirObjeto(Individual objeto);
	void removerObjeto(Individual objeto);

	int indice;
	list<Individual> prototipos;
	list<Individual> objetos;
	vector<float> pesos;
	Point ponto;

};

#endif /* CLUSTER_H_ */
