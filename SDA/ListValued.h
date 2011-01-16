/*
 * ListValued.h
 *
 *  Created on: 16/09/2010
 *      Author: Anderson
 */

#ifndef LISTVALUED_H_
#define LISTVALUED_H_

class ListValued {
public:
	ListValued();
	virtual ~ListValued();
	std::vector<float> ConstruirHistograma(std::vector<char*> dominioCategorias, std::vector<char*> listaCategorias);
};

#endif /* LISTVALUED_H_ */
