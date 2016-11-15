from random import random, shuffle, seed
seed()

def criar_individuos(num_individuos, num_atributos):
	"""
	Cria a populacao inicial. Cada atributo do individuo e' iniciado com um valor aleatorio "0" ou "1".

	@num_individuos: numero total de individuos na populacao.
	@num_atributos: numero total de atributos de um individuo.

	@return: lista da populacao onde cada individuo e' uma lista de atributos.
	"""
	populacao = list()													# Inicializa uma nova lista
	for i in range(num_individuos):										# Itera sob no numero total de individuos
		individuo = list()												# Cria um novo individuo
		for j in range(num_atributos):									# Itera sobe todos os atributos de um individuo
			individuo.append(1 if random() > 0.5 else 0)				# Adiciona no individuo um valor aleatorio "1" ou "0" para o atributo
		populacao.append(individuo)										# Adiciona o individuo na populacao
	return populacao


def fitness(individuo):
	"""
	Calcula a aptidao do individuo.

	@individuo: uma lista de valores "0" ou "1" (atributos).

	@return: um numero correspondente a aptidao.
	"""
	num_atributos = len(individuo)
	aptidao = 0
	for i in range(num_atributos):
		if individuo[i] == 1:
			aptidao += 1
	return aptidao


def roleta(populacao, fitness):
	"""
	Reamostra a populacao atravez do metodo da roleta.

	@populacao: lista com todos os individuos.

	@return: uma lista no mesmo formato de "populacao" com individuos reamostrados.
	"""
	# Calcula a aptidao de cada individuo e guarda na lista "aptidoes"
	aptidoes = list()
	for individuo in populacao:
		aptidoes.append(fitness(individuo))

	# Soma todas as aptidoes e guarda em "total_aptidoes"
	total_aptidoes = sum(aptidoes)

	# Calcula a aptidao relativa de cada individuo e guarda na lista "aptidoes_relativas"
	aptidoes_relativas = list()
	for aptidao in aptidoes:
		aptidoes_relativas.append(aptidao/total_aptidoes)

	populacao_reamostrada = list()
	num_individuos = len(populacao)
	beta = 0.0
	index = int(random()*num_individuos)								# Seleciona o primeiro indice aleatoriamente
	mais_apto = max(aptidoes_relativas)									# Pega a aptidao do individuo mais apto

	# Metodo da roleta propriamente dito
	for i in range(num_individuos):
		beta += random() * 2.0 * mais_apto
		while beta > aptidoes_relativas[index]:
			beta -= aptidoes_relativas[index]
			index = (index + 1) % num_individuos
		populacao_reamostrada.append(populacao[index])
		shuffle(populacao_reamostrada)									# Embaralha a populacao reamostrada
	return populacao_reamostrada


def torneio(populacao, fitness):
	"""
	Reamostra a populacao atravez do metodo do torneio.

	@populacao: lista com todos os individuos.

	@return: uma lista no mesmo formato de "populacao" com individuos reamostrados.
	"""
	populacao_reamostrada = list()										# Declara lista dos individuos reamostrados
	num_individuos = len(populacao)
	for i in range(num_individuos):
		competidor1 = populacao[int(num_individuos*random())]			# Seleciona aleatoriamente um individuo
		competidor2 = populacao[int(num_individuos*random())]			# Seleciona aleatoriamente outro individuo
		if fitness(competidor1) > fitness(competidor2):					# Compara os individuos e seleciona o mais apto
			populacao_reamostrada.append(competidor1)
		else:
			populacao_reamostrada.append(competidor2)
	return populacao_reamostrada										# Retorna os individuos reamostrados


def crossover(progenitor1, progenitor2, taxa_de_crossover=0.5):
	"""
	Performa o cruzamento (crossover) entre dois individuos.

	@progenitor1: lista de atributos do progenitor 1.
	@progenitor2: lista de atributos do progenitor 2.
	@taxa_de_crossover: Informa o quantos atributos devem ser pegos do progenitor 1 (default = 0.5).

	@return: lista de atributos da prole 1 e prole 2 (tuple).
	"""
	num_atributos = len(progenitor1)									# Numero total de atributos
	prole1 = list()
	prole2 = list()

	for i in range(num_atributos):
		if i < num_atributos*taxa_de_crossover:						# Enquanto o ponto de troca nao for excedido
			prole1.append(progenitor1[i])								# pega o atributo do progenitor 1
			prole2.append(progenitor2[i])								# pega o atributo do progenitor 2
		else:															# caso ja tenha excedido
			prole1.append(progenitor2[i])								# pega o atributo do progenitor 2
			prole2.append(progenitor1[i])								# pega o atributo do progenitor 1
	return prole1, prole2


