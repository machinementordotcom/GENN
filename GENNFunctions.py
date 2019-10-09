import random 
import numpy as np
from util.constants import * 
import csv

def createNets(conCurrentGame):
    maxlayers = 100
    maxNodes = 100
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

def createNet(specificLayers = None,specificNodes = None):
    maxlayers = 100
    maxNodes = 100
    inputsNum = 17
    # Create every network
    layers = []
    if specificLayers == None: totalLayers = random.randint(2, maxlayers)
    else: totalLayers = specificLayers 
    if specificNodes == None: totalNodes = np.random.randint(1,maxNodes,size=(1,totalLayers)).tolist()[0]
    else: totalNodes = specificNodes
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
    return Network(layers)

def createChildNets(parents,number):
    return createNets(number)
    newNets = []
    inputsNum = 17
    maxNodes = 100
    for i in range(number):
        parent1 = parents[random.randint(0, len(parents)-1)]
        parent2 = parents[random.randint(0, len(parents)-1)]
        if np.random.random_sample() > .5:totalLayers = len(parent1.layers)
        else:totalLayers = len(parent2.layers)
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

def countBits(n):
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
  return n
def toggleKthBit(n, k): 
    return (n ^ (1 << (k-1))) 

def mutateNets(nets):
    newNetsIndex = np.random.randint(0,len(nets),int(len(nets)*.1))
    for i in newNetsIndex:
        current = nets[i]
        currentLayers = len(current.layers)
        num = countBits(currentLayers)
        for i in range(num):
            if random.uniform(0, 1) < (1/num):
                currentLayers = toggleKthBit(currentLayers,i)
        nets[i] = createNet(specificLayers = currentLayers)
    return nets

def writeNetworks(nets):

    for i in range(len(nets)):
        with open("Genn/weights" + str(i) + ".csv",'w') as myfile:
            wr = csv.writer(myfile, quoting = csv.QUOTE_ALL) 
            for j in range(len(nets[i].layers)):
                # for k in range(len(nets[i].layers[j].weights)):
                wr.writerow(nets[i].layers[j].weights)
                #     wr.write(",")
                # wr.writerow("\n")

# def readNetworks(nets,path = None):

#     if path == None:
#         for i in range(len())
#     def readWeights(self,path = None):
#         tempWeights = [[],[]] 
#         if path == None:
#             for i in range(self.conGames):
#                 with open('DynamicController/weightsDynamicController' + self.id + "-" + str(self.conCurrentGameId) + '.csv') as csvfile:
#                     reader = csv.reader(csvfile)
#                     weightType = 0
#                     for row in reader:
#                         tempWeights[weightType].append([float(i) for i in row])
#                         weightType +=1
#             self.weights[0] = np.average(np.array(tempWeights[0]),axis = 0).tolist()
#             self.weights[1] = np.average(np.array(tempWeights[1]),axis = 0).tolist()
#         else:
#             with open(path) as csvfile:
#                 reader = csv.reader(csvfile)
#                 weightType = 0
#                 for row in reader:
#                     self.weights[weightType] = [float(i) for i in row]
#                     weightType +=1


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




