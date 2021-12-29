from cliente import *
from admin import *


@bot.message_handler(commands=["start", "menu"])
def menu_inicial(message):
	verificar_existe(message.from_user.id, message.from_user.username)
	bot.send_message(message.chat.id, f"""
	<b>🧙🏻‍♂️ | Store de Info'ccs

Olá</b> <a href='https://t.me/{message.from_user.username}'>{message.from_user.first_name}</a><b>, Seja bem vindo a store!</b>

<a href='https://t.me/{userDono}'>❓ Dúvidas</a>
<a href='https://t.me/KING_ST0RE_CHAT'>👥 Grupo</a>
<a href='https://t.me/REFKG'>📣 Canal</a>
<a href='https://t.me/Yusuke011'>⚙️ Dev</a>
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
		gift_enviado = message.text.split("/resgatar ")[1]
		try:
			cursor.execute(f"SELECT valor FROM gifts_cards WHERE gift_gerado = '{gift_enviado}'")
			for result in cursor.fetchone():
			    pass
			ADD_SALDO = procurar_dados(message.from_user.id)[0] + result
			total = procurar_dados(message.from_user.id)[2] + 1
			cursor.execute(f"UPDATE usuarios SET saldo = {ADD_SALDO}, gifts = {total} WHERE chat_id = {message.from_user.id}")
			conn.commit()
			g = gift_enviado[0:6]+'xxxxxxxx'
			bot.send_message(message.chat.id,f"*✅ Gift resgatado com sucesso\n\nGift: {g}\nValor: R${result}\n\nO valor foi adicionado na sua conta! Aproveite e compre suas info'ccs.*", parse_mode="MARKDOWN")
			cursor.execute(f"DELETE FROM gifts_cards WHERE gift_gerado = '{gift_enviado}'")
			conn.commit()
		except:
			bot.send_message(message.chat.id,"*❌ Gift Card inválido ou já foi resgatado!*", parse_mode="MARKDOWN")

@bot.message_handler(commands=['recarga'])
def recarga_pix(message):
  verificar_existe(message.from_user.id, message.from_user.username)
  if message.text == "/recarga":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  elif message.text == f"/recarga{userBot}":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  else:
    bot.send_message(message.chat.id, "Em manutenção!")

bot.infinity_polling()