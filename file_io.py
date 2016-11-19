#!/usr/bin/env python
# -*- coding: utf-8 -*-

arquivo = open("IFL.csv", "r")

def mostrar_arquivo(arquivo=arquivo):
	for linha in arquivo:
		print linha


def string_para_float(string):
	"""
	Converte um numero real no formato brasileiro em uma string para um float.

	@string: string com um numero real no formato brasileiro.

	@return: float equivalente ao numero entrado.
	"""
	string_list = string.split(".")										# Remove os pontos
	dezenas, centavos = string_list[-1].split(",")						# Separa as dezenas dos centesimos
	resposta = ""
	for i in string_list:
		if not("," in i):
			resposta += i 												# Concatena a resposta
	
	return float(resposta + dezenas + "." + centavos)					# Concatena a resposta total e converte para float


def ler_tabela_ifl(ug_desejada, nome_arquivo="ifl.csv"):
	"""
	A partir da tabela do Indicador Financeiro de Liquidacao, gera uma lista com o gasto anual de cada setor da unidade gestora selecionada.

	@ug_desejada: Unidade Gestora que se deseja obter os gastos.
	@arquivo: arquivo ".csv" com os dados das unidades gestoras.

	@return: retorna lista com pares setor-gasto no formato:
	         [[setor, gasto anual]
	          [setor, gasto anual]
	           ...
	          [setor, gasto anual]]

	"""
	arquivo = open(nome_arquivo, "r")
	gastos_da_ug = list()

	# Busca pela unidade gestora desejada
	for line in arquivo:
		line_list = line.split(',"')									# Transforma a linha numa lista
		split_index = line_list[0].rfind("-")							# Pega a posicao do ultimo hifen

		unidade_gestora = line_list[0][:split_index]					# Pega o nome da unidade gestora da linha
		setor = line_list[0][split_index+1:]							# Pega o setor da linha
		valor = line_list[-1][:-2]										# Pega o valor gasto no setor

		if unidade_gestora == ug_desejada:								# Caso a linha se refira a Unidade Gestora de interesse,
			gastos_da_ug.append([setor, string_para_float(valor)])		# adiciona o par "setor, gasto" a lista de gastos

	return gastos_da_ug


def ler_tabela_acoes(nome_arquivo="plano_de_acoes.csv"):
	"""
	TODO
	"""
	arquivo = open(nome_arquivo, "r")
	plano_de_acoes = list()
	for line in arquivo:
		try:
			line_list = line.split(",")
			acao = line_list[0]
			setor = line_list[1]
			impacto = string_para_float(line_list[2][1:] + ',' + line_list[3][:-2])
			plano_de_acoes.append([acao, setor, impacto])
		
		except IndexError:
			pass
		except ValueError:
			pass
		else:
			pass
	
	return plano_de_acoes