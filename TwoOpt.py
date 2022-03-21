'''

The 2-opt local search algorithm for TSP.

'''

import math
import numpy as np
import random
import time
import argparse
import re

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
	# print(node_coord_section)
	coordinates = [(0, 0) for i in range(dim)]
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

	return dim, adj_mat

class TwoOpt:
	'''
	
	Class to implement 2-opt algorithm for TSP.

	'''
	def __init__(self, matrix, dim, given_time, random_seed=None):
		'''

		The function initializes all variables
		
		'''

		random.seed(random_seed)
		self.matrix = matrix
		self.dim = dim
		self.given_time = given_time
		self.trace = []
		self.sol = []
		self.create_init_solution()

	def create_init_solution(self):
		'''

		The function initializes solution by randomly selecting node and appending the remaining nodes.

		'''

		rand_city = random.sample(range(self.dim), 1)[0]
		self.sol.append(rand_city)
		remaining = list(range(self.dim))
		remaining.remove(rand_city)
		self.sol = self.sol + remaining + self.sol

	def track_runtime(self, start_time):
		'''

		The function keeps track of time for runtime of the algorithm.

		'''
		return time.time() - start_time

	def swap_two(self, forward, backward):
		'''

		The function swaps value of forward index and value of backward index from a solution.

		'''
		self.sol = self.sol[:forward] + self.sol[backward:forward-1:-1] + self.sol[backward+1:]

	def cost_init_sol(self):
		'''

		The function calculates total cost of a given solution.

		'''
		dist = 0
		for i in range(0, self.dim):
			dist += self.matrix[self.sol[i]][self.sol[i + 1]]
		return dist

	def cost_sol(self, current_cost, i, j):
		'''

		The function calculates total cost of a swapped solution.

		'''
		update_cost = current_cost
		subtraction = self.matrix[self.sol[i-1]][self.sol[i]] + self.matrix[self.sol[j]][self.sol[j+1]]
		addition = self.matrix[self.sol[i-1]][self.sol[j]] + self.matrix[self.sol[i]][self.sol[j+1]]
		update_cost = update_cost - subtraction + addition

		return update_cost

	def two_opt(self):
		'''

		The function runs 2-opt algorithm on initialized solution.
		The function runs until the runtime passes the provided runtime.
		Keeps track on the best solution, cost, and runtime of the function.


		'''
		start_time = time.time()
		updated_runtime = self.track_runtime(start_time)
		best_cost = self.cost_init_sol()
		best_cost_so_far = best_cost


		while self.given_time - updated_runtime > 1:
			# print('runtime: ' + str(runtime/1000) + ', given time: ' + str(self.given_time) + ', distance: ' + str(round(best_cost, 1)))
			better_check = False

			for i in range(1, self.dim-1):

				for j in range(i + 1, self.dim):
					best_cost_so_far = self.cost_sol(best_cost, i, j)

					if best_cost_so_far < best_cost:
						best_cost = best_cost_so_far
						self.swap_two(i, j)
						better_check = True
						duration = self.track_runtime(start_time)
						duration_format = "{:.2f}".format(duration)
						self.trace.append(f"{duration_format}, {round(best_cost)}\n")
						break

				if better_check:
					updated_runtime = self.track_runtime(start_time)
					break

			if better_check == False:
				updated_runtime = self.track_runtime(start_time)
				break

		return self.sol, best_cost, self.trace

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
	dim, adj_mat = create_adj_mat(filename)
	if seed:
		twoopt = TwoOpt(adj_mat, dim, given_time, seed)
	else:
		twoopt = TwoOpt(adj_mat, dim, given_time)
	solution, cost, trace = twoopt.two_opt()

	solution_route = ""
	for i in range(len(solution)-1):
		if i != len(solution)-2:
			solution_route += str(solution[i]) + ","
		else:
			solution_route += str(solution[i])
	with open("TwoOpt.sol", "w") as sol_file:
		sol_file.write(str(round(cost)) + "\n")
		sol_file.write(solution_route)

	with open("TwoOpt.trace", "w") as trace_file:
		for i in trace:
			trace_file.write(i)

if __name__ == '__main__':
	main()
'''