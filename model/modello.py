
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] =f

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addedges3()

    def addedges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u , v):
                    self._grafo.add_edge(u , v)

    def addedges2(self):
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u , v)

    def addedges3(self):
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u , v)

    def getBFSNodesEdges(self, source):
        archi = nx.bfs_edges(self._grafo , source)
        nodiBfs = []
        for u,v in archi:
            nodiBfs.append(v)
        return nodiBfs

    def getDFSNodesEdges(self, source):
        archi = nx.dfs_edges(self._grafo , source)
        nodiDfs = []
        for u,v in archi:
            nodiDfs.append(v)
        return nodiDfs

    def getBfsNodesFromTree(self , source):
        tree = nx.bfs_tree(self._grafo, source)
        archi =list(tree.edges())
        nodi = list(tree.nodes())
        return  nodi

    def getDfsNodesFromTree(self , source):
        tree = nx.dfs_tree(self._grafo, source)
        archi =list(tree.edges())
        nodi = list(tree.nodes())
        return  nodi

    def get_numnodi(self):
        return len(self._grafo.nodes)

    def get_numarchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate
