from queue import Queue
from nodo import Node
import math

# Biblioteca de tratamento de grafos necessária para desenhar graficamente o grafo
import networkx as nx
# Biblioteca de tratamento de grafos necessária para desenhar graficamente o grafo
import matplotlib.pyplot as plt


class Graph:
    #construtor de classe
    def __init__(self, directed = False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {} # dicionario
        self.m_h = {}

    def __str__(self):
        string = ""
        for key in self.m_graph.keys():
            string = string + "Nodo " + str(key) + ": " + str(self.m_graph[key]) + "\n"

        return string 

    def get_node_by_name(self, name):
        for n in self.m_nodes:
            if(n.getName() == name):
                return n

    #adicionar aresta com peso
    def add_edge(self, node1, node2, weight):
        n1 = Node(node1) #cria um objeto com o nome dado
        n2 = Node(node2) #cria um objeto com o nome dado

        #self.m_nodes.append(node1)
        #self.m_nodes.append(node2)

        if(n1 not in self.m_nodes):
            self.m_nodes.append(n1)
            self.m_graph[node1] = set()
        else:
            n1 = self.get_node_by_name(node1)

        if(n2 not in self.m_nodes):
            self.m_nodes.append(n2) 
            self.m_graph[node2] = set()
        else:
            n2 = self.get_node_by_name(node2)

        self.m_graph[node1].add((node2, weight))

        #se o grafo for nao direcionado, colocar a resta inversa
        if not self.m_directed:
            self.m_graph[node2].add((node1, weight))


    def get_arc_cost(self, node1, node2):
        if(node1 == node2):
            return 0

        custoT = math.inf
        set = self.m_graph[node1]
        
        for (name, weight) in set:
            if(name == node2):
                custoT = weight

        return custoT


    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0

        while i +1 < len(teste): 
            custo = custo + self.get_arc_cost(teste[i], teste[i+1])
            i = i + 1 

        return custo

    ###########################
    # Desenha grafo  modo grafico
    #########################
    def desenha(self):
        ##criar lista de vertices
        lista_v = self.m_nodes
        lista_a = []
        g=nx.Graph()

        #Converter para o formato usado pela biblioteca networkx
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                #lista_a.append(lista)
                g.add_edge(n,adjacente,weight=peso)

        #desenhar o grafo
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def procura_DFS(self, start, end, path = [], visited = set()):
        path.append(start)
        visited.add(start)

        if start == end:
            #calcular o custo do caminho função calcula custo
            custoT = self.calcula_custo(path)
            return (path, custoT)

        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        
        path.pop() #se nao encontra, remover o que está no caminho
        return None


    def procura_BFS(self, start, end):
        #definir nodos visitados para evitar ciclos
        visited = set()
        q = Queue()

        #adicionar o nodo inicial à fila e aos visitados
        q.put(start)
        visited.add(start)

        #garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not q.empty() and path_found == False:
            nodo_atual = q.get()
            #nodo_name = nodo_atual.getName();
            if nodo_atual == end:
                path_found = True
            else:
                for (adj, peso) in self.m_graph[nodo_atual]:
                    if adj not in visited:
                        q.put(adj)
                        parent[adj] = nodo_atual
                        visited.add(adj)

        #reconstruir o caminho
        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            #funçao calcula custo caminho
            custo = self.calcula_custo(path)

        return (path, custo)


    def getNeighbours(self, nodo):
        lista = []
        for (adj, peso) in self.m_graph[nodo]:
            lista.append((adj, peso))
        return lista

    def add_heuristica(self, n, value):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = value


    def greedy(self, start, end):
        #open_list é uma lista de nodos visitados, mas com vizinhos que ainda nao foram todos visitados(começa com start)
        #closed_list é uma lista de nodos visitados e todos os seus vizinhos já o foram

        open_list = set()
        close_list = set()

        open_list.add(start)

        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n == None:
                print("Path doenst exist")
                return None

            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n):
                if m not in open_list and m not in close_list:
                    open_list.add(m)
                    parents[m] = n


            open_list.remove(n)
            close_list.add(n)

        print("Path doesnt exist")
        return None


    def star(self, start, end):
            # open_list é uma lista de nodos visitados, mas com vizinhos que ainda nao foram todos visitados(começa com start)
            # closed_list é uma lista de nodos visitados e todos os seus vizinhos já o foram
        custo_acumulado = dict()
        custo_acumulado[start] = 0

        open_list = set()
        close_list = set()

        open_list.add(start)

        parents = {}
        parents[start] = start

        i = 1

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or (custo_acumulado[parents[v]] + self.get_arc_cost(v, parents[v]) + self.m_h[v]) < (custo_acumulado[parents[n]] + self.get_arc_cost(n, parents[n]) + self.m_h[n]):
                    n = v

            #print(f"it {i} : {n}") # ver iteraçoes
            i+=1

            if n == None:
                print("Path doenst exist")
                return None

            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            custo_acumulado[n] = custo_acumulado[parents[n]] + self.get_arc_cost(n, parents[n])

            for (m, weight) in self.getNeighbours(n):
                if m not in open_list and m not in close_list:
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            close_list.add(n)

        print("Path doesnt exist")
        return None
