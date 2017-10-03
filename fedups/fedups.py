# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 12:49:49 2017
@author: Arcombe
"""
from  scipy import *
from  pylab import *
import numpy as np
import sys
import random as rd

class Road:
    
    def __init__(self, to, time, prob):
        self.to = int(to)
        self.time = float(time)
        self.prob = float(prob)

class Fedups:
    
    def __init1__(self, file):
        f = open(file, 'r')
        line = f.readline()
        line = line[:-1]
        first_line = line.split()
        
        self.N = int(first_line[0])
        self.M = int(first_line[1])
        self.H = int(first_line[2])
        self.F = int(first_line[3])
        self.P = int(first_line[4])
        
        self.roads = [ [] for _ in range(self.N)]
        
        for _ in range(self.M):
            line = f.readline()
            line = line[:-1]
            line = line.split()
            r1 = Road(line[1], line[2], line[3])
            r2 = Road(line[0], line[2], line[4])
            n1 = int(line[0])
            n2 = int(line[1])
            self.roads[n1].append(r1)
            self.roads[n2].append(r2)
       
    def __init__(self, file):
        f = open(file, 'r')
        line = f.readline()
        line = line[:-1]
        first_line = line.split()
        
        self.N = int(first_line[0])
        self.M = int(first_line[1])
        self.H = int(first_line[2])
        self.F = int(first_line[3])
        self.P = int(first_line[4])
        
        self.pMatrix = np.array([np.array([0.0 for _ in range(self.N)]) for _ in range(self.N)])
        self.time = np.array([0.0 for _ in range(self.N)])
        
        """self.pMatrix[0,0] = 2.0
        self.pMatrix[0,1] = 1.0
        self.pMatrix[0,2] = -1.0
        self.pMatrix[1,0] = -3.0
        self.pMatrix[1,1] = -1.0
        self.pMatrix[1,2] = 2.0
        self.pMatrix[2,0] = -2.0
        self.pMatrix[2,1] = 1.0
        self.pMatrix[2,2] = 2.0
        self.time[0] = 8.0
        self.time[1] = -11.0
        self.time[2] = -3.0"""
        
        for _ in range(self.M):
            line = f.readline()
            line = line[:-1]
            line = line.split()
            u = int(line[0])
            v = int(line[1])
            t = float(line[2])
            puv = float(line[3])
            pvu = float(line[4])
            self.pMatrix[u, v] = puv
            self.pMatrix[v, u] = pvu
            self.time[u] += t * puv
            self.time[v] += t * pvu
            
    def __call1__(self):
        fed = []
        post = []
        for x in range(1000):
            fed.append(self.monte_carlo(self.F, self.H))
            post.append(self.monte_carlo(self.P, self.H))
        print(np.mean(fed), " ", np.mean(post))
        
    def __call__(self):
        self.markov()
        print("FedUPS: ", self.time[self.F])
        print("PostNHL: ", self.time[self.P])
        
    def markov(self):
        for x in range(self.N):
            self.pMatrix[x,x] -= 1
            
        self.time = -1*self.time
        
        for pivot_index in range(self.N):
            
            pivot = self.pMatrix[pivot_index, pivot_index]
            if pivot == 0:
                print("pivot = 0")
                x = pivot_index + 1
                while self.pMatrix[x, pivot_index] == 0.0:
                    if x >= self.N:
                        print("cant find solution")
                    x += 1
                self.pMatrix[[x, pivot_index]] = self.pMatrix[[pivot_index, x]]
                self.time[x], self.time[pivot_index] = self.time[pivot_index], self.time[x]
                pivot = self.pMatrix[pivot_index, pivot_index]
            
            for row in range(pivot_index + 1, self.N):
                factor = self.pMatrix[row, pivot_index] / pivot
                self.pMatrix[row] = self.pMatrix[row] - factor * self.pMatrix[pivot_index]
                self.time[row] = self.time[row] - factor * self.time[pivot_index]
        
        for x in range(self.N - 1, -1, -1):
            for y in range(x):
                factor = self.pMatrix[y,x] / self.pMatrix[x,x]
                self.pMatrix[y] = self.pMatrix[y] - factor*self.pMatrix[x]
                self.time[y] = self.time[y] - factor*self.time[x]
            
            selffactor = 1 / self.pMatrix[x,x]
            self.pMatrix[x] = selffactor * self.pMatrix[x] 
            self.time[x] = selffactor * self.time[x]
        
        return self.time
        
    def monte_carlo(self, start, dest):
        current = start
        time = 0
        
        while current != dest:
            rand = rd.random()
            x = 0
            p = 0.0
            while p <= rand:
                p += self.roads[current][x].prob
                x += 1
            x -= 1
            time += self.roads[current][x].time
            current = self.roads[current][x].to
        
        return time  
    
if __name__ == "__main__":
    fedups = Fedups(sys.argv[1])
    fedups()