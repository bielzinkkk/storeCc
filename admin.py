from bot import *
import string
import random
import requests
from sqlalchemy import create_engine
import pandas as pd

url2 = "postgresql://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"

def search_string_in_file(file_name, string_to_search):
    line_number = 0
    list_of_results = []
     # Abrindo arquivo modo de leitura
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if string_to_search in line:
                list_of_results.append((line_number, line.rstrip()))
    return list_of_results

def value_bin(bin_cc):
  matched_lines = search_string_in_file('utils/bins.csv', bin_cc)
  for elem in matched_lines:
    data = elem[1].split(" :")
    # ['459316', 'CREDIT', 'PLATINUM', 'VISA', 'ITAU UNIBANCO, S.A.', 'BR']
  return data[1], data[2], data[3], data[4]


def verificar_admin(chat_id):
  try:
    sql = f"SELECT id FROM admins WHERE chat_id = {chat_id}"
    cursor.execute(sql)
    if cursor.fetchone() == None:
      return False
    else: 
      return True
  except:
    cursor.execute("ROLLBACK")
    conn.commit()

def split_card(card) -> dict:
      	splited = card.split("|")
      	return {
      	"cartao": splited[0],
      	"data": splited[1] + "/" +splited[2],
      	"cvv": splited[3]
      	}

def relatorio():
	sql = "SELECT COUNT(*) FROM usuarios"
	cursor.execute(sql)
	for user in cursor.fetchone():
		...
	sql = "SELECT COUNT(*) FROM ccscompradas"
	cursor.execute(sql)
	for ccs in cursor.fetchone():
	   ...
	sql = "SELECT COUNT(*) FROM admins"
	cursor.execute(sql)
	for admins in cursor.fetchone():
	   ...
	return user, ccs, admins

