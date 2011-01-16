/*
 * Intervalo.cpp
 *
 *  Created on: 13/09/2010
 *      Author: Anderson
 */

#include "Intervalo.h"

Intervalo::Intervalo(float _limiteInferior, float _limiteSuperior) {
	limiteInferior = _limiteInferior;
	limiteSuperior = _limiteSuperior;
}

Intervalo::Intervalo(){

}

float Intervalo::GetLimiteInferior(){
	return limiteInferior;
}

float Intervalo::GetLimiteSuperior(){
	return limiteSuperior;
}

void Intervalo::SetLimiteInferior(float _limiteInferior){
	limiteInferior = _limiteInferior;
}

void Intervalo::SetLimiteSuperior(float _limiteSuperior){
	limiteSuperior = _limiteSuperior;
}

Intervalo::~Intervalo() {
	// TODO Auto-generated destructor stub
}
