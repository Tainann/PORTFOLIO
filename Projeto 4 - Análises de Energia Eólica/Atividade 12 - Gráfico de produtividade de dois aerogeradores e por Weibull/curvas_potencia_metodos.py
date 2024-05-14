import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.special import gamma
from scipy.integrate import quad
from scipy.interpolate import interp1d
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

def pot_Weibull_4(x_medios, c, k):
    pot_media_weibull = 0
    densidade = 1.225 # kg/m3
    diametro = 4.0
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
dados = pd.read_excel('MACEIO_2021.xlsx', decimal=',')
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
valores_potencia_max_veros_4m = pot_Weibull_4(valores_medios_bins, c2, k2)
y2 = weibull(x_intervalo, c2, k2)

c3, k3 = momentos(dados_sem_null)
valores_potencia_momentos = pot_Weibull(valores_medios_bins, c3, k3)
y3 = weibull(x_intervalo, c3, k3)

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
velocidades_smooth = np.linspace(velocidades_xzeres.min(), velocidades_xzeres.max(), 100)
potencia_xzeres_smooth = f_xzeres(velocidades_smooth)
potencia_kestrel_smooth = f_kestrel(velocidades_smooth)

# Plotando as curvas suavizadas
# A curva que melhor se ajustou foi pelo métodos da Máxima Verossimilhança.
plt.plot(velocidades_smooth, potencia_xzeres_smooth, label='Xzeres Skystream')
plt.plot(velocidades_smooth, potencia_kestrel_smooth, label='Kestrel e400nb')
#plt.plot(valores_medios_bins, valores_potencia_min_quad, color="red", label=f'Mín. quadrados (c={c1:.2f}, k={k1:.2f})')
plt.plot(valores_medios_bins, valores_potencia_max_veros, color="green", label=f'Prod. de Weibull para D = 3,7m')
plt.plot(valores_medios_bins,valores_potencia_max_veros_4m, color="red", label=f'Prod. de Weibull para D = 4m')

#plt.plot(valores_medios_bins, valores_potencia_momentos, color="black", label=f'Mét. Momentos (c={c3:.2f}, k={k3:.2f})')
#plt.plot(valores_medios_bins, valores_potencia_rayleigh, color="blue", label=f'Rayleigh')
plt.xlabel('Velocidade horária (m/s)')
#plt.title(f'Análise de produtividade para Maceió em 2021')
plt.ylabel('Potência (W)')
plt.legend()
plt.grid(True)

plt.tight_layout()
nome_arquivo = 'ATIVIDADE_12.png'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()
