/*
 * Mapa.h
 *
 *  Created on: 23/08/2011
 *      Author: Anderson
 */

#ifndef MAPA_H_
#define MAPA_H_

using namespace std;

class Mapa {
public:
	Mapa(list<Individual> objetos, int nLinhas, int nColunas, int cardinalidade);
	virtual ~Mapa();

	list<list<Cluster>> mapa;
	list<Individual> objetos;
};

#endif /* MAPA_H_ */
