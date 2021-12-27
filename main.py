from cliente import *
from admin import *

@bot.message_handler(commands=["start", "menu"])
def menu_inicial(message):
	verificar_existe(message.from_user.id, message.from_user.username)
	bot.send_message(message.chat.id, f"""
	<b>🧙🏻‍♂️ | Store de Info'ccs

Olá</b> <a href='https://t.me/{message.from_user.username}'>{message.from_user.first_name}</a><b>, Seja bem vindo a store!</b>

<a href='https://t.me/{userDono}'>❓ Dúvidas</a>
<a href='https://t.me/{userDono}'>👥 Grupo</a>
<a href='https://t.me/{userDono}'>📣 Canal</a>
<a href='https://t.me/@Yusuke011'>⚙️ Dev</a>
""", reply_markup=menu, parse_mode="HTML")

@bot.message_handler(commands=["resgatar"])
def resgatar(message):
	if message.text == "/resgatar":
		bot.send_message(message.chat.id, """
		*🏷️ Resgatar Gift Card*

_- Modo de uso:_
*Para resgatar seu gift card apenas digite /resgatar [ gift card ]*

_- Avisos:_
*O código é só utilizado uma vez!
Quando creditar na conta , o gift será apago do bot, sem reutilização!*
		""", parse_mode="MARKDOWN")
	elif message.text == f"/resgatar{userBot}":
		bot.send_message(message.chat.id, """
		*🏷️ Resgatar Gift Card*

_- Modo de uso:_
*Para resgatar seu gift card apenas digite /resgatar [ gift card ]*

_- Avisos:_
*O código é só utilizado uma vez!
Quando creditar na conta , o gift será apago do bot, sem reutilização!*
		""", parse_mode="MARKDOWN")
	else:
		bot.send_message(message.chat.id, resgatar_gift(message.text.split("/resgatar ")[1], message.from_user.id))

@bot.message_handler(commands=["recarga"])
def recarga(message):
	# Manutenção
  pass

bot.infinity_polling()