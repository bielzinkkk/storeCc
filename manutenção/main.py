from bot import *

@bot.message_handler(content_types=['text'])
def manutencao(message):
	bot.reply_to(message, "Bot em manutenção.")
	
bot.polling()