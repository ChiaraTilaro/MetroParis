
import networkx as nx
import geopy.distance
from database.DAO import DAO


def getPesoTempoPercorrenza(u, v, vel):
    distanza = geopy.distance.distance((u.coordX, u.coordY) , (v.coordX , v.coordY)).km
    time = distanza/vel *60 #minuti
    return time


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] =f

    def getShortestPath(self , u , v):
        return nx.single_source_dijkstra(self._grafo , u , v)

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        #self.addEdgesPesati()
        self.addEdgesPesatiTempi()


    def addEdgesPesatiTempi(self):
        # crea degli archi il cui peso è pari al tempo di percorrenza di quell'arco
    # ottenuto come rapporto fra la distanza fra due stazioni e la velocita di percorrenza
        self._grafo.clear_edges()
        allEdgesVel = DAO.getAllEdgesVelocita()
        for e in allEdgesVel:
            u= self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = getPesoTempoPercorrenza(u , v , e[2])
            self._grafo.add_edge(u , v ,  weight = peso)

    def addEdgesPesati(self):
        # riutilizzare il principio di funzionamento del metodo addEdges3 ma contando quante volto provo ad aggiungere l'arco
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            if self._grafo.has_edge(u,v):
                self._grafo[u][v]["weight"]+=1
            else:
                self._grafo.add_edge(u , v , weight = 1)

    def addEdgesPesati2(self):
        # delega il calcolo del peso alla query sql per semplificare la vita in python
        self._grafo.clear_edges()
        allEdgesWPeso = DAO.getAllEdgesPesati()
        for e in allEdgesWPeso:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]
            self._grafo.add_edge(u ,v , weight = peso)

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True)
        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                edgesMaggiori.append(e)
        return edgesMaggiori


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
        self._grafo.clear_edges()
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
