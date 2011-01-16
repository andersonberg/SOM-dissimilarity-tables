/*
 * FuzzyKMeans.cpp
 *
 *  Created on: 21/09/2010
 *      Author: Anderson
 */

#include <stdio.h>
#include <vector>
#include <string.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include "FuzzyKMeans.h"
#include "HistogramValued.h"

using namespace std;

FuzzyKMeans::FuzzyKMeans(int _k, int _m, int _T, float _Epsilon)
{
	K = _k;
	m = _m;
	T = _T;
	Epsilon = _Epsilon;
}

void FuzzyKMeans::Inicializacao(std::vector<ObjetoSimbolico*> objetos)
{
	unsigned int i, x, z;
	int h, j, Hj, k, r;
	int p;
	float numerador;
	float denominador;
	float somaInterna;
	float somaInterna2;
	float resultado;
	float fator;
	float soma_geral;
	int aleatorio;
	int aleatorio_old = -1;
	std::vector<ObjetoSimbolico*> prototipos;

	criterio_parada = 0.0;

	cout << "########### INICIALIZAÇÃO ##########" << endl;

	//Inicializa conjunto de prototipos aleatoriamente
	for(p = 0; p < K; p++)
	{
		srand ( time(NULL) );
		aleatorio = rand() % objetos.size();

		while(aleatorio == aleatorio_old)
		{
			srand ( time(NULL) );
			aleatorio = rand() % objetos.size();
		}

		aleatorio_old = aleatorio;
		ObjetoSimbolico* prototipo = objetos[aleatorio]->ClonarObjeto();
		prototipos.push_back(prototipo);

		cout << "Objeto escolhido como protótipo: " << aleatorio << endl;
	}

	for(p = 0; p < K; p++){
		prototipos[p]->ImprimeHistograma();
	}

	//Inicializa o vetor de pertinências com 0
	for(i = 0; i < objetos.size(); i++)
	{
		for(r = 0; r < K; r++)
		{
			objetos[i]->pertinencias.push_back(0.0);
		}
	}

	for(z = 0; z < objetos.size(); z++)
	{
		for(x = 0; x < prototipos.size(); x++)
		{
			if(!objetos[z]->Equals(prototipos[x]))
			{
				objetos[z]->pertinencias[x] = 1;
			}
		}
	}

	//Inicializa pertinências
	for(i = 0; i < objetos.size(); i++)
	{
		//Tamanho do vetor de pertinências = K
		for(r = 0; r < K; r++)
		{
			soma_geral = 0.0;
			for(k = 0; k < K; k++)
			{
				p = objetos[i]->histogramas.size();
				numerador = 0.0;
				denominador = 0.0;
				for(j = 0; j < p; j++)
				{
					Hj = objetos[i]->histogramas[j]->GetHistograma().size();
					somaInterna = 0.0;
					somaInterna2 = 0.0;
					for(h = 0; h < Hj; h++)
					{
						float _p = objetos[i]->histogramas[j]->GetHistograma()[h];
						float _a = prototipos[k]->histogramas[j]->GetHistograma()[h];
						float _b = prototipos[r]->histogramas[j]->GetHistograma()[h];

						somaInterna += pow(_p - _a, 2);
						somaInterna2 += pow(_p - _b, 2);
					}
					numerador += somaInterna;
					denominador += somaInterna2;
				}

				fator = 1/(m-1);
				if(denominador != 0)
				{
					resultado = pow(numerador/denominador, fator);
				}
				else{
					resultado = 0;
				}
				soma_geral += resultado;
			}

			objetos[i]->pertinencias[r] = pow(soma_geral, -1);

			for(z = 0; z < objetos.size(); z++)
			{
				for(x = 0; x < prototipos.size(); x++)
				{
					if(!objetos[z]->Equals(prototipos[x]))
					{
						objetos[z]->pertinencias[x] = 1;
					}
				}
			}

//			cout << "Objeto " << i << " Cluster " << r << ": ";
//			cout << objetos[i]->pertinencias[r] << endl;
		}
	}

	//Inicializa critério de parada J(0)
	float soma_j, soma_n, soma_h;
	for(k = 0; k < K; k++)
	{
		for(i = 0; i < objetos.size(); i++)
		{
			soma_n = 0.0;
			p = objetos[i]->histogramas.size();
			soma_j = 0.0;
			for(j = 0; j < p; j++)
			{
				Hj = objetos[i]->histogramas[j]->GetHistograma().size();
				soma_h = 0.0;
				for(h = 0; h < Hj; h++)
				{
					soma_h += pow(objetos[i]->histogramas[j]->GetHistograma()[h] - prototipos[k]->histogramas[j]->GetHistograma()[h], 2);
				}

//				cout << "Soma h: " << soma_h << endl;

				soma_j += soma_h;
			}

			soma_n += (pow(objetos[i]->pertinencias[k], m)) * soma_j;

//			cout << "soma n: " << soma_n << endl;
		}
		if(!isnan(soma_n))
		{
			criterio_parada += soma_n;
		}
//		cout << "Criterio: " << criterio_parada << endl;
	}

	IniciaFuzzyKMeans(objetos, prototipos);
}

