#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient


from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped


from tf_transformations import quaternion_from_euler

class AutomatedPatroller(Node):
    def __init__(self):
        super().__init__('automated_patroller')
        
        
        self._action_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')

    def send_waypoints(self):
        self.get_logger().info('Waiting for Nav2 Action Server to wake up...')
        self._action_client.wait_for_server()

        goal_msg = FollowWaypoints.Goal()
        
        def create_pose(x, y, yaw):
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.stamp = self.get_clock().now().to_msg()
            
            pose.pose.position.x = float(x)
            pose.pose.position.y = float(y)
            pose.pose.position.z = 0.0

            q = quaternion_from_euler(0.0, 0.0, yaw)
            pose.pose.orientation.x = q[0]
            pose.pose.orientation.y = q[1]
            pose.pose.orientation.z = q[2]
            pose.pose.orientation.w = q[3]
            
            return pose

        waypoint1 = create_pose(3.5, 2.0, 0.0)      
        waypoint2 = create_pose(-0.5, 2.0, 1.57)    
        waypoint3 = create_pose(0.0, 0.0, -1.57)    

        goal_msg.poses = [waypoint1, waypoint2, waypoint3]

        self.get_logger().info('Dispatching robot to waypoints...')
        
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Nav2 rejected the patrol route!')
            return

        self.get_logger().info('Patrol route accepted! Robot is on the move.')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        current_wp = feedback.current_waypoint + 1
        self.get_logger().info(f'Navigating to Waypoint {current_wp}...')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('All Waypoints Reached! Patrol Complete!')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    patroller = AutomatedPatroller()
    
    patroller.send_waypoints()
    
    rclpy.spin(patroller)

if __name__ == '__main__':
    main()  