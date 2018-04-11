import sys
import os
import re
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
			terminate_vertex_reached = True if squashed[1]=='END' \
				else False
			
			# Fill in graph structure with the given info and
			# weights that've been parsed before
			if terminate_vertex_reached:
				(out_vertex, in_vertex), weight = squashed, 1
			else:
				(out_vertex, in_vertex, weight) = squashed
			# Substitute given variable's string representation
			# with the real value we've get before
			weight = weights[weight] if weight in weights else int(weight)
			if out_vertex not in graph:
				graph[out_vertex] = {in_vertex: weight}
			else:
				graph[out_vertex][in_vertex] = weight

	return graph, weights	
