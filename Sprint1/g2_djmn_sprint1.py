# -*- coding: utf-8 -*-
"""G2_DJMN_Sprint1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19GWbMhRwMikBbWVrjFJtZ1EpQMzjqmeo

COLETA DOS DADOS
"""

#Os imports não são finais
import pandas as pd
#import sqlite3
import numpy as np
import requests

#Para gerar o arquivo .csv sem tratamento a partir da página .html
dataHTML = pd.read_html('http://www.nuforc.org/webreports/ndxevent.html')
dataHTML[0].to_csv('file.csv')
dataCSV = pd.read_csv('file.csv')

#Para fazer o tratamento do DataFrame do pandas:
keep_col = ['Reports','Count']  #para o tratamento do arquivo com os index para o .csv
newData = dataCSV[keep_col]

#E agora para deixar apenas os dados do intervalo de tempo desejado
newData = newData.iloc[45:285]

#Gerar o novo arquivo usado como o dos dados que queremos acessar
newData.to_csv("OVNIs_Index.csv", index = False)
indexOVNIs = pd.read_csv('OVNIs_Index.csv')

#A partir daqui fazemos o tratamento para inserir o conteúdo das tabelas HTML dentro de cada link
#Método para acessar um link com uma data específica
def tableHMTL(date):
    url = 'http://www.nuforc.org/webreports/ndxe' + date + '.html'
    page = requests.get(url)
    dfHMTL = pd.read_html(page.text)
    dfHMTL = pd.DataFrame(np.concatenate(dfHMTL), columns=columns)
    return dfHMTL

#Passar dataOVNIs['Reports'] como index para chamar links do dataHTML
columns = ['Data/Hora','Cidade','Estado','Forma','Duracao','Descricao','Postagem']
tablesOVNIS = []
tablesOVNIS = pd.DataFrame(tablesOVNIS, columns=columns)

#Esse bloco acessa cada link da página de relatos de OVNIS e imprime cada relato
#passando dataOVNIs['Reports'] como index para chamar links do dataHTML
for i in indexOVNIs['Reports']:
    data_relato = str(i)
    data_split = data_relato.split("/")
    data_split.reverse()
    date = ''.join(data_split)
    tablesOVNIS = pd.concat([tableHMTL(date),tablesOVNIS])

tablesOVNIS.to_csv('OVNIS.csv')
tablesOVNIS

"""Exploração com PandasSQL

LISTA DE INTENS OBRIGATÓRIOS PARA A EXPLORAÇÃO
"""

# 1- Saber a quantidade de linhas, observações ou variáveis que foram coletadas. -> NÚMERO DE LINHAS 
import pandas as pd

print('A quantidade de linhas e colunas coletadas são:', tablesOVNIS.shape)

# 2- Quantos relatos ocorreram por estado em ordem decrescente?

q='''
  SELECT Estado, COUNT(*)
  FROM tablesOVNIS
  GROUP BY Estado
  HAVING COUNT(*)
  ORDER BY COUNT(*) desc
'''

consulta = pandasql.sqldf(q, locals())
consulta

# 3- Remover possíveis campos vazios (sem estado)
tablesOVNIS.drop(tablesOVNIS.index[tablesOVNIS['Estado'] == 'None'], inplace = True)
tablesOVNIS.drop(tablesOVNIS.index[tablesOVNIS['Estado'] == None], inplace = True)

# Remover possíveis campos NaN
tablesOVNIS['Estado'].dropna()

tablesOVNIS

# 4- Limitar a análise aos estados dos Estados Unidos.

import pandas
!pip install -U pandasql
import pandasql

def filtro_EUA(filename):

  # Tabela de Estados dos EUA
  ovnis_data = pandas.read_csv(filename)
  
  q='''
      SELECT *
      FROM ovnis_data
      WHERE Estado in ('AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL',
      'IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND',
      'NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN',
      'TX','UT','VT','VA','WA','WI','WV','WY')
      ORDER BY Estado
  '''
  filtro_est_USA = pandasql.sqldf(q, locals())

  OVNIS_limpo = pd.DataFrame(filtro_est_USA)
  OVNIS_limpo.to_csv("OVNIs_limpo.csv", index = False)
  
  return OVNIS_limpo

filtro_EUA('./OVNIS.csv')

# 5- Consulta por cidades, com o objetivo de saber quais contêm o maior número 
  # de relatos (cidades que apresentem ao menos 10 relatos).

df2 = pd.read_csv('./OVNIs_limpo.csv')

q='''
  SELECT Cidade, COUNT(*)
  FROM df2
  GROUP BY Cidade
  HAVING COUNT(*) > 9
  ORDER BY COUNT(*) desc
'''

consulta1 = pandasql.sqldf(q, locals())
consulta1



# 6- Com o dado anterior, responder a seguinte pergunta: por que será que essa é 
  #a cidade que possui mais relatos?

'''
  Phoenix é a cidade que possui mais relatos devido a um evento denominado 
  "Luzes de Phoenix" que ocorreu no estado do Arizona e Nevada (EUA) e em Sonora (MEX)
  no ano de 1997. Os fenômenos ópticos ocorridos nessa região foram visto por milhares de pessoas,
  o que ocasionou uma série de registros de avistamento de OVNIS's no BD do site do NUFORC
'''

# 7- Fazer uma query exclusiva para o estado com maior número de relatos, buscando 
# cidades que possuam um número superior a 10 relatos. 

# Enfatizar a cidade, a quantidade de relatos e formato do objeto não identificado.

df3 = pd.read_csv('./OVNIs_limpo.csv')

q='''
  SELECT Estado, Cidade, COUNT(*), Forma
  FROM df3
  WHERE Estado = 'CA'
  GROUP BY Cidade
  HAVING COUNT(*) > 9
  ORDER BY COUNT(*) desc
'''

consulta2 = pandasql.sqldf(q, locals())
consulta2