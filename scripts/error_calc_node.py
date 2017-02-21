#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
from gulliview_server.msg import *
from error_calc import *
import rospkg

pub = rospy.Publisher('error', Int64, queue_size=10)
ec = errorCalc()
currentCam = -1
timeoutCam = False
timeoutTime= -1
fromError = 0
errorDifference = 0
lookforToError = False
iteration = 0
updateTime = 0
tag1Pos= (-1,-1)
tag2Pos = (-1,-1)

def callback(msg):
    global pub
    global ec
    global currentCam
    global timeoutCam
    global timeoutTime
    global fromError
    global errorDifference
    global iteration
    global lookforToError
    global updateTime
    global tag1Pos
    global tag2Pos

    if msg.tagid == 1:
        tag1Pos = (msg.x,msg.y)
    if msg.tagid == 2:
        tag2Pos = (msg.x,msg.y)

    if tag1Pos>=0 and tag2Pos>=0:
        error = ec.calculateError(tag1Pos, tag2Pos)
    else:
        error = 0

    #look for common camera coverage areas:

    if(lookforToError and currentCam != msg.cameraid):
        #calculte camera adjumstment difference
        errorDifference = (fromError - error)/30
        lookforToError=False

    if(msg.cameraid!=currentCam and timeoutCam==False):
        #found new camera
        currentCam= msg.cameraid
        timeoutCam= True
        timeoutTime = rospy.get_time()+ rospy.Duration(3, 0).to_sec()
        updateTime = rospy.get_time()+ rospy.Duration(0.1, 0).to_sec()
        iteration = 1
        fromError = error
        lookforToError = True
    if(rospy.get_time() > timeoutTime):
        #three seconds pass, should not  be in area where 2 cameras look
        timeoutCam = False
    if(msg.cameraid==currentCam):
        if(timeoutCam and rospy.get_time() > updateTime):
            #calculate camera adjustment difference one time step
            updateTime = rospy.get_time()+ rospy.Duration(0.1, 0).to_sec()
            iteration= iteration+1

        # publishing only one camera
        error = error  -errorDifference*iteration
        rospy.loginfo("error is: %s", error)
        rospy.loginfo(rospy.get_caller_id() + "I heard x: %s and y: %s, and cameraid: %s, tagid: %s" , msg.x, msg.y, msg.cameraid, msg.tagid)
        pub.publish(error)


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
