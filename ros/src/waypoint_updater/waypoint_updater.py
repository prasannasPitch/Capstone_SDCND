#!/usr/bin/env python
from std_msgs.msg import Int32
import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint
import numpy as np
import math
from scipy.spatial import KDTree

'''
This node will publish waypoints from the car's current position. This node follows
the method suggested in walkthrough.
'''

LOOKAHEAD_WPS = 35
MAX_DECEL = 0.2

class WaypointUpdater(object):
	
	def __init__(self):
		rospy.init_node('waypoint_updater')

		self.pose = None
		self.base_waypoints = None
		self.waypoints_2d = None
		self.waypoint_tree = None
		self.stopline_wp_idx = -1

		#subcribers
		rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
		rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
		rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)
		
		#publishers
		self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)
	

		self.loop()
	
	def loop(self):
		rate = rospy.Rate(50)
		while not rospy.is_shutdown():
			if self.pose and self.base_waypoints:
				closest_waypoint_idx = self.get_closest_waypoint_id()
				self.publish_waypoints(closest_waypoint_idx)
			rate.sleep()

	def get_closest_waypoint_id(self):
		x = self.pose.pose.position.x
		y = self.pose.pose.position.y
		closest_idx = self.waypoint_tree.query([x,y],1)[1]

		# Check if the way_point is ahead or behind
		closest_coord = self.waypoints_2d[closest_idx]
		prev_coord = self.waypoints_2d[closest_idx-1]

		cl_vec = np.array(closest_coord)
		prev_vec = np.array(prev_coord)
		pos_vec = np.array([x,y])
		value = np.dot((cl_vec-prev_vec),(pos_vec - cl_vec))
		if value > 0:
			closest_idx = (closest_idx+1)% len(self.waypoints_2d)
		return closest_idx

	def publish_waypoints(self,closest_idx):
		lane = Lane()
		lane.header = self.base_waypoints.header
		farthest_idx = closest_idx + LOOKAHEAD_WPS
		base_waypoints = self.base_waypoints.waypoints[closest_idx:farthest_idx]

		if self.stopline_wp_idx == -1 or (self.stopline_wp_idx >= farthest_idx):
			lane.waypoints = base_waypoints
		else:
			lane.waypoints = self.decelerate_waypoints(base_waypoints, closest_idx)

		self.final_waypoints_pub.publish(lane)

	def decelerate_waypoints(self, waypoints, closest_idx):
		temp = []

		for i, wp in enumerate(waypoints):
			p = Waypoint()
			p.pose = wp.pose
			stop_idx = max(self.stopline_wp_idx - closest_idx - 3, 0)
			dist = self.distance(waypoints, i, stop_idx)
			vel = math.sqrt(MAX_DECEL * dist)
			if vel < 1.5:
				vel = 0.
			p.twist.twist.linear.x = min(vel, wp.twist.twist.linear.x)
			temp.append(p)

		return temp

	def pose_cb(self, msg):
		self.pose = msg


	def waypoints_cb(self, waypoints):
		self.base_waypoints = waypoints
		if not self.waypoints_2d:
			self.waypoints_2d = [[waypoint.pose.pose.position.x,waypoint.pose.pose.position.y] for waypoint in waypoints.waypoints]
			self.waypoint_tree = KDTree(self.waypoints_2d)

	def traffic_cb(self, msg):
		self.stopline_wp_idx = msg.data

	def obstacle_cb(self, msg):
		# TODO: Callback for /obstacle_waypoint message. We will implement it later
		pass

	def get_waypoint_velocity(self, waypoint):
		return waypoint.twist.twist.linear.x

	def set_waypoint_velocity(self, waypoints, waypoint, velocity):
		waypoints[waypoint].twist.twist.linear.x = velocity

	def distance(self, waypoints, wp1, wp2):
		dist = 0
		dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
		for i in range(wp1, wp2+1):
			dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
			wp1 = i
		return dist


if __name__ == '__main__':
	try:
		WaypointUpdater()
	except rospy.ROSInterruptException:
		rospy.logerr('Could not start waypoint updater node.')
