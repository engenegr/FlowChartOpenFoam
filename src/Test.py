from core.Project import *
from core.OFVertex import *

w1 = Weight(5)
w2 = Weight(6)

graph = Graph()

blockMeshFilePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict'
sourceTutorial = '/home/rocketman/OFProject/cavity/'
blockMeshTemplatePath = '/home/rocketman/OFProject/cavity/system/blockMeshDict.template'
varList = ['nElem']
valList = [[2000]]

paramStudy = ParameterVariation(blockMeshTemplatePath, varList, valList)
blockMesh = BlockMesh( blockMeshFilePath )
solver = Solver( sourceTutorial )
paraFoam = ParaFoam()

graph.add_vertex(blockMesh)
graph.add_vertex(solver)
graph.add_vertex(paraFoam)

graph.connect(blockMesh, solver, w1)
graph.connect(solver, paraFoam, w2)

project = Project(name='cavityProj', graph=graph, clearPath=True)
#project.run()
