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


def roleta(populacao, fitness):
	"""
	Reamostra a populacao atravez do metodo da roleta.

	@populacao: lista com todos os individuos.
	@fitness: funcao fitness.

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
	@fitness: Funcao fitness.

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


def crossover(progenitor1, progenitor2):
	"""
	Performa o cruzamento (crossover) entre dois individuos.

	@progenitor1: lista de atributos do progenitor 1.
	@progenitor2: lista de atributos do progenitor 2.

	@return: lista de atributos da prole 1 e prole 2 (tuple).
	"""
	num_atributos = len(progenitor1)									# Numero total de atributos
	prole1 = list()
	prole2 = list()
	crossover_point = int(random()*num_atributos)

	for i in range(num_atributos):
		if i < crossover_point:											# Enquanto o ponto de troca nao for excedido
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
	individuo_mutado = list()
	for i in range(num_atributos):
		if random() <= taxa_de_mutacao:
			individuo_mutado.append(0 if individuo[i] else 1)
		else:
			individuo_mutado.append(individuo[i])
	return individuo_mutado


def algoritmo_genetico(num_individuos, num_atributos, num_geracoes,  fitness, metodo="torneio", taxa_de_crossover=0.7, taxa_de_mutacao=0.2, tipo_de_retorno='individuo', debug=False):
	"""
	Utiliza um algoritmo genetico para encontrar uma solucao optima ou sub-optima.

	@num_individuos: Numero de individuos na populacao.
	@num_atributos: Numero de atributos de cada individuo.
	@num_geracoes: Numero de geracoes.
	@fitness: Funcao fitness.
	@metodo: Metodo de reamostragem. Possui dois valores "roleta" ou "torneio".
	@taxa_de_crossover: Ponto de troca no crossover (0.0 - 1.0).
	@taxa_de_mutacao: Probabilidade de um atributo ter seu valor invertido (0.0 - 1.0).
	@tipo_de_retorno: 'individuo' retorna o melhor individuo da ultima geracao, 'geracao' retorna toda a ultima geracao.
	@debug: Se possuir o valor "True", imprime mensagens de debug no terminal.

	@return: Uma tuple onde [0] e' uma lista dos atributos do melhor individuo da ultima geracao e [1] e' a sua aptidao ou uma lista de tuples ordenada.
	"""
	# Cria populacao inicial
	populacao = criar_individuos(num_individuos, num_atributos)

	for geracao in range(num_geracoes):

		# Informacoes para debug
		if debug and geracao%100 == 0:
			aptidao_total = 0
			for individuo in populacao:
				aptidao_total += fitness(individuo)
			print "Gearacao: " + str(geracao) + " aptidao media: " + str(float(aptidao_total)/num_individuos)
		
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

			if random() < taxa_de_crossover:
				prole1, prole2 = crossover(progenitor1, progenitor2)			# Faz o cruzamento entre os dois individuos recebendo duas proles
			else:
				prole1, prole2 = progenitor1, progenitor2						# Faz dos progenitores, as proles (nao ha' cruzamento)

			# Mutacao
			prole1 = mutar(prole1)
			prole2 = mutar(prole2)

			# Adiciona as proles a populacao
			populacao.append(prole1)
			populacao.append(prole2)

	solucao = []
	for individuo in populacao:												# Itera sob todos os individuos na populacao
		aptidao = fitness(individuo)										# Calcula a aptidao do individuo
		solucao.append((individuo, aptidao))								# Adiciona o par individuo-aptidao a solucao
	
	if tipo_de_retorno == 'individuo':										# Retorna o individuo mais apto
		return solucao[zip(*solucao)[1].index(max(zip(*solucao)[1]))]

	return sorted(solucao, key=lambda tup: -tup[1])							# Retorna toda a ultima geracao em ordem decrescente de aptidao