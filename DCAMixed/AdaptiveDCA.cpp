/*
 * AdaptiveDCA.cpp
 *
 *  Created on: 27/10/2010
 *      Author: Anderson
 */
#include <stdio.h>
#include <vector>
#include <string.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <fstream>
#include <sys/time.h>
#include "HistogramValued.h"
#include "AdaptiveDCA.h"
#include "Peso.h"

using namespace std;

AdaptiveDCA::AdaptiveDCA(int _K, int _single, int _iteracoes) {
	K = _K;
	iteracoes = _iteracoes;
	test = 1;
	single = _single;
}

std::vector<Cluster*> AdaptiveDCA::Inicializacao(std::vector<ObjetoSimbolico*> objetos){

	unsigned int objeto_atual_i, cluster_atual_k, iter;
	int p, j, i;
	int aleatorio;
	int aleatorio_old = -1;
	float distancia, menor_distancia;
	std::vector<ObjetoSimbolico*> prototipos;

	ofstream fout_clusters_begin("clusters_begin.txt");
	ofstream fout_indices("indices.txt");

	//Inicializa conjunto de prototipos aleatoriamente
	for(p = 0; p < K; p++)
	{
		srand ( time(NULL) * 1000);
		aleatorio = rand() % objetos.size();

		while(aleatorio == aleatorio_old)
		{
			srand ( time(NULL) * 1000);
			aleatorio = rand() % objetos.size();
		}

		aleatorio_old = aleatorio;
		ObjetoSimbolico* prototipo = objetos[aleatorio]->ClonarObjeto();
		prototipos.push_back(prototipo);

		cout << "Objeto escolhido como protótipo: " << aleatorio << endl;
	}

	for(cluster_atual_k = 0; cluster_atual_k < prototipos.size(); cluster_atual_k++)
	{
		Cluster* cluster_k = new Cluster();
		cluster_k->prototipo = prototipos[cluster_atual_k];
		cluster_k->id = cluster_atual_k;
		particao.push_back(cluster_k);
	}

	for(objeto_atual_i = 0; objeto_atual_i < objetos.size(); objeto_atual_i++){
		int cluster_id = 0;
		for(cluster_atual_k = 0; cluster_atual_k < particao.size(); cluster_atual_k++){
			distancia = 0;
			p = particao[cluster_atual_k]->prototipo->histogramas.size();
			for(j = 0; j < p; j++)
			{
				distancia += CalculaDistanciaEuclidiana(objetos[objeto_atual_i], particao[cluster_atual_k]->prototipo, j);
			}

			if(cluster_atual_k == 0){
				menor_distancia = distancia;
				cluster_id = cluster_atual_k;
			}

			if(cluster_atual_k > 0 && distancia < menor_distancia){
				menor_distancia = distancia;
				cluster_id = cluster_atual_k;
			}
		}
		objetos[objeto_atual_i]->cluster = cluster_id;
		particao[cluster_id]->objetos.push_back(objetos[objeto_atual_i]);
	}

	for(iter = 0; iter < particao.size(); iter++)
	{
		unsigned int tamanho_cluster = particao[iter]->objetos.size();
		fout_clusters_begin << "\nCluster: " << iter << " " << tamanho_cluster << " objetos. " << endl;
		for(list<ObjetoSimbolico*>::iterator it = particao[iter]->objetos.begin(); it != particao[iter]->objetos.end(); it++)
		{
			fout_clusters_begin << ((ObjetoSimbolico*)*it)->cidade << endl;
		}
	}

	std::vector<Peso*> pesos;
	i = 0;

	do
	{
		cout << "\nIteração: " << i << endl;
		AtualizaPrototipos(prototipos);
		cout << "Protótipos atualizados com sucesso!" << endl;
		pesos = AtualizaPesos(objetos, prototipos, single);
		cout << "Pesos atualizados com sucesso!" << endl;
		AtualizaParticao(objetos,prototipos,pesos);
		cout << "Clusters atualizados com sucesso!" << endl;
		i++;
	}
	while(test);

	prototipoGeral = CalculaPrototipoGeral(objetos);
	cout << "Protótipo geral definido com sucesso!" << endl;
	float t = CalculaSomaDosQuadradosGeral();
	float w = CalculaSomaQuadradosIntraClasse(prototipos);
	float b = CalculaSomaQuadradosInterClasses(prototipos);

	fout_indices << "\nT: " << t << endl;
	fout_indices << "\nW: " << w << endl;
	fout_indices << "\nB: " << b << endl;
	fout_indices << "\nW + B: " << w+b << endl;

	unsigned int iter_ssqGlobalVariavel, iter_ssqGlobalCluster;

	for(iter_ssqGlobalVariavel = 0; iter_ssqGlobalVariavel < ssqGlobalVariavel.size(); iter_ssqGlobalVariavel++)
	{
		float cor = ssqInterVariavel[iter_ssqGlobalVariavel]/ssqGlobalVariavel[iter_ssqGlobalVariavel];
		float ctr = ssqInterVariavel[iter_ssqGlobalVariavel]/b;
		cor_j.push_back(cor);
		ctr_j.push_back(ctr);
		fout_indices << "Variável " << iter_ssqGlobalVariavel << ": " << "COR(j): " << cor << " CTR(j): "<< ctr << endl;
	}

	int var = 0;
	int clust = 0;
	for(iter_ssqGlobalVariavel = 0; iter_ssqGlobalVariavel < ssqGlobalVariavel.size(); iter_ssqGlobalVariavel++)
	{
		clust = 0;
		for(iter_ssqGlobalCluster = 0; iter_ssqGlobalCluster < ssqGlobalCluster.size(); iter_ssqGlobalCluster++)
		{
			float cor = ssqInterClusterVariavel[iter_ssqGlobalVariavel][iter_ssqGlobalCluster]/ssqGlobalVariavel[iter_ssqGlobalVariavel];
			fout_indices << "Variavel/Cluster COR(j,k)" << var << "/" << clust << ": " << cor << " " << endl;
			float ctr = ssqInterClusterVariavel[iter_ssqGlobalVariavel][iter_ssqGlobalCluster]/ssqInterCluster[iter_ssqGlobalCluster];
			fout_indices << "Variavel/Cluster CTR(j,k)" << var << "/" << clust << ": " << ctr << " " << endl;
			clust++;
		}

		var++;
	}
	return particao;
}

