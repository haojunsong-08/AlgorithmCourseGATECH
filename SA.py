'''

The Simulated Annealing local search algorithm for TSP.

'''

import numpy as np
import math
import random
import time
import argparse
import re
import csv

'''

Parse through all arguments.

'''
'''
parser = argparse.ArgumentParser()
parser.add_argument('-i', required = True)
parser.add_argument('-t', required = True, type = int)
parser.add_argument('-s', required = False, type = int)
args = parser.parse_args()

filename = args.i
given_time = args.t
seed = args.s
'''
def create_adj_mat(f_name):
	'''
	
	The function reads through a file and generate corresponding name of city, number of nodes, and adjacency matrix.

	'''

	fh = open(f_name, 'r')
	lines = fh.read().splitlines()

	for i in range(len(lines)):
		if re.search(pattern = "NAME", string = lines[i]):
			line_list = lines[i].split(' ')
			city = line_list[1]
		if re.search(pattern = "DIMENSION", string = lines[i]):
			line_list = lines[i].split(' ')
			dim = int(line_list[1])
		if re.search(pattern = "NODE_COORD_SECTION", string = lines[i]):
			node_coord_section = lines[i+1: i+dim+1]
			break
	coordinates = [(0,0) for i in range(dim)]
	for i in node_coord_section:
		coord_list = i.split(' ')
		row = coord_list[0]
		x_coord = coord_list[1]
		y_coord = coord_list[2]
		row = int(row) - 1
		coordinates[row] = (float(x_coord), float(y_coord))

	adj_mat = [[0 for i in range(dim)] for j in range(dim)]
	for i in range(dim):
		x_coord_1, y_coord_1 = coordinates[i]
		for j in range(dim):
			x_coord_2, y_coord_2 = coordinates[j]
			adj_mat[i][j] = round(math.sqrt((x_coord_1-x_coord_2)**2 + (y_coord_1 - y_coord_2)**2))

	adj_mat = np.asarray(adj_mat, dtype='float')
	np.fill_diagonal(adj_mat, float('inf'))
	write_adj_mat = open("adj_mat.csv", 'w')
	writer = csv.writer(write_adj_mat)
	for i in adj_mat:
		writer.writerow(i)
	return dim, adj_mat

class SA(object):
	'''

	Class to implement simulated annealing algorithm for TSP.

	'''

	def __init__(self, matrix, dim, random_seed=None):
		'''

		The function initializes all variables
		
		'''

		random.seed(random_seed)
		self.matrix = matrix
		self.dim = dim
		self.T = 10000
		self.cooling_rate = 0.00001
		self.best_solution = None
		self.best_distance = float("inf")
		self.trace = []

	def create_init_solution(self):
		'''

		The function initializes solution by randomly selecting node and appending the remaining nodes.

		'''

		init_solution = []
		remaining = list(range(self.dim))

		rand_city = random.sample(range(self.dim), 1)[0]
		init_solution.append(rand_city)
		remaining.remove(rand_city)
		init_solution = init_solution + remaining

		return init_solution

	def cost_sol(self, solution):
		'''

		The function calculates total distance of a given solution.

		'''

		distance = 0
		for i in range(self.dim-1):
			distance += self.matrix[solution[i]][solution[i + 1]]
		distance += self.matrix[solution[-1]][solution[0]]
		return distance

	def swap_two_random(self, solution):
		'''

		The function randomly selects two indexes from solution and swaps the values of indexes.

		'''

		new_solution = np.copy(solution)
		two_random = random.sample(range(len(new_solution)), 2)
		first = two_random[0]
		second = two_random[1]
		temp = new_solution[first]
		new_solution[first] = new_solution[second]
		new_solution[second] = temp
		return new_solution

	def acceptance_criterion(self, test_distance, new_distance):
		'''

		The function compares given test distance and new distance to determine
		whether the test distance is accepted or not.

		'''

		if new_distance < test_distance:
			return 1.0
		else:
			return math.exp((test_distance - new_distance)/self.T)

	def simulated_annealing(self,given_time):
		'''

		The function runs simulated annealing algorithm on initialized solution.
		The algorithm runs while Temperature is not 0, then the algorithm keeps
		track on the best solution, distance, and runtime of the function.

		'''

		start_time = time.time()
		init_solution = self.create_init_solution()
		self.best_solution = np.copy(init_solution)

		while self.T > 1:

			new_solution = self.swap_two_random(init_solution)
			init_distance = self.cost_sol(init_solution)
			new_distance = self.cost_sol(new_solution)
			criterion = self.acceptance_criterion(init_distance, new_distance)

			if criterion > random.random():
				init_solution = new_solution

				if self.cost_sol(init_solution) < self.cost_sol(self.best_solution):
					self.best_solution = init_solution
					self.best_distance = round(self.cost_sol(self.best_solution))
					#print(self.best_solution)
					#print(self.best_distance)
					end_time = time.time()
					duration = end_time - start_time
					duration_format = '{:.2f}'.format(duration)
					self.trace.append(f"{duration_format}, {self.best_distance}\n")

			self.T *= (1-self.cooling_rate)
			#print(self.best_solution)

	def output_sol(self, cost, solution, filename):
		solution_write = ""
		for i in range(len(solution)):
			if i != len(solution)-1:
				solution_write += str(solution[i]) + ","
			else:
				solution_write += str(solution[i])
		with open(filename, "w") as sol_file:
			sol_file.write(str(cost) + "\n")
			sol_file.write(solution_write)

	def output_trace(self, trace, filename):
		with open(filename, "w") as trace_file:
			for i in trace:
				trace_file.write(i)


'''
def main():
	city, dim, adj_mat = create_adj_mat(filename)
	if seed:
		s = SA(adj_mat, dim, seed)
	else:
		s = SA(adj_mat, dim)
	s.simulated_annealing(given_time)
	quality = s.best_distance
	route = s.best_solution
	trace = s.trace

	print(quality)

	route_write = ""
	for i in range(len(route)):
		if i != len(route)-1:
			route_write += str(route[i]) + ","
		else:
			route_write += str(route[i])
	with open("SA.sol", "w") as sol_file:
		sol_file.write(str(quality) + "\n")
		sol_file.write(route_write)

	with open("SA.trace", "w") as trace_file:
		for i in trace:
			trace_file.write(i)


if __name__ == '__main__':
	main()
'''