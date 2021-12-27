from bot import *
import string
import random

def id_generator(size=14, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def total_user():
	cursor.execute("SELECT COUNT(*) FROM usuarios")
	for s in cursor.fetchone():
		...
	return s

def update_valores(tipo, valor):
	cursor.execute(f"UPDATE valores SET valor = {valor} WHERE nivel = {tipo}")
	conn.commit()
  
def procurar_usuario(chat_id):
	cursor.execute(f"SELECT saldo FROM usuarios WHERE chat_id = {chat_id}")
	if cursor.fetchone() == None:
		return None
	else:
		cursor.execute(f"SELECT saldo, recargas, gifts, compras, usuario FROM usuarios WHERE chat_id = {chat_id}")
		for s in cursor.fetchone():
			...
		return s[0], s[1], s[2], s[3], s[4]
@bot.message_handler(commands=['send'])
def notificar(message):
  if verificar_admin(message.from_user.id) == True:
    if message.text == "/send":
                bot.send_message(message.chat.id, """
                *📣 Envie uma mensagem para todos os usuários registrados no bot.

Ex:* _/send + a mensagem que deseja enviar_
                """, parse_mode="MARKDOWN")
    else:
                MSG = message.text.split("/send ")[1]
                bot.send_message(message.chat.id, "Enviando mensagem 📥")
                cursor.execute("SELECT chat_id FROM usuarios")
                for lista in cursor.fetchall():
                    for s in lista:
                      try:
                        bot.send_message(s, MSG, parse_mode="MARKDOWN")
                      except: 
                        contagem += 1
                        continue
                total = contagem - total_user()
                bot.send_message(message.chat.id, f"""
                     📁 Mensagem Enviada

Mensagem: {MSG}
Usuários que não recebeu a mensagem: {contagem} 
Usuários que recebeu: {total}

-> USERS BLOQUEADOS OU CONTAS EXCLUÍDAS NÃO VAI RECEBER AS MENSAGENS!
                      """)

@bot.message_handler(content_types=['photo'])
def photo(message):
	if idDono == message.from_user.id:
		if ("/send" in message.caption):
				raw = message.photo[2].file_id
				path = raw+".jpg"
				file_info = bot.get_file(raw)
				downloaded_file = bot.download_file(file_info.file_path)
				with open(path,'wb') as new_file:
					new_file.write(downloaded_file)
				bot.send_message(message.chat.id, """Enviando mensagem 📥""")
				cursor.execute("SELECT chat_id FROM usuarios")
				captio = message.caption
				for lista in cursor.fetchall():
					for s3 in lista:
						with open(path, "rb") as s2:
							if captio == None:
								captio = ""
								s=requests.post(f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={s3}&caption={captio}", files={'photo': s2})
							else:
								s=requests.post(f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={s3}&caption={captio}&parse_mode=MARKDOWN", files={'photo': s2})

@bot.message_handler(commands=['price'])
def price(message):
  if verificar_admin(message.from_user.id) == True:
      if message.text == "/price":
          bot.send_message(message.chat.id, """
         * ➕ Mude os valores das ccs
          
Modo de uso:* `/price nivel novo_valor`
          """, parse_mode="MARKDOWN")
      else:
            texto = message.text.split("/price ")[1]
            cont = texto.split(" ")[0]
            cc = cont.lower()
            valor = texto.split(" ")[1]
            update_valores(cc, int(valor))
            bot.send_message(message.chat.id, "Valor Modificado!")
  else:
      bot.send_message(message.chat.id, "*Você não possui autorização!*", parse_mode="MARKDOWN")

@bot.message_handler(commands=['adm'])
def admin(message):
  if idDono == message.from_user.id:
      bot.send_message(message.chat.id, """
*⚙️ PAINEL ADMINISTRATIVO*

_• Cmds Admin:_
 
`/add` *- ADICIONAR CC NA STORE*
`/send` *- NOTIFICAR USUÁRIOS*
`/gerar` *- GERAR GIFT*
`/price` *- MUDAR VALORES CONTAS*
`/infor` *- MOSTRA INFORMAÇÕES DO USUÁRIO NO BANCO DE DADOS*

*PARA ENVIAR UMA FOTO PARA OS USUÁRIOS DA STORE SÓ PRECISA ENVIAR A FOTO NO PRIVADO DO BOT.*
""", parse_mode="MARKDOWN")

@bot.message_handler(commands=['infor'])
def info(message):
  if idDono == message.from_user.id:
    if message.text == "/infor":
       bot.send_message(message.chat.id, """
         * 👤 Veja as informações
         
Modo de uso:* `/infor [id de usuário]`
          """, parse_mode="MARKDOWN")
    else:
        chat_id = message.text.split("/infor ")[1]
        if procurar_usuario(chat_id) == None:
        	bot.send_message(message.chat.id, "Esse usuário não esta cadastrado no bot")
        else:
        	bot.send_message(message.chat.id, f"""
        🔍 *USUÁRIO ENCONTRADO

- ID:* `{chat_id}`
*- SALDO:* `R${procurar_usuario(chat_id)[0]}`
*- RECARGA REALIZADAS:* `{procurar_usuario(chat_id)[1]}`
*- GIFTS RESGATADOS:* `{procurar_usuario(chat_id)[2]}`
*- INFO'CCS COMPRADAS:* `{procurar_usuario(chat_id)[3]}`
*- USUÁRIO:* `{procurar_usuario(chat_id)[4]}`
          """, parse_mode="MARKDOWN")

@bot.message_handler(commands=['gerar'])
def gerar_gift(message):
  if idDono == message.from_user.id:
            if message.text == "/gerar":
                bot.send_message(message.chat.id, """
                *💵 Gere um gift card para o usuário resgatar.*

*Ex:* `/gerar` [ valor que deseja ]
                """, parse_mode="MARKDOWN")
            else:
            	try:
            		VALOR = int(message.text.split("/gerar ")[1])
            		cursor.execute(f"INSERT INTO gifts_cards(id, gift_gerado, valor) VALUES(DEFAULT, '{id_generator()}', {VALOR})")
            		conn.commit()
            		bot.send_message(message.chat.id, f"""
             * ✅ GIFT GERADO

Gift Card gerado! O gift possuí o valor de R${VALOR}.

Digite o comando a seguir para resgatar o gift card*
`/resgatar {id_generator()}`""", parse_mode="MARKDOWN")
            	except:
            		bot.send_message(message.chat.id, "Você digitou o valor incorretamente!")