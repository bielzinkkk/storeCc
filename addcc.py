import json 
import psycopg2
url = "postgres://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"
conn = psycopg2.connect(url)
cursor = conn.cursor()

i = open("sample.txt", "r")
samples = i.read()

def split_card(card) -> dict:
  splited = card.split("|")
  return {
    "cartao": int(splited[0]),
    "data": splited[1] + "/" + splited[2],
    "cvv": int(splited[3])
  }
  
cards = [split_card(card) for card in samples.strip().split("\n")]
itemBank = [] 
for row in cards:
    itemBank.append((
        row['cartao'],
        row['data'],
        row['cvv'],
        )) #append data


q = """ insert ignore into infocc(
        cartao, data, cvv) 
        values (%s,%s,%s)           
    """

try:
    x.executemany(q, itemBank)
    conn.commit()
except:
    conn.rollback()
print("adicionado")