#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math

class Follower:
    def __init__(self):
        rospy.init_node('follower')
        self.velocity_publisher = rospy.Publisher('/follower/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/leader/odom', Odometry, self.update_leader_position)

        self.leader_x = 0.0
        self.leader_y = 0.0
        self.leader_yaw = 0.0
        self.follow_distance = 0.5  # meters

    def update_leader_position(self, data):
        pos = data.pose.pose.position
        ori = data.pose.pose.orientation
        self.leader_x = pos.x
        self.leader_y = pos.y
        _, _, self.leader_yaw = euler_from_quaternion([ori.x, ori.y, ori.z, ori.w])

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            twist = Twist()
            distance = math.sqrt((self.leader_x)**2 + (self.leader_y)**2)
            angle_to_leader = math.atan2(self.leader_y, self.leader_x)

            # Calculate the angle difference
            angle_diff = self.leader_yaw - angle_to_leader

            if distance > self.follow_distance:
                twist.linear.x = 0.2
                twist.angular.z = -angle_diff * 2  # Proportional controller for orientation

            self.velocity_publisher.publish(twist)
            rate.sleep()

if __name__ == '__main__':
    follower = Follower()
    follower.run()
