#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

import actionlib
import actionlib_msgs.msg
import rospy
from sound_play.msg import SoundRequest
from sound_play.msg import SoundRequestAction
from sound_play.msg import SoundRequestGoal


if __name__ == '__main__':
    rospy.init_node("boot_sound")

    actionclient = actionlib.SimpleActionClient(
        '/robotsound_jp',
        SoundRequestAction)
    actionclient.wait_for_server()

    # assuming pr1012, pr1012s, pr1040, pr1040s
    hostname = socket.gethostname()
    robot_id = hostname[4:6]

    msg = SoundRequest()
    msg.sound = SoundRequest.SAY
    msg.command = SoundRequest.PLAY_ONCE
    msg.arg = "{}号機、起動".format(robot_id)
    msg.volume = 1.0

    goal = SoundRequestGoal()
    goal.sound_request = msg
    actionclient.send_goal(goal)
    result = actionclient.wait_for_result()
    while actionclient.get_state() == actionlib_msgs.msg.GoalStatus.ABORTED:
        actionclient.send_goal(goal)
        result = actionclient.wait_for_result()
        rospy.sleep(1.0)
