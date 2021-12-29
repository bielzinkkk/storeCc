from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup()
menu.row_width = 2
menu.add(InlineKeyboardButton("💳 Comprar", callback_data="comprar"),
InlineKeyboardButton("📄 Histórico", callback_data="historico"))
menu.row_width = 1 
menu.add(InlineKeyboardButton("👤 Perfil", callback_data="perfil"),
InlineKeyboardButton("💵 Adicionar Saldo", callback_data="add_saldo"))

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

def aleatoriamenu(idcc):
	aleatoriamenu = InlineKeyboardMarkup()
	aleatoriamenu.row_width = 1
	aleatoriamenu.add(InlineKeyboardButton("✅ Comprar", callback_data=f"comprar_{idcc}"),
	InlineKeyboardButton("🔁 Escolher outra", callback_data="aleatoria"),
	InlineKeyboardButton("🔙 Voltar", callback_data="comprar"))
	return aleatoriamenu

def binmenu():
	aleatoriamenu = InlineKeyboardMarkup()
	aleatoriamenu.row_width = 1
	aleatoriamenu.add(InlineKeyboardButton("🔁 Pesquisar Outra", callback_data="pes_bin"),
	InlineKeyboardButton("🔙 Voltar", callback_data="comprar"))
	return aleatoriamenu


def menuunitarias():
    cursor.execute("SELECT nivel FROM infocc")
    v = cursor.fetchall()
    markup = types.InlineKeyboardMarkup()
    for i in sorted(set(v)):
      for value in i:
        print(value)
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "']"))
        markup.row_width = 1
        markup.add(InlineKeyboardButton("🔙 Voltar", callback_data="comprar"))
    return markup


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