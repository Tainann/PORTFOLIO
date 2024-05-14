import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os

# Função da curva de Weibull
def weibull(x, c, k):
    return (k/c) * ((x/c)**(k-1)) * np.exp(-(x/c)**k)

def leitura_dados(dados_sem_null):
    # Remover valores zeros da coluna escolhida
    dados_sem_null_sem_0 = dados_sem_null[dados_sem_null != 0]
    # Definindo os limites dos bins
    limites_bins = np.arange(0, max(dados_sem_null) + 0.5, 0.5)
    # Calcular a média dos valores em dados_sem_null
    media_dados_sem_null = np.mean(dados_sem_null) # Calculando a média da panda Series

    return dados_sem_null_sem_0, limites_bins, media_dados_sem_null

# Busca o arquivo com os dados
dados = pd.read_excel('SAO_LUIS_2022.xlsx', decimal=',')
dados_sem_null = dados['VENTO, VELOCIDADE HORARIA (m/s)'].dropna()

dados_sem_null_sem_0, limites_bins, media_dados_sem_null = leitura_dados(dados_sem_null)

c = 2.14
k = 1.33
velocidades = np.arange(0, max(limites_bins)+0.5, 0.5)
print(limites_bins)
print(velocidades)
#display(velocidades)
frequencias = weibull(velocidades, c, k)
print(frequencias)

# Dados da curva de potência da Turbina A
velocidades_xzeres = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 8.0, 9.0, 10.0, 10.5, 11.0, 12.0, 13.0, 14.0, 15.0])  # Velocidades do vento em m/s
potencia_xzeres = np.array([0, 0, 0, 0, 0, 25, 50, 70, 100, 180, 250, 370, 1000, 1300, 1750, 2000, 2100, 2100, 2100, 2100, 2100])  # Potência em kW

# Dados da curva de potência da Turbina B
velocidades_kestrel = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 12, 13, 14, 15])  # Velocidades do vento em m/s
potencia_kestrel = np.array([0, 0, 0, 0, 0, 100, 200, 300, 400, 500, 650, 800, 1000, 1250, 1500, 1750, 2100, 2450, 2750, 3000, 3250, 3400, 3500, 3500, 3500, 3500, 3500])  # Potência em kW

# Criando uma função interpoladora cúbica para suavizar as curvas
f_xzeres = interp1d(velocidades_xzeres, potencia_xzeres, kind='cubic')
f_kestrel = interp1d(velocidades_kestrel, potencia_kestrel, kind='cubic')

# Criando novos dados suavizados
potencia_xzeres_smooth = f_xzeres(velocidades)
potencia_kestrel_smooth = f_kestrel(velocidades)

energia_xzeres = frequencias * potencia_xzeres_smooth
energia_kestrel = frequencias * potencia_kestrel_smooth 

# Criando o Data Frame para Xzeres
# Especifique os nomes das colunas
nomes_colunas = ['Velocidade do vento (m/s)', 'Frequência de ocorrência', 'Potência do aerogerador (W)', 'f(v)*P(v) (W)']

# Calculando o total de energia
total_kestrel = np.sum(energia_kestrel)
total_xzeres = np.sum(energia_xzeres)
ead_kestrel = total_kestrel * 8760
ead_xzeres = total_xzeres * 8760

print(f'EAD da turbina Kestrel: {ead_kestrel/1000000:.2f} MW')
print(f'EAD da turbina Xzeres: {ead_xzeres/1000000:.2f} MW')

############################################################################################
# Criação das tabelas para Kestrel

# Adicionando o total de energia ao final da lista de energia_kestrel
energia_kestrel = np.append(energia_kestrel, total_kestrel)
energia_kestrel = np.round(energia_kestrel, 3)
print(energia_kestrel)

velocidades = np.append(velocidades, 'Total')
frequencias = np.round(frequencias, 3)
frequencias = np.append(frequencias, '')
potencia_kestrel_smooth = np.round(potencia_kestrel_smooth, 3)
potencia_kestrel_smooth = np.append(potencia_kestrel_smooth, '')

# Crie o DataFrame usando pd.DataFrame()
tabela_kestrel = pd.DataFrame({nomes_colunas[0]: velocidades,
                   nomes_colunas[1]: frequencias,
                   nomes_colunas[2]: potencia_kestrel_smooth,
                   nomes_colunas[3]: energia_kestrel})

# Substituir ponto por vírgula nos valores das células
tabela_kestrel = tabela_kestrel.map(lambda x: str(x).replace('.', ','))

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Salvando o DataFrame como um arquivo CSV na mesma pasta do script
caminho_arquivo = os.path.join(diretorio_atual, 'tabela_kestrel_SAO_LUIS_2022.csv')
tabela_kestrel.to_csv(caminho_arquivo, index=False)


########################################################################################
# Criação das tabela para Xzeres
# Adicionando o total de energia ao final da lista de energia_kestrel

energia_xzeres = np.append(energia_xzeres, total_xzeres)
energia_xzeres = np.round(energia_xzeres, 3)

potencia_xzeres_smooth = np.round(potencia_xzeres_smooth, 3)
potencia_xzeres_smooth = np.append(potencia_xzeres_smooth, '')

# Crie o DataFrame usando pd.DataFrame()
tabela_xzeres = pd.DataFrame({nomes_colunas[0]: velocidades,
                   nomes_colunas[1]: frequencias,
                   nomes_colunas[2]: potencia_xzeres_smooth,
                   nomes_colunas[3]: energia_xzeres})
tabela_xzeres = tabela_xzeres.round(3)

tabela_xzeres = tabela_xzeres.round(3)
# Substituir ponto por vírgula nos valores das células
tabela_xzeres = tabela_xzeres.map(lambda x: str(x).replace('.', ','))


diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Salvando o DataFrame como um arquivo CSV na mesma pasta do script
caminho_arquivo = os.path.join(diretorio_atual, 'tabela_xzeres_SAO_LUIS_2022.csv')
tabela_xzeres.to_csv(caminho_arquivo, index=False)
