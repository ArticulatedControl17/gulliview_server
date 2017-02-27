#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
from gulliview_server.msg import Pos
from error_calc import *
import rospkg

count =0


def talker():
    pub = rospy.Publisher('position', Pos, queue_size=10)
    rospy.init_node('error_calc_node_test', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        global count
        count +=1
        print count
        if count <50:
            p = bothCamera1()
        elif count >=50 and count <100:
            p= differentCamers(count)
        elif count >=100 and count <150:
            p = bothCamera2()
        elif count >=150 and count <200:
            p= differentCamersOtherway(count)
        else:
            p= bothCamera1()
        rospy.loginfo(p)
        pub.publish(p)
        rate.sleep()

def bothCamera1():
    p = Pos()
    p.x1 = 5
    p.y1 = 0
    p.cameraid1 = 1
    p.tagid1 = 1
    p.x2 = 5
    p.y2= 10
    p.cameraid2 = 1
    p.tagid2 = 2
    return p


def differentCamers(count):
    p = Pos()
    if count %2 == 1:
        p.cameraid1 = 1
        p.cameraid2 = 2

        p.x1 = 100
        p.y1 = 10
        p.tagid1 = 1
        p.x2 = 100
        p.y2= 20
        p.tagid2 = 2
    else:
        p.x1 = 5
        p.y1 = 10
        p.tagid1 = 1
        p.x2 = 5
        p.y2= 20
        p.tagid2 = 2
        p.cameraid1 = 1
        p.cameraid2 = 1
    return p


def bothCamera2():
    p = Pos()
    p.x1 = 100
    p.y1 = 20
    p.cameraid1 = 2
    p.tagid1 = 1
    p.x2 = 100
    p.y2= 30
    p.cameraid2 = 2
    p.tagid2 = 2
    return p

def differentCamersOtherway(count):
    p = Pos()
    if count %2 == 1:
        p.cameraid1 = 2
        p.cameraid2 = 2

        p.x1 = 100
        p.y1 = 40
        p.tagid1 = 1
        p.x2 = 100
        p.y2= 50
        p.tagid2 = 2
    else:
        p.x1 = 5
        p.y1 = 40
        p.tagid1 = 1
        p.x2 = 5
        p.y2= 50
        p.tagid2 = 2
        p.cameraid1 = 2
        p.cameraid2 = 1
    return p




if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
