import random 
import numpy as np
from util.constants import * 

def createNets(conCurrentGame):
    maxlayers = 10
    maxNodes = 10
    inputsNum = 17
    nets = []
    # Create every network
    for i in range(conCurrentGame):
        layers = []
        totalLayers = random.randint(2, maxlayers)
        totalNodes = np.random.randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
        # print(totalNodes)
        # Create every layer
        for j in range(totalLayers):
            if j == 0:
                nodeWeights = np.random.rand(1,inputsNum,totalNodes[0]).tolist()[0]
            else:
                nodeWeights = np.random.rand(1,totalNodes[j-1],totalNodes[j]).tolist()[0]
            # print("total amount of weights",len(nodeWeights))  
            layers.append(Layer(nodeWeights))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        # print("Total amount of layers",len(layers))
        nets.append(Network(layers))
    # print("Total amount of nets",len(nets))
    return nets

def createChildNets(parents,number):
    return createNets(number)
    newNets = []
    inputsNum = 17
    maxNodes = 10
    for i in range(number):
        parent1 = parents[random.randint(0, len(parents)-1)]
        parent2 = parents[random.randint(0, len(parents)-1)]
        if np.random.random_sample() > .5:totalLayers = len(parent1.layers)
        else:totalLayers = len(parent1.layers)
        totalNodes = np.random.randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
        layers = []
        for j in range(totalLayers -1):
            if j == 0:
                nodeWeights = np.random.rand(1,inputsNum,totalNodes[0]).tolist()[0]
            else:
                nodeWeights = np.random.rand(1,totalNodes[j-1],totalNodes[j]).tolist()[0]
            layers.append(Layer(nodeWeights))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        layers.append(Layer(np.random.rand(1,totalNodes[len(totalNodes)-1],1).tolist()[0]))
        newNets.append(Network(layers))
    return newNets



# def createChildNets(parents,number):
#     newNets = []
#     for i in range(number):
#         parent1 = parents[random.randint(0, len(parents)-1)]
#         parent2 = parents[random.randint(0, len(parents)-1)]
#         layers = []
#         for i in range(max(len(parent1.layers),len(parent2.layers))):
#             if i < len(parent1.layers) and i < len(parent2.layers):
#                 if np.random.random_sample() > .5:
#                     layers.append(parent1.layers[i])
#                 else:
#                     layers.append(parent2.layers[i])
#             elif i < len(parent1.layers):
#                 if np.random.random_sample() > .5: layers.append(parent1.layers[i])
#                 else: break
#             elif i < len(parent2.layers):
#                 if np.random.random_sample() > .5: layers.append(parent2.layers[i])
#                 else: break 
#         newNets.append(Network(layers))
#     return newNets




