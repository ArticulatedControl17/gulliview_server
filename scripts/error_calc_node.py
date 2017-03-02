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
prevError = 0

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
    global prevError
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
            error = ec.calculateError((msg.x1,msg.y1), (msg.x2,msg.y2))
            prevError = error
        else:
            #nr 2 is back and nr 1 is front
            cameraid=msg.cameraid1
            error = ec.calculateError((msg.x2,msg.y2), (msg.x1,msg.y1))
            prevError=error
    #look for common camera coverage areas:

    if(lookforToError and currentCam != cameraid):
        #calculte camera adjumstment difference
        errorDifference = (fromError - error)/40
        lookforToError=False

    if(cameraid!=currentCam and timeoutCam==False):
        #found new camera
        currentCam= cameraid
        timeoutCam= True
        timeoutTime = rospy.get_time()+ rospy.Duration(1, 0).to_sec()
        updateTime = rospy.get_time()+ rospy.Duration(0.025, 0).to_sec()
        iteration = 1
        fromError = error
        lookforToError = True
    if(rospy.get_time() > timeoutTime):
        #three seconds pass, should not  be in area where 2 cameras look
        timeoutCam = False
    if(cameraid==currentCam):
        if(timeoutCam and rospy.get_time() > updateTime):
            #calculate camera adjustment difference one time step
            updateTime = rospy.get_time()+ rospy.Duration(0.025, 0).to_sec()
            iteration= iteration+1

        # publishing only one camera
        error = error  -errorDifference*iteration
        #rospy.loginfo("error is: %s", error)
        #rospy.loginfo(rospy.get_caller_id() + "I heard x1: %s and y1: %s, and cameraid1: %s, tagid1: %s" , msg.x1, msg.y1,cameraid, msg.tagid1)
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
