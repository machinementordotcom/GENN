import random 
import numpy as np
from util.constants import * 

def createNets(conCurrentGame):
    maxlayers = 5
    maxNodes = 5
    inputsNum = 17
    nets = []
    # Create every network
    for i in range(conCurrentGame):
        layers = []
        totalLayers = random.randint(1, maxlayers)
        # Create every layer
        for j in range(totalLayers):
            totalNodes = random.randint(1,maxNodes)
            nodeWeights = []
            tempWeights = []
            # create every node 
            for k in range(totalNodes):
                if j == 0:
                    tempWeights.append( np.random.rand(1,inputsNum,totalNodes).tolist()[0] )
                else: 
                    tempWeights.append( np.random.rand(1,len(layers[j-1].weights),totalNodes).tolist()[0] )
                nodeWeights.append(tempWeights)
            print("total amount of nodes",len(nodeWeights))  
            layers.append(Layer(nodeWeights))
        print("Total amount of layers",len(layers))
        nets.append(Network(layers))
    print("Total amount of nets",len(nets))
    return nets