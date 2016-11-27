from file_io import *
from genetic_algorithm import *


# Declara variaveis globais
global max_setores
global plano_de_acoes
global unidades_gestoras
global output


def inicializar():
	"""
	TODO
	"""
	global max_setores
	max_setores = gastos_maximos_das_ugs("ifl.csv")
	global plano_de_acoes
	plano_de_acoes = ler_tabela_acoes("plano_de_acoes.csv")
	global unidades_gestoras
	unidades_gestoras = ler_ugs("ifl.csv")


def rodar_programa(ug_listbox, anoAtual_entry, anoAnterior_entry, economiaDesejada_entry, ifl_entry, plano_entry):
	"""
	TODO
	"""
	# Declara acesso as variaveis globais
	global max_setores
	global plano_de_acoes
	global unidades_gestoras

	# Decide entre calcular a partir do ano atual e anterior ou da economia desejada
	if anoAnterior_entry.get() != "" or anoAtual_entry.get() != "":
		economia_desejada = string_para_float(anoAtual_entry.get()) - string_para_float(anoAnterior_entry.get())
	elif economiaDesejada_entry.get():
		economia_desejada = string_para_float(economiaDesejada_entry.get())
	else:
		return "Informe o quanto deseja reduzir"

	# Coleta a Unidade Gestora de interesse. Aponta um erro caso nao seja informada.
	try:
		ug_desejada = unidades_gestoras[ug_listbox.curselection()[0]]
	except IndexError:
		return "Informe a Unidade Gestora de interesse"

	# Coleta o arquivo do Indice Financeiro de Liquidacao. Aponta um erro caso nao seja informado.
	if ifl_entry.get() != "":
		gastos_da_ug = ler_tabela_ifl(ug_desejada, ifl_entry.get())
	else:
		return "Informe o arquivo do Indice Financeiro de Liquidacao"

	# Coleta o arquivo do Indice Financeiro de Liquidacao. Aponta um erro caso nao seja informado.
	if ifl_entry.get() != "" and ifl_entry.get() != "ifl.csv":
		max_setores = gastos_maximos_das_ugs(ifl_entry.get())
	elif ifl_entry.get() == "":
		return "Informe o arquivo do Indice Financeiro de Liquidacao"

	# Coleta o arquivo do Plano de Acoes. Aponta um erro caso nao seja informado.
	if plano_entry.get() != "" and plano_entry.get() != "plano_de_acoes.csv":
		plano_de_acoes = ler_tabela_acoes(plano_entry.get())
	elif plano_entry.get() == "":
		return "Informe o arquivo do Plano de Acoes"


	def gasto_anual_no_setor(setor_desejado, gastos_da_ug=gastos_da_ug):
		"""
		Dado um setor, retorna o gasto anual da unidade gestora em analise.

		@setor_desejado: O setor desejado.
		@gastos_da_ug: Uma lista com pares "setor, gasto anual" proviniente da funcao "ler_tabela_ifl".

		@return: O gasto anual do setor da Unidade Gestora em analise.
		"""
		for setor, gasto_anual in gastos_da_ug:
			if setor_desejado == setor:
				return gasto_anual


	def fitness(individuo, max_setores=max_setores, plano_de_acoes=plano_de_acoes, gastos_da_ug=gastos_da_ug, economia_desejada=economia_desejada):
		"""
		Retorna a aptidao do individuo.

		@individuo: uma lista com valores "0" ou "1".
		@max_setor: o valor do setor de maior gasto.
		@plano_de_acoes: Uma lista com "acao, setor, impacto" proviniente da funcao "ler_tabela_acoes".
		@gastos_da_ug: Uma lista com pares "setor, gasto anual" proviniente da funcao "ler_tabela_ifl".
		@peso_de_punicao: O quanto a punicao ira impactar na aptidao final.
		@economia_desejada: O valor de impacto a ser atingido.

		@return: A aptidao do individuo (float).
		"""
		economia_atual = 0
		punicao = 0

		for i, (acao, setor, impacto) in enumerate(plano_de_acoes):
			if individuo[i] == 1:
				economia_atual += impacto
				punicao += gasto_anual_no_setor(setor) / float(max_setores[setor])

		return (1.0 - abs(economia_desejada - economia_atual) / float(economia_desejada)) - punicao


	# Roda o Algoritmo Genetico
	num_acoes = len(plano_de_acoes)
	solucao = algoritmo_genetico(num_individuos=40, num_atributos=num_acoes, num_geracoes=2000,  fitness=fitness, metodo="roleta")

	acoes_da_solucao = ""
	for i in range(num_acoes):
		if solucao[0][i] == 1:
			acoes_da_solucao += plano_de_acoes[i][0] + " - " + plano_de_acoes[i][1] + " - Economia: R$" + str(plano_de_acoes[i][2]) + "\n"
	print acoes_da_solucao
	return acoes_da_solucao


