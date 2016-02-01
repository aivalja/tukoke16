# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:28:59 2016

@author: Anssi
"""

import random, time, itertools, numpy as np, matplotlib.pyplot as plt, sys, pygame, math, json
from ctypes import *

libc = cdll.msvcrt

"""
Equation values
"""
snow_to_water = 0.1

x_res = int(2560/2)
y_res = 192/2
gap = 5
x_unit = int(x_res/4)
x_unit_small = int(x_res/8)
things = {}
width_multiplier = 1
lidar_a = 1
mean = False
selector = {'left':0,'front':x_unit,'right':2*x_unit,'back':3*x_unit}
radar_chunks = 3
max_distance = 120.0
test = True
no_rnd_objects = True

RED = 255
GREEN = 255
BLUE = 0

background_colour = (40,40,40)
(width, height) = ((x_res+gap*3)*width_multiplier, int(y_res*3+gap*2))
pygame.init()
clock = pygame.time.Clock()

# How many snowflakes in cubic meter
snow_a = 1000
# Diameter of snowflake in m, usually 0.001-0.08
snow_s = 0.01
# probability of colliding with a snowflake per meter
snow_p = math.pi*(snow_s/2)**2*snow_a

"""
things:
    contains one value for every type of thing
        every value contains one value for each direction (front, left, right, back)
            amount a
            reflectivity r (float 0.0-1.0)
                (min, max)
            size s
                ((min width, max width), (min width/height, max width/height))
            distance d
                (min, max)
            location on y axel y
                (min, max)
template:
name = {'left':{'a':, 'r':_r, 's':((,), (,)), 'd':(,), 'y':()},
       'front':{'a':, 'r':_r, 's':((,), (,)), 'd':(,), 'y':()},
       'right':{'a':, 'r':_r, 's':((,), (,)), 'd':(,), 'y':()},
       'back':{'a':, 'r':_r, 's':((,), (,)), 'd':(,)}, 'y':()}
