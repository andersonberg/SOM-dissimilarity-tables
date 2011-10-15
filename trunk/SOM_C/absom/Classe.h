/*
 * Classe.h
 *
 *  Created on: 22/08/2011
 *      Author: Anderson
 */

#ifndef CLASSE_H_
#define CLASSE_H_

#include <string>
#include <vector>

class Classe {
public:
	Classe(int indice, std::string descricao);
	void InserirObjeto(Individual objeto);
	virtual ~Classe();
	int indice;
	std::string descricao;
	std::vector<Individual> objetos;
};

#endif /* CLASSE_H_ */
