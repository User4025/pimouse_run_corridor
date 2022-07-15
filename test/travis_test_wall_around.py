#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time

class WallAroundTest(unittest.TestCase):
    def set_and_get(self,lf,ls,rs,rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" %(rf,rs,ls,lf))

        time.sleep(0.3)

        with open("/dev/rtmotor_raw_l0","r") as lf, open("/dev/rtmotor_raw_r0","r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())

        return left, right

    def test_io(self):
        left, right = self.set_and_get(100,0,0,0) #total: 600
        self.assertTrue(left > right, "don't curve right")

        left, right = self.set_and_get(0,0,1000,0) #total: 49
        self.assertTrue(left < right, "don't curve left")

        left, right = self.set_and_get(0,50,0,0) #total: 49
        self.assertTrue(left > right, "don't curve to right left_side")

        left, right = self.set_and_get(0,2,0,0) #total: 50
        self.assertTrue(left < right, "don't curve left left_side")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_wall_around')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_around',WallAroundTest)