float AdaptiveDCA::CalculaDistanciaEuclidiana(ObjetoSimbolico* objeto, ObjetoSimbolico* prototipo, int variavel)
{
	int Hj, h;
	float dist;
	float somatorioH;

	Hj = prototipo->histogramas[variavel]->GetHistograma().size();
	somatorioH = 0;
	for(h = 0; h < Hj; h++)
	{
		dist = pow(objeto->histogramas[variavel]->GetHistograma()[h] - prototipo->histogramas[variavel]->GetHistograma()[h],2);
		somatorioH += dist;
	}

	return somatorioH;
}

void AdaptiveDCA::AtualizaPrototipos(std::vector<ObjetoSimbolico*> prototipos){
	int k, j, Hj, h;
	int p;

	cout << "Atualizando protótipos..." << endl;
	for(k = 0; k < K; k++)
	{
		p = prototipos[k]->histogramas.size();
		for(j = 0; j < p; j++)
		{
			Hj = prototipos[k]->histogramas[j]->GetHistograma().size();
			for(h = 0; h < Hj; h++)
			{
				float soma_pesos_objetos = 0;
				for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
				{
					soma_pesos_objetos += ((ObjetoSimbolico*)*it)->histogramas[j]->GetHistograma()[h];
				}
				float peso_histo = soma_pesos_objetos/(float)particao[k]->objetos.size();
				prototipos[k]->histogramas[j]->GetHistograma()[h] = peso_histo;
				particao[k]->prototipo->histogramas[j]->GetHistograma()[h] = peso_histo;
			}
		}
	}
}

