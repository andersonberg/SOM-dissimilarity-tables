/*
 * Individual.h
 *
 *  Created on: 22/08/2011
 *      Author: Anderson
 */

#ifndef INDIVIDUAL_H_
#define INDIVIDUAL_H_

using namespace std;

class Individual {
public:
	Individual(int indice, int id2, string nome);
	virtual ~Individual();

	void setCluster(Cluster cluster);
	void setClasse(Classe classe);

	int indice;
	int id2;
	string nome;
	Classe classe;
	Cluster cluster;
};

#endif /* INDIVIDUAL_H_ */
