import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Busca o arquivo com os dados
dados = pd.read_excel('C:\\Users\\tdw07\\Downloads\\Tainan_04_03_SMEE_email.xlsm', sheet_name='AT4 - PARTE 3', decimal=',', skiprows=4)
y1 = dados['Média de ws_25'].dropna()
y2 = dados['Média de ws_50'].dropna()
x = dados['Hora']

# Cria o gráfico de barras
plt.bar(x, y1, color='green', alpha=0.8)
# Define os rótulos do eixo x
plt.xticks(x)


plt.xlabel('Horas do dia')
plt.ylabel('Velocidade do vento (m/s)')
plt.grid(axis='y', color='black', linestyle = "--", linewidth = 0.5)

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'ATV3_P3_1'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()



#################################################################################################33
# Cria o gráfico de barras
plt.bar(x, y2, color='#F0AB20', alpha=0.8)
# Define os rótulos do eixo x
plt.xticks(x)
plt.tight_layout()

plt.xlabel('Horas do dia')
plt.ylabel('Velocidade do vento (m/s)')
plt.grid(axis='y', color='black', linestyle = "--", linewidth = 0.5)

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'ATV3_P3_2'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()