def callback(ug_listbox, anoAtual_entry, anoAnterior_entry, economiaDesejada_entry, ifl_entry, plano_entry):
	global output
	output.set(rodar_programa(ug_listbox, anoAtual_entry, anoAnterior_entry, economiaDesejada_entry, ifl_entry, plano_entry))
	return


# ======================================================================
# Interface Grafica
# ======================================================================

import Tkinter as tk

# Inicializa o codigo lendo as tabelas e coletando informacoes importantes
inicializar()

root = tk.Tk()
root.title("Sugestao de Plano de Acoes")
root.geometry("800x600")

# Espacos para o design
ou = tk.Label(root, text="ou").grid(row=6, column=4)
space="                                                        "
linha_vazia_1 = tk.Label(root, text=space).grid(row=3, column=3)
linha_vazia_2 = tk.Label(root, text=space).grid(row=8, column=3)

# Arquivo do Indice Financeiro de Liquidacao
ifl_label = tk.Label(root, text=space+"Arquivo do Indicador Financeiro de Liquidacao:")
ifl_label.grid(row=1, column=3, sticky='e')
ifl_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
ifl_entry.insert(0, "ifl.csv")
ifl_entry.grid(row=1, column=4)

# Arquivo do Plano de Acoes
plano_label = tk.Label(root, text="Arquivo do Plano de Acoes:")
plano_label.grid(row=2, column=3, sticky='e')
plano_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
plano_entry.insert(0, "plano_de_acoes.csv")
plano_entry.grid(row=2, column=4)

# Gasto do ano anterior
anoAnterior_label = tk.Label(root, text="Informe o gasto deste mes no ano anterior:")
anoAnterior_label.grid(row=4, column=3, sticky='e')
anoAnterior_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
anoAnterior_entry.grid(row=4, column=4)

# Gasto do ano atual
anoAtual_label = tk.Label(root, text="Informe o gasto do mes atual:")
anoAtual_label.grid(row=5, column=3, sticky='e')
anoAtual_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
anoAtual_entry.grid(row=5, column=4)

# Economia desejada
economiaDesejada_label = tk.Label(root, text="Informe o quanto deseja reduzir:")
economiaDesejada_label.grid(row=7, column=3, sticky='e')
economiaDesejada_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
economiaDesejada_entry.grid(row=7, column=4)

# Lista de Unidades Gestoras
listbox_label = tk.Label(root, text="Informe a Unidade Gestora de Interesse:")
listbox_label.grid(row=0, column=0)
scrollbar = tk.Scrollbar(root, orient="vertical")
ug_listbox = tk.Listbox(root, yscrollcommand=scrollbar.set, selectmode="single")
for i, ug in enumerate(unidades_gestoras):
	ug_listbox.insert(i+1, ug)
scrollbar.config(command=ug_listbox.yview)
scrollbar.grid(row=1, column=1, rowspan=7, sticky='nsw')
ug_listbox.grid(row=1, column=0, rowspan=7, sticky='nse')

# Botao de otimizar
otimizar_button = tk.Button(root, text="Otimizar Acoes", command=lambda:callback(ug_listbox, anoAtual_entry, anoAnterior_entry, economiaDesejada_entry, ifl_entry, plano_entry), height=2, bd=0, bg="#546E7A", fg="#FFFFFF")
otimizar_button.grid(row=9, column=4, sticky='ew')

# Saida do programa
output = tk.StringVar()
resultados_label = tk.Label(root, text="Resultatos:").grid(row=11, column=0, sticky='w')
resultado_label = tk.Label(root, textvariable=output, justify='left').grid(row=12, column=0, sticky='w', columnspan=4)

root.mainloop()