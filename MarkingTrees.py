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
        while self.counter < self.nodes:
            x = rd.randint(0, self.nodes - 1)
            "print(x)"
            self.tryMark(x)
            
    def second(self):
        self.indexTree = [x for x in range(self.nodes)]
        
        for x in range(self.nodes - 1, 0, -1):
            if self.counter == self.nodes:
                break
            rand = rd.randint(0, x)
            index = self.indexTree[rand]
            self.indexTree[rand] = self.indexTree[x]
            self.indexTree[x] = index
            self.tryMark(index)
            
        print(self.tree)
            
    def third(self):
        self.indexTree = [x for x in range(self.nodes)]
        
        while len(self.indexTree) > 1:
            last = len(self.indexTree) - 1
            rand = rd.randint(0, last)
            index = self.indexTree[rand]
            self.tryMark2(index)
        
        print(self.tree)
            
    def tryMark(self, index):
        if self.tree[index] == False:
            self.tree[index] = True
            self.counter += 1
            self.checkOthers(index)
        else:
            pass
                            
    def checkOthers(self, index):
        parent = ((index + 1 )// 2) - 1
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
        
            
             
        
if __name__ == "__main__":
    m = marking(7)
    m.third()