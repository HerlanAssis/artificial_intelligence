import random

def f(x): return abs(36 - sum(x))

def make_population(number_of_individuals, cards, genes_per_individual, population=[]):	
	if number_of_individuals:
		individual = []
		while len(individual) < genes_per_individual:
			genes = random.choice(cards)
			if not(genes in individual): individual.append(genes)
		population.append(individual)
		return make_population(number_of_individuals-1, cards, genes_per_individual, population)
	return population

def evaluate_individuals(individuals):
	return [(f(individual), individual) for individual in individuals]

def uniform_crossover(parents):
	while True:
		children = [[],[]]
		for i in range(len(parents[0])):
			number_drawn = random.randint(0, 1)
			children[0].append(parents[number_drawn][i])
			children[1].append(parents[1 if number_drawn == 0 else 0][i])
		if len(children[0]) == len(set(children[0])) and len(children[1]) == len(set(children[1])): break
	return children

def roulette(n, population):
	parents = []
	evaluated_population = evaluate_individuals(population)
	sum_evaluated_population = sum([individual[0] for individual in evaluated_population])
	interval_list_map = {}
	init_interval = float(0)
	for individual in evaluated_population:
		interval_list_map[str(init_interval)+'_'+str(init_interval + individual[0])] = individual[1]
		init_interval = init_interval + individual[0]
	while len(parents) < n:
		random_number = random.random() * sum_evaluated_population
		key = [key for key in interval_list_map.keys() if float(key[:key.find('_')]) <= random_number and random_number <float(key[key.find('_')+1:])][0]
		if len(interval_list_map[key]) == len(set(interval_list_map[key])) and not(interval_list_map[key] in parents):
			parents.append(interval_list_map[key])
	return parents

def genetic_algorithm(population, max_gerations, percent_of_mutation):
	number_of_individuals_original_population = len(population)	
	while max_gerations > 0:
		evaluated_population = evaluate_individuals(population)
		if number_of_individuals_original_population != len(population):
			evaluated_population.sort()
			evaluated_population =  evaluated_population[:number_of_individuals_original_population]
			population = [individual[1] for individual in evaluated_population]		
		for individual in evaluated_population:
			if individual[0] == 0: return individual[1]
		parents = roulette(int(len(population)*0.2), population)
		parents_pair = [[parents[i], parents[i+1]] for i in range(0, len(parents)-1, 2)]		
		children = []
		for parents_pair_element in parents_pair:
			children += uniform_crossover(parents_pair_element)
		population += children
		max_gerations-= 1
	return population[:number_of_individuals_original_population]

def main():
	cards = range(1, 11)
	population = make_population(20, cards, 5)
	print genetic_algorithm(population, 4, 5)	

main()