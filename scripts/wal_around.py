#!/usr/bin/env python
import rospy,copy,math
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallAround():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self,messages):
        self.sensor_values = messages

    def run(self):
        rate = rospy.Rate(20)
        data = Twist()

        data.linear.x = 0.3
        data.angular.z = 0.0
        while not rospy.is_shutdown():
            s = self.sensor_values
            
            if s.left_forward > 50 or s.right_forward > 50:
                data.angular.z = - math.pi
            elif s.right_side > 50: data.angular.z = math.pi
            elif s.left_side > 50: data.angular.z = - math.pi
            else:
                error = 50 - s.left_side
                data.angular.z = error * math.pi / 180.0

            self.cmd_vel.publish(data)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('wall_around')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()
    WallAround().run()
