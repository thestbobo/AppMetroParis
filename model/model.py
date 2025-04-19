from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMap = {}
        for f in self._fermate:
            self._idMap[f.id_fermata] = f

    def getBFSNodes(self, source):
        edges = nx.bfs_edges(self._grafo, source)
        visited = []
        for u,v in edges:
            visited.append(v)
        return visited

    def getDFSNodes(self, source):
        edges = nx.dfs_edges(self._grafo, source)
        visited = []
        for u,v in edges:
            visited.append(v)
        return visited

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgeMode3()
        pass

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgePesati()

    def addEdgePesati(self):
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            if self._grafo.has_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA]):
                self._grafo[self._idMap[c.id_stazP]][self._idMap[c.id_stazA]]['weight'] += 1
            else:
                self._grafo.add_edge(self._idMap[c.id_stazP],self._idMap[c.id_stazA], weight=1)
        pass

    def addEdgeMode1(self):
        # Method 1 : doppio loop su nodi e query per ogni arco (con tanti nodi è lento, non conviene)
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                res = DAO.getEdge(u,v)
                if len(res)>0:
                    self._grafo.add_edge(u,v)
                    print(f'Added edge between {u} and {v}')
        pass

    def addEdgeMode2(self):
        # Method 2: loop singolo sui nodi e query per identificare i nodi vicini
        self._grafo.clear_edges()
        for u in self._fermate:
            vicini = DAO.getEdgesVicini(u)
            for v in vicini:
                v_nodo = self._idMap[v.id_stazA]
                self._grafo.add_edge(u,v_nodo)
                print(f'Added edge between {u} and {v_nodo}')
        pass

    def addEdgeMode3(self):
        #Method 3: unica query che legge tutte le connessioni
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConnessioni()
        for c in allConnessioni:
            u_nodo = self._idMap[c.id_stazP]
            v_nodo = self._idMap[c.id_stazA]
            self._grafo.add_edge(u_nodo,v_nodo)
            print(f'Added edge between {u_nodo} and {v_nodo}')
        pass

    def getEdgeWeight(self,v1,v2):
        return self._grafo[v1][v2]['weight']

    @property
    def fermate(self):
        return self._fermate

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)