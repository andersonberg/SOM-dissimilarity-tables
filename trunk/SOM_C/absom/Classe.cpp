/*
 * Classe.cpp
 *
 *  Created on: 22/08/2011
 *      Author: Anderson
 */

#include "Classe.h"

Classe::Classe(int indice, std::string descricao) {
	this->indice = indice;
	this->descricao = descricao;

}

void Classe::InserirObjeto(Individual objeto){
	this->objetos.push_back(objeto);
}

Classe::~Classe() {
	// TODO Auto-generated destructor stub
}

