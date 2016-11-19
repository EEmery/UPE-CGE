from genetic_algorithm import *

def fitness1(individuo):
	"""
	Calcula a aptidao do individuo.
	Melhor individuo deve ser do tipo: 1, 1, 1, 1, 1, 1, ...

	@individuo: uma lista de valores "0" ou "1" (atributos).

	@return: um numero correspondente a aptidao.
	"""
	num_atributos = len(individuo)
	aptidao = 0
	for i in range(num_atributos):
		if individuo[i] == 1:
			aptidao += 1
	return aptidao


def testar_a_criacao(num_individuos=6, num_atributos=10):
	populacao = criar_individuos(num_individuos, num_atributos)
	print "Criei " + str(num_individuos) + " individuos com " + str(num_atributos) + " atributos..."
	for individuo in populacao:
		print individuo


def testar_reamostragens():
	ind1 = [1, 1, 1, 1, 1, 1, 1, 1]
	ind2 = [0, 0, 0, 0, 0, 0, 0, 0]
	ind3 = [1, 1, 1, 1, 1, 0, 0, 0]
	ind4 = [0, 0, 0, 0, 0, 1, 1, 1]
	populacao = [ind1, ind2, ind3, ind4]
	print torneio(populacao, fitness1)
	print roleta(populacao, fitness1)


def teste_completo():
	ind1 = [1, 1, 1, 1, 1, 1, 1, 1]
	ind2 = [0, 0, 0, 0, 0, 0, 0, 0]
	ind3 = [1, 1, 1, 1, 1, 0, 0, 0]
	ind4 = [0, 0, 0, 0, 0, 1, 1, 1]
	populacao = [ind1, ind2, ind3, ind4]

	# Testa 1 da funcao fitness
	if fitness1(ind1) == 8:
		print ("Teste 1 da funcao fitness: correto")
	else:
		print ("Teste 1 da funcao fitness: incorreto")
	# Testa 2 da funcao fitness
	if fitness1(ind2) == 0:
		print ("Teste 2 da funcao fitness: correto")
	else:
		print ("Teste 2 da funcao fitness: incorreto")
	# Testa 3 da funcao fitness
	if fitness1(ind3) == 5:
		print ("Teste 3 da funcao fitness: correto")
	else:
		print ("Teste 3 da funcao fitness: incorreto")
	# Testa 4 da funcao fitness
	if fitness1(ind4) == 3:
		print ("Teste 4 da funcao fitness: correto")
	else:
		print ("Teste 4 da funcao fitness: incorreto")
	print "-------------------------------------------"

	prole1, prole2 = crossover(ind1, ind2)
	prole3, prole4 = crossover(ind3, ind4)
	# Teste 1 de crossover
	if prole1 == [1, 1, 1, 1, 0, 0, 0, 0] and prole2 == [0, 0, 0, 0, 1, 1, 1, 1]:
		print ("Teste 1 do crossover: correto")
	else:
		print ("Teste 1 do crossover: incorreto")
	# Teste 2 de crossover
	if prole3 == [1, 1, 1, 1, 0, 1, 1, 1] and prole4 == [0, 0, 0, 0, 1, 0, 0, 0]:
		print ("Teste 2 do crossover: correto")
	else:
		print ("Teste 2 do crossover: incorreto")
	print "-------------------------------------------"

	# Teste de mutacao
	if ind1!=mutar(ind1) or ind2!=mutar(ind2) or ind3!=mutar(ind3) or ind4!=mutar(ind4):
		print ("Teste de mutacao: correto")
	else:
		print ("Teste de mutacao: incorreto")


def teste_rapido():
	print "Iniciando teste pelo metodo do torneio...\n"
	solucao_torneio = algoritmo_genetico(num_individuos=30, num_atributos=8, num_geracoes=2000,  fitness=fitness1, metodo="torneio", taxa_de_crossover=0.5, taxa_de_mutacao=0.2, debug=True)
	print "\nIniciando teste pelo metodo da roleta...\n"
	solucao_roleta = algoritmo_genetico(num_individuos=30, num_atributos=8, num_geracoes=2000,  fitness=fitness1, metodo="roleta", taxa_de_crossover=0.5, taxa_de_mutacao=0.2, debug=True)
	print "\nMelhores solucoes encontradas:\n"
	print str(solucao_torneio[0]) + " Aptidao: " + str(solucao_torneio[1]) + " (metodo do torneio)"
	print str(solucao_roleta[0]) + " Aptidao: " + str(solucao_roleta[1]) + " (metodo da roleta)"
	print "[1, 1, 1, 1, 1, 1, 1, 1] Aptidao: 8 (solucao ideal)\n"

teste_rapido()