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

def createChildNets(parents,number):
    return createNets(number)
    newNets = []
    inputsNum = 17
    maxNodes = 100
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

def writeNetworks(nets):

    for i in range(len(nets)):
        with open("Genn/weights" + str(i),'w') as myfile:
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




