from igraph import *

class Grafos():

    def __init__(self):

        self.grafo = Graph(directed=True)

        #linhas e colunas da matriz de adjacencia
        self.linhas = 26
        self.colunas = 26

    def criaGrafo(self):

        self.grafo.add_vertices(26)
        
        for i in range (len(self.grafo.vs)):
            self.grafo.vs[i]["id"] = i+1
            self.grafo.vs[i]["label"]= str(i+1)

        # self.grafo.add_edges([(1,2), (2,4), (3,1), (3,2), (3,4), (4,6), (5,4),(5,2),(6,5)])
        # self.grafo.add_edges([(0,1), (1,3), (2,0), (2,1), (2,3), (3,5), (4,3), (4,1), (5,4)])
        self.grafo.add_edges([
            (0,1), (1,0),(1,2),(2,3),(3,2),(3,0),(3,4),(4,5),(4,13),(5,6),(6,5),
            (6,7),(6,2),(2,25),(7,8),(8,9),(9,10),(10,11),(11,4),(13,12),(12,8),
            (13,14),(14,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),
            (22,23),(23,3),(25,24),(24,23)
        ])
        weights = [280,280,260,170,170,550,850,1900,400,1100,1100,
                   700,2400,500,3200,350,30,950,950,1000,1100,
                    800,600,230,170,290,300,260,70,90,
                    2700,700,70,140
                   ]
        self.grafo.es['weight'] = weights
        self.grafo.es['label'] = weights

        

    def imprimeGrafo(self):

        visual_style = {}

        out_name = "graph.png"

        # Set bbox and margin
        visual_style["bbox"] = (300,300)
        visual_style["margin"] = 27

        # Set vertex colours
        visual_style["vertex_color"] = 'white'

        # Set vertex colours
        visual_style["vertex_color"] = 'white'

        # Set vertex size
        visual_style["vertex_size"] = 45

        # Set vertex lable size
        visual_style["vertex_label_size"] = 22

        # Don't curve the edges
        visual_style["edge_curved"] = False

        # Set  layout
        #my_layout = g.layout_lgl()
        #visual_style["layout"] = my_layout

        # Plot o grafo
        plot(self.grafo, out_name, **visual_style)

        print("Number of vertices in the graph:", self.grafo.vcount())
        print("Number of edges in the graph", self.grafo.ecount())
        print("Is the graph directed:", self.grafo.is_directed())
        print("Maximum degree in the graph:", self.grafo.maxdegree())
        adjacency_matrix = self.grafo.get_adjacency()
        print("Adjacency matrix:\n", adjacency_matrix)


    def caminhoMinimo(self, source, destination):

        shortest_path = self.grafo.get_shortest_path(source-1, to=destination-1)
        
        # matriz com os pesos
        adjacency__weight_matrix = self.grafo.get_adjacency(attribute='weight')
        # print("\nMATRIZ COM PESOS\n")
        # print(adjacency__weight_matrix)

        custo_total = 0
        for i in range(len(shortest_path)-1):
            # shortest_path[i] += 1
            # print("i: ", shortest_path[i])
            # print("i+1: ", shortest_path[i+1])
            linha =  shortest_path[i]
            coluna = shortest_path[i+1]
            custo_parcial = adjacency__weight_matrix[linha][coluna]
            # print("\nPeso parcial: ", custo_parcial)

            custo_total += custo_parcial

        print("Melhor caminho é: ")
        print([x + 1 for x in shortest_path])
        print("Custo total do caminho: ", custo_total)

        return custo_total
            
    def verticesAdjacentesAcessiveis(self, vertice):

        adjacency_matrix = self.grafo.get_adjacency()
        vertices_adjacentes = []
        if vertice != 0:
            vertice -= 1
        for i in range(self.linhas):
            if i == vertice:
                for j in range(self.colunas): 
                    # print(adjacency_matrix[i][j])
                    if adjacency_matrix[i][j] == 1: 
                        vertices_adjacentes.append(j+1)

        print(vertices_adjacentes)

    def calculaFrete(self,custo_total):

        # 15 reais por km do custo
        km = float(custo_total)/1000.00
        frete = km * 15

        # km = float(1256)/1000.00 #teste
        # print(km)
        # print(frete)

        return frete

def main():

    grafos = Grafos()
    print("Criando grafo\n")
    grafos.criaGrafo()
    print("------GRAFO GERADO-----\n")
    grafos.imprimeGrafo()
    print("\nNós adjacentes acessíveis a partir do nó 3: ")
    grafos.verticesAdjacentesAcessiveis(3)
    # print("\nCalculando caminho mínimo do nó 3 para o nó 5: \n")
    # custo1 = grafos.caminhoMinimo(3,5)
    # grafos.calculaFrete(custo1)
    print("\nCalculando o caminho mínimo do nó 1 para o nó 1: \n")
    custo2 = grafos.caminhoMinimo(1,1)
    frete = grafos.calculaFrete(custo2)
    print('frete a ser pago',frete)



if __name__ == '__main__':
    main()        