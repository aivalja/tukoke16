# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:28:59 2016

@author: Anssi
"""

import random, time, itertools, numpy as np, matplotlib.pyplot as plt, sys, pygame

x_res = 402
y_res = 192
things = 10 #int(sys.argv[1])
background_colour = (0,0,0)
(width, height) = (x_res, int(y_res*2))
pygame.init()
clock = pygame.time.Clock()
"""
Create map that includes the "real image"
"""
map = [[{'r':0,'d':0} for j in xrange(y_res)] for i in xrange(x_res)]

print 'map:' , len(map) , '*' , len(map[0])
"""
Will be used to calculate the strength of return signal
"""
def pulse_s(x, y):
    point = map[x][y]
    # calculate strength of return signal (0-1)
    if (point['d']!=0 and point['r']!=0):
        return 1
    else:
        return 0
"""
Adds an thing to specific place
"""
def add_thing(x,y,width,height,distance,reflectivity):
    for i in range(width):
        for j in range(height):
            try:
                if map[x+i][y+j]['d'] < distance:
                    map[x+i][y+j]['d'] = distance
                    map[x+i][y+j]['r'] = reflectivity
            except:
                #print "Out of range"
                pass
"""
Draws real image under, where darker = further. Top one is what lidar sees, darker = less likely true
"""
def plot():
    pygame.draw.line(screen,(100,100,100),(0,y_res),(x_res,y_res))
    for i in xrange(x_res):
        for j in xrange(y_res):
            if (map[i][j]['d']!= 0):
                screen.set_at((int(i), int(j+y_res+1)),((255*map[i][j]['d']/100), (255*map[i][j]['d']/100), (255*map[i][j]['d']/100) ))
                #pygame.display.update()
                
    for i in range(x_res/3):
        #print i
        for j in range(y_res/3):
            a = []
            for k in range(3):
                for l in range(3):
                    a.append(pulse_s(i*3+k,j*3+l))
            mean = np.mean(a)
            screen.fill((255*mean, 255*mean, 255*mean ),rect=((int(i*3), int(j*3),3,3)))
            #screen.set_at((int(i), int(j)),(255*mean, 255*mean, 255*mean ))
            #pygame.display.update()
         
print things
for i in range(things):
    add_thing(np.random.randint(0,x_res),np.random.randint(0,y_res),np.random.randint(1,100),np.random.randint(1,20),np.random.randint(0,100),np.random.random())

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('View')
screen.fill(background_colour)

plot()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()    
    clock.tick(60)
    
    