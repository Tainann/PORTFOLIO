# É preciso otimizar o lucro de uma sapataria.
# O sapateiro produz 5 sapatos(x1) ou 5 cintos(x2) em uma hora.
# 10x1 + 12x2 <=60
# Cada sapato é vendido por 5 reais
# Cada cinto é vendido por 2 reais
# Cada sapato consome duas peças de couro.
# Cada sapato cosome uma peça de couro.
# 2x1 + x2 <= 6
# x1 e x2 sempre >=0.
# Restrições:
    # tempo = 60 minutos
    # matéria-prima = 6 peças de couro.



####
# Irei criei subclasses de AGLDE
# As subclasses podem ter atributos e métodos próximos
####
 
from AGLDE import *

class Sapataria(AGLDE): # Criando sublclasses da superclasse AGLDE

    def __init__(self, tPopulacao, qtdGenes, tMutacao, tElitismo): # Método consrutor
        super().__init__(tPopulacao, qtdGenes, tMutacao, tElitismo) # Construtor da superclasses

    def fitness(self, cromossomo): # Cromossomo será dividido em dois subgrupos de 4 dígitos (x1 e x2)
        valores = self.leituraDeValores(cromossomo, 4)
        valores = self.getDecimal(valores)
        x1 = valores[0]
        x2 = valores[1]
        nota = 5*x1 + 2*x2

        if not ((10*x1 + 12*x2) <= 60 and (2*x1 +x2) <= 6 and x1>= 0 and x2>= 0):
            nota = 0

        return [cromossomo, nota]


ags = Sapataria(10, 8, 0.05, 0.1)
ags.runAG(100)
print(ags.obtemMelhorIndividuo()) # Obtem o melhor indivíduo de todos
valores = ags.leituraDeValores(ags.obtemMelhorIndividuo()[0], 4)
print(ags.getDecimal(valores))