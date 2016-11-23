from file_io import *
from genetic_algorithm import *


def rodar_programa(ug_listbox, anoAtual_entry, anoAnterior_entry, economiaDesejada_entry, ifl_entry, plano_entry, unidades_gestoras, peso_de_punicao=0.3):
	"""
	TODO
	"""
	# Decide entre calcular a partir do ano atual e anterior ou da economia desejada
	if anoAnterior_entry.get() != "" or anoAtual_entry.get() != "":
		economia_desejada = string_para_float(anoAtual_entry.get()) - string_para_float(anoAnterior_entry.get())
	elif economiaDesejada_entry.get():
		economia_desejada = string_para_float(economiaDesejada_entry.get())
	else:
		print "Informe o quanto deseja reduzir"
		return

	# Coleta a Unidade Gestora de interesse. Aponta um erro caso nao seja informada.
	try:
		ug_desejada = unidades_gestoras[ug_listbox.curselection()[0]]
	except IndexError:
		print "Informe a Unidade Gestora de interesse"
		return

	# Coleta o arquivo do Indice Financeiro de Liquidacao. Aponta um erro caso nao seja informado.
	if ifl_entry.get() != "":
		gastos_da_ug = ler_tabela_ifl(ug_desejada, ifl_entry.get())
	else:
		print "Informe o arquivo do Indice Financeiro de Liquidacao"
		return

	# Coleta o arquivo do Plano de Acoes. Aponta um erro caso nao seja informado.
	if plano_entry.get() != "":
		plano_de_acoes = ler_tabela_acoes(plano_entry.get())
	else:
		print "Informe o arquivo do Plano de Acoes"
		return

	max_setor = max(zip(*gastos_da_ug)[1])


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


	def fitness(individuo, max_setor=max_setor, plano_de_acoes=plano_de_acoes, gastos_da_ug=gastos_da_ug, peso_de_punicao=peso_de_punicao, economia_desejada=economia_desejada):
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
				punicao += gasto_anual_no_setor(setor) * peso_de_punicao / float(max_setor)

		return (1.0 - abs(economia_desejada - economia_atual) / float(economia_desejada)) - punicao


	# Roda o Algoritmo Genetico
	num_acoes = len(plano_de_acoes)
	solucao = algoritmo_genetico(num_individuos=40, num_atributos=num_acoes, num_geracoes=2000,  fitness=fitness, metodo="roleta")

	for i in range(num_acoes):
		if solucao[0][i] == 1:
			print plano_de_acoes[i][0], plano_de_acoes[i][1], plano_de_acoes[i][2]


# ======================================================================
# Interface Grafica
# ======================================================================

import Tkinter as tk

root = tk.Tk()
root.title("Sugestao de Plano de Acoes")
root.geometry("800x600")

x_margin1 = 20
x_margin = 330
x_margin_entry = 650
y_margin = -10
y_padding = 25

# Arquivo do Indice Financeiro de Liquidacao
ifl_label = tk.Label(root, text="Arquivo do Indicador Financeiro de Liquidacao:")
ifl_label.place(x=x_margin, y=y_margin+y_padding)
ifl_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
ifl_entry.insert(0, "ifl.csv")
ifl_entry.place(x=x_margin_entry, y=y_margin+y_padding)

# Arquivo do Plano de Acoes
plano_label = tk.Label(root, text="Arquivo do Plano de Acoes:")
plano_label.place(x=x_margin, y=y_margin+y_padding*2)
plano_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
plano_entry.insert(0, "plano_de_acoes.csv")
plano_entry.place(x=x_margin_entry, y=y_margin+y_padding*2)

# Gasto do ano anterior
anoAnterior_label = tk.Label(root, text="Informe o gasto deste mes do ano anterior:")
anoAnterior_label.place(x=x_margin, y=y_margin+y_padding*3)
anoAnterior_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
anoAnterior_entry.place(x=x_margin_entry, y=y_margin+y_padding*3)

# Gasto do ano atual
anoAtual_label = tk.Label(root, text="Informe o gasto do mes atual:")
anoAtual_label.place(x=x_margin, y=y_margin+y_padding*4)
anoAtual_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
anoAtual_entry.place(x=x_margin_entry, y=y_margin+y_padding*4)

# Economia desejada
economiaDesejada_label = tk.Label(root, text="Informe o quanto deseja reduzir:")
economiaDesejada_label.place(x=x_margin, y=y_margin+y_padding*5)
economiaDesejada_entry = tk.Entry(root, bg="#546E7A", bd=0, fg="#FFFFFF")
economiaDesejada_entry.place(x=x_margin_entry, y=y_margin+y_padding*5)

# Lista de Unidades Gestoras
listbox_label = tk.Label(root, text="Informe a Unidade Gestora de Interesse:")
listbox_label.place(x=x_margin1, y=y_margin+y_padding*1)
if ifl_entry.get() != "":
	unidades_gestoras = ler_ugs(ifl_entry.get())
else:
	unidades_gestoras = []
scrollbar = tk.Scrollbar(root, orient="vertical")
ug_listbox = tk.Listbox(root, yscrollcommand=scrollbar.set, selectmode="single", height=12)
for i, ug in enumerate(unidades_gestoras):
	ug_listbox.insert(i+1, ug)
scrollbar.config(command=ug_listbox.yview)
scrollbar.place(x=x_margin1+130, y=y_margin+y_padding*2)
ug_listbox.place(x=x_margin1+6, y=y_margin+y_padding*2)

# Botao de otimizar
otimizar_button = tk.Button(root, text="Otimizar Acoes", command=lambda:rodar_programa(ug_listbox, anoAtual_entry, anoAnterior_entry, economiaDesejada_entry, ifl_entry, plano_entry, unidades_gestoras), height=2, width=20, bd=0, bg="#546E7A", fg="#FFFFFF")
otimizar_button.place(x=x_margin_entry-23, y=y_margin+y_padding*8)

root.mainloop()