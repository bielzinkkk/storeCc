from bot import *
from random import randint

def buscarpreco(nivel):
  cursor.execute("SELECT valor FROM valores WHERE nivel = '{nivel}'")
  if cursor.fetchone() == None:
    return 10
  else:
    for valor in cursor.fetchone():
      ...
    return valor

def total_infocc():
	cursor.execute("SELECT COUNT(*) FROM infocc")
	for i in cursor.fetchone():
		...
	return i

def verificar_existe(chat_id, usuario):
    try:
      cursor.execute( f"SELECT id FROM usuarios WHERE chat_id = {chat_id}")
      if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO usuarios(id, chat_id, saldo, compras, recargas, gifts, usuario) VALUES (DEFAULT, {chat_id}, 0, 0, 0, 0, '{usuario}')")
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()


def buscar_ccscompradas(chat_id):
	cursor.execute(f"SELECT id FROM ccscompradas WHERE chat_id = {chat_id}")
	if cursor.fetchone() == None:
		return "Não possui nenhuma cc comprada"
	else:
		cursor.execute(f"SELECT cartao, data, cvv FROM ccscompradas WHERE chat_id = {chat_id}")
		for y in cursor.fetchall():
			...
		return f"{y[0]}|{y[1]}|{y[2]}"
  	
def pesquisar_bin(bin_j):
  cursor.execute(f"SELECT id FROM infocc WHERE bin = {int(bin_j)}")
  if cursor.fetchone() == None:
    return "*❌ Bin não encontrada!*"
  else:
    cursor.execute(f"SELECT cartao FROM infocc WHERE bin = {bin_j}")
    for cc in cursor.fetchone():
    	...
    cartao = str(cc)[0:6] + "xxxxxxxxxxxx"
    cursor.execute(f"SELECT id, data, bandeira, tipo, nivel, banco, cartao FROM infocc WHERE cartao = {cc}")
    for u in cursor.fetchall():
    	...
    txt = f"""
  	*	🔍 | Bin Encontrada

💳 Cartão:* `{cartao}`
*📆 Expiração:* `{u[1]}`
*🏳️ Bandeira:* `{u[2]}`
*⚜️ Tipo:* `{u[3]}`
*💠 Nível:* `{u[4]}`
*🏦 Banco:* `{u[5]}`
"""
    return txt

def procurar_dados(chat_id):
	cursor.execute(f"SELECT id FROM usuarios WHERE chat_id = {chat_id}")
	if cursor.fetchone() == None:
		return None
	else:
		cursor.execute(f"SELECT saldo, compras, gifts, recargas FROM usuarios WHERE chat_id = {chat_id}")
		for s in cursor.fetchall():
			...
		return s[0], s[1], s[2], s[3]


def view_cardaleatoria():
    cursor.execute(f"SELECT cartao FROM infocc")
    if cursor.fetchone() == None:
      return None
    else:
      cursor.execute(f"SELECT cartao FROM infocc")
      for cc in cursor.fetchone():
        ...
      cartao = str(cc)[0:6] + "xxxxxxxxxxxx"
      cursor.execute(f"SELECT id, data, bandeira, tipo, nivel, banco, cartao FROM infocc WHERE cartao = {cc}")
      for u in cursor.fetchall():
        ...
      return cartao, u[0], u[1], u[2], u[3], u[4], u[5]

@bot.callback_query_handler(func=lambda call: call.data == "aleatoria")
def aleatoriacall(call):
    if view_cardaleatoria() == None:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
  	*❌ Não possuimos estoque no momento, tente mais tarde...*
  """,reply_markup=voltar_menucomprar,parse_mode="MARKDOWN")
    else:
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
  *	📁 | Detalhes do cartão:
  
  💳 Cartão:* `{view_cardaleatoria()[0]}`
  *📆 Expiração:* `{view_cardaleatoria()[2]}`
  *🏳️ Bandeira:* `{view_cardaleatoria()[3]}`
  *⚜️ Tipo:* `{view_cardaleatoria()[4]}`
  *💠 Nível:* `{view_cardaleatoria()[5]}`
  *🏦 Banco:* `{view_cardaleatoria()[6]}`
  """, reply_markup=aleatoriamenu(idcc), parse_mode="MARKDOWN")
      

