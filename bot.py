import json
import telebot
import os

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
import time
from telebot import types


def makeKeyboard():
    cursor.execute("SELECT nivel FROM infocc")
    v = cursor.fetchall()
    markup = types.InlineKeyboardMarkup()
    for i in sorted(set(v)):
      for value in i:
        print(value)
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "']"))
     
    return markup

@bot.message_handler(commands=['test'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the values of stringList",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data.startswith("['valor'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="You Clicked " + valueFromCallBack + " and key is")

bot.polling()