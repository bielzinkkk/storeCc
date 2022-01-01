from bot import *
from random import randint

def buscarpreco(nivel):
  try:
    cursor.execute(f"SELECT valor FROM valores WHERE nivel = '{nivel}'")
    if cursor.fetchone() == None:
      return 10
    else:
      cursor.execute(f"SELECT valor FROM valores WHERE nivel = '{nivel}'")
      for valor in cursor.fetchone():
        ...
      return valor
  except:
    cursor.execute("ROLLBACK")
    conn.commit()


def total_infocc():
  try:
    cursor.execute("SELECT COUNT(*) FROM infocc")
    for i in cursor.fetchone():
      ...
    return i
  except:
	  cursor.execute("ROLLBACK")
	  conn.commit()

def viewccunitarias(nivel):
  cursor.execute(f"SELECT id FROM infocc WHERE  nivel = '{nivel}'")
  for idcc in cursor.fetchone():
    ...
  cursor.execute(f"SELECT data, bandeira, tipo, nivel, banco, bin FROM infocc WHERE id = {idcc}")
  for u in cursor.fetchall():
    ...
  cvv = "xxx"
  cartao = u[5] + "xxxxxxxxxx"
  txt = f"""
 * 💳 | Informações do Cartão

💳 Cartão:* `{cartao}`
*📆 Expiração:* `{u[0]}`
*🔒 Cvv:* `{cvv}`
*🏳️ Bandeira:* `{u[1]}`
*⚜️ Tipo:* `{u[2]}`
*💠 Nível:* `{u[3]}`
*🏦 Banco:* `{u[4]}`

*💸 Preço:* `R${buscarpreco(nivel)},00`
  """
  return txt, idcc
    
def pegar_cc(idcc, chat_id):
  cursor.execute(f"SELECT cartao, data, cvv, bandeira, tipo, nivel, banco, cpf, nome FROM infocc WHERE id = {idcc}")
  for u in cursor.fetchall():
    ...
  cursor.execute(f"INSERT INTO ccscompradas(id, chat_id, cartao, data, cvv) VALUES(DEFAULT, {chat_id}, {int(u[0])}, '{u[1]}', {int(u[2])})")
  conn.commit()
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
  cursor.execute(f"DELETE FROM infocc WHERE cartao = '{u[0]}'")
  conn.commit()
  return txt
    

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
		cursor.execute(f"SELECT * FROM ccscompradas WHERE chat_id = {chat_id}")
		return cursor.fetchall()
  	
def pesquisar_bin(bin_j):
  cursor.execute(f"SELECT id FROM infocc WHERE bin = '{bin_j}'")
  if cursor.fetchone() == None:
    return "*❌ Bin não encontrada!*"
  else:
    cursor.execute(f"SELECT cartao FROM infocc WHERE bin = '{bin_j}'")
    for cc in cursor.fetchone():
    	...
    cartao = str(cc)[0:6] + "xxxxxxxxxxxx"
    cursor.execute(f"SELECT id, data, bandeira, tipo, nivel, banco, cartao FROM infocc WHERE cartao = '{cc}'")
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
		cursor.execute(f"SELECT saldo, recargas, gifts, compras FROM usuarios WHERE chat_id = {chat_id}")
		for s in cursor.fetchall():
			...
		return s[0], s[1], s[2], s[3]


def comprarunitariafuction(idcc, chat_id):
  cursor.execute(f"SELECT nivel FROM infocc WHERE id = {idcc}")
  for nivel in cursor.fetchone():
  	...
  preco = buscarpreco(nivel.lower())
  total = procurar_dados(chat_id)[0] - preco
  total2 = procurar_dados(chat_id)[3] + 1
  if procurar_dados(chat_id)[0] >= preco:
    cursor.execute(f"UPDATE usuarios SET saldo = {total}, compras = {total2} WHERE chat_id = {chat_id}")
    conn.commit()
    return "Sim", nivel
  else:
    return "Não"


@bot.callback_query_handler(func=lambda call: call.data == "aleatoria")
def aleatoriacall(call):
  bot.answer_callback_query(callback_query_id=call.id , text="Manutenção.", show_alert=True) 

