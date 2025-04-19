from model.model import Model

mymodel = Model()
mymodel.buildGraph()

print(f'The Graph has {mymodel.getNumNodes()} nodes.')
print(f'The Graph has {mymodel.getNumEdges()} edges.')
