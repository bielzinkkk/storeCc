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
		gift_enviado = message.text.split("/resgatar ")[1]
		try:
			cursor.execute(f"SELECT valor FROM gifts_cards WHERE gift_gerado = '{gift_enviado}'")
			for result in cursor.fetchone():
			    pass
			ADD_SALDO = saldo(message.from_user.id) + result
			cursor.execute(f"UPDATE usuarios SET saldo = {ADD_SALDO} WHERE chat_id = {message.from_user.id}")
			conn.commit()
			g = gift_enviado[0:6]+'xxxxxxxx'
			bot.send_message(message.chat.id,f"*✅ Gift resgatado com sucesso\n\nGift: {g}\nValor: R${result}\n\nO valor foi adicionado na sua conta! Aproveite e compre suas info'ccs.*", parse_mode="MARKDOWN")
			cursor.execute(f"DELETE FROM gifts_cards WHERE gift_gerado = '{gift_enviado}'")
			conn.commit()
		except:
			bot.send_message(message.chat.id,"*❌ Gift Card inválido ou já foi resgatado!*", parse_mode="MARKDOWN")

@bot.message_handler(commands=["recarga"])
def recarga(message):
	# Manutenção
  pass

@bot.message_handler(commands=['recarga'])
def recarga_pix(message):
  verificar_existe(message.from_user.id)
  if message.text == "/recarga":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  elif message.text == "/recarga@RedzinVendSBot":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  else:
    try:
      VALOR = message.text.split("/recarga ")[1]
      id_pix = gerar_pagamento(int(VALOR))[0]
      token = "APP_USR-6957443970470439-111320-82c9e0f14ae9cc53ffb6151facfba46b-1008178867"
      headers = {"Authorization": f"Bearer {token}"}
      request = requests.get(f'https://api.mercadopago.com/v1/payments/{id_pix}', headers=headers)
      response = request.json()
      pix = response['point_of_interaction']['transaction_data']['qr_code']
      msg = bot.send_message(message.chat.id, f"""
    *✅ PAGAMENTO GERADO

ℹ️  ID DO PAGAMENTO:* `{id_pix}`
*ℹ️  PIX QR CODE:* `{pix}`
*ℹ️  A COMPRA IRÁ EXPIRAR EM 5 MINUTOS.
ℹ️  DEPOIS DO PAGAMENTO SEU SALDO SERÁ ADICIONADO AUTOMÁTICAMENTE.*""",
  reply_markup=aguardando, parse_mode="MARKDOWN")
      if status(id_pix) == True:
        adicao = int(VALOR) + saldo(message.from_user.id)
        sql = f"UPDATE usuarios SET saldo = {adicao} WHERE chat_id = {message.from_user.id}"
        cursor.execute(sql)
        conn.commit()
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*• PAGAMENTO APROVADO!!! SEU SALDO JA ESTÁ DISPONÍVEL.🤴💰*", parse_mode="MARKDOWN")
        notificar_recarga(id_pix, VALOR, message.from_user.first_name)
      else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*• O PAGAMENTO FOI EXPIRADO.*", parse_mode="MARKDOWN")
    except:
      bot.send_message(message.chat.id,"*• Você digitou o valor incorretamente , use um valor inteiro , exemplo: /recarga 1.*", parse_mode="MARKDOWN")


bot.infinity_polling()