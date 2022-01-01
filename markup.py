from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import psycopg2
url = "postgres://njwtqqfcpjsxht:650ee0cd2c99aaf100cc25dbb25843209fdf5bb7b39d19ae741f7d1856499d17@ec2-18-213-179-70.compute-1.amazonaws.com:5432/d56f1hlgaibe59"
conn = psycopg2.connect(url)
cursor = conn.cursor()
menu = InlineKeyboardMarkup()
menu.row_width = 2
menu.add(InlineKeyboardButton("💳 Comprar", callback_data="comprar"),
InlineKeyboardButton("📄 Histórico", callback_data="historico"))
menu.row_width = 1
menu.add(InlineKeyboardButton("👤 Perfil", callback_data="perfil"),
InlineKeyboardButton("💵 Adicionar Saldo", callback_data="add_saldo"))
menu.row_width = 2
menu.add(InlineKeyboardButton("⚙️ Dev", url="https://t.me/Yusuke011"),
InlineKeyboardButton("❓ Suporte", url="https://t.me/LORDEKG"))


aguardando = InlineKeyboardMarkup()
aguardando.row_width = 2
aguardando.add(InlineKeyboardButton("🔁 AGUARDANDO PAGAMENTO", callback_data="."))

menucomprar = InlineKeyboardMarkup()
menucomprar.row_width = 2
menucomprar.add(InlineKeyboardButton("💳 Unitárias", callback_data="unitarias"),
InlineKeyboardButton("🔀 Mix", callback_data="mix"),
InlineKeyboardButton("🎲 Aleatória", callback_data="aleatoria"),
InlineKeyboardButton("🔍 Pesquisar Bin", callback_data="pes_bin"),)
menucomprar.row_width = 1 
menucomprar.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu"))

comprouprodu = InlineKeyboardMarkup()
comprouprodu.add(InlineKeyboardButton("✔️ Menu", callback_data="menu"))

def comprarcc_s(idcc):
	aleatoriamenu = InlineKeyboardMarkup()
	aleatoriamenu.row_width = 1
	aleatoriamenu.add(InlineKeyboardButton("✅ Comprar", callback_data=f"['comprar', '" + str(idcc) + "']"),
	InlineKeyboardButton("🔙 Voltar", callback_data="unitarias"))
	return aleatoriamenu

def binmenu():
	aleatoriamenu = InlineKeyboardMarkup()
	aleatoriamenu.row_width = 1
	aleatoriamenu.add(InlineKeyboardButton("🔁 Pesquisar Outra", callback_data="pes_bin"),
	InlineKeyboardButton("🔙 Voltar", callback_data="comprar"))
	return aleatoriamenu

def verificar_valor():
  cursor.execute("SELECT nivel FROM infocc")
  v = cursor.fetchall()
  for i in sorted(set(v)):
    for value in i:
      cursor.execute(f"SELECT id FROM valores WHERE nivel = '{value.lower()}'")
      if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO valores(id, valor, nivel) VALUES(DEFAULT, 10, '{value.lower()}')")
        conn.commit()
verificar_valor()

def chunks(items, n):
    for item in range(0, len(items), n):
        yield items[item:item+n]

def generate_keyboard(buttons: list, **kargs) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup() 
    for buttons in chunks(buttons, 2):
        for i in buttons:
	        if len(buttons) == 1:
	            button = buttons.pop()
	            keyboard.add(
	                 InlineKeyboardButton(text=button, callback_data=f"['value', {button}']")
	            )
	            continue
	        u, y = buttons
	        keyboard.row(
	            InlineKeyboardButton(text=u, callback_data=f"['value', '{u}']"),
	            InlineKeyboardButton(text=y, callback_data=f"['value', '{y}']")
	        )
               
    extra = kargs.get("extra")
    keyboard.add(extra)
    return keyboard




menuperfil = InlineKeyboardMarkup()
menuperfil.row_width = 1
menuperfil.add(InlineKeyboardButton("💵 Adicionar Saldo", callback_data="add_saldo"),
InlineKeyboardButton("🔙 Voltar", callback_data="menu"))

menuhistorico = InlineKeyboardMarkup()
menuhistorico.row_width = 1
menuhistorico.add(InlineKeyboardButton("📥 Baixar Informações", callback_data="baixar_info"),
InlineKeyboardButton("🔙 Voltar", callback_data="menu"))

menuaddsaldo = InlineKeyboardMarkup()
menuaddsaldo.row_width = 2
menuaddsaldo.add(InlineKeyboardButton("🔹 Pix Automático", callback_data="pix_auto"),
InlineKeyboardButton("🔸 Pix Manual", callback_data="pix_manu"))
menuaddsaldo.row_width = 1 
menuaddsaldo.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu"))

voltar_menucomprar = InlineKeyboardMarkup()
voltar_menucomprar.add(InlineKeyboardButton("🔙 Voltar", callback_data="comprar"))

voltar_addsaldo = InlineKeyboardMarkup()
voltar_addsaldo.add(InlineKeyboardButton("🔙 Voltar", callback_data="add_saldo"))