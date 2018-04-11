import sys
import os
import re

def preprocess(filename):
	"""
	Input graph preprocessing from txt file
	
	Arguments: filename
	Returns: dict with adjacency list, adjacency matrix
	"""
	graph = {}
	
	with open(filename, 'r') as f:
		f = open('input.txt','r')
		terminate_vertex_reached = False
		
		while not terminate_vertex_reached:
			raw_string = f.readline()[:-1]
			splitted = re.split(r'[->, ]', raw_string)
			squashed = [elem for elem in splitted if elem]
			print(squashed)
			terminate_vertex_reached = True if squashed[1]=='END' \
				else False
			
			# Fill in graph structure with the given info
			if terminate_vertex_reached:
				(out_vertex, in_vertex), weight = squashed, 0
			else:
				(out_vertex, in_vertex, weight) = squashed

			if out_vertex not in graph:
				graph[out_vertex] = {in_vertex: weight}
			else:
				graph[out_vertex][in_vertex] = weight

	return graph	
