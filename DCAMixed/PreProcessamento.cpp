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
#include "HistogramValued.h"
#include "ObjetoSimbolico.h"
#include "AdaptiveDCA.h"
#include "Cluster.h"

using namespace std;

std::vector<IntervalValued*> LeituraArquivo()
{
	const int MAX = 500;
	char buff[MAX];
	char* palavra;
	std::string cidade;
	std::string pais;
	Intervalo* intervaloTemp;
	std::vector<Intervalo*> temperaturasCidade;
	std::vector<IntervalValued*> cidades;
	IntervalValued* city;
	int i;

	char* city_text = (char*)"City:";
	char* country_text = (char*)"#Country:";

	ifstream fin("base de dados SDA--top.txt");

	while(fin)
	{
		fin.getline(buff, MAX);
		palavra = strtok(buff, " ");
		while (palavra != NULL)
		{
			if(atof(palavra) || strlen(palavra)==1)
			{
				//Limite inferior de temperatura
				if(i == 0)
				{
					intervaloTemp = new Intervalo();
					intervaloTemp->SetLimiteInferior(atof(palavra));
					i++;
				}
				//Limite superior de temperatura
				else
				{
					intervaloTemp->SetLimiteSuperior(atof(palavra));
					city->intervalosOriginais.push_back(intervaloTemp);
					i = 0;
				}
			}
			else if(!strcmp(palavra, city_text))
			{
				palavra = strtok(NULL, " ");
				cidade = "";
				while(strcmp(palavra, country_text))
				{
					i = 0;
					cidade += palavra;
					cidade += " ";
					palavra = strtok(NULL, " ");
				}
				//Cria um novo objeto IntervalValued que armazena os dados de uma cidade
				// e seta o nome da cidade
				city = new IntervalValued();
				city->setCidade(cidade);
				cidades.push_back(city);

				palavra = strtok(NULL, " ");
				pais = "";
				while(palavra != NULL)
				{
					pais += palavra;
					pais += " ";
					palavra = strtok(NULL, " ");
				}
				city->setPais(pais);
			}
			palavra = strtok(NULL, " ,");
		}
	}

	/*DEBUG Imprime cidades e temperaturas*/
//	unsigned int c;
//	for(count = 0; count < cidades.size(); count++)
//	{
//		cout << "Cidade: " << cidades[count]->getCidade() << " País: " << cidades[count]->getPais() << endl;
//		cout << "Temperaturas: " << endl;
//		for(c = 0; c < cidades[count]->intervalosOriginais.size(); c++)
//		{
//			cout << cidades[count]->intervalosOriginais[c]->GetLimiteInferior() << " " <<
//					cidades[count]->intervalosOriginais[c]->GetLimiteSuperior() << endl;
//		}
//	}

	return cidades;
}

int main(int argc, char** argv)
{
	std::vector<IntervalValued*> cidades = LeituraArquivo();
	unsigned int a;
	std::vector<ObjetoSimbolico*> objetosSimbolicos;
	unsigned int i, j, h;

	ofstream fout("histogramas.txt");
	ofstream fout_clusters("clusters.txt");

	//Agrupa todos os intervalos originais no array intervalos_originais
	for(i = 0; i < cidades.size(); i++)
	{
		std::vector<float> intervalos;
		intervalos = cidades[i]->OrdenaVetor(cidades[i]->intervalosOriginais);
		cidades[i]->intervalosElementares = cidades[i]->CriaIntervalosElementares(intervalos);

		ObjetoSimbolico* objeto_cidade = new ObjetoSimbolico();
		objeto_cidade->cidade = cidades[i]->getCidade();
		for(a = 0; a < cidades[i]->intervalosOriginais.size(); a++)
		{
			HistogramValued* histo = new HistogramValued();
			histo->SetHistograma(cidades[i]->CalculaPesos(cidades[i]->intervalosOriginais[a], cidades[i]->intervalosElementares));
			objeto_cidade->histogramas.push_back(histo);
		}
		objetosSimbolicos.push_back(objeto_cidade);
	}

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

	AdaptiveDCA* adaptive = new AdaptiveDCA(4, 1, 10);

	cout << "Tamanho da base: " << objetosSimbolicos.size() << endl;

	std::vector<Cluster*> particao = adaptive->Inicializacao(objetosSimbolicos);

	for(i = 0; i < particao.size(); i++)
	{
		unsigned int tamanho_cluster = particao[i]->objetos.size();
		fout_clusters << "\nCluster: " << i << " " << tamanho_cluster << " objetos. " << endl;
		for(list<ObjetoSimbolico*>::iterator it = particao[i]->objetos.begin(); it != particao[i]->objetos.end(); it++)
		{
			fout_clusters << ((ObjetoSimbolico*)*it)->cidade << endl;
		}
	}

//	getchar();
	cout << "Fim da execução." << endl;
	return 0;
}
