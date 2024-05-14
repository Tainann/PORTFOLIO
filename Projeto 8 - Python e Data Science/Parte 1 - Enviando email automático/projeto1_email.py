import pandas as pd
import plotly.express as px
import smtplib
import email.message as em
from babel.numbers import format_currency
# valor_formatado = format_currency(valor, 'BRL', locale='pt_BR')

tabela_vendas = pd.read_excel("Vendas.xlsx")
print(tabela_vendas)

tb_quantidade_produto = tabela_vendas.groupby('Produto').sum()
# Ao aplicar filtros, usar colchetes para mais de um filtro.
# Até para um filtro, usar colchetes é bom porque melhora a visualização
tb_quantidade_produto = tb_quantidade_produto[['Quantidade', 'Valor Unitário']]
tb_quantidade_produto = tb_quantidade_produto.sort_values(by='Quantidade', ascending=False)
# Formatação numérica
tb_quantidade_produto_formatado = pd.DataFrame(tb_quantidade_produto['Quantidade'].apply(lambda x: "{:,}".format(x).replace(",",".")))
tb_quantidade_produto_formatado = tb_quantidade_produto_formatado.reset_index()
tb_quantidade_produto_formatado_html = tb_quantidade_produto_formatado.to_html(index=False, justify='center', border=0).replace('<tbody>', '<tbody style="text-align: center; color: #484848; background: #F7F7F7">')
print(tb_quantidade_produto_formatado)
print(tb_quantidade_produto_formatado_html)

# Vendo o produto com maior faturamento 
# Criando uma nova coluna 
tabela_vendas['Faturamento'] = tabela_vendas['Quantidade']*tabela_vendas['Valor Unitário']
tb_faturamento_produto = tabela_vendas.groupby('Produto').sum()
tb_faturamento_produto = tb_faturamento_produto[['Faturamento']]
tb_faturamento_produto = tb_faturamento_produto.sort_values(by='Faturamento', ascending=False)
tb_faturamento_produto_formatado = pd.DataFrame(tb_faturamento_produto['Faturamento'].apply(lambda x: format_currency(x, 'BRL', locale='pt_BR')))
tb_faturamento_produto_formatado = tb_faturamento_produto_formatado.reset_index()
tb_faturamento_produto_formatado_html = tb_faturamento_produto_formatado.to_html(index=False, justify='center', border=0).replace('<tbody>', '<tbody style="text-align: center; color: #484848; background: #F7F7F7">')
print(tb_faturamento_produto_formatado)

tb_faturamento_loja = tabela_vendas.groupby('Loja').sum()
tb_faturamento_loja = tb_faturamento_loja[['Faturamento']]
# O fator de agrupamento ('Loja') será mantido após o filtro
tb_faturamento_loja = tb_faturamento_loja.sort_values(by='Faturamento', ascending=False)
tb_faturamento_loja_formatado = pd.DataFrame(tb_faturamento_loja['Faturamento'].apply(lambda x: format_currency(x, 'BRL', locale='pt_BR')))
tb_faturamento_loja_formatado = tb_faturamento_loja_formatado.reset_index()
tb_faturamento_loja_formatado_html = tb_faturamento_loja_formatado.to_html(index=False, justify='center', border=0).replace('<tbody>', '<tbody style="text-align: center; color: #484848; background: #F7F7F7">')
print(tb_faturamento_loja_formatado)

tabela_vendas['Ticket Médio'] = tabela_vendas['Valor Unitário']
# Cuidado com datas, pois não dá pra somar ou fazer a média.
tb_ticket_medio = tabela_vendas[['Loja', 'Ticket Médio']]
tb_ticket_medio = tb_ticket_medio.groupby('Loja').mean()
tb_ticket_medio = tb_ticket_medio.sort_values(by="Ticket Médio", ascending=False)
tb_ticket_medio_formatado = pd.DataFrame(tb_ticket_medio['Ticket Médio'].apply(lambda x: format_currency(x, 'BRL', locale='pt_BR')))
tb_ticket_medio_formatado = tb_ticket_medio_formatado.reset_index()
tb_ticket_medio_formatado_html = tb_ticket_medio_formatado.to_html(index=False, justify='center', border=0).replace('<tbody>', '<tbody style="text-align: center; color: #484848; background: #F7F7F7">')
print(tb_ticket_medio_formatado)

grafico = px.line(tb_faturamento_loja, y = 'Faturamento', x = tb_faturamento_loja.index)
#grafico.show()

grafico = px.area(tb_faturamento_loja, y = 'Faturamento', x = tb_faturamento_loja.index)
#grafico.show()

# Código para enviar email.
# pt.stackoverflow é um site para tirar dúvidas.
 
# 3 aspas para aceitar várias linhas numa variável
corpo_email = f""" 
<p>Prezados,</p>

<p>Segue o relatório de vendas do mês.</p>

<p>Faturamento por loja:</p>
<p>{tb_faturamento_loja_formatado_html}</p>

<p>Quantidade vendida por produto:</p>
<p>{tb_quantidade_produto_formatado_html}</p>

<p>Faturamento por produto:</p>
<p>{tb_faturamento_produto_formatado_html}</p>

<p>Ticket Médio por loja:</p>
<p>{tb_ticket_medio_formatado_html}</p>

<p>Qualquer dúvida estou à disposição.</p>
<p>Att.</p>

<p>Tainan</p>
"""

# Configurações para envio
msg = em.Message() # Cria uma mensagem vazia para eu ir adicionando as informações
msg['Subject'] = "Relatório de Vendas" #ASSUNTO DO E-MAIL#
msg['From'] = 'xxxxxxxx' #E-MAIL QUE VAI ENVIAR O E-MAIL#
msg['To'] = 'xxxxxxx'#E-MAIL QUE VAI RECEBER
password = 'xxxxxxxx' #SENHA DO E-MAIL QUE VAI ENVIAR
msg.add_header('Content-Type', 'text/html') # Tipo/Formato do conteúdo
msg.set_payload(corpo_email )

# Configurações do servidor do Gmail.
s = smtplib.SMTP('smtp.gmail.com: 587')
s.starttls() # Porta de segurança.

# Credenciais de login.
s.login(msg['From'], password)
s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
print('Email enviado')

