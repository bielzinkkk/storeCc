import json
import telebot
from markup import *
import time
import fordev
from ferramentas.ferramentas import *
with open('config/config.json', 'r') as e:
	data_json = json.loads(e.read())
	token = data_json["token"]
	userDono = data_json["userDono"]
	idGroup = data_json["idGroup"]
	manutencao = data_json["manutenção"]
	idDono = data_json["idDono"]
	userBot = data_json["userBot"]
import psycopg2

url = "postgres://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"
conn = psycopg2.connect(url)
cursor = conn.cursor()

bot = telebot.TeleBot(token)
import ast

@bot.message_handler(commands=['gen'])
def gen_command(message):
	bot.send_message(message.chat.id, gen_full(), reply_markup=gen_markup, parse_mode="MARKDOWN")
	
@bot.callback_query_handler(func=lambda call: call.data == "trocar_dados")
def trocardadoscall(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=gen_full(), reply_markup=gen_markup,parse_mode="MARKDOWN")

@bot.message_handler(commands=['chk'])
def chk_command(message):
	bot.send_message(message.chat.id, checker_full(), parse_mode="MARKDOWN")