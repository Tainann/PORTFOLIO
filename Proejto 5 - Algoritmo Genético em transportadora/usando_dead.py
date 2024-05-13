import random
import numpy
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
lista_produtos = []
lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))

espacos = []
valores = []
nomes = []
for produto in lista_produtos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nomes.append(produto.nome)
limite = 3

# Serve para Registrar e organizar as diferentes operações e funções que serão 
# usadas em algoritmos evolutivos.
toolbox = base.Toolbox()

# Abaixo indica que quanto mais perto de 1, melhor o resultado. 
# Fitness maximizadora
# Indica que cada individuo tera uma funcao maximizadora de 0 a 1
creator.create("FitnessMax", base.Fitness, weights=(1.0, )) 

# Cria a classe Individual
# Cada indivíduo terá uma lista como sua representação cromossômica e 
# uma função de fitness associada a ele.
creator.create("Individual", list, fitness=creator.FitnessMax)

# Usada para gerar valores booleanos aleatórios (0 ou 1) que representam genes em um cromossomo
toolbox.register("attr_bool", random.randint, 0, 1) 

# individual irá criar indivíduos para a população. Esta função utiliza 
# tools.initRepeat para inicializar uma lista de genes (cromossomo) para um indivíduo. 
# A função initRepeat recebe como argumentos o tipo de indivíduo 
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, n=len(espacos))

# Esta função será usada para criar uma população de indivíduos. Ela utiliza 
# tools.initRepeat para criar uma lista de indivíduos, chamando a função individual
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
       if individual[i] == 1:
           nota += valores[i]
           soma_espacos += espacos[i]
    if soma_espacos > limite:
        nota = 1
    return nota / 100000,

# Dizendo o tipo de crossover
# Definindo a funcao avaliacao para avaliar a aptidão (fitness) de um indivíduo
toolbox.register("evaluate", avaliacao)

# Realizando o crossover a partir de um ponto aleatorio dos pais
toolbox.register("mate", tools.cxOnePoint)

# Configurando a mutacao
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01)

# Selecao pela roleta viciada
toolbox.register("select", tools.selRoulette)

if __name__ == "__main__":
    #random.seed(1)
    populacao = toolbox.population(n = 40)
    probabilidade_crossover = 1.0 # Sempre irá fazer crossover
    probabilidade_mutacao = 0.01
    numero_geracoes = 500
    
    # Definindo cálculos estatísticos para cada geração
    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    estatisticas.register("max", numpy.max)
    estatisticas.register("min", numpy.min)
    estatisticas.register("med", numpy.mean)
    estatisticas.register("std", numpy.std)
    
    # O trecho de codigo de 4 linhas abaixo é o alg. genetico em si
    # toolbox irá chamar funcao avaliacao. Assim o alg genetico irá agir
    # sobre todos os individuos de todas as geracoes.
    populacao, info = algorithms.eaSimple(populacao, toolbox,
                                          probabilidade_crossover,
                                          probabilidade_mutacao,
                                          numero_geracoes, estatisticas)
    
    melhores = tools.selBest(populacao, 1)
    # Selecionando os melhores individuos
    for individuo in melhores:
        print(individuo)
        print(individuo.fitness)
        #print(individuo[1])
        soma = 0
        for i in range(len(lista_produtos)):
            if individuo[i] == 1:
                soma += valores[i]
                print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                           lista_produtos[i].valor))
        print("Melhor solução: %s" % soma)
        
    # Selecionando os valores máximos de fitness registrados durante a evolução
    valores_grafico = info.select("max")
    plt.plot(valores_grafico)
    plt.title("Acompanhamento dos valores")
    plt.show()