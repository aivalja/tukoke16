# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:28:59 2016

@author: Anssi
"""

import random, time, itertools, numpy as np, matplotlib.pyplot as plt, sys, pygame, math

"""
Equation values
"""
snow_to_water = 0.1

x_res = 402
y_res = 192

things = {}

max_distance = 100.0

background_colour = (0,0,0)
(width, height) = (x_res, int(y_res*2))
pygame.init()
clock = pygame.time.Clock()

# How many snowflakes in cubic meter
snow_a = 1000
# Diameter of snowflake in m, usually 0.001-0.08
snow_s = 0.01
# probability of colliding with a snowflake per meter
snow_p = math.pi*(snow_s/2)**2*snow_a

car_a = 10 
car_r = (0.1,0.3)
car_s = ((int(x_res/16),int(x_res/4)),(int(y_res/4),y_res))
car = {'car':{'a':car_a, 'r':car_r,'s':car_s}}

human_a = 15
human_r = (0.04,0.1)
human_s = ((int(x_res/64),int(x_res/16)),(int(y_res/4),y_res))
human = {'human':{'a':human_a, 'r':human_r,'s':human_s}}

things.update(car)
things.update(human)


f = open('output.txt','w')
"""
Create map that includes the "real image"
"""
map = [[{'r':0,'d':int(max_distance)} for j in xrange(y_res)] for i in xrange(x_res)]

print 'map:' , len(map) , '*' , len(map[0])

"""
Calculate correct H using some formula
"""
def H(R):
    return R
"""
Will be used to calculate the strength of return signal
"""
def pulse_s(x, y):
    point = map[x][y]
    if point['d'] == 0:
        x = int(max_distance)
    else:
        x = point['d']
    for i in range(x):
        if (random.random()<snow_p):
            return (1,i)
    # calculate strength of return signal (0-1)
    if (point['d']!=0 and point['r']!=0):
        return (1,point['d'])
    else:
        return (0, max_distance)
"""
Adds an thing to specific place
"""
def add_thing(x,y,width,height,distance,reflectivity):
    for i in range(width):
        for j in range(height):
            try:
                point = map[x+i][y+j]
                if point['d'] > distance:
                    point['d'] = distance
                    point['r'] = reflectivity
            except:
                #print "Out of range"
                pass
"""
Draws real image under, where darker = further. Top one is what lidar sees, darker = less likely true
"""
def plot(initial=False):
    if initial:
        screen.fill(background_colour)
        pygame.draw.line(screen,(100,100,100),(0,y_res),(x_res,y_res))
        for i in xrange(x_res):
            for j in xrange(y_res):
                if (map[i][j]['d']!= 0):
                    screen.set_at((int(i), int(j+y_res+1)),(int(255*(1-map[i][j]['d']/max_distance)), int(255*(1-map[i][j]['d']/max_distance)), int(255*(1-map[i][j]['d']/max_distance)) ))
                
    for i in range(int(x_res/3)):
        for j in range(int(y_res/3)):
            d = []
            for k in range(3):
                for l in range(3):
                    #r = pulse_s(i*3+k,j*3+l)
                    d.append(pulse_s(i*3+k,j*3+l)[1])
            mean_d = np.mean(d)
            multiplier = 1-1.0*mean_d/max_distance
            screen.fill((int(multiplier*255), int(multiplier*255), 0),rect=((int(i*3), int(j*3),3,3)))

for i in things:
    i = things[i]
    for j in range(i['a']):
        print i
        add_thing(np.random.randint(0,x_res),np.random.randint(0,y_res),np.random.randint(*i['s'][0]),np.random.randint(*i['s'][1]),np.random.randint(1,max_distance),np.random.uniform(*i['r']))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('View')
screen.fill(background_colour)

plot(initial=True)
f.close()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snow_a+=100
            if event.key == pygame.K_DOWN:
                if (snow_a>100):
                    snow_a-=100
            if event.key == pygame.K_RIGHT:
                snow_s +=0.001
            if event.key == pygame.K_LEFT:
                if(snow_s>0.001):
                    snow_s-=0.001
            snow_p = math.pi*(snow_s/2)**2*snow_a
            snow_p = math.pi*(snow_s/2)**2*snow_a
            print snow_a,snow_p, snow_s
            plot()
    pygame.display.update()
    clock.tick(60)
pygame.display.quit()
pygame.quit()
sys.exit()
    