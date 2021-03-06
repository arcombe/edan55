# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 08:08:18 2017
@author: Arcombe
"""

import scipy as scy
import pylab as py
import random as rd
import math as ma

class marking:
    
    def __init__(self, nodes):
        self.tree = [False for x in range(nodes)]
        self.nodes = nodes
        self.counter = 0
        
    def __call__(self):
        pass
        
    def first(self):
        rounds = 0
        
        while self.counter < self.nodes:
            rounds += 1
            x = rd.randint(0, self.nodes - 1)
            "print(x)"
            self.tryMark(x)
            
        return rounds
            
    def second(self):
        self.indexTree = [x for x in range(self.nodes)]
        rounds = 0
        
        for x in range(self.nodes - 1, 0, -1):
            rounds += 1
            if self.counter == self.nodes:
                break
            rand = rd.randint(0, x)
            index = self.indexTree[rand]
            self.indexTree[rand] = self.indexTree[x]
            self.indexTree[x] = index
            self.tryMark(index)

        return rounds
            
    def third(self):
        self.indexTree = [x for x in range(self.nodes)]
        self.indexAtTree = [x for x in range(self.nodes)]
        rounds = 0
        
        while len(self.indexTree) > 1:
            rounds += 1
            last = len(self.indexTree) - 1
            rand = rd.randint(0, last)
            index = self.indexTree[rand]
            self.tryMark2(index)

        return rounds
    
    def third2(self):
        self.indexTree = [x for x in range(self.nodes)]
        self.indexAt = [x for x in range(self.nodes)]
        rounds = 0
        
        while self.counter < self.nodes:
            rounds += 1
            rand = rd.randint(0, self.nodes - self.counter - 1)
            index = self.indexTree[rand]
            self.tryMark3(index)
            
        return rounds
    
    def tryMark(self, index):
        if self.tree[index] == False:
            self.tree[index] = True
            self.counter += 1
            self.checkOthers(index)
        else:
            pass
                            
    def checkOthers(self, index):
        if index != 0:
            parent = (((index + 1 )// 2) - 1)
        else:
            parent = 0 
        leftChild = index * 2 + 1
        rightChild = index * 2 + 2
        if parent != index:
            if self.tree[parent]:
                if index % 2 == 0:
                    self.tryMark(index - 1)
                else:
                    self.tryMark(index + 1)
            if index % 2 == 0:
                if self.tree[index - 1]:
                    self.tryMark(parent)
            elif self.tree[index + 1]:
                self.tryMark(parent)
        if leftChild < self.nodes:
            if self.tree[leftChild]:
                self.tryMark(rightChild)
            elif self.tree[rightChild]:
                self.tryMark(leftChild)
                
    def tryMark2(self, index):
        if self.tree[index] == False:
            self.tree[index] = True
            self.checkOthers2(index)
            self.indexTree.remove(index)
        else:
            pass
                
    def tryMark3(self, index):
        
        if self.tree[index] == False:
            self.tree[index] = True
            self.counter += 1
            
            indexat = self.indexAt[index]
            last = self.indexTree[self.nodes - self.counter]
            
            self.indexTree[indexat] = last
            self.indexTree[self.nodes - self.counter] = index
            
            self.indexAt[last] = indexat
            self.indexAt[index] = self.nodes - self.counter
            
            self.checkOthers3(index)
        else:
            pass
            
        
    def checkOthers2(self, index):
        if index != 0:
            parent = (((index + 1 )// 2) - 1)
        else:
            parent = 0 
        leftChild = index * 2 + 1
        rightChild = index * 2 + 2
        if parent != index:
            if self.tree[parent]:
                if index % 2 == 0:
                    self.tryMark2(index - 1)
                else:
                    self.tryMark2(index + 1)
            if index % 2 == 0:
                if self.tree[index - 1]:
                    self.tryMark2(parent)
            elif self.tree[index + 1]:
                self.tryMark2(parent)
        if leftChild < self.nodes:
            if self.tree[leftChild]:
                self.tryMark2(rightChild)
            elif self.tree[rightChild]:
                self.tryMark2(leftChild)
                
    def checkOthers3(self, index):
        if index != 0:
            parent = (((index + 1 )// 2) - 1)
        else:
            parent = 0 
        leftChild = index * 2 + 1
        rightChild = index * 2 + 2
        if parent != index:
            if self.tree[parent]:
                if index % 2 == 0:
                    self.tryMark3(index - 1)
                else:
                    self.tryMark3(index + 1)
            if index % 2 == 0:
                if self.tree[index - 1]:
                    self.tryMark3(parent)
            elif self.tree[index + 1]:
                self.tryMark3(parent)
        if leftChild < self.nodes:
            if self.tree[leftChild]:
                self.tryMark3(rightChild)
            elif self.tree[rightChild]:
                self.tryMark3(leftChild)
        
    def reset(self):
        self.__init__(self.nodes)
        
    
        
if __name__ == "__main__":
    result = np.zeros(10)
    x = 20
    m = marking(pow(2,x) - 1)
    for i in range(0, 10):
        result[i] = m.third2()
        m.reset()
    print(pow(2,x) - 1)
    print(np.mean(result))
    print(np.std(result))
    
    
    