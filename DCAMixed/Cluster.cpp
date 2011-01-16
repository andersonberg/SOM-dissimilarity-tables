/*
 * Cluster.cpp
 *
 *  Created on: 06/12/2010
 *      Author: Anderson
 */

#include "Cluster.h"
#include <stdio.h>
#include <vector>
#include <iostream>
#include <string.h>
#include <fstream>
#include <stdlib.h>
#include <list>

using namespace std;

Cluster::Cluster() {
	// TODO Auto-generated constructor stub

}

int Cluster::Contains(ObjetoSimbolico* objeto)
{
	unsigned int i;
	int result = 0;
	for(list<ObjetoSimbolico*>::iterator it = objetos.begin(); it != objetos.end(); it++)
	{
		if(*it == objeto)
		{
			result = 1;
			break;
		}
	}
	return result;
}

int Cluster::GetPosition(ObjetoSimbolico* objeto)
{
	unsigned int i = 0;
	int position;
	for(list<ObjetoSimbolico*>::iterator it = objetos.begin(); it != objetos.end(); it++)
	{
		if(*it == objeto)
		{
			position = i;
		}
		i++;
	}
	return position;
}

Cluster::~Cluster() {
	// TODO Auto-generated destructor stub
}
