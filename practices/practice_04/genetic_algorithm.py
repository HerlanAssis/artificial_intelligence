import random

def f(individual):	
	return abs(36 - sum([card + 1 for card in range(len(individual)) if individual[card]]))

def make_population(number_of_individuals, population=[]):	
	if number_of_individuals:
		individual = [0] * 10		
		number_of_chosen_cards = random.randint(1, 10)
		chosen_cards = []
		while len(chosen_cards) < number_of_chosen_cards:
			chosen_card = random.randint(1, 10)
			if not(chosen_card in chosen_cards):
				individual[chosen_card-1] = 1
				chosen_cards.append(chosen_card)
		population.append(individual)
		return make_population(number_of_individuals-1, population)
	return population

def evaluate_individuals(individuals):
	return [(f(individual), individual) for individual in individuals]

def uniform_crossover(parents):	
	children = [[],[]]
	for i in range(len(parents[0])):
		drawn_number = random.randint(0, 1)
		children[0].append(parents[drawn_number][i])
		children[1].append(parents[1 if drawn_number == 0 else 0][i])		
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
		key = [key for key in interval_list_map.keys() if float(key[:key.find('_')]) <= random_number and random_number < float(key[key.find('_')+1:])][0]
		if not(interval_list_map[key] in parents):
			parents.append(interval_list_map[key])
	return parents

def mutate(individual, percent_of_mutate):
	qtde_genes_for_mutate = int(len(individual) * percent_of_mutate)
	indices_of_modified_genes = []	
	while qtde_genes_for_mutate:
		index_gene = random.randint(0, len(individual) -1)
		if index_gene in indices_of_modified_genes: continue
		individual[index_gene] = 0 if individual[index_gene] else 1
		indices_of_modified_genes.append(index_gene)
		qtde_genes_for_mutate-= 1	
	return individual

def mutate_all(individuals, percent_of_mutate):
	return [mutate(individual, percent_of_mutate) for individual in individuals]

def individual_to_cards(individual):
	return [card + 1 for card in range(len(individual)) if individual[card]]

def genetic_algorithm(population, max_generations, percent_of_mutate):
	number_of_individuals_original_population = len(population)
	mutate_over_generations = int(max_generations * 0.5)
	generation = 1
	while max_generations > 1:
		evaluated_population = evaluate_individuals(population)
		if number_of_individuals_original_population != len(population):
			evaluated_population.sort()
			evaluated_population =  evaluated_population[:number_of_individuals_original_population]
			population = [individual[1] for individual in evaluated_population]		
		for individual in evaluated_population:	
			if individual[0] == 0:				
				return individual_to_cards(individual[1])				
		parents = roulette(int(len(population)*0.2), population)
		parents_pair = [[parents[i], parents[i+1]] for i in range(0, len(parents)-1, 2)]		
		children = []
		for parents_pair_element in parents_pair:
			children += uniform_crossover(parents_pair_element)
		if generation > mutate_over_generations:			
			children = mutate_all(children, percent_of_mutate)
		population += children
		max_generations-= 1
		generation += 1
	return individual_to_cards(sorted(evaluate_individuals(population))[0][1])	

def main():		
	population = make_population(number_of_individuals=20)		
	print genetic_algorithm(population, max_generations=5, percent_of_mutate=0.2)		
	
main()