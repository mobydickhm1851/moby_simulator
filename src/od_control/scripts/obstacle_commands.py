#!/usr/bin/env python

# 2018 11 13 LiuYC SOLab
# Add the command to control moving obstacle

import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import sys, select, termios, tty
import numpy as np
import time


flag_move = 0

obsParam = {
        'f':(0.5), # diff increase 0.5 meter
        'd':(-0.5), # diff decrease 0.5 meter
        's':(0.2), # speed up * 1.2 
        'a':(0.2), # slow down * 1.2
           }

pub_rate = 100 # publish rate in Hz
speed = 10 # normal speed
diff = 2 # from -1 to 1, the moving range of obstacle

'''

# this is the teleop getkey function for turtlebot
def getKey():

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

'''


def getKeyUnix():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


# For now, only movement in y direction is set
def set_y_pose():

    # pub_x_joint_position = rospy.Publisher('/obs1/obs1_x_joint_controller/command', Float64, queue_size=1)
    # pode_x = data.linear.x
    # pub_x_joint_position.publish(throttle)
   
    pub_y_joint_position = rospy.Publisher('/obs1/obs1_y_joint_controller/command', Float64, queue_size=1)
    rospy.init_node('obstacle_commands', anonymous=True)	
    rate = rospy.Rate(pub_rate) # default is 100
    
    while not rospy.is_shutdown():
        i =10 * time.time() # time_stamp
        
	pose_y = np.sin( i / pub_rate * speed ) * diff
	
	# rospy.loginfo(str): write to screen, node's log file and rosout
        rospy.loginfo(pose_y)
        pub_y_joint_position.publish(pose_y)
        rate.sleep()

if __name__ == '__main__':
    # part of getKeyUnix input
    settings = termios.tcgetattr(sys.stdin)
    try:
        set_y_pose()
    except rospy.ROSInterruptException:
        pass
    
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

