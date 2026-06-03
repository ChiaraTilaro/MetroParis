from model.fermata import Fermata
from model.modello import Model

model = Model()
model.buildGraphPesato()

print(f"Numero nodi: {model.get_numnodi()}")
print(f"Numero archi: {model.get_numarchi()}")

source = Fermata(2	, "Abbesses",	2.33855	, 48.8843)

nodiBfs = model.getBFSNodesEdges(source)
for i in range(0 , 10):
    print(nodiBfs[i])
print(len(nodiBfs))
nodiDfs = model.getDFSNodesEdges(source)
for i in range(0 , 10):
    print(nodiDfs[i])
print(len(nodiDfs))

print("===============================================")
print("Archi con peso 2")
archiMaggiori = model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a[0] ,"->" ,  a[1] , ":" , a[2]["weight"])
