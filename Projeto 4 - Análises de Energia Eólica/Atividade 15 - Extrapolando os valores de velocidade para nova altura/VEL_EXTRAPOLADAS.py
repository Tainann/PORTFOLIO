import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os

def leitura_dados(dados_sem_null):
    # Remover valores zeros da coluna escolhida
    dados_sem_null_sem_0 = dados_sem_null[dados_sem_null != 0]
    # Definindo os limites dos bins
    limites_bins = np.arange(0, max(dados_sem_null) + 0.5, 0.5)
    # Calcular a média dos valores em dados_sem_null
    media_dados_sem_null = np.mean(dados_sem_null) # Calculando a média da panda Series

    return dados_sem_null_sem_0, limites_bins, media_dados_sem_null

def metodo_log(velocidades, z0, h1, h2):
    return velocidades*(math.log(h2/z0))/(math.log(h1/z0))

def exponencial(v1, h1, h2, alfa):
    return v1 * (h2/h1) ** alfa

# Busca o arquivo com os dados
dados = pd.read_excel('ATIVIDADE_4.xlsx', sheet_name='UNIAO', decimal=',')

# Agrupar por ano e nome do mês e calcular a média
dados = dados[['Mês', 'ws_25', 'ws_50']]
dados_agrupados = dados.groupby(['Mês']).mean()
meses = dados_agrupados.index
dados_agrupados.reset_index()
print(dados_agrupados)

v1 = dados_agrupados['ws_25']
v2 = dados_agrupados['ws_50']
v3 = metodo_log(v1, 0.292, 25, 50)
v4 = exponencial(v1, 25, 50, 0.14)

plt.style.use('seaborn-v0_8-bright')
#plt.title('Variação da velocidade com a altura para São João do Cariri')
plt.xlabel('Meses do ano')
plt.ylabel('Velocidade (m/s)')
plt.plot(meses, v1, label='25m Medido')
plt.plot(meses, v2, label='50m Método do Log')
plt.plot(meses, v3, label='50m Medido')
plt.plot(meses, v4, label='50m Método Exponencial')
plt.legend()
plt.grid(True)

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'VELOCIDADE_ALTURA.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()


