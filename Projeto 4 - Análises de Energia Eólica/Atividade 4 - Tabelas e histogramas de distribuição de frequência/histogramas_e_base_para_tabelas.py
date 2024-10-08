import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Busca o arquivo com os dados
dados = pd.read_excel('04_03_SMEE_email.xlsm', sheet_name='AT5 - COPIA', decimal=',')
dados_sem_null_25 = dados['ws_25'].dropna()
dados_sem_null_50 = dados['ws_50'].dropna()

# Definindo os limites dos bins
limites_bins_25 = np.arange(0, max(dados_sem_null_25), 1) 
limites_bins_50 = np.arange(0, max(dados_sem_null_50), 1) 

y1, x1 = np.histogram(dados_sem_null_25, bins=limites_bins_25)
y2, x2 = np.histogram(dados_sem_null_50, bins=limites_bins_50)

fig, ax = plt.subplots()
# Criando o histograma para 25 m

f1, bins_25, _ = plt.hist(dados_sem_null_25, bins=limites_bins_25, color='blue', alpha=0.8, density=True, label='Histograma')
# plt.title('Histograma da distribuição de frequência para 25m de altura')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Frequência da distribuição (%)')
plt.grid(color='black', linestyle = "--", linewidth = 0.5)
#plt.legend()
plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'ATV4_1'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()

###########################################################################
# Criando tabela para 25 m
intervalos = ['(0-1)', '(1-2)', '(2-3)', '(3-4)', '(4-5)', '(5-6)', '(6-7)', '(7-8)', '(8-9)', '(9-10)', '(10-11)', '(11-12)']

f1 = np.round(f1, 4)
fr = f1*100
fr = np.round(fr, 2)

df_25 = pd.DataFrame({
    'Velocidade do vento (m/s)': intervalos, 
    'N° de ocorrências': y1,
    'Freq. relativa': f1,
    'FR (%)': fr
    })


df_25 = df_25.map(lambda x: str(x).replace('.', ','))

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Salvando o DataFrame como um arquivo CSV na mesma pasta do script
caminho_arquivo = os.path.join(diretorio_atual, 'df_25.csv')
df_25.to_csv(caminho_arquivo, index=False)


######################################################################

# Criando o histograma para 50 m
f2, f, _ = plt.hist(dados_sem_null_50, bins=limites_bins_50, color='blue', alpha=0.8, density=True, label='Histograma')
# plt.title('Histograma da distribuição de frequência para 50m de altura')
plt.xlabel('Velocidade do vento (m/s)')
plt.ylabel('Frequência da distribuição (%)')
plt.style.use('seaborn-v0_8-bright')
plt.tight_layout()
plt.grid(color='black', linestyle = "--", linewidth = 0.5)
#plt.legend()

plt.tight_layout()
# Salvando o gráfico na mesma pasta que o script
nome_arquivo = 'ATV4_2'
caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
plt.savefig(caminho)
plt.show()

#######################################################################
# Criando tabela para 50 m
intervalos = ['(0-1)', '(1-2)', '(2-3)', '(3-4)', '(4-5)', '(5-6)', '(6-7)', '(7-8)', '(8-9)', '(9-10)', '(10-11)', '(11-12)', '(12-13)', '(13-14)']

f2 = np.round(f2, 5)
fr = f2*100
fr = np.round(fr, 3)

df_50 = pd.DataFrame({
    'Velocidade do vento (m/s)': intervalos, 
    'N° de ocorrências': y2,
    'Freq. relativa': f2,
    'FR (%)': fr
    })

df_50 = df_50.map(lambda x: str(x).replace('.', ','))

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Salvando o DataFrame como um arquivo CSV na mesma pasta do script
caminho_arquivo = os.path.join(diretorio_atual, 'df_50.csv')
df_50.to_csv(caminho_arquivo, index=False)
