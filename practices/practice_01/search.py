
# -*- coding: utf-8 -*-
import heapq

class City(object):
	def __init__(self, name=None, estimate=None, actions=None, acumulated_cost=0):
		self.name = name
		self.estimate = estimate
		self.actions = actions
		self.acumulated_cost = acumulated_cost

class Action(object):
	def __init__(self, city=None, cost=None):
		self.cost = cost
		self.city = city

# >>>>>>>>>> please don't look this <<<<<<<<<<<<<<<<<<<
joao_pessoa = City('João Pessoa', 460)
santa_rita = City('Santa Rita', 451)
mamanguape = City('Mamanguape', 380)
guarabira = City('Guarabira', 340)
areia = City('Areia', 316)
itabaiana = City('Itabaiana', 360)
campina_grande = City('Campina Grande', 300)
soledade = City('Soledade', 243)
picui = City('Picui', 250)
patos = City('Patos', 122)
pombau = City('Pombau', 55)
catole_do_rocha = City('Catole do Rocha', 110)
souza = City('Souza', 20)
coxixola = City('Coxixola', 232)
monteiro = City('Monteiro', 195)
itaporanga = City('Itaporanga', 65)
cajazeiras = City('Cajazeiras', 0)

joao_pessoa.actions = [Action(santa_rita, 26), Action(campina_grande, 125), Action(itabaiana, 68)]
santa_rita.actions = [Action(mamanguape, 38), Action(joao_pessoa, 26)]
mamanguape.actions = [Action(santa_rita, 38), Action(guarabira, 42)]
guarabira.actions = [Action(mamanguape, 42), Action(areia, 41)]
areia.actions = [Action(guarabira, 41), Action(campina_grande, 40)]
itabaiana.actions = [Action(joao_pessoa, 68), Action(campina_grande, 65)]
campina_grande.actions = [Action(itabaiana, 65), Action(joao_pessoa, 68), 
						  Action(areia, 40), Action(soledade, 58), Action(coxixola, 128)]
soledade.actions = [Action(campina_grande, 58), Action(picui, 69), Action(patos, 117)]
picui.actions = [Action(soledade, 69)]
patos.actions = [Action(soledade, 117), Action(itaporanga, 108), Action(pombau, 71)]
pombau.actions = [Action(patos, 71), Action(catole_do_rocha, 57), Action(souza, 56)]
catole_do_rocha.actions = [Action(pombau, 57)]
souza.actions = [Action(pombau, 56), Action(cajazeiras, 43)]
coxixola.actions = [Action(campina_grande, 128), Action(monteiro, 83)]
monteiro.actions = [Action(coxixola, 83), Action(itaporanga, 224)]
itaporanga.actions = [Action(patos, 108), Action(monteiro, 224), Action(cajazeiras, 121)]
cajazeiras.actions = [Action(souza, 43), Action(itaporanga, 121)]

# ####################  ########################

class GraphSearch(object):

	def __init__(self, goals=None):
		self.goals = goals

	def search(self, inital):
		explored = set()
		frontier = [[inital.acumulated_cost + inital.estimate, inital]]

		steps_count = 0 # code for print in the format required
		while True:
			if len(frontier) == 0: return False			
			steps_count += 1 # code for print in the format required
			dic = {'frontier': frontier, 'step':steps_count} # code for print in the format required
			print self.pretty_print_frontier(dic) # code for print in the format required
			remove_choice = self.remove_choice(frontier)
			new_state = remove_choice[1]
			new_state.acumulated_cost = remove_choice[0] - new_state.estimate
			explored.add(new_state)						
			print 'Explorado: ' +  new_state.name + '\n' # code for print in the format required
			if new_state in self.goals:				
				return new_state	
			dic = {'frontier': frontier, 'current_city': new_state, 'explored':explored}		
			self.update_frontier(dic)

	def remove_choice(self, frontier):		
		return heapq.heappop(frontier)

	def update_frontier(self, kwargs):		
		frontier = kwargs.get('frontier')		
		explored = kwargs.get('explored')					
		current_city = kwargs.get('current_city')		
		for action in current_city.actions:			
			action.city.acumulated_cost = current_city.acumulated_cost + action.cost
			if (not action.city in explored): 
				heapq.heappush(frontier, [action.city.estimate + action.city.acumulated_cost, action.city])			

	def pretty_print_frontier(self, kwargs):		
		frontier = kwargs.get('frontier')		
		format_value =  'Passo '+str(kwargs.get('step')) + '.\n'
		format_value += 'Fronteira: '		
		for i in range(len(frontier)):
			format_value += frontier[i][1].name + ': ' + str(frontier[i][0]) + (', ' if i != len(frontier) -1 else '')
		return format_value

# Execution Test

graph = GraphSearch(goals=[cajazeiras])
graph.search(joao_pessoa)