# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:28:59 2016

@author: Anssi
"""

import random, time, itertools, numpy as np, matplotlib.pyplot as plt, sys

x_res = 120
y_res = 56
things = sys.argv[0]

map = [[[{'r':0,'d':0} for k in xrange(9)] for j in xrange(y_res)] for i in xrange(x_res)]

print 'map:' , len(map) , '*' , len(map[0]) , '*' , len(map[0][0])

def add_thing(x,y,layer,width,height,distance,reflectivity):
    for i in range(width):
        print i
        for j in range(height):
            #try:
            print x,y,i,j,layer
            if map[x+i][y+j][layer]['d'] > distance:
                map[x+i][y+j][layer]['d'] = distance
                map[x+i][y+j][layer]['r'] = reflectivity
            """except:
                #print "Out of range"
                pass"""
def plot():
    for i in xrange(len(map)):
        print i
        for j in xrange(len(map[i])):
            plt.scatter(i,j,s=map[i][j][0]['d'])
            #for k in xrange(9):
            #    plt.scatter(i,j,s=map[i][j][k]['d'])
    plt.grid(True)
    plt.show()

for i in things:
    add_thing(np.random.randint(0,*x_res,np.random.randint()*y_res,0,np.random.randint(1,100),np.random.randint(1,20),np.random.random()*120,np.random.random())
plot()
