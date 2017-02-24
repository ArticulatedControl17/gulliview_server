#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
from gulliview_server.msg import *
from error_calc import *
import rospkg

pub = rospy.Publisher('error', Int64, queue_size=10)
ec = errorCalc()
frontCamera = -1
backCamera = -1
camera = -1
nextCamera = -1
first = True

def callback(msg):
    global pub
    global ec
    global camera
    global nextCamera
    global first

    if (msg.x2==0 and msg.y2==0 and msg.cameraid2==0 and msg.tagid2==0):
        #only one tag out
        cameraid= msg.cameraid1
        error = -100000
    else:
        #two tags
        #front == id 2
        #back == id 1
        if msg.tagid1 ==1:
            #nr 1 is back and nr 2 is front
            cameraid=msg.cameraid2
            error = ec.calculateError((msg.x1,msg.y1), (msg.x2,msg.y2))
        else:
            #nr 2 is back and nr 1 is front
            cameraid=msg.cameraid1
            error = ec.calculateError((msg.x2,msg.y2), (msg.x1,msg.y1))

    #look for common camera coverage areas:

    if first:
        #TODO: be able to start in common areas
        #initiate
        camera= msg.tagid1

    #define front and back tags
    if (msg.tagid1 == 2):
        front = (msg.x1, msg.y1, msg.camid1)
        back = (msg.x2, msg.y2, msg.camid2)
    else:
        back = (msg.x1, msg.y1, msg.camid1)
        front = (msg.x2, msg.y2, msg.camid2)

    if(not msg.cameraid1 == msg.cameraid2 and not commonArea):
        #entering common area
        camera = back[2]
        nextCamera = front[2]
        commonArea = True

    if(not msg.cameraid1 == msg.cameraid2 and commonArea):
        #leaving common area
        camera = nextCamera
        commonArea = False

    if msg.cameraid1==camera and msg.cameraid2==camera:
        rospy.loginfo("error is: %s", error)
        rospy.loginfo(rospy.get_caller_id() + "I heard x1: %s and y1: %s, and cameraid1: %s, tagid1: %s" , msg.x1, msg.y1,cameraid, msg.tagid1)
        oldError = error
        pub.publish(error)
    else: #wrong camera
        print "Fel camera, should happen every second time"
        #pub.publish(oldError)


def listener():
    rospy.init_node('error_calc_node', anonymous=True)
    rospy.Subscriber('position', Pos, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

#Command for manually publishing in terminal
#rostopic pub -1 /position gulliviewServer/Pos "x: 60
#y: 20
#cameraid: 0"
