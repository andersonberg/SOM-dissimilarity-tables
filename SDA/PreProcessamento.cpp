/*
 * PreProcessamento.cpp
 *
 *  Created on: 13/09/2010
 *      Author: Anderson
 */

#include <stdio.h>
#include <vector>
#include <iostream>
#include <string.h>
#include <fstream>
#include <stdlib.h>
#include "IntervalValued.h"
#include "Categorias.h"
#include "SetValued.h"
#include "HistogramValued.h"
#include "FuzzyKMeans.h"
#include "ObjetoSimbolico.h"

using namespace std;

int main(int argc, char** argv)
{
	unsigned int a, x;
	const int MAX = 500;
	char buff[MAX];
	ifstream fin("testecar2.txt");
	ofstream fout("resultados.txt");

	char* palavra;
	char* compara = (char*)"Pattern";
	char* dado;

	std::vector<ObjetoSimbolico*> objetosSimbolicos;
	unsigned int i, j, h;

	//Variáveis intervalares
	std::vector<IntervalValued*> variaveis_intervalares;
	IntervalValued* interval_valued = new IntervalValued();
	Intervalo* interv;

	while(fin){
		fin.getline(buff, MAX);

		palavra = strtok(buff, " ");

		if (palavra != NULL) {
			if(!strcmp(palavra, compara))
			{
				fin.getline(buff, MAX);
				while(fin)
				{
					fin.getline(buff, MAX);
					dado = strtok(buff, " ");
					a = 0;
					x = 0;
					interv = new Intervalo();
					while(dado != NULL)
					{
						if(a > 0)
						{
							if(a % 2 != 0)
							{
								interv->SetLimiteInferior(atof(dado));
							}
							else if(a % 2 == 0)
							{
								interv->SetLimiteSuperior(atof(dado));

								if(variaveis_intervalares.size() > x)
								{
									/*** DEBUG ***/
//									cout << ">>>>>>> Variável " << x << endl;
//
//									for(i = 0; i < variaveis_intervalares[x]->intervalosOriginais.size(); i++){
//										cout << ">>>>>>> Objeto " << i << endl;
//										cout << variaveis_intervalares[x]->intervalosOriginais[i]->GetLimiteInferior() << " : " <<
//												variaveis_intervalares[x]->intervalosOriginais[i]->GetLimiteSuperior() << endl;
//									}
									/*** DEBUG ***/

									variaveis_intervalares[x]->intervalosOriginais.push_back(interv);
								}
								else
								{
									interval_valued = new IntervalValued();
									interval_valued->intervalosOriginais.push_back(interv);
									variaveis_intervalares.push_back(interval_valued);
								}

								interv = new Intervalo();
								x++;
							}
						}
						else
						{
							ObjetoSimbolico* objeto = new ObjetoSimbolico();
							objetosSimbolicos.push_back(objeto);
						}
						dado = strtok(NULL, " ");
						a++;
					}
				}
			}
		}
	}

	/*** DEBUG ***/
	fout << "*********** Intervalos Originais ***********" << endl;

	for (x = 0; x < variaveis_intervalares.size(); x++) {
		fout << ">>>>>>> Variável " << x << endl;

		for(i = 0; i < variaveis_intervalares[x]->intervalosOriginais.size(); i++){
			fout << ">>>>>>> Objeto " << i << endl;
			fout << variaveis_intervalares[x]->intervalosOriginais[i]->GetLimiteInferior() << " : " <<
					variaveis_intervalares[x]->intervalosOriginais[i]->GetLimiteSuperior() << endl;
		}
	}
	/*** DEBUG ***/

	//Variáveis intervalares
//	IntervalValued* intV = new IntervalValued();
//	intV->intervalosOriginais.push_back(new Intervalo(10,30));
//	intV->intervalosOriginais.push_back(new Intervalo(25,35));
//	intV->intervalosOriginais.push_back(new Intervalo(90,130));
//	intV->intervalosOriginais.push_back(new Intervalo(125,140));

	//Agrupa todos os intervalos originais no array intervalos_originais
	for(i = 0; i < variaveis_intervalares.size(); i++)
	{
		fout << "\nVariável # " << i << endl;
//		intervalos_originais = new std::vector<Intervalo*>();
//		for(j = 0; j < variaveis_intervalares[i]->intervalosOriginais.size(); j++)
//		{
//			intervalos_originais.push_back(variaveis_intervalares[i]->intervalosOriginais[j]);
//		}
		std::vector<float> intervalos;
		intervalos = variaveis_intervalares[i]->OrdenaVetor(variaveis_intervalares[i]->intervalosOriginais);

		/*** DEBUG ***/
		fout << "---------- Tam intv orig: " << variaveis_intervalares[i]->intervalosOriginais.size() << " ----------" << endl;
		for(a = 0; a < intervalos.size(); a++){
			fout << intervalos[a] << endl;
		}
		/*** DEBUG ***/

		variaveis_intervalares[i]->intervalosElementares = variaveis_intervalares[i]->CriaIntervalosElementares(intervalos);

		/*** DEBUG ***/
		fout << "*********** Intervalos Elementares ***********" << endl;
		fout << "---------- Tam intv elem: " << variaveis_intervalares[i]->intervalosElementares.size() << " ----------" << endl;
		for(a = 0; a < variaveis_intervalares[i]->intervalosElementares.size(); a++){
			fout << "# " << a;
			fout << " Limite Inf: " << variaveis_intervalares[i]->intervalosElementares[a]->GetLimiteInferior();
			fout << " Limite Sup: " << variaveis_intervalares[i]->intervalosElementares[a]->GetLimiteSuperior() << endl;
		}
		/*** DEBUG ***/

		for (x = 0; x < objetosSimbolicos.size(); x++)
		{
			HistogramValued* hist = new HistogramValued();
			hist->SetHistograma(variaveis_intervalares[i]->CalculaPesos(variaveis_intervalares[i]->intervalosOriginais[x], variaveis_intervalares[i]->intervalosElementares));
			objetosSimbolicos[x]->histogramas.push_back(hist);
		}
	}

//	for(i = 0; i < objetosSimbolicos.size(); i++)
//	{
//		fout << "\n\n********* Objeto #" << i << endl;
//		fout << "--------- Tam histogramas: " << objetosSimbolicos[i]->histogramas.size() << " -----------" << endl;
//
//		for(j = 0; j < objetosSimbolicos[i]->histogramas.size(); j++)
//		{
//			fout << "=========== Tam histograma: " << objetosSimbolicos[i]->histogramas[j]->GetHistograma().size() << " ==========" << endl;
//		}
//	}

//	std::vector<HistogramValued*> histogramas;
//	for(i = 0; i < intervalos_originais.size(); i++)
//	{
//		ObjetoSimbolico* obj_simb = new ObjetoSimbolico();
//		HistogramValued* hist = new HistogramValued();
//		hist->SetHistograma(interval_valued->CalculaPesos(intervalos_originais[i], intElem));
//
//		obj_simb->histogramas.push_back(hist);
//		objetosSimbolicos.push_back(obj_simb);
//		histogramas.push_back(hist);
//	}

	//Variáveis categóricas
//	SetValued* setV = new SetValued();
//	setV->dominioCategorias.push_back((char*)"A");
//	setV->dominioCategorias.push_back((char*)"C");
//	setV->dominioCategorias.push_back((char*)"Co");
//	setV->dominioCategorias.push_back((char*)"E");
//	setV->dominioCategorias.push_back((char*)"En");
//	setV->dominioCategorias.push_back((char*)"I");
//
//	Categorias* categoria1 = new Categorias();
//	categoria1->listaCategorias.push_back((char*)"A");
//	categoria1->listaCategorias.push_back((char*)"Co");
//	setV->variaveis.push_back(categoria1);
//	categoria1->peso = setV->CalculaPeso(categoria1->listaCategorias.size());
//	HistogramValued* histograma1 = new HistogramValued();
//	histograma1->SetHistograma(setV->ConstruirHistograma(categoria1->peso, setV->dominioCategorias, categoria1->listaCategorias));
//
//	objetosSimbolicos[0]->histogramas.push_back(histograma1);
//
//	Categorias* categoria2 = new Categorias();
//	categoria2->listaCategorias.push_back((char*)"C");
//	categoria2->listaCategorias.push_back((char*)"Co");
//	categoria2->listaCategorias.push_back((char*)"E");
//	setV->variaveis.push_back(categoria2);
//	categoria2->peso = setV->CalculaPeso(categoria2->listaCategorias.size());
//	HistogramValued* histograma2 = new HistogramValued();
//	histograma2->SetHistograma(setV->ConstruirHistograma(categoria2->peso, setV->dominioCategorias, categoria2->listaCategorias));
//
//	objetosSimbolicos[1]->histogramas.push_back(histograma2);
//
//	Categorias* categoria3 = new Categorias();
//	categoria3->listaCategorias.push_back((char*)"A");
//	categoria3->listaCategorias.push_back((char*)"C");
//	categoria3->listaCategorias.push_back((char*)"E");
//	setV->variaveis.push_back(categoria3);
//	categoria3->peso = setV->CalculaPeso(categoria3->listaCategorias.size());
//	HistogramValued* histograma3 = new HistogramValued();
//	histograma3->SetHistograma(setV->ConstruirHistograma(categoria3->peso, setV->dominioCategorias, categoria3->listaCategorias));
//
//	objetosSimbolicos[2]->histogramas.push_back(histograma3);
//
//	Categorias* categoria4 = new Categorias();
//	categoria4->listaCategorias.push_back((char*)"A");
//	categoria4->listaCategorias.push_back((char*)"C");
//	categoria4->listaCategorias.push_back((char*)"Co");
//	categoria4->listaCategorias.push_back((char*)"E");
//	setV->variaveis.push_back(categoria4);
//	categoria4->peso = setV->CalculaPeso(categoria4->listaCategorias.size());
//	HistogramValued* histograma4 = new HistogramValued();
//	histograma4->SetHistograma(setV->ConstruirHistograma(categoria4->peso, setV->dominioCategorias, categoria4->listaCategorias));
//
//	objetosSimbolicos[3]->histogramas.push_back(histograma4);

	//Apresentando os objetos simbólicos em forma de histograma
	for(i = 0; i < objetosSimbolicos.size(); i++)
	{
		fout << "\n\nObjeto " << i << ":" << endl;
		for(j = 0; j < objetosSimbolicos[i]->histogramas.size(); j++)
		{
			fout << "\nVariável " << j << ": ";
			for(h = 0; h < objetosSimbolicos[i]->histogramas[j]->GetHistograma().size(); h++)
			{
				fout << objetosSimbolicos[i]->histogramas[j]->GetHistograma()[h] << " ";
			}
		}
	}

	FuzzyKMeans* fuzzy = new FuzzyKMeans(3,2,350,0.000000001);
	fuzzy->Inicializacao(objetosSimbolicos);

	//Fazer várias repetições e escolher a melhor

	//getchar();
	return 0;
}
