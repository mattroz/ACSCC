#!/usr/bin/python3.5
import preprocessor as pp
import sympy as sp

sp.init_printing()

graph = pp.get_graph_from('input.txt')
W = pp.get_equivalent_transfer_function(graph)

print(W)
