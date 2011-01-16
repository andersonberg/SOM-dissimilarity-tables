/*
 * Categorias.h
 *
 *  Created on: 15/09/2010
 *      Author: Anderson
 */

#ifndef CATEGORIAS_H_
#define CATEGORIAS_H_

#include <vector>
#include <string>
#include <iostream>

class Categorias {
public:
	Categorias();
	virtual ~Categorias();
	std::vector<char*> listaCategorias;
	float peso;
};

#endif /* CATEGORIAS_H_ */
