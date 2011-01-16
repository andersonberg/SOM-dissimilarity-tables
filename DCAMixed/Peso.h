/*
 * Peso.h
 *
 *  Created on: 08/12/2010
 *      Author: Anderson
 */

#ifndef PESO_H_
#define PESO_H_
#include <vector>
#include <string>

class Peso {
public:
	Peso();
	std::vector<float> lambda;
	virtual ~Peso();
};

#endif /* PESO_H_ */
