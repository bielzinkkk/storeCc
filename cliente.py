from bot import *

def total_infocc():
	cursor.execute("SELECT COUNT(*) FROM infocc")
	for i in cursor.fetchone():
		...
	return i

def pesquisar_bin(bin_j):
  cursor.execute(f"SELECT id FROM infocc WHERE bin = {bin_j}")
  if cursor.fetchone() == None:
    return False
  else:
    cursor.fetchone(f"SELECT cartao FROM infocc WHERE bin = {bin_j}")
    for c in cursor.fetchone():
      ...
    cartao = c[0:6] + "xxxxxxxxxxx"
    return cartao

def view_card(nivel):
  ...  
def aleatoria():
	...

def saldo(chat_id):
	cursor.execute(f"SELECT saldo FROM usuarios WHERE chat_id = {chat_id}")
	for saldo in cursor.fetchone():
		...
	return saldo
def compras(chat_id):
	...
def gift_resgatados(chat_id):
	...
def recargas(chat_id):
	...


def verificar_existe(chat_id, username):
    try:
      cursor.execute( f"SELECT saldo FROM usuarios WHERE chat_id = {chat_id}")
      if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO usuarios(id, chat_id, saldo, compras, recargas, gifts, usuario) VALUES(DEFAULT, {chat_id}, 0, 0, 0, 0, '{username}')")
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def back_menu(call):
	print(call.data)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	<b>🧙🏻‍♂️ | Store de Info'ccs

Olá</b> <a href='https://t.me/{call.from_user.username}'>{call.from_user.first_name}</a><b>, Seja bem vindo a store!</b>

<a href='https://t.me/Yusuke011'>❓ Dúvidas</a>
<a href='https://t.me/Yusuke011'>👥 Grupo</a>
<a href='https://t.me/Yusuke011'>📣 Canal</a>
<a href='https://t.me/Yusuke011'>⚙️ Dev</a>
""", reply_markup=menu, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "pix_auto")
def pixautomatico(call):
	bot.answer_callback_query(callback_query_id=call.id , text="Essa função está temporariamente indisponível! Tente mais tarde.", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "add_saldo")
def menu_addsaldocall(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Escolha uma opção de pagamento abaixo*", reply_markup=menuaddsaldo, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "pix_manu")
def pix_manual(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*💸 Pix Manual

🔑 Chave ( TIPO DE CHAVE ):* `exemplo-chave`
*👤 Nome da conta bancária:* `Jubileuzinho Santos`

*- Não responsabilizaremos por enviar dinheiro a contas random(aleatórias), faça o pix corretamente para adicionar saldo no bot.*

⚠️ _Depois do pagamento envie o comprovante para o {userDono}
⚠️ Depois de realizar o pagamento não possuirá devolução_
	""", reply_markup=voltar_addsaldo, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "baixar_info")
def baixarinfor(call):
	txt = f"""📄 Seu Histórico
	
Cartões Comprados:


Transações:

Recargas ->
Saldo ->
Gifts resgatados ->
Cartões comprados ->
	"""
	arquivo = open("infor.txt", "a+")
	arquivo.write(txt)
	arquivo.close()
	arquivo2 = open("infor.txt", "rb")
	bot.send_document(call.message.chat.id, arquivo2)
	arquivo2.close()
	os.remove("infor.txt")

@bot.callback_query_handler(func=lambda call: call.data == "historico")
def historico(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*📄 Histórico de transações:

💳 Cartões:* `0`
*💰 Saldo:* `R$0`
*💵 Recargas:* `0`
*🎁 Gifts resgatados:* ``

_Atenção:  Os valores presentes nesta sessão, é o total comprado, adicionado e resgatado, respectivamente.
Baixe seu histórico para obter a lista de todos os cartões adquiridos_""", reply_markup=menuhistorico, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "perfil")
def perfil(call):
	print(call.id)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*🧙🏻‍♂️ Perfil de Usuário*
	
_- Informações Básicas_
*Id:* `{call.from_user.id}`
*Username:* @{call.from_user.username}

_- Informações Store_
*Id da carteira:* `{call.from_user.id}`
*Saldo:* `R$0`
*Compras Realizadas:* `0`
*Gifts Resgatados:* `0`
*Recargas Realizadas:* `0`
	""", reply_markup=menuperfil, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "pes_bin")
def pes_bin(call):
	msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
	*Digite uma bin , para buscá-la nas ccs da store:*
	""", reply_markup=menucomprar, parse_mode="MARKDOWN")
	bot.register_next_step_handler(msg, bin_pesquisa)
	
def bin_pesquisa(message):
	try:
		if message.text == "/start":
			bot.send_message(message.chat.id, f"""
	<b>🧙🏻‍♂️ | Store de Info'ccs

Olá</b> <a href='https://t.me/{message.from_user.username}'>{message.from_user.first_name}</a><b>, Seja bem vindo a store!</b>

<a href='https://t.me/{userDono}'>❓ Dúvidas</a>
<a href='https://t.me/{userDono}'>👥 Grupo</a>
<a href='https://t.me/{userDono}'>📣 Canal</a>
<a href='https://t.me/@Yusuke011'>⚙️ Dev</a>
""", reply_markup=menu, parse_mode="HTML")
		if message.text == "/menu":
			bot.send_message(message.chat.id, f"""
	<b>🧙🏻‍♂️ | Store de Info'ccs

Olá</b> <a href='https://t.me/{message.from_user.username}'>{message.from_user.first_name}</a><b>, Seja bem vindo a store!</b>

<a href='https://t.me/{userDono}'>❓ Dúvidas</a>
<a href='https://t.me/{userDono}'>👥 Grupo</a>
<a href='https://t.me/{userDono}'>📣 Canal</a>
<a href='https://t.me/@Yusuke011'>⚙️ Dev</a>
""", reply_markup=menu, parse_mode="HTML")
		elif message.text == "/resgatar":
			bot.send_message(message.chat.id, f"""
	*🏷️ Resgatar Gift Card*

_- Modo de uso:_
*Para resgatar seu gift card apenas digite /resgatar [ gift card ]*

_- Avisos:_
*O código é só utilizado uma vez!
Quando creditar na conta , o gift será apago do bot, sem reutilização!*
""", reply_markup=menu, parse_mode="MARKDOWN")

		elif len(message.text) >= 6:
	 	   bot.send_message(message.chat.id, pesquisar_bin(message.text[0:6]), reply_markup=binmenu(),parse_mode="MARKDOWN")
		else:
			pass
	except:
	  pass
@bot.callback_query_handler(func=lambda call: call.data == "comprar")
def comprar(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*Escolha a opção adequada ao seus propósitos*
	
_- Avisos_
*CHK ON [✓]

Total de Ccs:* `{total_infocc}`
*Saldo Disponível:* `{saldo}`
	""", reply_markup=menucomprar, parse_mode="MARKDOWN")