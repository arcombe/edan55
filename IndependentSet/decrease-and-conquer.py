import scipy as scy
import pylab as py
import random as rd
import math as ma
import numpy as np

class decreaseAndConquer:
    
    def __init__(self):
        f = open('C:\\Users\\anton\\Code\\g4.in', 'r')
        self.n = int(f.readline())
        self.temp = []
        for x in range(0,self.n):
            self.temp.append(f.readline().split())
        self.m = np.matrix(self.temp, dtype=int)
        self.m.reshape(self.n,self.n)
        print(self.m)
        print(self.r0(self.m))
            
    def r0(self, graph):
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
    "dac = decreaseAndConquer()"
    