import scipy as sp
import numpy as np
import sys
import random as rd
import matplotlib.pyplot as plt

class maxcut:
    
    def __init__(self, file):
        f = open(file, 'r')
        self.n, self.m = [int(x) for x in f.readline().split()]
        self.e = np.array([np.zeros(self.n) for x in range(self.n)])
        for line in f:
            v1, v2, w = [int(x) for x in line.split()]
            self.e[v1 - 1][v2 - 1] = w
            self.e[v2 - 1][v1 - 1] = w
        
    def __call__(self):
        resultR = np.zeros(100)
        #resultS = np.zeros(100)
        #resultRS = np.zeros(100)
        for x in range(100):
            A, B, sum = self.r()
            resultR[x] = sum
        mean = np.mean(resultR)
        var = np.max(resultR)
        print(mean)
        print(var)
        
        
        
    def r(self):
        A = []
        B = []
        sum = 0
        for x in range(self.n):
            flip = rd.randint(0,1)
            if(flip):
                A.append(x)
            else:
                B.append(x)
        for x in range(len(A)):
            for y in range(len(B)):
                sum += self.e[A[x]][B[y]]
        return A, B, sum
    
    def s(self, A = [], B = None, sum = 0):
        if (B == None):
            B = [x for x in range(self.n)]
        old = -1
        while (old != sum):
            old = sum
            tmpA = A
            for x in tmpA:
                value_A = self.__get_sum(x, A)
                value_B = self.__get_sum(x, B)
                if value_A >= value_B:
                    A.remove(x)
                    B.append(x)
                    sum += value_A - value_B
            tmpB = B
            for x in tmpB:
                value_A = self.__get_sum(x, A)
                value_B = self.__get_sum(x, B)
                if value_B >= value_A:
                    B.remove(x)
                    A.append(x)
                    sum += value_B - value_A
    
        return A, B, sum
    
    def __get_sum(self, v, A):
        sum = 0
        for x in A:
            sum += self.e[v][x]
        return sum
    
    def sr(self):
        A, B, sum = self.r()
        return self.s(A = A, B = B, sum = sum)
        
        
if __name__ == "__main__":
    maxc = maxcut(sys.argv[1])
    maxc()
    