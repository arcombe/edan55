import scipy as scy
import pylab as py
import random as rd
import sys
import math
import numpy as np
import copy

class decreaseAndConquer:
            
    def __init__(self, file):
        f = open(file, 'r')
        self.n = int(f.readline())
        self.G = dict()
        self.iterations = 0
        for x in range(self.n):
            tmp = f.readline()
            e = []
            for y in range(self.n):
                if tmp[y*2] == '1':
                    e.append(y)
            self.G[x] = e
            
    def __call__(self):
        res = self.r2(self.G)
        return res, self.iterations
    
    def __remove_v(self, v, G, neighbours = 0):
        nb = G[v]
        del G[v]        
        for x in nb:
            G[x].remove(v)
            if neighbours == 1:
                G = self.__remove_v(x, G)     
        return G
            
    def r0(self, G):
        size = len(G)
        self.iterations += 1
        if size != 0:
            max = 0
            v = 0
            for x in G:
                s = len(G[x])
                if s == 0:
                    G = self.__remove_v(x, G)
                    return 1 + self.r0(G)
                elif s > max:
                    max = s
                    v = x
            G_copy = copy.deepcopy(G)
            G1 = self.__remove_v(v, G_copy)
            G2 = self.__remove_v(v, G, neighbours = 1)
            res1 = self.r0(G1)
            res2 = 1 + self.r0(G2)
            if res1 > res2:
                return res1
            else:
                return res2
        else:
            return 0        
    
    def r1(self, G):
        size = len(G)
        self.iterations += 1
        if size != 0:
            max = 0
            v = 0
            for x in G:
                s = len(G[x])
                if s == 0:
                    G = self.__remove_v(x, G)
                    return 1 + self.r1(G)
                elif s == 1:
                    G = self.__remove_v(x, G, neighbours = 1)
                    return 1 + self.r1(G)
                elif s > max:
                    max = s
                    v = x
            G_copy = copy.deepcopy(G)
            G1 = self.__remove_v(v, G_copy)
            G2 = self.__remove_v(v, G, neighbours = 1)
            res1 = self.r1(G1)
            res2 = 1 + self.r1(G2)
            if res1 > res2:
                return res1
            else:
                return res2
        else:
            return 0
        
    def r2(self, G):
        size = len(G)
        self.iterations += 1
        if size != 0:
            max = 0
            v = 0
            for x in G:
                s = len(G[x])
                if s == 0:
                    G = self.__remove_v(x, G)
                    return 1 + self.r2(G)
                elif s == 2:
                    if G[x][0] in G[G[x][1]]:
                        G = self.__remove_v(x, G, neighbours = 1)
                        return 1 + self.r2(G)
                    else:
                        neighbours = []
                        for y in G[G[x][0]]:
                            neighbours.append(y)
                            G[y].append(self.n)
                        for y in G[G[x][1]]:
                            if y not in neighbours:
                                neighbours.append(y)
                                G[y].append(self.n)
                        G[self.n] = neighbours
                        self.n += 1
                        G = self.__remove_v(x, G, neighbours = 1)
                        return 1 + self.r2(G)
                elif s == 1:
                    G = self.__remove_v(x, G, neighbours = 1)
                    return 1 + self.r2(G)
                elif s > max:
                    max = s
                    v = x
            G_copy = copy.deepcopy(G)
            G1 = self.__remove_v(v, G_copy)
            G2 = self.__remove_v(v, G, neighbours = 1)
            res1 = self.r2(G1)
            res2 = 1 + self.r2(G2)
            if res1 > res2:
                return res1
            else:
                return res2
        else:
            return 0
        
if __name__ == "__main__":
    dac = decreaseAndConquer(sys.argv[1])
    res,x = dac()
    print(res, " nbr calls: ", math.log(x))