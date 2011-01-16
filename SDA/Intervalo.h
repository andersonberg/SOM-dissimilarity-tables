/*
 * Intervalo.h
 *
 *  Created on: 13/09/2010
 *      Author: Anderson
 */

#ifndef INTERVALO_H_
#define INTERVALO_H_

class Intervalo {
public:
	Intervalo(float limiteInferior, float limiteSuperior);
	Intervalo();
	float GetLimiteInferior();
	void SetLimiteInferior(float limiteInferior);
	float GetLimiteSuperior();
	void SetLimiteSuperior(float limiteSuperior);
	virtual ~Intervalo();

private:
	float limiteInferior;
	float limiteSuperior;
};

#endif /* INTERVALO_H_ */
