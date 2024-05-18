from random import random
import matplotlib.pyplot as plt
import pymysql

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
    
    # Individuos representam as solucoes (quais produtos irao ou nao para a viagem)
    # População é o conjunto de individuos (conunto de solucoes do problema)
    # O cromossomo é uma solução
    # O indivuduo pode ser o propio cromossomo ou conter o cromossomo como atributo
class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []
            
        # Cromossomo está sendo definido de forma aleatoria
        # 1 indica que o produto será transportado
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")

    # Função fitness serve para avaliar como o cromossomo resolve o problema. Se é aceitável e 
    # pode ser usada para evolucao
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
        
        # O ponto de corte do crossover não importa
        # Crossover combina pedaços do cromossomo de dois genitores gerando filhos mais aptos
        # Representa a reprodução sexuada
    def crossover(self, outro_individuo):
        # round() arredonda numeros
        # random() retorna um numero entre 0 e 1
        corte = round(random()  * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
    
        # Mutacao cria diversidade mudando aleatoriamente genes dentro de individuos
        # Menos frequente que a reproducao
        # Possui uma taxa associada a uma probabilidade extremamente baixa para alterar um gene
    def mutacao(self, taxa_mutacao):
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("Depois %s " % self.cromossomo)
        return self
     
# Abaixo está o algoritmo genético em si
# Essa é a classe principal do projeto  
# Classe 1: Produtos com seus atributos
# Classe 2: Indivíduos (soluções) com seus métodos e atributos
# Classe 3: População (conjunto de indivíduos)
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
        # Abaixo são criados varios individuos (solucoes), e cada um deles
        # é dotado de mutacao, crossover, avaliacao, cromossomo...
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]      
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma
    
    # Mutacao e crossover devem ser aplicados em individuos selecionados da populacao
    # Os individuos mais aptos devem ser selecionados mais frequentemente que os menos aptos
    # Deve simular o mecanismo de selecao natural das especies biologicas, em que
    # pais mais capazes geram mais filhos. Os pais menos aptos também geram descendentes.
    # É importante não desprezar totalmente os menos aptos para manter diversidade dentro do algoritmo
    # Algum individuo menos apto pode ter alguma caracteristica util para o algoritmo e não deve ser ignorado.
    # Método da roleta viciada: cada cromossomo recebe um pedaço proporcional à sua avaliacao e a 
    # roleta é rodada
    def seleciona_pai(self, soma_avaliacao):
        pai = -1 # nao selecionou nenhum individuo ainda
        valor_sorteado = random() * soma_avaliacao # Simula a roleta sendo girada
        soma = 0
        i = 0
        # Os individuos menos aptos tem nota 1, então dificilmente serão escolhidos na roleta
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        # Em populacao[0] está o melhor individuo dessa geração
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
    # A funcao abaixo faz tudo junto o que as outras fazem
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)
        # populacao[0] foi salvo dentro de melhor_solucao
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        # Coloca o melhor da geração 0 como melhor_solucao
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        # Irá mostrar o melhor individuo da geração 1
        self.visualiza_geracao()
        
        # O critério de parada do algoritmo será chegar na geração 100
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                # A parte mais importante é a roleta
                # A roleta irá aumentar a eficiencia da solucao por escolher mais
                # os individuos mais aptos
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao) # Apagada geração anterior
            # A quantidade de indivíduos é constante nas gerações
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao() # Vendo o melhor de cada geracao
            
            melhor = self.populacao[0]
            # Verifica se o melhor da geração atual é melhor que o que está salvo como melhor até o momento
            self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s \nValor: %s \nEspaço: %s \nCromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo
        
        
if __name__ == '__main__':
    # Tudo dentro de main não vai precisar mais de crtl + enter para rodar mais
    # p1 = Produto('Iphone 6', 0.0000899, 2199.12)
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
    #for produto in lista_produtos:
    #    print(produto.nome)
    
    espacos = []
    valores = []
    nomes = []
    # Colocando as caracteristicas dos produtos em listas
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3 # 3m^3 é o limite de espaço no caminhão
    tamanho_populacao = 60
    taxa_mutacao = 0.01
    numero_geracoes = 1000
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
            
    #for valor in (ag.lista_solucoes):
    #    print(valor)
    # É IMPORTANTE RODAR O ALGORITMO VÁRIAS VEZES PARA ACHAR A MELHOR SOLUÇÃO POSSÍVEL
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show()
            
    