std::vector<Peso*> AdaptiveDCA::AtualizaPesos(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos, int single)
{
	int k, cluster_k;
	unsigned int numero_variaveis, j, l;
	//Vetor de lambdas para cada cluster
	std::vector<Peso*> lambdas_clusters;
	float distancia, somatorio_objetos, somatorio_clusters, produtorio_variaveis, numerador;

	cout << "\nAtualizando os pesos..." << endl;

	for(k = 0; k < K; k++)
	{
		cout << "\nCluster " << k << endl;
		Peso* peso = new Peso();
		//Número de histogramas = número de variáveis
		numero_variaveis = prototipos[k]->histogramas.size();
		for(j = 0; j < numero_variaveis; j++)
		{
			cout << "Variável " << j << endl;
			//Cálculo do numerador
			produtorio_variaveis = 1;
			for(l = 0; l < numero_variaveis; l++)
			{
				if(single)
				{
					somatorio_clusters = 0;
					for(cluster_k = 0; cluster_k < K; cluster_k++)
					{
						somatorio_objetos = 0;
						for(list<ObjetoSimbolico*>::iterator it = particao[cluster_k]->objetos.begin(); it != particao[cluster_k]->objetos.end(); it++)
						{
							distancia = CalculaDistanciaEuclidiana((ObjetoSimbolico*)*it, prototipos[cluster_k], l);
							somatorio_objetos += distancia;
						}
						somatorio_clusters += somatorio_objetos;
					}
					produtorio_variaveis *= somatorio_clusters;
				}
				else
				{
					somatorio_objetos = 0;
					for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
					{
						distancia = CalculaDistanciaEuclidiana((ObjetoSimbolico*)*it, prototipos[k], l);
						somatorio_objetos += distancia;
					}
					produtorio_variaveis *= somatorio_objetos;
				}
			}
			numerador = pow(produtorio_variaveis, 1/numero_variaveis);
			//Fim de Cálculo do numerador

			//Cálculo do denominador
			float somatorio_clusters2 = 0;
			if(single)
			{
				for(cluster_k = 0; cluster_k < K; cluster_k++)
				{
					somatorio_objetos = 0;
					for(list<ObjetoSimbolico*>::iterator it = particao[cluster_k]->objetos.begin(); it != particao[cluster_k]->objetos.end(); it++)
					{
						distancia = CalculaDistanciaEuclidiana((ObjetoSimbolico*)*it, prototipos[cluster_k], j);
						somatorio_objetos += distancia;
					}
					somatorio_clusters2 += somatorio_objetos;
				}
			}
			else
			{
				somatorio_objetos = 0;
				for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
				{
					distancia = CalculaDistanciaEuclidiana((ObjetoSimbolico*)*it, prototipos[k], j);
					somatorio_objetos += distancia;
				}
				somatorio_clusters2 = somatorio_objetos;
			}
			//Fim de Cálculo do denominador
			float lambda_j = numerador / somatorio_clusters2;
			cout << lambda_j << endl;
			peso->lambda.push_back(lambda_j);
		}
		lambdas_clusters.push_back(peso);
		particao[k]->pesos = peso;
	}
	return lambdas_clusters;
}

void AdaptiveDCA::AtualizaParticao(std::vector<ObjetoSimbolico*> objetos, std::vector<ObjetoSimbolico*> prototipos, std::vector<Peso*> lambdas_clusters)
{
	int k, cluster_prox, m;
	unsigned int objeto_i, distancia, cluster;
	float dist, menor_dist;

	cout << "Atualizando clusters..." << endl;
	test = 0;

	for(objeto_i = 0; objeto_i < objetos.size(); objeto_i++)
	{
		std::vector<float> distancias;
		for(k = 0; k < K; k++)
		{
			dist = CalculaDistanciaAdaptativa(objetos[objeto_i], prototipos[k], lambdas_clusters[k]->lambda);
			distancias.push_back(dist);
		}
		menor_dist = distancias[0];
		cluster_prox = 0;
		for(distancia = 1; distancia < distancias.size(); distancia++)
		{
			if(distancias[distancia] < menor_dist)
			{
				menor_dist = distancias[distancia];
				cluster_prox = (int)distancia;
			}
		}

		for(cluster = 0; cluster < particao.size(); cluster++)
		{
			if(particao[cluster]->Contains(objetos[objeto_i]))
			{
				m = cluster;
				if(m != cluster_prox)
				{
					test = 1;
					particao[cluster_prox]->objetos.push_back(objetos[objeto_i]);
//					int position = particao[cluster_prox]->GetPosition(objetos[objeto_i]);
					particao[m]->objetos.remove(objetos[objeto_i]);
				}
				break;
			}
		}
	}
}

