#!/usr/bin/env python
import rospy
from custom_msgs.msg import *

from sensor_msgs.msg import Joy
import time


class GatherDataPoints:
    def __init__(self):
        rospy.init_node('gather_data', anonymous=False)
        
        self.last_point = None
        self.filename = raw_input("input file name: ")
        
        rospy.Subscriber('gv_positions', GulliViewPositions, self.gvPositionsHandler)
        rospy.Subscriber('joy', Joy, self.joyHandler)
        
        self.prev_x = 0
    
    
    def writeToFile(self):
        if self.last_point == None:
            print "last_point is None"
        else:
            print "appending: " + str(self.last_point)
            with open(self.filename, 'a') as f:
                f.write(str(self.last_point[0]) + " " + str(self.last_point[1]) + '\n')
    
    def joyHandler(self, data):
        if data.buttons[14] == 1.0 and self.prev_x == 0.0:
            self.writeToFile()
            
        self.prev_x = data.buttons[14]
            
    
    def gvPositionsHandler(self, data):
        p1 = (data.p1.x, data.p1.y)
        p2 = (data.p2.x, data.p2.y)
        tagid1 = data.tagid1
        tagid2 = data.tagid2
        cameraid = data.cameraid
        
        print cameraid
        
        self.last_point = p1
        
        


    def spin(self):
        
        while True:
            raw_input("press enter to get data point")
            
            if rospy.is_shutdown():
                break
            self.writeToFile()
        



if __name__ == '__main__':
    g = GatherDataPoints()
    g.spin()
