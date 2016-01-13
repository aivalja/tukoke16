# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:28:59 2016

@author: Anssi
"""

import random, time, itertools, numpy as np, matplotlib.pyplot as plt, sys, pygame

x_res = 1200
y_res = 560
things = 10 #int(sys.argv[1])
background_colour = (255,255,255)
(width, height) = (1200, 560)

map = [[[{'r':0,'d':0} for k in xrange(9)] for j in xrange(y_res)] for i in xrange(x_res)]

print 'map:' , len(map) , '*' , len(map[0]) , '*' , len(map[0][0])

def add_thing(x,y,layer,width,height,distance,reflectivity):
    print distance
    for i in range(width):
        for j in range(height):
            try:
                if map[x+i][y+j][layer]['d'] < distance:
                    map[x+i][y+j][layer]['d'] = distance
                    map[x+i][y+j][layer]['r'] = reflectivity
            except:
                #print "Out of range"
                pass
def plot():
    for i in xrange(len(map)):
        for j in xrange(len(map[i])):
            if (map[i][j][0]['d']!= 0):
                pygame.draw.rect( screen, (0, 0, (255*map[i][j][0]['d']/100) ), ( (int(i*width/x_res), int(j*height/y_res), int(map[i][j][0]['d']/1), int(map[i][j][0]['d']/1) ) ) )
                pygame.display.flip()
            #for k in xrange(9):
            #    plt.scatter(i,j,s=map[i][j][k]['d'])
print things
for i in range(things):
    add_thing(np.random.randint(0,x_res),np.random.randint(0,y_res),0,np.random.randint(1,100),np.random.randint(1,20),np.random.random()*100,np.random.random())

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('View')
screen.fill(background_colour)

plot()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False