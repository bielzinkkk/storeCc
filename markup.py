from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import *

menu = InlineKeyboardMarkup()
menu.row_width = 2
menu.add(InlineKeyboardButton("💳 Comprar", callback_data="comprar"),
InlineKeyboardButton("📄 Histórico", callback_data="historico"),InlineKeyboardButton("👤 Perfil", callback_data="perfil"),
InlineKeyboardButton("💵 Adicionar Saldo", callback_data="add_saldo"),InlineKeyboardButton("🧰 Ferramentas", callback_data="ferramentas"),InlineKeyboardButton("❓ Suporte", url="https://t.me/LORDEKG"))
menu.row_width = 1
menu.add(InlineKeyboardButton("❓ Suporte", url="https://t.me/LuizzGustavo"))

def troca_cc(id_cc):
	trocarcc = InlineKeyboardMarkup()
	trocarcc.row_width = 2
	trocarcc.add(InlineKeyboardButton("Trocar Cc", callback_data="trocar"))
	return trocarcc

aguardando = InlineKeyboardMarkup()
aguardando.row_width = 2
aguardando.add(InlineKeyboardButton("🔁 AGUARDANDO PAGAMENTO", callback_data="."))

gen_markup = InlineKeyboardMarkup()
gen_markup.add(InlineKeyboardButton("🎲 ATUALIZAR DADOS", callback_data="trocar_dados"))

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

def comprarcc_i(idcc):
	aleatoriamenu = InlineKeyboardMarkup()
	aleatoriamenu.row_width = 1
	aleatoriamenu.add(InlineKeyboardButton("✅ Comprar", callback_data=f"['comprar', '" + str(idcc) + "']"),
	InlineKeyboardButton("🔙 Voltar", callback_data="comprar"))
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

def generate_keyboard(fields: list, **kargs) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup() 
    for buttons in chunks(fields, 2):
        if len(buttons) == 1:
            button = buttons.pop()
            keyboard.add(
                InlineKeyboardButton(text=button, callback_data=f"['value', {button}']")
            )
            continue

        first, second = buttons
        print(first, second)
        keyboard.row(
            InlineKeyboardButton(text=first, callback_data=f"['value', '{first}']"),
            InlineKeyboardButton(text=second, callback_data=f"['value', '{second}']")
        )
            
    extra = kargs.get("extra")
    keyboard.add(extra)
    return keyboard

menuferra = InlineKeyboardMarkup()
menuferra.row_width = 1
menuferra.add(InlineKeyboardButton("🔙 Voltar", callback_data="menu"))

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