float AdaptiveDCA::CalculaDistanciaAdaptativa(ObjetoSimbolico* objeto, ObjetoSimbolico* prototipo, std::vector<float> lambda)
{
	unsigned int j;
	int Hj, iter_hist;
	unsigned int numero_variaveis = prototipo->histogramas.size();
	float distanciaEucAdaptativa = 0;
	float distanciaEucAdaptativaVariavel;

	for(j = 0; j < numero_variaveis; j++)
	{
		float lambda_j = lambda[j];
		float soma_distancias = 0;
		Hj = objeto->histogramas[j]->GetHistograma().size();
		for(iter_hist = 0; iter_hist < Hj; iter_hist++)
		{
			soma_distancias += CalculaDistanciaEuclidiana(objeto, prototipo, j);
		}
		distanciaEucAdaptativaVariavel = lambda_j * soma_distancias;
		distanciaEucAdaptativa += distanciaEucAdaptativaVariavel;
	}
	return distanciaEucAdaptativa;
}

ObjetoSimbolico* AdaptiveDCA::CalculaPrototipoGeral(std::vector<ObjetoSimbolico*> objetos)
{
	ObjetoSimbolico* _prototipoGeral = new ObjetoSimbolico();
	unsigned int iter_obj;
	int iter_var, p, Hj, iter_hist;
	float soma_pesos_objetos;

	cout << "Calculando protótipo geral..." << endl;

	p = objetos[0]->histogramas.size();
	for(iter_var = 0; iter_var < p; iter_var++)
	{
		HistogramValued* histo = new HistogramValued();
		Hj = objetos[0]->histogramas[iter_var]->GetHistograma().size();
		std::vector<float> histograma;
		for(iter_hist = 0; iter_hist < Hj; iter_hist++)
		{
			soma_pesos_objetos = 0;
			for(iter_obj = 0; iter_obj < objetos.size(); iter_obj++)
			{
				soma_pesos_objetos += objetos[iter_obj]->histogramas[iter_var]->GetHistograma()[iter_hist];
			}
			histograma.push_back(soma_pesos_objetos / (float)objetos.size());
		}
		histo->SetHistograma(histograma);
		_prototipoGeral->histogramas.push_back(histo);
	}
	return _prototipoGeral;
}

float AdaptiveDCA::CalculaSomaDosQuadradosGeral()
{
	float soma_quadrados_geral = 0;
	unsigned int k;
	unsigned int j, numero_variaveis;
	float distanciaEucAdaptativaVariavel;
	float distEucAdapt, distAdapt;
	float distancia;

	for(k = 0; k < particao.size(); k++)
	{
		distAdapt = 0;
		for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
		{
			distAdapt += CalculaDistanciaAdaptativa((ObjetoSimbolico*)*it, prototipoGeral, particao[k]->pesos->lambda);
		}
		soma_quadrados_geral += distAdapt;
		ssqGlobalCluster.push_back(distAdapt);
	}

	numero_variaveis = particao[0]->prototipo->histogramas.size();
	for(j = 0; j < numero_variaveis; j++)
	{
		distanciaEucAdaptativaVariavel = 0;
		for(k = 0; k < particao.size(); k++)
		{
			float lambda_j = particao[k]->pesos->lambda[j];
			distEucAdapt = 0;
			for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
			{
				ObjetoSimbolico* objeto = (ObjetoSimbolico*)*it;

				distancia = CalculaDistanciaEuclidiana(objeto, prototipoGeral, j);

				distEucAdapt += lambda_j * distancia;
			}
			ssqGlobalClusterVariavel.push_back(distEucAdapt);
			distanciaEucAdaptativaVariavel += distEucAdapt;
		}
		ssqGlobalVariavel.push_back(distanciaEucAdaptativaVariavel);
	}

	return soma_quadrados_geral;
}