std::vector<ObjetoSimbolico*> FuzzyKMeans::AtualizaPrototipos(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos)
{
	int k, j, Hj, h;
	int p;
	unsigned int i;
	std::vector<ObjetoSimbolico*> novos_prototipos;

	for(i = 0; i < prototipos.size(); i ++)
	{
		novos_prototipos.push_back(prototipos[i]->ClonarObjeto());
	}

	for(k = 0; k < K; k++)
	{
		p = prototipos[k]->histogramas.size();
		for(j = 0; j < p; j++)
		{
			Hj = prototipos[k]->histogramas[j]->GetHistograma().size();
			std::vector<float> histograma;
			for(h = 0; h < Hj; h++)
			{
				float numerador, denominador;
				for(i = 0; i < objetos.size(); i++)
				{
//					cout << "\n>>>>>>>> Pertinencia: " << objetos[i]->pertinencias[k] << endl;
//					cout << "\n>>>>>>>> Peso do histograma: " << objetos[i]->histogramas[j]->GetHistograma()[h] << endl;
//					cout << "\n>>>>>>>> m: " << m << endl;
					numerador += pow(objetos[i]->pertinencias[k], m) * objetos[i]->histogramas[j]->GetHistograma()[h];
					denominador += pow(objetos[i]->pertinencias[k], m);
//					cout << "\n>>>>>>>> Numerador: " << numerador << endl;
//					cout << "\n>>>>>>>> Denominador: " << denominador << endl;
				}
				if(denominador != 0)
				{
					histograma.push_back(numerador/denominador);
				}
				else{
					histograma.push_back(0);
				}
			}
			novos_prototipos[k]->histogramas[j]->SetHistograma(histograma);
		}
	}

	return novos_prototipos;
}

std::vector<ObjetoSimbolico*> FuzzyKMeans::AtualizaPertinencias(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos)
{
	unsigned int i;
	int h, j, Hj, k, r;
	int p;
	float numerador;
	float denominador;
	float somaInterna;
	float somaInterna2;
	float resultado;
	float fator;
	float soma_geral;
	std::vector<ObjetoSimbolico*> novos_objetos;
	novos_objetos = objetos;

	for(i = 0; i < objetos.size(); i++)
	{
//		cout << "\ni: " << i;
		//Tamanho do vetor de pertinências = K
		for(r = 0; r < K; r++)
		{
//			cout <<"\nr: " << r;
			soma_geral = 0.0;
			for(k = 0; k < K; k++)
			{
//				cout << "\nk: " << k;
				p = objetos[i]->histogramas.size();
				numerador = 0.0;
				denominador = 0.0;
				for(j = 0; j < p; j++)
				{
//					cout << "\nj: " << j;
					Hj = objetos[i]->histogramas[j]->GetHistograma().size();
					somaInterna = 0.0;
					somaInterna2 = 0.0;
					for(h = 0; h < Hj; h++)
					{
						somaInterna += pow(objetos[i]->histogramas[j]->GetHistograma()[h] - prototipos[k]->histogramas[j]->GetHistograma()[h], 2);
						somaInterna2 += pow(objetos[i]->histogramas[j]->GetHistograma()[h] - prototipos[r]->histogramas[j]->GetHistograma()[h], 2);
					}
					numerador += somaInterna;
					denominador += somaInterna2;

//					cout << "\nNumerador: " << numerador;
//					cout << "\nDenominador: " << denominador;
				}

				fator = 1/(m-1);
				if(denominador != 0)
				{
					resultado = pow(numerador/denominador, fator);
				}
				else
				{
					resultado = 0;
				}
				soma_geral += resultado;
			}

			novos_objetos[i]->pertinencias[r] = pow(soma_geral, -1);

//			cout << "Objeto " << i << " Cluster " << r << ": ";
//			cout << novos_objetos[i]->pertinencias[r] << endl;
		}
	}

	return novos_objetos;
}

float FuzzyKMeans::AtualizaCriterio(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos)
{
	unsigned int i;
	int h, j, Hj, k;
	int p;
	float soma_j, soma_n, soma_h;
	float criterio;

	for(k = 0; k < K; k++)
	{
		for(i = 0; i < objetos.size(); i++)
		{
			soma_n = 0.0;
			p = objetos[i]->histogramas.size();
			soma_j = 0.0;
			for(j = 0; j < p; j++)
			{
				Hj = objetos[i]->histogramas[j]->GetHistograma().size();
				soma_h = 0.0;
				for(h = 0; h < Hj; h++)
				{
					soma_h += pow(objetos[i]->histogramas[j]->GetHistograma()[h] - prototipos[k]->histogramas[j]->GetHistograma()[h], 2);
				}

//				cout << "Soma h: " << soma_h << endl;

				soma_j += soma_h;
			}

			soma_n += (pow(objetos[i]->pertinencias[k], m)) * soma_j;

//			cout << "soma n: " << soma_n << endl;
		}
		if(!isnan(soma_n))
		{
			criterio += soma_n;
		}
	}
	cout << "Criterio: " << criterio << endl;

	return criterio;
}

void FuzzyKMeans::IniciaFuzzyKMeans(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos)
{
	int t = 1;
	unsigned int i;
	float criterio_anterior;
	criterio_anterior = criterio_parada;

	cout << "########## ATUALIZAÇÃO ###########" << endl;

	do
	{
//		getchar();
		cout << "\nIteração: " << t << endl;
		criterio_anterior = criterio_parada;
		prototipos = AtualizaPrototipos(objetos, prototipos);

//		for(i = 0; i < prototipos.size(); i++)
//		{
//			cout << "\nPrototipo: " << i << endl;
//			prototipos[i]->ImprimeHistograma();
//		}

		objetos = AtualizaPertinencias(objetos, prototipos);
		criterio_parada = AtualizaCriterio(objetos, prototipos);
		t++;
	}
	while(t <= T && (abs(criterio_parada - criterio_anterior)) >= Epsilon);
}

FuzzyKMeans::~FuzzyKMeans() {
	// TODO Auto-generated destructor stub
}
