from src.cliente.cliente import *
from src.adm.admin import *
from src.pix_auto.juno import *
from src.pix_auto.mp import *

@bot.message_handler(commands=["start", "menu"])
def menu_inicial(message):
  if verify_manutencao() != "DESATIVA":
      bot.send_message(message.chat.id, verify_manutencao(), parse_mode="MARKDOWN")
  else:
    txt = """
  *🤖OLÁ, SEJA BEM VINDO A TREMBALA SHOP🚂

✅SO GARANTIMOS LIVE!!
❎NÃO GARANTIMOS SALDO!!
✅TODAS AS INFO SÃO TESTADAS PELO CHK ANTES DA COMPRA!!

💠CANAL DE REFS: @TREMDONATES
👥GRUPO: @TREMBALASTORE
✅SUPORTE: @BALL19874*
    """
    verificar_existe(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, txt, reply_markup=menu, parse_mode="MARKDOWN")

@bot.message_handler(commands=["resgatar"])
def resgatar(message):
  if verify_manutencao() != "DESATIVA":
      bot.send_message(message.chat.id, verify_manutencao(), parse_mode="MARKDOWN")
  else:
    verificar_existe(message.from_user.id, message.from_user.username)
    txt = """
  *🏷️ Resgatar Gift Card*

_- Modo de uso:_
*Para resgatar seu gift card apenas digite /resgatar [ gift card ]*

_- Avisos:_
*O código é só utilizado uma vez!
Quando creditar na conta , o gift será apago do bot, sem reutilização!*
    """
    if message.text == "/resgatar":
      bot.send_message(message.chat.id, txt, parse_mode="MARKDOWN")
    elif message.text == f"/resgatar{userBot}":
  	  bot.send_message(message.chat.id, txt, parse_mode="MARKDOWN")
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
        bot.send_message(idGroup, f"""
      *💳 | Gift resgatado

Gift: {g}
Quem resgatou: {message.from_user.first_name}*
      """, parse_mode="MARKDOWN")
      except:
        bot.send_message(message.chat.id,"*❌ Gift Card inválido ou já foi resgatado!*", parse_mode="MARKDOWN")

@bot.message_handler(commands=['recarga'])
def recarga_pix(message):
  if verify_manutencao() != "DESATIVA":
      bot.send_message(message.chat.id, verify_manutencao(), parse_mode="MARKDOWN")
  else:
    verificar_existe(message.from_user.id, message.from_user.username)
    txt = """
    *Digite /recarga + o valor que deseja.*
    """
    if message.text == "/recarga":
      bot.send_message(message.chat.id, txt, parse_mode="MARKDOWN")
    elif message.text == f"/recarga{userBot}":
      bot.send_message(message.chat.id, txt, parse_mode="MARKDOWN")
    else:
      try:
      	valor = message.text.split("/recarga ")[1]
      	if int(valor) >= 5:
      		id_pix = gerar_pagamento(int(valor))[0]
      		token = "APP_USR-2918657575686072-122219-643ea31e5a0c8930b44b55c2337fe1a3-750863305"
      		headers = {"Authorization": f"Bearer {token}"}
      		request = requests.get(f'https://api.mercadopago.com/v1/payments/{id_pix}', headers=headers)
      		response = request.json()
      		pix = response['point_of_interaction']['transaction_data']['qr_code']
      		msg = bot.send_message(message.chat.id, f"""
*🔮| COMPRAR SALDO|🔮*

_⚡️Você está prestes a comprar saldo para usar no bot!
Para poder pagar, geramos um PIX com duração de 60 minutos, use ele para pagar com o seu banco via PIX usando o PIX gerado para a transação.⚡️

⚠️O saldo irá cair em até 1 minuto após o pagamento via pix. Caso ocorra algum erro após o pagamento, por favor avise o suporte do bot, que te ajudaremos.⚠️_

*ID da compra:* `{id_pix}`
*Chave PIX temporária:* `{pix}`

*Valor:* `R${valor}`""", parse_mode="MARKDOWN")
      		if status(id_pix) == True:
    			   adicao = procurar_dados(message.from_user.id)[0] + int(valor)
    			   total = procurar_dados(message.from_user.id)[1] + 1
    			   cursor.execute(f"UPDATE usuarios SET saldo = {adicao}, recargas = {total} WHERE chat_id = '{message.from_user.id}'"
  )
    			   conn.commit()
    			   bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*⚡️SALDO ADICIONADO COM SUCESSO DIGITE /menu PARA COMPRAR AS CCS⚡️*", parse_mode="MARKDOWN")
    			   bot.send_message(idGroup, f"""
      *💳 | Recarga Realizada
  
Valor: R${valor}
Id do pagamento: {id_pix}
Comprador: {message.from_user.first_name}*
      """, parse_mode="MARKDOWN")
      		else:
      			bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*Pagamento expirado!*", parse_mode="MARKDOWN")
      	else:
      		bot.send_message(message.chat.id, "*O valor da recarga precisa ser igual ou maior que R$5! Tente /recarga 5*", parse_mode="MARKDOWN")
      except:
        bot.reply_to(message, "Ocorreu um erro ao criar o pagamento!")

while True:
  try:
    bot.infinity_polling()
  except:
    continue