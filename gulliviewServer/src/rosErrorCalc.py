#!/usr/bin/env python
import rospy
from gulliviewServer.msg import *
import errorCalc

queue = errorCalc.createQueuePath()
p1 = queue.get()
p2 = queue.get()
queue.put(p1)
queue.put(p2)
pub = rospy.Publisher('error', Num, queue_size=10)

def callback(msg):
    global p1
    global p2
    global queue
    global pub

    rospy.loginfo(rospy.get_caller_id() + "I heard x: %s and y: %s", msg.x, msg.y)
    p0 = errorCalc.Point(msg.x, msg.y)
    if errorCalc.isAboveEnd(p1,p2,p0):
        rospy.loginfo("changing line")
        queue.put(p1)
        p1=p2
        p2=queue.get()
    error = errorCalc.calculateError(p1,p2,p0)
    rospy.loginfo("error is: %s", error)
    #TODO: maybe change so that Num.msg is a float
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
