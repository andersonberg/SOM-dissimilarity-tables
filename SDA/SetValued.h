/*
 * SetValued.h
 *
 *  Created on: 14/09/2010
 *      Author: Anderson
 */

#ifndef SETVALUED_H_
#define SETVALUED_H_

#include <vector>
#include <string>
#include <iostream>
#include "Categorias.h"

class SetValued {
public:
	SetValued();
	float CalculaPeso(unsigned int tamanho);
	std::vector<float> ConstruirHistograma(float peso, std::vector<char*> dominioCategorias, std::vector<char*> listaCategorias);
	virtual ~SetValued();
	std::vector<char*> dominioCategorias;
	std::vector<Categorias*> variaveis;

private:

};

#endif /* SETVALUED_H_ */
