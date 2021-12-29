import json
import telebot
import os
from markup import *

with open('config/config.json', 'r') as e:
	data_json = json.loads(e.read())
	token = data_json["token"]
	userDono = data_json["userDono"]
	idgroup = data_json["idGroup"]
	manutencao = data_json["manutenção"]
	idDono = data_json["idDono"]
	userBot = data_json["userBot"]
import psycopg2

url = "postgres://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"
conn = psycopg2.connect(url)
cursor = conn.cursor()

bot = telebot.TeleBot(token)
import ast
