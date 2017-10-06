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
import copy

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
        
        self.H_start = self.H
        
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
        
        self.links = [[] for _ in range(self.N)]
        
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
            if puv != 0.0:
                self.links[u].append(v)
            if pvu != 0.0:
                self.links[v].append(u)
        
    def __call1__(self):
        fed = []
        post = []
        for x in range(1):
            fed.append(self.monte_carlo(self.F, self.H))
            post.append(self.monte_carlo(self.P, self.H))
        print(np.mean(fed), " ", np.mean(post))
        
    def __call__(self):
        self.M = []
        self.t = []
        if self.build_matrix(self.F, self.H, 'f') == 0:
            print("FedUPS has no solution")
        else:
            t = self.markov(self.M, self.t)
            print("FedUPS: ", t[self.F])
        
        self.H = self.H_start
        if self.build_matrix(self.P, self.H, 'p') == 0:
            print("PostNHL has no solution")
        else:
            t = self.markov(self.M, self.t)
            print("PostNHL: ", t[self.P])
    
    def build_matrix(self, s, f, typ):
        self.finish = 0
        self.taken = []
        self.__build_path__(s)
        
        if self.finish == 0:
            return 0
        
        l = len(self.taken)
        if l == self.N:
            self.M = copy.deepcopy(self.pMatrix)
            self.t = copy.deepcopy(self.time)
            return 1
        
        pM = np.array([np.array([0.0 for _ in range(l)]) for _ in range(l)])
        t = np.array([0.0 for _ in range(l)])
        
        
        
        not_in_path = np.array([x for x in range(self.N - 1, -1, -1)])
        for x in self.taken:
            index = np.argwhere(not_in_path==x)
            not_in_path = np.delete(not_in_path, index)
        
        for x in range(l):
            v = self.taken[x]
            if v == s:
                if typ == 'f':
                    self.F = x
                else:
                    self.P = x
            if v == f:
                self.H = x
            vect = copy.copy(self.pMatrix[v])
            for y in not_in_path:
                vect = np.delete(vect, y)        
            pM[x] = vect
            t[x] = self.time[v]
            
        self.M = pM
        self.t = t
        
        return 1
        
        
    def __build_path__(self, n):
        if n == self.H:
            self.finish = 1
        self.taken.append(n)
        for x in self.links[n]:
            if x not in self.taken:
                self.__build_path__(x)
        
    
    def markov(self, pMatrix, time):
        l = len(pMatrix)
        
        for x in range(l):
            pMatrix[x,x] -= 1
        
        time = -1*self.time
        
        
        for pivot_index in range(l):
            
            pivot = pMatrix[pivot_index, pivot_index]
            if pivot == 0:
                x = pivot_index + 1
                while pMatrix[x, pivot_index] == 0.0:
                    x += 1
                    if x >= l:
                        print("cant find solution")
                        return 1
                pMatrix[[x, pivot_index]] = pMatrix[[pivot_index, x]]
                time[x], time[pivot_index] = time[pivot_index], time[x]
                pivot = pMatrix[pivot_index, pivot_index]
            
            for row in range(pivot_index + 1, l):
                factor = pMatrix[row, pivot_index] / pivot
                pMatrix[row] = pMatrix[row] - factor * pMatrix[pivot_index]
                time[row] = time[row] - factor * time[pivot_index]
        
        for x in range(l - 1, -1, -1):
            for y in range(x):
                factor = pMatrix[y,x] / pMatrix[x,x]
                pMatrix[y] = pMatrix[y] - factor*pMatrix[x]
                time[y] = time[y] - factor*time[x]
            
            selffactor = 1 / pMatrix[x,x]
            pMatrix[x] = selffactor * pMatrix[x] 
            time[x] = selffactor * time[x]
        
        return time
        
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