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

def fc_xzeres(freq, pot):
    fc = []
    for i in range(len(pot)):
        valor = 0  # Definindo valor para zero em cada iteração do loop externo
        for j in range(i + 1):  # Corrigindo o range do loop interno
            valor += freq[j] * pot[j]
        fc.append(valor * 100 / 2100)
    return fc

def fc_kestrel(freq, pot):
    fc = []
    for i in range(len(pot)):
        valor = 0  # Definindo valor para zero em cada iteração do loop externo
        for j in range(i + 1):  # Corrigindo o range do loop interno
            valor += freq[j] * pot[j]
        fc.append(valor * 100 / 3500)
    return fc 

# Busca o arquivo com os dados
dados = pd.read_excel('E:\\SMEE - 2024.1\\MACEIO_2022.xlsx', decimal=',')
dados_sem_null = dados['VENTO, VELOCIDADE HORARIA (m/s)'].dropna()

dados_sem_null_sem_0, limites_bins, media_dados_sem_null = leitura_dados(dados_sem_null)

c1 = 2.96; k1 = 1.47; c2 = 2.77; k2 = 1.63; c3 = 2.73; k3 = 1.44

velocidades = np.arange(0, max(limites_bins)+0.5, 0.5)

freq_min_quad = weibull(velocidades, c1, k1)
freq_max_veros = weibull(velocidades, c2, k2)
freq_momentos = weibull(velocidades, c3, k3)

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

curva_min_quad_xzeres = fc_xzeres(freq_min_quad, potencia_xzeres_smooth)
curva_max_veros_xzeres = fc_xzeres(freq_max_veros, potencia_xzeres_smooth)
curva_momentos_xzeres = fc_xzeres(freq_momentos, potencia_xzeres_smooth)

max_min_quad_xzeres = max(curva_min_quad_xzeres)
print(f'FC total para Xzeres em Maceió - 2022 pelo método dos Mín. Quad: {max_min_quad_xzeres:.2f} %')
max_max_veros_xzeres = max(curva_max_veros_xzeres)
print(f'FC total para Xzeres em Maceió - 2022 pelo método da Máx. Veros.: {max_max_veros_xzeres:.2f} %')
max_momentos_xzeres = max(curva_momentos_xzeres)
print(f'FC total para Xzeres em Maceió - 2022 pelo método dos Momentos: {max_momentos_xzeres:.2f} %')

# plt.title('Fator de capacidade para a turbina Xzeres Skystream em Maceió - 2022')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Fator de capacidade (%)')
plt.plot(velocidades, curva_min_quad_xzeres, label='Mín. Quadrados')
plt.plot(velocidades, curva_max_veros_xzeres, label='Máx. Verosim.')
plt.plot(velocidades, curva_momentos_xzeres, label='Momentos')
plt.legend()
plt.grid(True)

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'FC_XZERES_MACEIO_2022.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()

curva_min_quad_kestrel = fc_kestrel(freq_min_quad, potencia_kestrel_smooth)
curva_max_veros_kestrel = fc_kestrel(freq_max_veros, potencia_kestrel_smooth)
curva_momentos_kestrel = fc_kestrel(freq_momentos, potencia_kestrel_smooth)

max_min_quad_kestrel = max(curva_min_quad_kestrel)
print(f'FC total para Kestrel em Maceió - 2022 pelo método dos Mín. Quad: {max_min_quad_kestrel:.2f} %')
max_max_veros_kestrel = max(curva_max_veros_kestrel)
print(f'FC total para Kestrel em Maceió - 2022 pelo método da Máx. Veros.: {max_max_veros_kestrel:.2f} %')
max_momentos_kestrel = max(curva_momentos_kestrel)
print(f'FC total para Kestrel em Maceió - 2022 pelo método dos Momentos: {max_momentos_kestrel:.2f} %')

# plt.title('Fator de capacidade para a turbina Kestrel e400nb em Maceió - 2022')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Fator de capacidade (%)')
plt.plot(velocidades, curva_min_quad_kestrel, label='Mín. Quadrados')
plt.plot(velocidades, curva_max_veros_kestrel, label='Máx. Verosim.')
plt.plot(velocidades, curva_momentos_kestrel, label='Momentos')
plt.legend()
plt.grid(True)

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'FC_KESTREL_MACEIO_2022.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()