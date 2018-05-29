import sys
import os
import re
import networkx as nx
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
from itertools import combinations

def preprocess(filename):
	"""
	Input graph preprocessing from txt file
	
	Arguments: filename
	Returns: dict with adjacency list, adjacency matrix
	"""
	graph = {}
	weights = {}
	
	with open(filename, 'r') as f:
		#f = open('input.txt','r')
		
		# Get graph dataflow (arcs' values)
		raw_edge_info = f.readline()[:-1]
		while raw_edge_info != '':
			edge = raw_edge_info.replace(' ','').split('=')
			weights[edge[0]] = parse_expr(edge[1])
			raw_edge_info = f.readline()[:-1]

		# Get graph structure
		terminate_vertex_reached = False
		
		while not terminate_vertex_reached:
			raw_string = f.readline()[:-1]
			splitted = re.split(r'[->, ]', raw_string)
			squashed = [elem for elem in splitted if elem]
			print(squashed)
			terminate_vertex_reached = True if squashed[1]=='END' else False
			
			# Fill in graph structure with the given info and
			# weights that've been parsed before
			if terminate_vertex_reached:
				(out_vertex, in_vertex), weight = squashed, 1
			else:
				(out_vertex, in_vertex, weight) = squashed
			# Substitute given variable's string representation
			# with the real value we've get before, 1 otherwise
			weight = weights[weight] if weight in weights else int(weight)
			if out_vertex not in graph:
				graph[out_vertex] = {in_vertex: weight}
			else:
				graph[out_vertex][in_vertex] = weight

	return graph, weights


def get_graph_from(filename):
	"""Method for forming a directed graph.

	Arguments:
		filename -- file containing graph description in a specific format
	
	Returns:
		g -- NetworkX directed graph
	"""

	graph, weights = preprocess(filename)
	g = nx.DiGraph()
	# Create directed graph
	for parent_node in graph:
		for child_node in graph[parent_node]:
			w = graph[parent_node][child_node]
			g.add_edge(parent_node, child_node, weight=w)
	return g


def get_direct_paths(graph, src='X', dest='END'):
	"""Method for obtaining a set of direct paths from src to dest node.

	Arguments:
		graph -- NetworkX directed graph
		src -- start node for pathfinding algorithm
		dest -- destination node for pathfinding algorithm
	
	Returns:
		paths -- list of all paths from src node to dest node.
	"""

	paths = nx.all_shortest_paths(graph, source=src, target=dest)
	paths = [p for p in paths]
	return paths


def get_closed_loops(graph, src='X'):
	"""Method for obtaining a set of closed loops in the given graph.
	
	Arguments:
		graph -- NetworkX directed graph
		src -- start node for loops searching algorithm
	
	Returns:
		cycles -- list of all loops from the src node in a format [(n1,n2),(n2,n3),(n3,n4), ...]
	"""

	cycles = list(nx.simple_cycles(graph))
	return cycles


def calculate_transfer_function(graph, paths):
	"""Method for calculating the equivalent transfer function for every path given.
	
	Arguments:
		graph -- NetworkX directed graph
		paths -- list of paths for equivalent transfer function calculation.
	
	Returns:
		transfer_functions -- list of equivalent transfer functions for the given paths (transfer_function[0] is for paths[0] and so on)
	"""

	transfer_functions = []
	# Calculate transfer function for every path given
	for path in paths:
		transfer_functions.append(1)
		for i in range(1, len(path)-1):	
			parent_node = path[i-1]
			child_node = path[i]
			curr_transfer_func = graph[parent_node][child_node]['weight']
			transfer_functions[-1] *= curr_transfer_func
	return transfer_functions


def find_disjoint_paths(cycles):
	# Generate all combinations through the number of cycles,
	# e.g. pairs, threes, foursome etc.
	# Works only with len(cycles >= 2)
	combs = []
	for i in range(2, len(cycles)+1):
		combs.append(list(combinations(cycles,i)))
	# Check all the combinations for intersection:
	# if there is no intersection, add this combination to the result list
	disjoint_paths = []
	for outer_comb in combs:
		for inner_comb in outer_comb:
			counter = 0
			for i in range(len(inner_comb)):
				for j in range(i+1, len(inner_comb)):
					counter += 1 if len(set(inner_comb[i]) & set(inner_comb[j])) else 0
			if counter == 0:
				disjoint_paths.append(inner_comb)
	return disjoint_paths


def calculate_determinator(graph, cycles):
	# Check cycles for intersections (TODO)
	intersection_found = False
	find_disjoint_paths()
	# Calculate determinator using the formula from the Mason's rule
	# Get transfer functions for each cycle
	cycles_tf = calculate_transfer_function(graph, cycles)
	combs = np.array([])
	# Get all combinations (pairs, triplets, etc) and do sum of prods
	for i in range(1, len(cycles_tf)):
		comb = np.array(list(combinations(cycles_tf, i+1)))
		comb = sum([np.prod(x) for x in comb])
		combs = np.append(combs,c)
