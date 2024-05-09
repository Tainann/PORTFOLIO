import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.special import gamma
from scipy.integrate import quad
import os


# Função da curva de Weibull
def weibull(x, c, k):
    return (k/c) * ((x/c)**(k-1)) * np.exp(-(x/c)**k)

def rayleigh(x, media_dados_em_null):
    return ( math.pi/ 2) * (x / media_dados_em_null**2) * np.exp(-(math.pi / 4) * (x / media_dados_em_null)**2)

def calcula_momentos(parameters, data):
    c, k = parameters
    mean_data = np.mean(data)
    variance_data = np.var(data)
    
    # Calculando os momentos teóricos
    mean_theoretical = c * gamma(1 + 1/k)
    variance_theoretical = c**2 * (gamma(1 + 2/k) - gamma(1 + 1/k))
    
    # Calculando a função objetivo (soma dos quadrados dos desvios)
    objective = (mean_data - mean_theoretical)**2 + (variance_data - variance_theoretical)**2
    
    return objective

def momentos(dados_sem_null):
    # Estimando os parâmetros iniciais
    valores_inicio = [1, 1]  # Você pode ajustar esses valores conforme necessário
    
    # Minimizando a função objetivo usando o método dos momentos
    resultado = minimize(calcula_momentos, valores_inicio, args=(dados_sem_null,), method='Nelder-Mead')
    
    # Retornando os parâmetros estimados
    c, k = resultado.x
    return c, k

# Função de verossimilhança da distribuição de Weibull
def log_veross(params, data):
    c, k = params
    if c <= 0 or k <= 0:
        return np.inf
    return -np.sum(np.log(k/c) + (k-1)*np.log(data/c) - (data/c)**k)

def max_veros(dados_sem_null_sem_0, media_dados_sem_null):
    # Minimizar a função de verossimilhança para encontrar os parâmetros c e k
    # dados_sem_null_sem_0 é usado para não passar valor 0 para maxima_veros
    resultado = minimize(log_veross, [media_dados_sem_null, 2], args=(dados_sem_null_sem_0,), method='L-BFGS-B', bounds=[(0.001, None), (0.001, None)])
    c, k = resultado.x
    return c, k

def leitura_dados(dados_sem_null):
    # Remover valores zeros da coluna escolhida
    dados_sem_null_sem_0 = dados_sem_null[dados_sem_null != 0]
    # Definindo os limites dos bins
    limites_bins = np.arange(0, max(dados_sem_null) + 0.5, 0.5)
    # Calcular a média dos valores em dados_sem_null
    media_dados_sem_null = np.mean(dados_sem_null) # Calculando a média da panda Series

    return dados_sem_null_sem_0, limites_bins, media_dados_sem_null

def min_quad(dados_sem_null, limites_bins, media_dados_sem_null):
    # Histograma das velocidades
    hist, bin_edges = np.histogram(dados_sem_null, bins=limites_bins, density=True)

    # Calcula o centro de cada bin do histograma
    bins_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # Ajuste da curva de Weibull aos dados
    params, covariance = curve_fit(weibull, bins_centers, hist, p0=[media_dados_sem_null, 2])
    
    return params

# Função da potência
def pot(x, densidade, area, cp, n):
    return 0.5 * densidade * area * cp * n * x**3

# Função a ser integrada (pot * weibull)
def integral1(x, densidade, area, cp, n, c, k):
    return pot(x, densidade, area, cp, n) * weibull(x, c, k)

def integral2(x, densidade, area, cp, n, media_dados_sem_null):
    return pot(x, densidade, area, cp, n) * rayleigh(x, media_dados_sem_null)

def pot_Weibull(x_medios, c, k):
    pot_media_weibull = 0
    densidade = 1.225 # kg/m3
    diametro = 3.7
    area = math.pi*(diametro/2)**2
    cp = 16/27
    n = 1
    valores_potencia = [0]
    for indice, valor in enumerate(x_medios):
        if indice == 0:
            continue
        valor_anterior = x_medios[indice-1]
        pot = 0.5*densidade*area*cp*n*valor**3
        pot_media_weibull += (np.exp(-(valor_anterior/c)**k)-np.exp(-(valor/c)**k))*pot*((valor_anterior+valor)/2)
        valores_potencia.append(pot_media_weibull)
    # print(f'Potência média de Weibull usando o método {metodo}: {pot_media_weibull/1000:.2f} kW')
    # print(f'Energia média: {pot_media_weibull*8760/1000:.2f} kWh')
    # print()
    return valores_potencia 

