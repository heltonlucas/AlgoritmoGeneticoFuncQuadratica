# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 10:35:35 2017

@author: helto
"""
import random
import math
import numpy as np
import matplotlib.pyplot as plt

GERACOES = 20
TAM_POPULACAO = 100
NUM_CROMOSSOMOS_ELITE = 1
TAM_SELECAO_TORNEIO = 4
TAXA_DE_MUTACAO = 0.05
#CROMOSSOMO_ALVO = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0]

limite_inferior = -10
limite_superior = 10
precisao = 1

quantidade_possibilidades = (limite_superior - limite_inferior) * (10 ** precisao)
tam_cromossomo  =  math.ceil(math.log(quantidade_possibilidades, 2))

print ("Tamanho cromossomo (bits): ", tam_cromossomo) 
print ("Quantidade de possibilidades: ", quantidade_possibilidades) 

# Calcula tamanho do cromossomo (Bits) de acordo com o limite inferior e superior
#tam_cromossomo  =  math.ceil (math.log((limite_superior-(limite_inferior)*((10 ** precisao) + 1)),2)) 

CROMOSSOMO_ALVO = [0]*tam_cromossomo
                  
for i in range(tam_cromossomo):
    CROMOSSOMO_ALVO [i] = random.randint(1,1)
print ("Cromossomo Random: ", CROMOSSOMO_ALVO)

soma = 0
potencia = tam_cromossomo - 1

for i in range (tam_cromossomo):
    soma = soma + (CROMOSSOMO_ALVO[i] * (2 ** potencia))
    potencia = potencia - 1
    val_decimal = limite_inferior + soma * ((limite_superior - (limite_inferior)) / (quantidade_possibilidades))

print ("Conversao Inteiro: ", soma)
print ("Valor Decimal: ", val_decimal)

class Cromossomo:
    
    def cromossomo_randon(self):
        ''''''
    
    ''' Metodo para gerar 1 ou 0 e preencher o array de bits do cromossomo'''
    def __init__(self):
        self._genes = []
        self._fitness = 0 
        i = 0
        while i < CROMOSSOMO_ALVO.__len__(): 
            if random.random() >= 0.5:
                self._genes.append(1)
            else:
                self._genes.append(0)
            i += 1
        
    def get_genes(self):
        return self._genes
    
    
    ''' Metodo calcular o Fitness '''    
    def get_fitness(self):
        self._fitness = 0
        val_inteiro = 0
        potencia = tam_cromossomo - 1
        fitness_total = 0
        fitness_average = 0
 
        for i in range (self._genes.__len__()):
            
            ''' Valores inteiros dos individuos (fitness) '''    
            val_inteiro = val_inteiro + (self._genes[i] * (2 ** potencia))
            
            ''' Valores decimais dos individuos (fitness) '''
#            val_decimal = val_inteiro / (10 ** precisao)
            val_decimal = limite_inferior + val_inteiro * ((limite_superior - (limite_inferior)) / (quantidade_possibilidades))
            potencia = potencia - 1
            
            ''' Valores decimais dos individuos na funcao de X^2 '''    
            self._fitness = math.pow (val_decimal,2)
#
            fitness_total = fitness_total + self._fitness
        
        self.fitness_average = fitness_total/TAM_POPULACAO
        
#        print("Fit total", fitness_average)
        return self._fitness

    def somarLista(self):
        return self.fitness_average

    
    def __srt__(self):
        return self._genes.__str__()    
    
class Populacao:
    def __init__(self, size):
        self._cromossomos = []
        i = 0
        while i < size:
            self._cromossomos.append(Cromossomo())
            i += 1
            
    def get_cromossomos(self): return self._cromossomos


class AlgoritmoGenetico:
    @staticmethod
    def evoluir(pop): 
        return AlgoritmoGenetico._mutacao_populacao(AlgoritmoGenetico._crossover_populacao(pop))
    
    ''' Recebe dois individuos, ponto de crossover é a metade do individuo, retorna individuo resultante '''
    @staticmethod
    def _crossover_populacao(pop):
        crossover_pop = Populacao(0)
        for i in range(NUM_CROMOSSOMOS_ELITE):
            crossover_pop.get_cromossomos().append(pop.get_cromossomos()[i])
        i = NUM_CROMOSSOMOS_ELITE
        while i < TAM_POPULACAO:
            cromossomo1 = AlgoritmoGenetico._selecao_pop_torneio(pop).get_cromossomos()[0]
            cromossomo2 = AlgoritmoGenetico._selecao_pop_torneio(pop).get_cromossomos()[0]
            crossover_pop.get_cromossomos().append(AlgoritmoGenetico._crossover_cromossomos(cromossomo1, cromossomo2))
            i += 1
        return crossover_pop

    ''' Metodo de mutacao '''
    ''' Copia da melhor solucao da geração é passada para a nova populacao (elitismo)'''
    @staticmethod
    def _mutacao_populacao(pop):
        for i in range(NUM_CROMOSSOMOS_ELITE, TAM_POPULACAO):
            AlgoritmoGenetico._mutacao_cromossomo(pop.get_cromossomos() [i])
        
        return pop
    
    @staticmethod
    def _crossover_cromossomos(cromossomo1, cromossomo2):
        crossover_cromos = Cromossomo()
        for i in range (CROMOSSOMO_ALVO.__len__()):
            if random.random() >= 0.5:
                crossover_cromos.get_genes()[i] = cromossomo1.get_genes() [i]
            
            else:
                crossover_cromos.get_genes()[i] = cromossomo2.get_genes() [i]
        return crossover_cromos
    

    '''Executa a mutação da primeira posicao de 4% da populacao'''
    @staticmethod
    def _mutacao_cromossomo(cromossomo):
        for i in range(CROMOSSOMO_ALVO.__len__()):
            if random.random() < TAXA_DE_MUTACAO:
                if random.random() < 0.5:
                    cromossomo.get_genes() [i] = 1
                else:
                    cromossomo.get_genes() [i] = 0
                                        
                                        
    ''' Percorre a lista de fitness e seleciona os individuos por torneio '''
    ''' Retorna vencedores de menor Fitness'''
    @staticmethod
    def _selecao_pop_torneio(pop):
        torneio_pop = Populacao(0)
        i = 0
        while i < TAM_SELECAO_TORNEIO:
            torneio_pop.get_cromossomos().append(pop.get_cromossomos()[random.randrange(0, TAM_POPULACAO)])
            i += 1
        # Ordenar usando parametro "key" do metodo "sort" pelo fitness, atributo get_fitness()
        # lambda funcao anonima,que recebe uma entrada (a variável x) - So é usada aqui no trecho de 
        # reverse = True, odenar decrescentemente
        torneio_pop.get_cromossomos().sort(key=lambda x: x.get_fitness(), reverse=True)
        return torneio_pop
    
    
def plot_Output():
#        data = np.loadtxt('output.txt')
#        # plot the first column as x, and second column as y
#        x=data[:,0]
#        y=data[:,1]
#        plt.plot(x,y)          
        plt.xlabel('Gerações')       
        plt.ylabel('Fitness Media')
        x = np.linspace(limite_inferior,limite_superior)
        y = x**2
        plt.plot(x,y)    
        plt.show()
#    
    
def _print_populacao(pop, numero_ger):
    print("\n--------------------------------------------------------------------")
    print("Geração ->", numero_ger, "| Física cromossômica mais Apta: %.3f" % pop.get_cromossomos()[0].get_fitness())
#    print("Fitness Medio:", pop.get_cromossomos()[0].fitness_average)
    print("-------------------------------------------------------------------")
    i = 0 
    for x in pop.get_cromossomos():
        print("Cromossomo -->", i, " :", x.get_genes(), "| Fitness: %.4f" % x.get_fitness())
        i += 1

populacao = Populacao(TAM_POPULACAO)
populacao.get_cromossomos().sort(key=lambda x: x.get_fitness(), reverse=True)
_print_populacao(populacao, 0)
numero_geracao = 1

'''Ver resultados com n GERACOES ?'''
#conta = 0
#while (conta <= GERACOES):
#    conta += 1
#    
'''Ver resultados com cromossomo alvo ?'''
while populacao.get_cromossomos()[0].get_fitness() < CROMOSSOMO_ALVO.__len__():
    populacao = AlgoritmoGenetico.evoluir(populacao)
    populacao.get_cromossomos().sort(key=lambda x: x.get_fitness(), reverse=True)
    _print_populacao(populacao, numero_geracao)
    numero_geracao += 1


#plt.xlabel('Gerações')       
#plt.ylabel('Fitness Media')
#x = np.linspace(limite_inferior,limite_superior)
#y = x**2
#plt.plot(x,y)          
#plt.show ()

#plot_Output()


        
    
    
    
    
    
            
            
    
    
    
    
    
    