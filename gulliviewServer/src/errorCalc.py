#!/usr/bin/env python

from math import sqrt
from Queue import Queue

class Point:
    def __init__(self, x , y):
        self.x = x
        self.y = y


def calculateError(p1, p2, p0):
        return abs((p2.x - p1.x)*(p1.y-p0.y) - (p1.x-p0.x)*(p2.y-p1.y)) / (sqrt((p2.x-p1.x)*(p2.x-p1.x) + (p2.y-p1.y)*(p2.y-p1.y)))

def isAboveEnd (begin, end, p0):
    #checks if a point is passed the end point of a line.
    if begin.x - end.x !=0 and begin.y - end.y !=0:
        slope = float(begin.y - end.y) / float(begin.x - end.x)
        prependularSlope = (-1)/slope
        prependularM = end.y - end.x*prependularSlope
        if begin.y < end.y:
            #going up
            if (p0.x*prependularSlope + prependularM - p0.y) < 0:
                return True
            else:
                return False
        else:
            #going down
            if (p0.x*prependularSlope + prependularM - p0.y) > 0:
                return True
            else:
                return False
    elif begin.x - end.x:
        #going straight in x direction
        if begin.x < end.x:
            #going right
            return p0.x > end.x
        else:
            #going left
            return p0.x < end.x
    else:
        #going straight in y direction
        if begin.y < end.y:
            #going up
            return p0.y > end.y
        else:
            #going down
            return p0.y < end.y


def createQueuePath():
    f = open('/home/filip/Prog/edu/DATX02/catkin_ws/src/gulliviewserver/gulliviewServer/src/path.txt', 'r')
    lines = [line.rstrip('\n') for line in f.readlines()]
    posL = [s.split(' ', 1 ) for s in lines]
    queue = Queue()
    for l in posL:
        queue.put(Point(int(l[0]),int(l[1])))
    return queue

#TODO: Write tests for errorCalc
