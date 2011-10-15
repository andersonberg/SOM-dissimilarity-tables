import ubigraph

def plot_graph(mapa):
	
	U = ubigraph.Ubigraph()
	U.clear()

	smallRed = U.newVertexStyle(shape="cube", color="#ff0000", size="1.0")
	cluster_point = U.newVertexStyle(shape="sphere", color="#ffff00", size="2.0")
	
	for cluster in mapa.mapa.flat:
		c = U.newVertex(style=cluster_point, label=str(cluster.indice))
#		previous_o = None
		for obj in cluster.objetos:
			o = U.newVertex(style=smallRed, label=str(obj.classe_a_priori.indice))
			U.newEdge(c, o, arrow=True, strength="0.3")
#			if previous_o != None:
#				U.newEdge(o, previous_o, spline=True, stroke="dashed")
#			previous_o = o

