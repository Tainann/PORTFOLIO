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
    return v1 * (h2 / h1) ** alfa

def rugosidade(v1, v2, h1, h2):
    rugs = []
    for v_1, v_2 in zip(v1,v2):
        rugs.append(np.exp((v_2*np.log(h1)-v_1*np.log(h2))/(v_2-v_1)))
    return rugs

# Busca o arquivo com os dados
dados = pd.read_excel('E:\\DOWNLOADS_DISCO_C\\ATIVIDADE_4.xlsx', sheet_name='UNIAO', decimal=',')

# Agrupar por ano e nome do mês e calcular a média
dados = dados[['Mês', 'ws_25', 'ws_50']]
dados_agrupados = dados.groupby(['Mês']).mean()
meses = dados_agrupados.index
dados_agrupados.reset_index(inplace=True)

v1 = dados_agrupados['ws_25']
v2 = dados_agrupados['ws_50']
v3 = metodo_log(v1, 0.292, 25, 50)
v4 = exponencial(v1, 25, 50, 0.14)

rug1 = rugosidade(v1, v2, 25, 50)
rug2 = rugosidade(v1, v3, 25, 50)
rug3 = rugosidade(v1, v4, 25, 50)

plt.style.use('seaborn-v0_8-bright')
# plt.title('Variação do comp. de rugosidade')
plt.ylabel('Comp. de rugosidade (m)')
plt.xlabel('Meses do ano')
plt.plot(meses, rug1, label='Rug. por velocidades medidas')
plt.plot(meses, rug2, label='Rug. por velocidades mét. log.')
plt.plot(meses, rug3, label='Rug. por velocidades mét. exp.')
plt.legend()
plt.grid(linestyle = "--", linewidth = 0.5)

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'RUGOSIDADE.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()



