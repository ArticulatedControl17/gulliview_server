#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
from gulliviewserver.msg import *
from errorCalc import *
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
    p0 = Point(msg.x, msg.y)
    error = ec.calculateError(p0)

    #look for common camera coverage areas:

    if(lookforToError and currentCam != msg.heading):
        #calculte camera adjumstment difference
        errorDifference = (fromError - error)/30
        lookforToError=False

    if(msg.heading!=currentCam and timeoutCam==False):
        #found new camera
        currentCam= msg.heading
        timeoutCam= True
        timeoutTime = rospy.get_time()+ rospy.Duration(3, 0).to_sec()
        updateTime = rospy.get_time()+ rospy.Duration(0.1, 0).to_sec()
        iteration = 1
        fromError = error
        lookforToError = True
    if(rospy.get_time() > timeoutTime):
        #three seconds pass, should not  be in area where 2 cameras look
        timeoutCam = False
    if(msg.heading==currentCam):
        if(timeoutCam and rospy.get_time() > updateTime):
            #calculate camera adjustment difference one time step
            updateTime = rospy.get_time()+ rospy.Duration(0.1, 0).to_sec()
            iteration= iteration+1

        # publishing only one camera
        error = error  -errorDifference*iteration
        rospy.loginfo("error is: %s", error)
        rospy.loginfo(rospy.get_caller_id() + "I heard x: %s and y: %s, and heading: %s", msg.x, msg.y, msg.heading)
        pub.publish(error)


def listener():
    rospy.init_node('errorCalc', anonymous=True)
    rospy.Subscriber('position', Pos, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()

#Command for manually publishing in terminal
#rostopic pub -1 /position gulliviewServer/Pos "x: 60
#y: 20
#heading: 0"