def pot_Rayleigh(x_medios):
    densidade = 1.225
    diametro = 3.7  # diâmetro em metros
    area = math.pi * (diametro / 2) ** 2  # área em metros quadrados
    cp = 16/27
    n = 1
    valores_potencia = [0]
    pot_media_rayleigh = 0
    for indice, valor in enumerate(x_medios):
        if indice == 0:
            continue
        pot_media_rayleigh = densidade * (2/3 * diametro)**2 * valor**3
        valores_potencia.append(pot_media_rayleigh)
    #print(f'Potência média por Rayleigh: {pot_media_rayleigh:.2f} W')
    #print(f'Energia média anual por Rayleigh: {pot_media_rayleigh*8760/1000000:.2f} MWh')
    #print()
    return valores_potencia

# Busca o arquivo com os dados
dados = pd.read_excel('E:\\SMEE - 2024.1\\MACEIO_2022.xlsx', decimal=',')
dados_sem_null = dados['VENTO, VELOCIDADE HORARIA (m/s)'].dropna()

dados_sem_null_sem_0, limites_bins, media_dados_sem_null = leitura_dados(dados_sem_null) 
hist, bin_edges = np.histogram(dados_sem_null, bins=limites_bins, density=True)

# Calcula o centro de cada bin do histograma
x_medios = 0.5 * (bin_edges[1:] + bin_edges[:-1])
valores_medios_bins = np.concatenate(([0], x_medios, [max(limites_bins)]))
print(valores_medios_bins)
valores_medios_bins = np.linspace(0, max(limites_bins), 1000)

# Exibir a média que será o valor de c
print(f'Média dos valores: {media_dados_sem_null:2f} m/s')
valores_potencia_rayleigh = pot_Rayleigh(valores_medios_bins)

# Plotagem das curvas
x_intervalo = np.linspace(0, max(limites_bins), 1000)

c1, k1 = min_quad(dados_sem_null, limites_bins, media_dados_sem_null)
valores_potencia_min_quad = pot_Weibull(valores_medios_bins, c1, k1)
y1 = weibull(x_intervalo, c1, k1)

c2, k2 = max_veros(dados_sem_null_sem_0, media_dados_sem_null)
valores_potencia_max_veros = pot_Weibull(valores_medios_bins, c2, k2)
y2 = weibull(x_intervalo, c2, k2)

c3, k3 = momentos(dados_sem_null)
valores_potencia_momentos = pot_Weibull(valores_medios_bins, c3, k3)
y3 = weibull(x_intervalo, c3, k3)

'''
plt.hist(dados_sem_null, bins=limites_bins, color='blue', edgecolor='black', alpha=0.7, density=True)
plt.xlabel('Velocidade horária (m/s)')
plt.title(f'Ajuste de Curva de Weibull para São Luís em 2022 usando 3 métodos')
plt.ylabel('Densidade de probabilidade')
plt.plot(x_intervalo, y1, color='red', label=f'Mín.quadrados (c={c1:.2f}, k={k1:.2f})')
plt.plot(x_intervalo, y2, color='green', label=f'Máx.verossimilhança (c={c2:.2f}, k={k2:.2f})')
plt.plot(x_intervalo, y3, color='black', label=f'Mét.Momentos (c={c3:.2f}, k={k3:.2f})')
plt.legend(loc='upper right')
'''
plt.plot(valores_medios_bins, valores_potencia_min_quad, color="red", label=f'Mín. quadrados (c={c1:.2f}, k={k1:.2f})')
plt.plot(valores_medios_bins, valores_potencia_max_veros, color="green", label=f'Máx. verossimilhança (c={c2:.2f}, k={k2:.2f})')
plt.plot(valores_medios_bins, valores_potencia_momentos, color="black", label=f'Mét. Momentos (c={c3:.2f}, k={k3:.2f})')
plt.plot(valores_medios_bins, valores_potencia_rayleigh, color="blue", label=f'Rayleigh')
plt.xlabel('Velocidade horária (m/s)')
#plt.title(f'Curvas de produtividade para Maceió em 2022')
plt.ylabel('Potência (W)')
plt.legend()
plt.grid(linestyle = "--", linewidth = 0.5)

plt.tight_layout()
nome_arquivo = 'CURVAS_POT_MACEIO_2022.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()
