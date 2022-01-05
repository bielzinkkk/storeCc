from cliente import *
from admin import *
from pix_auto.juno import *

@bot.message_handler(commands=["start", "menu"])
def menu_inicial(message):
	verificar_existe(message.from_user.id, message.from_user.username)
	bot.send_message(message.chat.id, f"""
	*⚠️BEM VINDO A KING STORE⚠️

☑️SO GARANTIMOS LIVE!!
☑️NÃO GARANTIMOS SALDO!!
☑️TODAS AS INFO SÃO TESTADAS PELO CHK ANTES DA COMPRA!!
☑️OS PREÇOS PODEM VARIAS MAIS SEMPRE VÃO FICAR NA MEDIA DE 7$-10$ NOS NIVEIS BAIXOS!!

☑️REF: @REFKG
☑️GRUPO: @KINGSTORECHAT*""", reply_markup=menu, parse_mode="MARKDOWN")

@bot.message_handler(commands=["resgatar"])
def resgatar(message):
  verificar_existe(message.from_user.id, message.from_user.username)
  if message.text == "/resgatar":
    bot.send_message(message.chat.id, """
  *🏷️ Resgatar Gift Card*

_- Modo de uso:_
*Para resgatar seu gift card apenas digite /resgatar [ gift card ]*

_- Avisos:_
*O código é só utilizado uma vez!
Quando creditar na conta , o gift será apago do bot, sem reutilização!*""", parse_mode="MARKDOWN")
  elif message.text == f"/resgatar{userBot}":
	  bot.send_message(message.chat.id, """
	  *🏷️ Resgatar Gift Card*

_- Modo de uso:_
*Para resgatar seu gift card apenas digite /resgatar [ gift card ]*

_- Avisos:_
*O código é só utilizado uma vez!
Quando creditar na conta , o gift será apago do bot, sem reutilização!*""", parse_mode="MARKDOWN")
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
  verificar_existe(message.from_user.id, message.from_user.username)
  if message.text == "/recarga":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  elif message.text == f"/recarga{userBot}":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  else:
    try:
    	valor = message.text.split("/recarga ")[1]
    	if int(valor) >= 10:
    		token, url = get_token(), get_url()
    		request = requests.post(
            f"{url}/pix-api/v2/cob",
            json={
                "calendario": {"expiracao": 900},
                "valor": {"original": valor},
                "chave": get_key(),
                "solicitacaoPagador": "Recarga ao bot!",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "X-API-Version": "2",
                "Content-Type": "application/json",
                "X-Resource-Token": get_juno_token(),
            },
        )
    		data = request.json()
    		txid = data["txid"]
    		request2 = requests.get(
            f"{url}/pix-api/qrcode/v2/{txid}/imagem",
            headers={
                "Authorization": f"Bearer {token}",
                "X-API-Version": "2",
                "Content-Type": "application/json",
                "X-Resource-Token": get_juno_token(),
            }
        )
    		pixqr = request2.json()
    		copy_past = base64.b64decode(pixqr["qrcodeBase64"]).decode("utf-8")
    		msg = bot.send_message(message.chat.id, f"""
 *🔮| COMPRAR SALDO|🔮*

_⚡️Você está prestes a comprar saldo para usar no bot!
Para poder pagar, geramos um PIX com duração de 60 minutos, use ele para pagar com o seu banco via PIX usando o PIX gerado para a transação.⚡️

⚠️O saldo irá cair em até 1 minuto após o pagamento via pix. Caso ocorra algum erro após o pagamento, por favor avise o suporte do bot, que te ajudaremos.⚠️_

*ID da compra:* `{txid}`
*Chave PIX temporária:* `{copy_past}`

*Valor:* `R${valor}`
  			""", parse_mode="MARKDOWN")
    		if payment_sucess(txid, token) == True:
  			   adicao = int(valor) + procurar_dados(message.from_user.id)[0]
  			   sql = f"UPDATE usuarios SET saldo = {adicao} WHERE chat_id = {message.from_user.id}"
  			   cursor.execute(sql)
  			   conn.commit()
  			   bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*⚡️SALDO ADICIONADO COM SUCESSO DIGITE /menu PARA COMPRAR AS CCS⚡️*", parse_mode="MARKDOWN")
    		else:
    			bot.edit_message_text(chat_id=message.chst.id, message_id=msg.message_id, text="*Pagamento expirado!*", parse_mode="MARKDOWN")
    	else:
    		bot.send_message(message.chat.id, "*O valor da recarga precisa ser igual ou maior que R$10! Tente /recarga 10*", parse_mode="MARKDOWN")
    except:
    	return "Erro!"

while True:
  try:
    bot.infinity_polling()
  except:
    continue