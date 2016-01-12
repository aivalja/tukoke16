# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:28:59 2016

@author: Anssi
"""

import random, time, itertools, numpy as np, matplotlib.pyplot as plt, sys

x_res = 1200
y_res = 576
things = sys.argv[0]

map = [[[{'r':0,'d':0} for k in xrange(9)] for j in xrange(y_res)] for i in xrange(x_res)]

print 'map:' , len(map) , '*' , len(map[0]) , '*' , len(map[0][0])

def add_thing(x,y,width,height,distance,reflectivity):
    for i in range(width):
        for j in range(height):
            for k in xrange(9):
                print x,y,i,j,k
                try:
                    if map[x+i][y+j][k]['d'] > distance:
                        map[x+i][y+j][k]['d'] = distance
                        map[x+i][y+j][k]['r'] = reflectivity
                except:
                    print "Out of range"
                    pass
def plot():
    for i in xrange(len(map)):
        for j in xrange(len(map[i])):
            for k in xrange(9):
                plt.scatter(i,j,s=map[i][j][k]['d'])
    plt.grid(True)
    plt.show()

for i in things:
    add_thing(np.random.random()*x_res,np.random.random()*y_res,np.random.randint(1,1000),np.random.randint(1,200),np.random.random()*120,np.random.random())

