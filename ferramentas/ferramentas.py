import sys, os, requests
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from bot import *
def gen_full():
	data = fordev.generators.people(uf_code="SP")
	nome = data['nome']
	cpf = data['cpf']
	idade = data['idade']
	rg = data['rg']
	sexo = data['sexo']
	mae = data['mae']
	pai = data['pai']
	cep = data['cep']
	endereco = data['endereco']
	numero = data['numero']
	bairro = data['bairro']
	cidade = data['cidade']
	estado = data['estado']
	celular = data['celular']
	data_nasc = data['data_nasc']
	txt = f"""
	*⚙️ Dados Gerado

• Cpf:* `{cpf}`
*• Nome:* `{nome}
*• Data de nascimento:* `{data_nasc}`
*• Idade:* `{idade}`
*• Rg:* `{rg}`
*• Sexo:* `{sexo}`
*• Mãe:* `{mae}`
*• Pai:* `{pai}`
*• Cep:* `{cep}`
*• Endereço:* `{endereco}`
*• Número:* `{numero}`
*• Bairro:* `{bairro}`
*• Cidade:* `{cidade}`
*• Estado:* `{estado}`

*⚜ By: @KGSTORE_BOT*
"""
	return txt

def checker_full(cartao):
	return "*Está em manutenção*"