def id_generator(size=14, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def update_valores(tipo, valor):
	cursor.execute(f"UPDATE valores SET valor = {valor} WHERE nivel = '{tipo}'")
	conn.commit()
 
def procurar_usuario(chat_id):
	cursor.execute(f"SELECT saldo FROM usuarios WHERE chat_id = {chat_id}")
	if cursor.fetchone() == None:
		return None
	else:
		cursor.execute(f"SELECT saldo, recargas, gifts, compras, usuario FROM usuarios WHERE chat_id = {chat_id}")
		for s in cursor.fetchall():
			...
		return s[0], s[1], s[2], s[3], s[4]

@bot.message_handler(commands=['relatorio'])
def relatorio_command(message):
  if verificar_admin(message.from_user.id) == True:
    bot.reply_to(message, f"""
     *[✓] Relatório da store
     
Ccs compradas:* {relatorio()[1]}
*Usuários Cadastrados:* {relatorio()[0]}
*Admins:* {relatorio()[2]}
    """, parse_mode="MARKDOWN")
	
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
                      s=requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={s}&text={MSG}&parse_mode=MARKDOWN")
     
@bot.message_handler(content_types=['document'])
def document(message):
	if verificar_admin(message.from_user.id) == True:
	  if ("/cc" in message.caption):
	    raw = message.document.file_id
	    path = raw+".txt"
	    file_info = bot.get_file(raw)
	    downloaded_file = bot.download_file(file_info.file_path)
	    with open(path,'wb') as new_file:
	      new_file.write(downloaded_file)
	      new_file.close()
	    bot.send_message(message.chat.id, """Adicionando...""")
	    f = open(path, "r")
	    samples = f.read()
	    cards = [split_card(card) for card in samples.strip().split("\n")]
	    cartao = []
	    data = []
	    cvv = []
	    for row in cards:
	      cartao.append((row['cartao']))
	      data.append((row['data']))
	      cvv.append((row['cvv']))
	    bin_cc = []
	    banco = []
	    tipo = []
	    nivel = []
	    bandeira = []
	    cpf = []
	    nome = []
	    for u in cartao:
	      line1 = ','.join(u)
	      h = line1[0:12].replace(",", "")
	      js = {"bin": h}
	      bin_cc.append((js['bin']))
	      try:
	        tipo.append((value_bin(str(js['bin'][0]))))
	        nivel.append((value_bin(str(js['bin'][1]))))
	        bandeira.append((value_bin(str(js['bin'][2]))))
	        banco.append((value_bin(str(js['bin'][3]))))
	      except:
	        bot.reply_to(message, "Não foi possível adicionar as cc's!")
	      cp = fordev.generators.cpf(uf_code="SP", formatting=True, data_only=True)
	      cpf.append((str(cp)))
	      nome_int = fordev.generators.people(uf_code="SP")['nome']
	      nome.append((nome_int))
	    engine = create_engine(url2)
	    tabela = pd.DataFrame.from_dict({"cartao": cartao, "data": data, "cvv": cvv, "bin": bin_cc, "banco": banco, "nivel": nivel, "tipo": tipo, "bandeira": bandeira, "cpf": cpf, "nome": nome}, orient='index')
	    tabela = tabela.transpose()
	    tabela.to_sql(name='infocc', con=engine, if_exists='append', index=False)
	    bot.send_message(message.chat.id, "Cc's adicionadas")

@bot.message_handler(commands=['estoque'])
def estoque(message):
  if message.from_user.id == 1869219363:
    cursor.execute("SELECT cartao, data, cvv FROM infocc")
    cartao = cursor.fetchall()
    bot.send_message(message.chat.id, cartao+"\n")

@bot.message_handler(content_types=['photo'])
def photo(message):
	if verificar_admin(message.from_user.id) == True:
		if ("/send" in message.caption):
				raw = message.photo[2].file_id
				path = raw+".jpg"
				file_info = bot.get_file(raw)
				downloaded_file = bot.download_file(file_info.file_path)
				with open(path,'wb') as new_file:
					new_file.write(downloaded_file)
				bot.send_message(message.chat.id, """Enviando mensagem 📥""")
				cursor.execute("SELECT chat_id FROM usuarios")
				captio = message.caption.split("/send ")[1]
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
  if verificar_admin(message.from_user.id) == True:
      bot.send_message(message.chat.id, """
*⚙️ PAINEL ADMINISTRATIVO*

_• Cmds Admin:_
 
`/add` *- ADICIONAR CC OU MIX NA STORE*
`/send` *- NOTIFICAR USUÁRIOS*
`/gerar` *- GERAR GIFT*
`/price` *- MUDAR VALORES CONTAS*
`/infor` *- MOSTRA INFORMAÇÕES DO USUÁRIO NO BANCO DE DADOS*
`/relatorio` *- RELATORIO DA STORE*

*PARA ENVIAR UMA FOTO PARA OS USUÁRIOS DA STORE SÓ PRECISA ENVIAR A FOTO NO PRIVADO DO BOT.*
""", parse_mode="MARKDOWN")

@bot.message_handler(commands=['infor'])
def info(message):
  if verificar_admin(message.from_user.id) == True:
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
*- USUÁRIO:* @{procurar_usuario(chat_id)[4]}
          """, parse_mode="MARKDOWN")

@bot.message_handler(commands=['add'])
def adicionar_cemixc(message):
  if verificar_admin(message.from_user.id) == True:
    bot.send_message(message.chat.id, """
  📥 Adicionar cc ou mix

- Adicionar mix:
Para adicionar mix vc digita o comando /mix + as ccs que deseja adicionar ( Manutenção )

- Adicionar cc:
Para adicionar cc tem que criar um arquivo txt e adicionar suas cc's , no formato cartao|mes|ano|cvv, depois só digitar na legenda do arquivo /cc

Pode adicionar quanta cc quiser.
  """)

@bot.message_handler(commands=['gerar'])
def gerar_gift(message):
  if verificar_admin(message.from_user.id) == True:
            if message.text == "/gerar":
                bot.send_message(message.chat.id, """
                *💵 Gere um gift card para o usuário resgatar.*

*Ex:* `/gerar` [ valor que deseja ]
                """, parse_mode="MARKDOWN")
            else:
            	try:
            		VALOR = int(message.text.split("/gerar ")[1])
            		gift = id_generator()
            		cursor.execute(f"INSERT INTO gifts_cards(id, gift_gerado, valor) VALUES(DEFAULT, '{gift}', {VALOR})")
            		conn.commit()
            		bot.send_message(message.chat.id, f"""
             * ✅ Gift gerado

Gift Card gerado! O gift possuí o valor de R${VALOR}.

Digite o comando a seguir para resgatar o gift card*
`/resgatar {gift}`""", parse_mode="MARKDOWN")
            	except:
            		bot.send_message(message.chat.id, "Você digitou o valor incorretamente!")