def mutar(individuo, taxa_de_mutacao=0.2):
	"""
	Performa a mutacao do individuo.

	@individuo: lista de atributos do individuo.
	@taxa_de_mutacao: a taxa de atributos a serem invertidos onde 1 equivale a 100% (default = 0.04).

	@return: lista de atributos do individuo com alguns atributos trocados.
	"""
	num_atributos = len(individuo)
	for i in range(num_atributos):
		if random() <= taxa_de_mutacao:
			individuo[i] = 0 if individuo[i] else 1
	return individuo


def algoritmo_genetico(num_individuos, num_atributos, num_geracoes,  fitness, metodo="torneio", taxa_de_crossover=0.5, taxa_de_mutacao=0.2, debug=False):
	"""
	# TODO
	"""
	#if num_individuos % 2:
	#	raise ValueError("Numero de individuos deve ser par")

	# Cria populacao inicial
	populacao = criar_individuos(num_individuos, num_atributos)

	for geracao in range(num_geracoes):
		
		# Reamostragem
		if metodo == "roleta":
			populacao = roleta(populacao, fitness)
		elif metodo == "torneio":
			populacao = torneio(populacao, fitness)
		else:
			raise ValueError("Este metodo nao existe")

		# Crossover
		for i in range(num_individuos):
			progenitor1, progenitor2 = populacao.pop(0), populacao.pop(0)		# Remove da populacao os dois primeiros individuos
			prole1, prole2 = crossover(progenitor1, progenitor2)				# Faz o cruzamento entre os dois individuos recebendo duas proles

			# Mutacao
			prole1 = mutar(prole1)
			prole2 = mutar(prole2)

			# Adiciona as proles a populacao
			populacao.append(prole1)
			populacao.append(prole2)

		# Informacoes para debug
		if debug and geracao%100 == 0:
			aptidao_total = 0
			for individuo in populacao:
				aptidao_total += fitness(individuo)
			print "Gearacao: " + str(geracao+1) + " aptidao media: " + str(float(aptidao_total)/num_individuos)

	# Itera sob todos os individuos da ultima geracao para encontrar o mais apto
	solucao = populacao[0], fitness(populacao[0])								# Inicialmente marca o primeiro individuo como a solucao
	for individuo in populacao:													# Itera sob todos os individuos na populacao
		aptidao = fitness(individuo)											# Calcula a aptidao do individuo
		if solucao[1] < aptidao:
			solucao = individuo, aptidao										# Substitui a solucao pela melhor
	return solucao																# Retorna a solucao mais adaptada


# ========================================================
# SCRIPT DE TESTES

# Criar Individuos
def teste_1():
	populacao = criar_individuos(6, 10)
	for individuo in populacao:
		print individuos

# fitness
def teste_2():
	ind1 = [1, 1, 1, 1, 1, 1, 1, 1]			# Fitness = 8
	ind2 = [0, 0, 0, 0, 0, 0, 0, 0]			# Fitness = 0
	ind3 = [1, 1, 1, 1, 0, 0, 0, 0]			# Fitness = 4
	ind4 = [0, 0, 0, 0, 1, 1, 1, 1]			# Fitness = 4
	print fitness(ind1), fitness(ind2), fitness(ind3), fitness(ind4)

# Crossover
def teste_3():
	ind1 = [1, 1, 1, 1, 1, 1, 1, 1]
	ind2 = [0, 0, 0, 0, 0, 0, 0, 0]
	ind3 = [1, 1, 1, 1, 0, 0, 0, 0]
	ind4 = [0, 0, 0, 0, 1, 1, 1, 1]
	prole1, prole2 = crossover(ind1, ind2)
	prole3, prole4 = crossover(ind3, ind4)
	print prole1
	print prole2
	print prole3
	print prole4

# Mutacao
def teste_4():
	ind1 = [1, 1, 1, 1, 1, 1, 1, 1]
	ind2 = [0, 0, 0, 0, 0, 0, 0, 0]
	print mutar(ind1)
	print mutar(ind2)

# Reamostragens
def teste_5():
	ind1 = [1, 1, 1, 1, 1, 1, 1, 1]
	ind2 = [0, 0, 0, 0, 0, 0, 0, 0]
	ind3 = [1, 1, 1, 1, 1, 0, 0, 0]
	ind4 = [0, 0, 0, 0, 0, 1, 1, 1]
	populacao = [ind1, ind2, ind3, ind4]
	print torneio(populacao)
	print roleta(populacao)