float AdaptiveDCA::CalculaSomaQuadradosIntraClasse(std::vector<ObjetoSimbolico*> prototipos)
{
	float soma_quadrados_intra = 0;
	float distEucAdapt, distAdapt;
	unsigned int j, numero_variaveis;
	float distanciaEucAdaptativaVariavel;
	float soma_distancias;
	unsigned int k;

	for(k = 0; k < particao.size(); k++)
	{
		distAdapt = 0;
		for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
		{
			distAdapt += CalculaDistanciaAdaptativa((ObjetoSimbolico*)*it, prototipos[k], particao[k]->pesos->lambda);
		}
		soma_quadrados_intra += distAdapt;
		ssqIntraCluster.push_back(distAdapt);
	}

	numero_variaveis = particao[0]->prototipo->histogramas.size();
	for(j = 0; j < numero_variaveis; j++)
	{
		distanciaEucAdaptativaVariavel = 0;
		for(k = 0; k < particao.size(); k++)
		{
			float lambda_j = particao[k]->pesos->lambda[j];
			distEucAdapt = 0;
			for(list<ObjetoSimbolico*>::iterator it = particao[k]->objetos.begin(); it != particao[k]->objetos.end(); it++)
			{

				ObjetoSimbolico* objeto = (ObjetoSimbolico*)*it;

				soma_distancias = CalculaDistanciaEuclidiana(objeto, prototipos[k], j);

				distEucAdapt += lambda_j * soma_distancias;
			}
			ssqIntraClusterVariavel.push_back(distEucAdapt);
			distanciaEucAdaptativaVariavel += distEucAdapt;
		}
		ssqIntraVariavel.push_back(distanciaEucAdaptativaVariavel);
	}

	return soma_quadrados_intra;
}

float AdaptiveDCA::CalculaSomaQuadradosInterClasses(std::vector<ObjetoSimbolico*> prototipos)
{
	float soma_quadrados_inter = 0;
	float distEucAdapt, distAdapt;
	unsigned int j, numero_variaveis;
	float distanciaEucAdaptativaVariavel;
	float soma_distancias;
	unsigned int k;

	for(k = 0; k < particao.size(); k++)
	{
		distAdapt = (float)particao[k]->objetos.size() * CalculaDistanciaAdaptativa(prototipos[k], prototipoGeral, particao[k]->pesos->lambda);
		soma_quadrados_inter += distAdapt;
		ssqInterCluster.push_back(distAdapt);
	}


	std::vector<float> ssqInterPorCluster;
	numero_variaveis = particao[0]->prototipo->histogramas.size();
	for(j = 0; j < numero_variaveis; j++)
	{
		distanciaEucAdaptativaVariavel = 0;
		for(k = 0; k < particao.size(); k++)
		{
			float lambda_j = particao[k]->pesos->lambda[j];
			distEucAdapt = 0;

			soma_distancias = CalculaDistanciaEuclidiana(prototipos[k], prototipoGeral, j);

			distEucAdapt += (float)particao[k]->objetos.size() * lambda_j * soma_distancias;

			ssqInterPorCluster.push_back(distEucAdapt);
			distanciaEucAdaptativaVariavel += distEucAdapt;
		}
		ssqInterClusterVariavel.push_back(ssqInterPorCluster);
		ssqInterVariavel.push_back(distanciaEucAdaptativaVariavel);
	}

	return soma_quadrados_inter;
}

AdaptiveDCA::~AdaptiveDCA() {
	// TODO Auto-generated destructor stub
}
