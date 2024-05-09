import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Busca o arquivo com os dados
dados = pd.read_excel('E:\\SMEE - 2024.1\\SAO_LUIS_2021.xlsx')

# Função da curva de Weibull
def weibull(x, c, k):
    return (k/c) * ((x/c)**(k-1)) * np.exp(-(x/c)**k)

# Remover valores nulos da coluna escolhida
dados_sem_null = dados['VENTO, VELOCIDADE HORARIA (m/s)'].dropna()

# Calcular a média dos valores em dados_sem_null
media_dados_sem_null = np.mean(dados_sem_null) # Calculando a média da panda Series

# Definindo os limites dos bins
limites_bins = np.arange(0, max(dados_sem_null)+0.5, 0.5) 
eixo_x = np.linspace(0, max(limites_bins), 1000)

# Exibir a média que será o valor de c
print(f'Média dos valores: {media_dados_sem_null}')

# Criando o histograma
plt.hist(dados_sem_null, bins=limites_bins, color='blue', alpha=0.7, density=True, label='Histograma')

c = 1.6596342857142856
k_chute = 2

# Criação das curvas (cw = Curva de Weibull)
cw1 = weibull(eixo_x, c, k_chute)
cw2 = weibull(eixo_x, c, 1.5)
cw3 = weibull(eixo_x, c, 1.2)

# Plotagem do histograma
plt.xlabel('Velocidade horária (m/s)')
plt.ylabel('Frequência relativa')
# plt.title('Ajuste de Curva de Weibull para São Luís em 2021')
plt.grid(color='black', linestyle = "--", linewidth = 0.5)

# Criação do segundo eixo vertical
plt.twinx()
plt.ylabel('Densidade de probabilidade')

# Plotagem da curva ajustada
plt.plot(eixo_x, cw1, color='red', label=f'CW1 (c={c:.2f}, k={k_chute:.2f})')
plt.plot(eixo_x, cw2, color='#14DD21', label=f'CW2 (c={c:.2f}, k=1.50)')
plt.plot(eixo_x, cw3, color='black', label=f'CW3 (c={c:.2f}, k=1.20)')
plt.legend()

plt.tight_layout()
# Salvando a figura
nome_arquivo = 'SAO_LUIS_2021.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)

# Exibir o gráfico
plt.show()