"""

car_r = (0.1,0.3)
car_s = ((int(x_res/16),int(x_res/4)),(int(y_res/4),y_res))
car_y = (0,y_res/16)
car = {'car':{'left':{'a':3, 'r':car_r, 's':((int(x_res/8), int(x_res/6)), (2.0,4.0)), 'd':(1,10), 'y':car_y},
       'front':{'a':5, 'r':car_r, 's':((int(x_res/32),int(x_res/8)), (0.5,2.0)), 'd':(1,120), 'y':car_y},
       'right':{'a':1, 'r':car_r, 's':((int(x_res/8),int(x_res/6)), (2.0,4.0)), 'd':(1,5), 'y':car_y},
       'back':{'a':5, 'r':car_r, 's':((int(x_res/32),int(x_res/8)), (0.5,2.0)), 'd':(1,120), 'y':car_y}}}

pedestrian_r = (0.04,0.1)
pedestrian_y = (0,y_res/16)
pedestrian = {'pedestrian':{'front':{'a':1, 'r':pedestrian_r, 's':((int(x_res/64),int(x_res/32)), (0.2,0.5)), 'd':(1,50), 'y':pedestrian_y},
              'right':{'a':5, 'r':pedestrian_r, 's':((int(x_res/64),int(x_res/32)), (0.2,0.5)), 'd':(1,10), 'y':pedestrian_y}}}

obstacle_y = (0,y_res/16)
obstacle = {'obstacle':{'front':{'a':1, 'r':(0.01,0.3), 's':((int(x_res/64),int(x_res/12)), (1,2)), 'd':(1,120), 'y':obstacle_y}}}


things.update(car)
things.update(pedestrian)
things.update(obstacle)


f = open('output.txt','w')
json.dump(things,f)
f.close

"""
Create map that is the "real image"
"""
map = [[{'r':0,'d':int(max_distance)} for j in xrange(y_res)] for i in xrange(x_res)]
print 'map:' , len(map) , '*' , len(map[0])
sys.stdout.flush()

"""
Contains locations and ranges of all windows, 
format {'x':int, 'y':int, 'width':int, 'height':int, 'sensors':[boolean(lidar), boolean(radar), boolean(infrared)], 'image':boolean, 'gap':(x,y), 'clean':Boolean}
"""
windows = []

windows.append({'x':0, 'y':0, 'width':x_unit, 'height':y_res, 'sensors':[True, False, False], 'image':False, 'gap':(gap*0,gap*0), 'clean':True})
windows.append({'x':x_unit, 'y':0, 'width':x_unit, 'height':y_res, 'sensors':[True, False, False], 'image':False, 'gap':(gap*1,gap*0), 'clean':True})
windows.append({'x':(x_unit)*2, 'y':0, 'width':x_unit, 'height':y_res, 'sensors':[True, False, False], 'image':False, 'gap':(gap*2,gap*0), 'clean':True})
windows.append({'x':(x_unit)*3, 'y':0, 'width':x_unit, 'height':y_res, 'sensors':[True, False, False], 'image':False, 'gap':(gap*3,gap*0), 'clean':True})
windows.append({'x':0, 'y':y_res, 'width':x_unit, 'height':y_res, 'sensors':[True, True, False], 'image':False, 'gap':(gap*0,gap*1), 'clean':True})
windows.append({'x':x_unit, 'y':y_res, 'width':x_unit, 'height':y_res, 'sensors':[True, True, False], 'image':False, 'gap':(gap*1,gap*1), 'clean':True})
windows.append({'x':(x_unit)*2, 'y':y_res, 'width':x_unit, 'height':y_res, 'sensors':[True, True, False], 'image':False, 'gap':(gap*2,gap*1), 'clean':True})
windows.append({'x':(x_unit)*3, 'y':y_res, 'width':x_unit, 'height':y_res, 'sensors':[True, True, False], 'image':False, 'gap':(gap*3,gap*1), 'clean':True})
windows.append({'x':0, 'y':y_res*2, 'width':x_unit, 'height':y_res, 'sensors':[False, False, False], 'image':True, 'gap':(gap*0,gap*2)})
windows.append({'x':x_unit, 'y':y_res*2, 'width':x_unit, 'height':y_res, 'sensors':[False, False, False], 'image':True, 'gap':(gap*1,gap*2)})
windows.append({'x':(x_unit)*2, 'y':y_res*2, 'width':x_unit, 'height':y_res, 'sensors':[False, False, False], 'image':True, 'gap':(gap*2,gap*2)})
windows.append({'x':(x_unit)*3, 'y':y_res*2, 'width':x_unit, 'height':y_res, 'sensors':[False, False, False], 'image':True, 'gap':(gap*3,gap*2)})

"""
Will be used to calculate the strength of return signal
"""
def pulse_s(x, y):
    #print x,y
    point = map[x][y]
    x = point['d']
    # This causes the lag, because the less there is snow, the longer this loop will continue before stopping
    for i in range(x):
        if (random.random()<snow_p):
            if (random.random()<(1-snow_p)**i):
                return (1,i)
            else:
                return (0,1)
    # calculate strength of return signal (0-1)
    if (point['d']!=0 and point['r']!=0):
        return (1,point['d'])
    else:
        return (0, max_distance)

"""
Adds a thing to specific place
"""

def add_thing(x,y,width,height,distance,reflectivity, x_min, x_max): 
    #print x,y,width,height,distance,reflectivity,x_min,x_max
    #sys.stdout.flush()
    for i in range(width):
        for j in range(height):
            try:
                if (((x+i)>=x_min and (x+i)<=x_max)):
                    #print i, x_min, x_max
                    point = map[x+i][y+j]
                    if point['d'] > distance:
                        point['d'] = distance
                        point['r'] = reflectivity
                else:
                    print 'out of range:',i, x_min, x_max
            except:
                #print "Out of range"
                pass
            
"""
Draws the simulated image for each sensor type seperatly. The darker the pixel is, the futher away it is OR there was no return signal
"""
def plot(index, sensors):
    window = windows[index]
    scale = int(window['width']/radar_chunks)
    if sensors[1]:
        try:
            for i in range(radar_chunks):
                d = max_distance
                for j in range(int(window['width']/3)):
                    for k in range(window['height']):
                        d_t = map[scale*i+j+window['x']][k]['d']
                        if (d_t<d):
                            d = d_t
                multiplier = 1-1.0*(d/max_distance)
                screen.fill((int(multiplier*RED), int(multiplier*GREEN), int(multiplier*BLUE)),rect=((int(width_multiplier*i*scale+width_multiplier*window['x']+window['gap'][0]), int(window['y']+window['gap'][1]),scale,window['y'])))
        except:
            print "Unexpected error:", sys.exc_info()[0], i, scale, index
        multiplier = 1-1.0*(d/max_distance)
        screen.fill((int(multiplier*RED), int(multiplier*GREEN), int(multiplier*BLUE)),rect=((int(width_multiplier*i*scale+width_multiplier*window['x']+window['gap'][0]), int(window['y']+window['gap'][1]),scale,window['y'])))
    if sensors[0]:
        for i in range(int(window['width']/3)):
            for j in range(int(window['height']/3)):
                d = []
                for m in range(lidar_a):
                    for k in range(3):
                        for l in range(3):
                            #r = pulse_s(i*3+k,j*3+l)
                            d.append(pulse_s(i*3+k+window['x'],j*3+l)[1])
                if(mean):
                    mean_d = np.mean(d)
                else:
                    mean_d = max(d)
                multiplier = 1-1.0*(mean_d/max_distance)
                
                screen.fill((int(multiplier*RED), int(multiplier*GREEN), int(multiplier*BLUE)),rect=((int(width_multiplier*i*3+width_multiplier*window['x']+window['gap'][0]), int(j*3+window['y']+window['gap'][1]),width_multiplier*3,3)))
    if window['image']:
        for i in range(int(window['width']/3)):
            for j in range(int(window['height']/3)):
                for k in range(width_multiplier):
                    screen.fill((int(255*(1-map[window['x']+i*3][j*3]['d']/max_distance)), int(255*(1-map[window['x']+i*3][j*3]['d']/max_distance)), int(255*(1-map[window['x']+i*3][j*3]['d']/max_distance))),((int(width_multiplier*i*3+width_multiplier*window['x']+window['gap'][0]), int(j*3+window['y']+window['gap'][1])),(3,3)))
                    #screen.set_at((int(width_multiplier*i*3+width_multiplier*window['x']+window['gap'][0]), int(j*3+window['y']+window['gap'][1])),(int(255*(1-map[window['x']+i*3][j*3]['d']/max_distance)), int(255*(1-map[window['x']+i*3][j*3]['d']/max_distance)), int(255*(1-map[window['x']+i*3][j*3]['d']/max_distance)) ))
            
"""
Add elements to map
"""
def set_things(amount):
    sys.stdout.flush()
    for i in amount:
        i = things[i]
        for k in xrange(len(i)):
            l = i.values()[k]
            x_min = selector[i.keys()[k]]
            sys.stdout.flush()
            x_max = x_min+x_unit
            sys.stdout.flush()
            for j in range(l['a']):
                width = np.random.randint(*l['s'][0])
                height = int(width/np.random.uniform(*l['s'][1]))
                x = np.random.randint(x_min,x_max-width)
                y = int(y_res-np.random.uniform(*l['y'])-height)
                distance = np.random.randint(*l['d'])
                reflectivity = np.random.uniform(*l['r'])
                if not no_rnd_objects:
                    add_thing(x, y, width, height ,distance, reflectivity, x_min, x_max)

def plot_all():
    i = len(windows)-1
    while i>=0:
        plot(i,windows[i]['sensors'])
        i -= 1
def plot_one(x, y, width, height, distance):
    print distance
    d_all = []
    for i in range(int(width/3)):
        for j in range(int(height/3)):
            d = []
            for k in range(lidar_a):
                for l in range(3):
                    for m in range(3):
                        d.append(pulse_s(i*3+l+x,j*3+m+y)[1])
            d_max = max(d)
            d_all.append(d_max)
    d_all_mean = np.mean(d_all)
    
    print 'Range:',distance, ' Probability:',int(d_all_mean/distance*1000)/10.0
   

"""
Create a test object, whose detection rate is calculated
"""
t_x = int(x_unit*1.5)
t_y = int(y_res*0.1)
t_w = x_unit_small
t_h = y_res/2
t_d = 50
if test:
    add_thing(t_x, t_y, t_w, t_h, t_d, 1, 0, x_res)
set_things(things)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('View')
screen.fill(background_colour)

screen.fill(background_colour)
"""
for i in xrange(x_res):
    for j in xrange(y_res):
        for k in range(width_multiplier):
            screen.set_at((int(width_multiplier*i+k), int(j+y_res*2+1)),(int(255*(1-map[i][j]['d']/max_distance)), int(255*(1-map[i][j]['d']/max_distance)), int(255*(1-map[i][j]['d']/max_distance)) ))
"""
plot_all()
color = screen.get_at((t_x,t_y))
print color
if test:
    plot_one(t_x, t_y, t_w, t_h, t_d)
sys.stdout.flush()
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
            if event.key == pygame.K_KP8:
                lidar_a +=1
            if event.key == pygame.K_KP2:
                lidar_a -=1
            if event.key == pygame.K_SPACE:
                mean = not mean
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            snow_p = math.pi*(snow_s/2)**2*snow_a
            print '\nValues:',snow_a, snow_s, snow_p, lidar_a, mean
            if test:
                plot_one(t_x, t_y, t_w, t_h, t_d)
            sys.stdout.flush()
            plot_all()
            color = screen.get_at((t_x,t_y+y_res))[0]*1.0/RED*max_distance
            print color
    pygame.display.update()
    clock.tick(60)
pygame.display.quit()
pygame.quit()
sys.exit()
    