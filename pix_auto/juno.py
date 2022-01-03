import base64, os, requests, pytz, datetime, time, json
import telebot
token = "5099084790:AAHPLEzuj_c2uTy3Ge9uTezqbhz9EX9Aihk"
bot = telebot.TeleBot(token)
def make_credentials() -> str:
    client_id = "Edw690zjdWn66p8X"
    client_secret = "[3*a$k.181ZDFkl^_T]-FSL5lU]Z*H#B"
    credentials_encoded = f"{client_id}:{client_secret}".encode("ascii")
    credentials_base64 = base64.b64encode(credentials_encoded)

    return credentials_base64.decode("ascii")


def get_url():
	return "https://api.juno.com.br"

def get_token() -> str:
    credentials = make_credentials()
    url = get_url()
    request = requests.post(
            f"{url}/authorization-server/oauth/token",
            data={"grant_type": "client_credentials"},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {credentials}",
            },
        )
    response = request.json()
    return response["access_token"]

def get_juno_token():
	return "D9DF3F980E95CC362D214274DD101C0A712CA391BF9665E5FACF803FA0F48BD1"

def get_key():
	return "e6024d84-6741-4a2b-9628-a7ca939e7e12"

        
def expiration():
    with open('../config/config.json', 'r') as file:
        config = json.loads(file.read())
        expiration_payment = config['expiration_payment_in_minutes']
    
    time_change = datetime.timedelta(minutes=int(expiration_payment))
    new_time = datetime.datetime.now() + time_change

    tz = pytz.timezone("America/Bahia")
    aware_dt = tz.localize(new_time)

    a = aware_dt.isoformat()
    
    return a[:23]+a[26:]
    
def payment_sucess(txid: str, token: str) -> dict:
	url = get_url()
	request = requests.get(
				f"{url}/pix-api/v2/cob/{txid}",
	headers={
                "Authorization": f"Bearer {token}",
                "X-API-Version": "2",
                "Content-Type": "application/json",
                "X-Resource-Token": get_juno_token(),
            },
	)
	data = request.json()
	status = data['status']
	print(status)
	with open('../config/config.json', 'r') as file:
          config = json.loads(file.read())

	expiration_payment = config['expiration_payment_in_minutes']
	contador = 0
	while True:
            contador += 1
            
            if not contador > int(expiration_payment):
                if status == 'ATIVA':
                    pass
                    
                elif status == 'CONCLUIDA':
                    r = 1
                    break
                
                time.sleep(60)
                
            else:
                r = 0
                break

	if r == 1:
	       return True
        
	else:
		return False

@bot.message_handler(commands=['pix'])
def pix(message):
	token, url = get_token(), get_url()
	valor = message.text.split("/pix ")[1]
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
	bot.send_message(message.chat.id, f"Copy past: {copy_past}")
	if payment_sucess(txid, token) == True:
		bot.reply_to(message, "Pago")
	else:
		bot.reply_to(message, "Expirado")
bot.polling()