def comprar_ccaleatoria(idcc):
    cursor.execute(f"SELECT nome FROM infocc WHERE id = {idcc}")
    if cursor.fetchone() == None:
      return "Esse cartão ja foi comprado! Tente atualizar e comprar uma cc que deseja."
    else:
      cursor.execute(f"SELECT cartao, data, cvv, bandeira, tipo, nivel, banco, cpf, nome FROM infocc WHERE id = {self.idcc}")
      for u in cursor.fetchall():
      	...
      txt = f"""
    	*	✅ Compra efetuada
  
  💳 Cartão:* `{u[0]}`
  *📆 Expiração:* `{u[1]}`
  *🔒 Cvv:* `{u[2]}`
  *🏳️ Bandeira:* `{u[3]}`
  *⚜️ Tipo:* `{u[4]}`
  *💠 Nível:* `{u[5]}`
  *🏦 Banco:* `{u[6]}`
  
  *👤 Nome:* `{u[8]}`
  *📁 Cpf:* `{u[7]}`
  
  Cartão Verificado (Live) ✔️
  """
      return txt

@bot.callback_query_handler(func=lambda call: call.data == "unitarias")
def unitariascall(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 | Unitárias:*

- CLASSIC: R${buscarpreco('CLASSIC')},00
- PLATINUM: R${buscarpreco('PLATINUM')},00
- ELO: R${buscarpreco('ELO')},00
- CORPORATE: R${buscarpreco('CORPORATE')},00
- GOLD: R${buscarpreco('GOLD')},00
- BUSINESS: R${buscarpreco('BUSINESS')},00
- STANDARD: R${buscarpreco('STANDARD')},00
- BLACK: R${buscarpreco('BLACK')},00
- AMEX: R${buscarpreco('AMEX')},00

Outros níveis consultar com: {userDono}*

_⚠️ Avisos:_

*- O checker está ativo, portanto ele irá checar as CCs antes da compra!*""", reply_markup=menuunitarias() ,parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def back_menu(call):
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
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*💸 Pix Automático

- _Modo de uso:_
/recarga 2

- Utilize um valor inteiro.
- Não responsabilizaremos por enviar dinheiro a contas random(aleatórias), faça o pix corretamente para adicionar saldo no bot.
- Tem prazo de 5 minutos para realizar o pix*

⚠️ _Depois do pagamento , o saldo será adicionado na hora
⚠️ Depois de realizar o pagamento não possuirá devolução_
	""", reply_markup=voltar_addsaldo, parse_mode="MARKDOWN")


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

{buscar_ccscompradas(call.from_user.id)}

Transações:

Recargas -> {procurar_dados(call.from_user.id)[1]}
Saldo -> {procurar_dados(call.from_user.id)[0]}
Gifts resgatados -> {procurar_dados(call.from_user.id)[2]}
Cartões comprados -> {procurar_dados(call.from_user.id)[3]}
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

💳 Cartões:* `{procurar_dados(call.from_user.id)[3]}`
*💰 Saldo:* `R${procurar_dados(call.from_user.id)[0]}`
*💵 Recargas:* `{procurar_dados(call.from_user.id)[1]}`
*🎁 Gifts resgatados:* `{procurar_dados(call.from_user.id)[2]}`

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
*Saldo:* `R${procurar_dados(call.from_user.id)[0]}`
*Compras Realizadas:* `{procurar_dados(call.from_user.id)[3]}`
*Gifts Resgatados:* `{procurar_dados(call.from_user.id)[2]}`
*Recargas Realizadas:* `{procurar_dados(call.from_user.id)[1]}`
	""", reply_markup=menuperfil, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "mix")
def mixcall(call):
  bot.answer_callback_query(callback_query_id=call.id , text="Função temporariamente indisponível!")

@bot.callback_query_handler(func=lambda call: call.data == "pes_bin")
def pes_bin(call):
	msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
	*Digite uma bin , para buscá-la nas ccs da store:*
	""", reply_markup=voltar_menucomprar, parse_mode="MARKDOWN")
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
			 try:
			 	bin_s = message.text[0:6]
			 	bot.send_message(message.chat.id, pesquisar_bin(bin_s), reply_markup=binmenu(),parse_mode="MARKDOWN")
			 except:
			 	bot.send_message(message.chat.id, "Ocorreu um erro ao buscar a bin!")
		else:
			pass
	except:
	  pass
@bot.callback_query_handler(func=lambda call: call.data == "comprar")
def comprar(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*Escolha a opção adequada ao seus propósitos*
	
_- Avisos_
*Pix Automático ativo.

Total de Ccs:* `{total_infocc()}`
*Saldo Disponível:* `R${procurar_dados(call.from_user.id)[0]}`
	""", reply_markup=menucomprar, parse_mode="MARKDOWN")