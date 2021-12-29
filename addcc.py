import json 
import pandas as pd
import psycopg2
url = "postgresql://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"
con = psycopg2.connect(url)
cursor = con.cursor()

i = open("sample.txt", "r")
samples = i.read()

def split_card(card) -> dict:
  splited = card.split("|")
  return {
    "cartao": splited[0],
    "data": splited[1] + "/" + splited[2],
    "cvv": splited[3]
  }
  
cards = [split_card(card) for card in samples.strip().split("\n")]
cartao = [] 
data = []
cvv = []
for row in cards:
    cartao.append((row['cartao']))
    data.append((row['data']))
    cvv.append((row['cvv']))
print(cartao)
from sqlalchemy import create_engine
engine = create_engine(url)
tabela = pd.DataFrame({"id": 'RETURNING id;',"cartao": cartao, "data": data, "cvv": cvv, "bin": '122', "banco": 'BANCO DO BRASIL', "nivel": 'PLATINUM', "tipo": 'CREDIT', "bandeira": 'VISA', "cpf": '282922', "nome": 'GABRIEL SANTOS'})
tabela.to_sql(name='infocc', con=engine, if_exists='append', index=False)