@bot.callback_query_handler(func=lambda call: call.data == "unitarias")
def unitariascall(call):
  if total_infocc() == 0:
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*💳 | Estamos sem estoque no momento, volte mais tarde...*""", reply_markup=menuunitarias() ,parse_mode="MARKDOWN")
  else:
    	cursor.execute("SELECT nivel FROM infocc")
    	for niveltotal in cursor.fetchall():
    		markups = generate_keyboard(sorted(niveltotal),extra=InlineKeyboardButton(text="🔙 Voltar", callback_data="comprar"))
    	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
💳 | Unitárias:*

- CLASSIC: R${buscarpreco('classic')},00
- PLATINUM: R${buscarpreco('platinum')},00
- ELO: R${buscarpreco('elo')},00
- CORPORATE: R${buscarpreco('corporate')},00
- GOLD: R${buscarpreco('gold')},00
- BUSINESS: R${buscarpreco('business')},00
- STANDARD: R${buscarpreco('standard')},00
- BLACK: R${buscarpreco('black')},00
- AMEX: R${buscarpreco('amex')},00

Outros níveis consultar com: {userDono}*

_⚠️ Avisos:_

*- O checker está ativo, portanto ele irá checar as CCs antes da compra!*""", reply_markup=markups,parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def back_menu(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*⚠️BEM VINDO A KING STORE⚠️

☑️SO GARANTIMOS LIVE!!
☑️NÃO GARANTIMOS SALDO!!
☑️TODAS AS INFO SÃO TESTADAS PELO CHK ANTES DA COMPRA!!
☑️OS PREÇOS PODEM VARIAS MAIS SEMPRE VÃO FICAR NA MEDIA DE 7$-10$ NOS NIVEIS BAIXOS!!

☑️REF: @REFKG
☑️GRUPO: @KINGSTORECHAT
*""", reply_markup=menu, parse_mode="MARKDOWN")

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

🔑 Chave ( EMAIL ):* `indeed.company.jobs@gmail.com`
*👤 Nome da conta bancária:* `Tiago Celestino`

*- Não responsabilizaremos por enviar dinheiro a contas random(aleatórias), faça o pix corretamente para adicionar saldo no bot.*

⚠️ _Depois do pagamento envie o comprovante para o {userDono}
⚠️ Depois de realizar o pagamento não possuirá devolução_
	""", reply_markup=voltar_addsaldo, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data.startswith("['value'"))
def viewlal_unirarias(call):
  nivel = ast.literal_eval(call.data)[1]
  idcc = viewccunitarias(nivel)[1]
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=viewccunitarias(nivel)[0], reply_markup=comprarcc_s(idcc),parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data.startswith("['comprar'"))
def comprarlal_unirarias(call):
  idcc = ast.literal_eval(call.data)[1]
  if comprarunitariafuction(idcc, call.from_user.id)[0] == "Sim":
    nivel = comprarunitariafuction(idcc, call.from_user.id)[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Compra efetuda! Clique no botão abaixo para voltar no menu inicial*", reply_markup=comprouprodu,parse_mode="MARKDOWN")
    bot.send_message(call.message.chat.id, pegar_cc(idcc, call.from_user.id),parse_mode="MARKDOWN")
    bot.send_message(idGroup, f"""
    *💳 | Cartão Comprado

Nível: {nivel}
Comprador: {call.from_user.first_name}*
    """, parse_mode="MARKDOWN")
  else:
    bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True) 


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
  verificar_existe(call.from_user.id, call.from_user.username)
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
  verificar_existe(call.from_user.id, call.from_user.username)
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
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*🔀 Comprar Mix*

_- Caso queira comprar seus mix entre contato com {userDono}_
*Não garantimos saldo! 
Garantimos live nos produtos!*

*Futuramente vai está disponibilizado a compra de mixs na store.*
	""", reply_markup=voltar_menucomprar, parse_mode="MARKDOWN")

@bot.callback_query_handler(func=lambda call: call.data == "pes_bin")
def pes_bin(call):
	msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
	*Digite uma bin , para buscá-la nas ccs da store:*
	""", reply_markup=voltar_menucomprar, parse_mode="MARKDOWN")
	bot.register_next_step_handler(msg, bin_pesquisa)
	
def bin_pesquisa(message):
	try:
	  if len(message.text) >= 6:
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
  
  verificar_existe(call.from_user.id, call.from_user.username)
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	*Escolha a opção adequada ao seus propósitos*
	
_- Avisos_
*O checker está ativo

Total de Ccs:* `{total_infocc()}`
	""", reply_markup=menucomprar, parse_mode="MARKDOWN")