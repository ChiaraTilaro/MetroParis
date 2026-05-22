from model.modello import Model

model = Model()
model.buildGraph()

print(f"Numero nodi: {model.get_numnodi()}")
print(f"Numero archi: {model.get_numarchi()}")
