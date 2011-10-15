/*
 * Individual.cpp
 *
 *  Created on: 22/08/2011
 *      Author: Anderson
 */

#include "Individual.h"

using namespace std;

Individual::Individual(int indice, int id2, string nome) {
	this->indice = indice;
	this->id2 = id2;
	this->nome = nome;

}

void Individual::setClasse(Classe classe){
	this->classe = classe;
}

void Individual::setCluster(Cluster cluster){
	this->cluster = cluster;
}

Individual::~Individual() {
	// TODO Auto-generated destructor stub
}

