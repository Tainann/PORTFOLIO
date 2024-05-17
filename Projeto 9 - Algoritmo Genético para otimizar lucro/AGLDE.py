
#################
# ESSE ARQUIVO É O ALGORITMO EM FORMA DE BIBLIOTECA QUE VOU USAR NOS CÓDIGOS DE OTIMIZAÇÃO DE LUCRO
# AQUI populacao PASSOU A SER UM ATRIBUTO DA CLASSE PARA ASSIM SER CHAMADA NO MÉTODO obtemMelhorIndividuo
################



import random


class AGLDE:

    # SELF INDICA QUE ALGO PERTENCE À CLASSE
    def __init__(self, tPopulacao, qtdGenes, tMutacao, tElitismo): # Todas as funções enxergam o que é definido aqui
        self.tPopulacao = tPopulacao
        self.qtdGenes = qtdGenes
        self.tMutacao = tMutacao
        self.tElitismo = tElitismo


    def criaCromossomo(self, nGenes):
        cromossomo = ""

        for i in range(nGenes):
            gene = str(random.randint(0, 1))
            cromossomo = str(cromossomo) + str(gene) # Garantindo que os operandos são strings

        return cromossomo

    
    # Criando população inicial de cromossomos
    def criaPopulacao(self, nCromossomos, nGenes):
        populacao = []

        for i in range(nCromossomos):
            cromossomo = self.criaCromossomo(nGenes)
            populacao.append(cromossomo)

        return populacao
    
    # Definindo quantos dígitos vão haver dentro de cada subgrupo do cromossomo
    def leituraDeValores(self, cromossomo, tCadeia):
        grupo = []

        subgrupos = []
        valor = ""
        for i in range(1, len(cromossomo)+1):
            valor = str(valor) + str(cromossomo[i-1]) # Garantindo que os operandos são strings
            if i % tCadeia == 0:
                subgrupos.append(valor)
                valor = ""

        return subgrupos
    
    # Converte cada subgrupo de binário para decimal
    def getDecimal(self, lsBinaria):
        valoresDecimais = []

        for i in lsBinaria:
            valoresDecimais.append(int(i, 2))

        return valoresDecimais
  
    # Recebe um cromossomo e calcula a sua nota de aptidão;
    # A rotina devolve uma lista contendo dois elementos, sendo o primeiro deles
    # o próprio cromossomo avaliado e o segundo é a sua nota de aptidão.
    def fitness(self, cromossomo):
        pass


    # Recebe dois cromossomos e devolve aquele que possui maior nota de aptidão.
    # O cálculo da nota de aptidão é feito utilizando-se a função fitness.
    def selecionaIndividuo(self, cromossomo1, cromossomo2):
        if (self.fitness(cromossomo1))[1] > (self.fitness(cromossomo2))[1]:
            return cromossomo1
        else:
            return cromossomo2
  
    # Recebe dois cromossomos e retorna um novo gerado a partir da operação de
    # crossover realizada entre eles. O crossover é feito com divisão central.
    def crossover(self, cromossomo1, cromossomo2):
        if len(cromossomo1) % 2 != 0: # Garantindo que o tamanho é par
            cromossomo1 = "0" + cromossomo1
        if len(cromossomo2) % 2 != 0: # Garantindo que o tamanho é par
            cromossomo2 = "0" + cromossomo2
        if len(cromossomo1) > len(cromossomo2): # Garantindo que têm o mesmo tamanho
            digitosExtras = len(cromossomo1) - len(cromossomo2)
            cromossomo2 = ("0" * digitosExtras) + cromossomo2 # Add 0 à esquerda não muda um número binário
        if len(cromossomo2) > len(cromossomo1): # Garantindo que têm o mesmo tamanho
            digitosExtras = len(cromossomo2) - len(cromossomo1)
            cromossomo1 = ("0" * digitosExtras) + cromossomo1 # Add 0 à esquerda não muda um número binário

        parte1 = cromossomo1[0:int(len(cromossomo1)/2)]
        parte2 = cromossomo2[int(len(cromossomo2)/2):]
        novoCromossomo = str(parte1) + str(parte2)

        return novoCromossomo
   
    # Realiza a mutação de cada um dos genes do nosso cromossomo de acordo com
    # uma taxa específica.
    def mutation(self, cromossomo, tMutacao):
        lgenes = list(cromossomo) # Convertendo de string para lista

        for i in range(len(cromossomo)): # Mutação será analisada para cada gene do  cromossomo
            sorteio = random.random()
            if sorteio <= tMutacao: # A mutação ocorre se o valor sorteado é menor que a taxa de mutação
                if lgenes[i] == "0": 
                    lgenes[i] = "1"
                else:
                    lgenes[i] = "0"

        cromossomo = "".join(lgenes) # Atualizando o cromossomo

        return cromossomo
    
    # Verifica dentro da população de cromossomos qual é o indivíduo que possui
    # a melhor nota de aptidão. Retorna o cromossomo com melhor aptidão.
    def obtemMelhorIndividuo(self):
        # Escolhe um cromossomo aleatório como o melhor
        melhorIndividuo = self.fitness(self.populacao[random.randint(0, len(self.populacao) - 1)])

        for i in self.populacao:
            individuo = self.fitness(i)

            if individuo[1] > melhorIndividuo[1]:
                melhorIndividuo = individuo

        return melhorIndividuo
    
    # Serão gerados clones para a próxima do melhor indivíduo da geração atual
    def elitismo(self, populacao, telitismo):
        novaPopulacao = []

        melhorindividuo = self.obtemMelhorIndividuo()
        numeroRepeticoes = int(len(populacao) * telitismo)
        
        for i in range(numeroRepeticoes):
            novaPopulacao.append(melhorindividuo[0])

        return novaPopulacao
 
    # Essa rotina recebe uma população de indivíduos, aplica as operações do
    # do algoritmo genético a cada um deles, gerando uma nova população de
    # indivíduos com a mesma quantidade de elementos da população inicial.
    def geraNovaPopulacao(self, populacaoInicial, tMutation, tElitismo):
        # O elitismo é aplicado para selecionar o melhor indivíduo e gerar n clones dele
        # O crossover é aplicado selecionando indivíduos entre toda a populaçao atual
        # Uma outra forma de aplicar o crossover poderia ser ordenar a população de acordo com a nota de cada indivíduo,
        # então fatiar a população para ficar com os y melhores para aplicar o crossover só nesses indivíduos que se tem certeza que são bem avaliados 
        novaPopulacao = self.elitismo(populacaoInicial, tElitismo)

        while len(novaPopulacao) < len(populacaoInicial):
            i1 = random.randint(0, len(populacaoInicial) - 1)
            i2 = random.randint(0, len(populacaoInicial) - 1)
            selecionado1 = populacaoInicial[i1]
            selecionado2 = populacaoInicial[i2]
            individuoMaisApto1 = self.selecionaIndividuo(selecionado1, selecionado2)

            i1 = random.randint(0, len(populacaoInicial) - 1)
            i2 = random.randint(0, len(populacaoInicial) - 1)
            selecionado1 = populacaoInicial[i1]
            selecionado2 = populacaoInicial[i2]
            individuoMaisApto2 = self.selecionaIndividuo(selecionado1, selecionado2)

            novoIndividuo = self.crossover(individuoMaisApto1, individuoMaisApto2)
            filho = self.mutation(novoIndividuo, tMutation)

            novaPopulacao.append(filho)

        return novaPopulacao

    ### EXECUÇÃO DO ALGORITMO GENÉTICO
    def runAG(self, nGeracoes):
        self.populacao = self.criaPopulacao(self.tPopulacao, self.qtdGenes) # Criando 10 cromossomos com 20 genes
        for i in range(nGeracoes):
            melhorIndividuo = self.obtemMelhorIndividuo() 
            self.populacao = self.geraNovaPopulacao(self.populacao, self.tMutacao, self.tElitismo)
        
        return melhorIndividuo

