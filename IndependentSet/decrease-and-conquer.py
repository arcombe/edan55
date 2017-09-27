import scipy as scy
import pylab as py
import random as rd
import sys
import math as ma
import numpy as np
import copy

class decreaseAndConquer:
    
    def __init__2(self, file):
        f = open(file, 'r')
        self.n = int(f.readline())
        self.temp = []
        for x in range(0,self.n):
            self.temp.append(f.readline().split())
        self.m = np.matrix(self.temp, dtype=int)
        self.m.reshape(self.n,self.n)
        print(self.m)
        print(self.r0(self.m))
            
    def __init__(self, file):
        f = open(file, 'r')
        self.n = int(f.readline())
        self.G = [[],[]]
        for x in range(self.n):
            self.G[0].append(x)
            tmp = f.readline()
            e = []
            for y in range(self.n):
                if tmp[y*2] == '1':
                    e.append(y)
            self.G[1].append(e)
        
    def __call__(self):
        res = self.r0(self.G)
        return res
    
    def __remove_v(self, v, G, neighbours = 0):
        node = G[0][v]
        nb = G[1][v]
        del G[0][v]
        del G[1][v]
        for x in range(len(nb)):
            n = G[0].index(nb[x])
            G[1][n].remove(node)
            if neighbours == 1:
                G = self.__remove_v(n, G)
        return G
        
    
    def r0(self, G):
        size = len(G[0])
        if size != 0:
            max = 0
            v = 0
            for x in range(size):
                s = len(G[1][x])
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
        
    def r0_2(self, graph):
        print('Calling r0...')
        self.m = graph
        self.oldSum = 0
        if self.m.size != 0:
            for x in range(0,self.n):
                self.sum = self.m[x].sum()
                if self.sum == 0:
                    self.temp = self.m[x]
                    self.m.remove(self.m[x])
                    return 1 + self.r0(self.m)
            for x in range(0,self.n):
                self.sum = self.m[x].sum()
                if self.sum > self.oldSum:
                    self.index = x
                    self.oldSum = self.sum
            self.leave = self.m.remove(self.m[self.index])
            self.toRemove = self.m[self.index].nonzero()
            for i in range(0,self.toRemove.size()):
                self.m = self.m.delete(self.m[self.toRemove[i]])
            self.take = self.m
            return 1 + max(self.r0(self.take), self.r0(self.leave))
        else:
            return 0 
        
        
if __name__ == "__main__":
    dac = decreaseAndConquer(sys.argv[1])
    res = dac()
    print(res)
    #x = [[1,2,3], [[2,3],[1,3], [1,2]]]
    #print(x[1][0])