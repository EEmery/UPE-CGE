#!/usr/bin/env python
# -*- coding: utf-8 -*-

def mostrar_arquivo(nome_arquivo="ifl.csv"):
	"""
	Imprime o arquivo inserido.

	@nome_arquivo: Nome do arquivo ".csv" que se deseja imprimir.
	"""
	arquivo = open(nome_arquivo, 'r')
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


def index_de_corte(string):
	"""
	Encontra a posicao (index de corte) do hifen que separa a unidade gestora do setor de atuacao dela.

	@string: string com a unidade gestora e o setor de atuacao concatenados.

	@return: o index do hifen (um inteiro) ou "-1" se nao houver hifen na string.
	"""
	split_index = len(string)
	while True:
		split_index = string[:split_index].rfind("-")					# Pega a posicao do ultimo hifen
		if split_index == -1:											# Caso ele nao encontre um hifen
			return -1
		if string[:split_index].isupper():								# Caso a string resultante seja toda maiuscula
			return split_index											# retorna a posicao do ultimo hifen


def ler_tabela_ifl(ug_desejada, nome_arquivo="ifl.csv"):
	"""
	A partir da tabela do Indicador Financeiro de Liquidacao, gera uma lista com o gasto anual de cada setor da unidade gestora selecionada.

	@ug_desejada: Unidade Gestora que se deseja obter os gastos.
	@nome_arquivo: Nome do arquivo ".csv" com os dados das unidades gestoras.

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
		split_index = index_de_corte(line_list[0])						# Pega a posicao do ultimo hifen

		unidade_gestora = line_list[0][:split_index]					# Pega o nome da unidade gestora da linha
		setor = line_list[0][split_index+1:]							# Pega o setor da linha
		valor = line_list[-1][:-2]										# Pega o valor gasto no setor

		if unidade_gestora == ug_desejada:								# Caso a linha se refira a Unidade Gestora de interesse,
			gastos_da_ug.append([setor, string_para_float(valor)])		# adiciona o par "setor, gasto" a lista de gastos

	return gastos_da_ug


def ler_tabela_acoes(nome_arquivo="plano_de_acoes.csv"):
	"""
	A partir da tabela do Plano de Acoes, gera uma lista com as acoes, os setores e os impactos do plano.

	@nome_arquivo: Nome do arquivo ".csv" com o plano de acoes.

	@return: retorna lista com pares setor-gasto no formato:
			 [[acao, setor, impacto],
			  [acao, setor, impacto],
			   ...
			  [acao, setor, impacto]]
	"""
	arquivo = open(nome_arquivo, "r")
	plano_de_acoes = list()
	for line in arquivo:
		try:
			line_list = line.split(",")													# Separa a linha numa lista
			acao = line_list[0]															# Pega a acao da linha (string)
			setor = line_list[1]														# Pega o setor da linha (string)
			impacto = string_para_float(line_list[2][1:] + ',' + line_list[3][:-2])		# Pega o impacto da linha (float)
			plano_de_acoes.append([acao, setor, impacto])								# Adiciona a acao, o setor e o impacto na lista de saida
		
		# Em caso de erro no nome do arquivo e demais erros
		except IndexError:
			pass
		except ValueError:
			pass
		else:
			pass
	
	return plano_de_acoes


def ler_ugs(nome_arquivo="ifl.csv"):
	"""
	A partir do arquivo do Indice Financeiro de Liquidacao, le todas as Unidades Gestoras e retorna em uma lista.

	@nome_arquivo: Nome do arquivo ".csv" com os dados do Indice Financeiro de Liquidacao.

	@return: lista de strings com todas as Unidades Gestoras no Indice Financeiro de Liquidacao.
	"""
	arquivo = open(nome_arquivo, "r")
	unidades_gestoras = list()
	for line in arquivo:
		line_list = line.split(',"')									# Transforma a linha numa lista
		split_index = index_de_corte(line_list[0])

		if split_index != -1:
			ug = line_list[0][:split_index]								# Pega o nome da unidade gestora da linha
			if not(ug in unidades_gestoras):							# Caso a unidade gestora ainda nao esteja na lista
				unidades_gestoras.append(ug)							# adiciona a mesma na lista de unidades gestoras
	return unidades_gestoras