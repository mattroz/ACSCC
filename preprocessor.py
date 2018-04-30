import sys
import os
import re
import networkx as nx
from sympy.parsing.sympy_parser import parse_expr

def preprocess(filename):
	"""
	Input graph preprocessing from txt file
	
	Arguments: filename
	Returns: dict with adjacency list, adjacency matrix
	"""
	graph = {}
	weights = {}
	
	with open(filename, 'r') as f:
		f = open('input.txt','r')
		
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
	graph, weights = preprocess(filename)
	g = nx.DiGraph()
	# Create directed graph
	for parent_node in graph:
		for child_node in graph[parent_node]:
			w = graph[parent_node][child_node]
			g.add_edge(parent_node, child_node, weight=w)
	return g


def get_direct_paths(graph, src='X', dest='END'):
	paths = nx.all_shortest_paths(graph, source=src, target=dest)
	paths = [p for p in paths]
	return paths


def get_closed_loops(graph, src='X'):
	cycles = list(nx.simple_cycles(graph))
	return cycles


def calculate_transfer_function(graph, paths):
	transfer_functions = []
	# Calculate transfer function for every path given
	for path in paths:
		transfer_functions.append(1)
		for i in range(1, len(path)-1):	
			curr_transfer_func = graph[path[i-1]][path[i]]['weight']
			transfer_functions[-1] *= curr_transfer_func
	return transfer_functions
