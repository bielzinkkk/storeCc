from bot import *
import string
import random
import requests
from sqlalchemy import create_engine
import pandas as pd
import fordev
url2 = "postgresql://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"

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
  try:
    splited = card.split("|")
    return {
      "cartao": splited[0],
      "data": splited[1] + "/" + splited[2],
      "cvv": splited[3]
    }
  except:
    continue


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
	      response2 = requests.get("https://lookup.binlist.net/"+h)
	      bin_cc.append((js['bin']))
	      try:
	        if response2.status_code != 400:
	          response = response2.json()
	          banco1 = response["bank"]
	          tipo.append((response["type"].upper()))
	          nivel.append((response["brand"].upper()))
	          bandeira.append((response["scheme"].upper()))
	          if banco1 == {}:
	            banco.append(("Não disponível"))
	          else:
	            banco.append((banco1["name"]))
	      except:
	        continue
	      cp = fordev.generators.cpf(uf_code="SP", formatting=True, data_only=True)
	      cpf.append((str(cp)))
	      nome_int = fordev.generators.people(uf_code="SP")['nome']
	      nome.append((nome_int))
	    engine = create_engine(url2)
	    tabela = pd.DataFrame.from_dict({"cartao": cartao, "data": data, "cvv": cvv, "bin": bin_cc, "banco": banco, "nivel": nivel, "tipo": tipo, "bandeira": bandeira, "cpf": cpf, "nome": nome}, orient='index')
	    tabela = tabela.transpose()
	    tabela.to_sql(name='infocc', con=engine, if_exists='append', index=False)
	    cursor.execute("delete from infocc where not (infocc is not null);")
	    conn.commit()
	    bot.send_message(message.chat.id, "Cc's adicionadas")
 

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
Para adicionar mix vc digita o comando /mix + as ccs que deseja adicionar

- Adicionar cc:
Para adicionar cc vc digita o comando /cc + as ccs que deseja adicionar

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