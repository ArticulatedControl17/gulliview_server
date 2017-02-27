#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
from gulliview_server.msg import *
from error_calc import *
import rospkg

pub = rospy.Publisher('error', Int64, queue_size=10)
ec = errorCalc()
camera = -1
nextCamera = -1
first = True
commonArea = False
prevFront = {}
prevBack = {}

def callback(msg):
    global pub
    global ec
    global camera
    global nextCamera
    global first
    global commonArea
    global prevFront
    global prevBack

    print camera

    if (msg.x2==0 and msg.y2==0 and msg.cameraid2==0 and msg.tagid2==0):
        print "ONE MESSAGE ZERO*************"
        #only one tag out
        cameraid= msg.cameraid1
        error = prevError
    else:
        #two tags
        #front == id 2
        #back == id 1
        if msg.tagid1 ==1:
            #nr 1 is back and nr 2 is front
            cameraid=msg.cameraid2
            error = ec.calculateError((msg.x1,msg.y1), (msg.x2,msg.y2), 0)
            prevError = error
        else:
            #nr 2 is back and nr 1 is front
            cameraid=msg.cameraid1
            error = ec.calculateError((msg.x2,msg.y2), (msg.x1,msg.y1), 0)
            prevError=error
    #look for common camera coverage areas:

    #define front and back tags
    if (msg.tagid1 == 2):
        front = (msg.x1, msg.y1, msg.cameraid1)
        back = (msg.x2, msg.y2, msg.cameraid2)
    else:
        back = (msg.x1, msg.y1, msg.cameraid1)
        front = (msg.x2, msg.y2, msg.cameraid2)

    if first:
        #TODO: be able to start in common areas
        #initiate
        camera= back[2]
        first=False


    if(not msg.cameraid1 == msg.cameraid2 and not commonArea):
        #entering common area
        camera = back[2]
        nextCamera = front[2]
        commonArea = True

    if(back[2]==nextCamera and commonArea):
        print "leaving ***********************************************"
        #leaving common area
        camera = nextCamera
        commonArea = False

    if msg.cameraid1==camera and msg.cameraid2==camera:
        prevBack = back
        prevFront = front
        rospy.loginfo("error is: %s", error)
        rospy.loginfo(rospy.get_caller_id() + "I heard x1: %s and y1: %s, and cameraid1: %s, tagid1: %s" , msg.x1, msg.y1,cameraid, msg.tagid1)
        pub.publish(error)
    else: #wrong camera
        print "Fel camera, should happen every second time"
        if commonArea:
            #calculate with previous point, increase lookahead
            error = ec.calculateError(prevBack[0],prevBack[1],back[0], back[1], 15)
            rospy.loginfo("error is: %s", error)
            pub.publish(error)
        if not commonArea:
            pass



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
