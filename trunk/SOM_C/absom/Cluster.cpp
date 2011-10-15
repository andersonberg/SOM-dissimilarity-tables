/*
 * Cluster.cpp
 *
 *  Created on: 22/08/2011
 *      Author: Anderson
 */

using namespace std;

#include "Cluster.h"

Cluster::Cluster(int indice) {
	this->indice = indice;
	this->prototipos = new vector<Individual>();
	this->objetos = new vector<Individual>();
	this->pesos = new vector<float>();

}

void Cluster::definirPonto(int x, int y){
	this->ponto = new Point(x, y);
}

void Cluster::inserirObjeto(Individual objeto){
	this->objetos.push_back(objeto);
}

void Cluster::removerObjeto(Individual objeto){
	this->objetos.remove(objeto);
}

Cluster::~Cluster() {
	// TODO Auto-generated destructor stub
}

