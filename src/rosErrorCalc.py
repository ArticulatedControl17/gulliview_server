#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
from gulliviewserver.msg import *
from errorCalc import *
import rospkg

pub = rospy.Publisher('error', Int64, queue_size=10)
ec = errorCalc()
#ec = errorCalc(rospack.get_path('gulliviewServer')+'src/path.txt')

def callback(msg):
    global pub
    global ec

    rospy.loginfo(rospy.get_caller_id() + "I heard x: %s and y: %s", msg.x, msg.y)
    p0 = Point(msg.x, msg.y)
    error = ec.calculateError(p0)
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
