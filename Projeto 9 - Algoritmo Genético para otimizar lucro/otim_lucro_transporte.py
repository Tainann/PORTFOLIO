# Objetivo é otimizar o lucro de transporte.
# Um centro de coleta A recebe  os produtos dos vendedores.
# Os motoboys desse centro irão levar os produtos para o centro de distribuição.
# Nesse centro de distribuição, os produtos chegarão ao cliente final.

# Cada produto tem registrado o seu volume e o preço.
# Em um cromossomo, cada gene significa um produto.
# 1 indica que o item será transportado.

# A RESTRIÇÃO É QUE O SOMATÓRIO DO VOLUME NÃO SEJA MAIOR QUE O ESPAÇO DA MOTO.

from AGLDE import *

class Motoboy(AGLDE):
    def __init__(self, tPopulacao, qtdGenes, tMutacao, tElitismo):
        super().__init__(tPopulacao, qtdGenes, tMutacao, tElitismo)

        self.itens = [
                    ["Celular", 0.000899, 15],
                    ["Notebook", 0.00350, 18],
                    ["Furadeira", 0.06075, 9],
                    ["Carteira Masculina", 0.00008, 4],
                    ["Livro", 0.00095, 5],
                    ["Vídeo Game", 0.050635, 18],
                    ["Almofada Couro", 0.0225, 5],
                    ["Liquidificador", 0.03125, 9],
                    ["Jogo de Pratos", 0.072, 12],
                    ["Anel de Ouro", 0.000048, 19]
            ]
        self.espacoBau = 0.162
        
    def fitness(self, cromossomo):
        genes = self.leituraDeValores(cromossomo, 1)

        pagamentoAcumulado = 0
        espacoAcumulado = 0

        for i in range(len(self.itens)):
            if genes[i] == "1":
                pagamentoAcumulado += self.itens[i][2]
                espacoAcumulado += self.itens[i][1]

        if espacoAcumulado > self.espacoBau:
            nota = 1/espacoAcumulado
        else:
            nota = pagamentoAcumulado

        return [cromossomo, nota]

agmotoboy = Motoboy(150, 10, 0.05, 0.1)
agmotoboy.runAG(250)
melhor = agmotoboy.obtemMelhorIndividuo()
print(melhor)

count = 0
espaco = 0
for i, j in enumerate(melhor[0]):
    if j == "1":
        print('%-20s -- R$%s' % (agmotoboy.itens[i][0], agmotoboy.itens[i][2]))
        count += agmotoboy.itens[i][2]
        espaco += agmotoboy.itens[i][1]
total = 'Valor total'
print('%-20s -- RS%s' % (total, count))
print('\n')
print(f'Espaço ocupado: {espaco}')
