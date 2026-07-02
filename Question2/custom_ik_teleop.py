#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class CustomIKExecutor(Node):
    def __init__(self):
        super().__init__('custom_ik_executor')
      
        self.publisher_ = self.create_publisher(
            JointTrajectory, 
            '/arm_controller/joint_trajectory', 
            10
        )
        
        self.timer = self.create_timer(2.0, self.publish_trajectory)
        self.trajectory_sent = False

    def publish_trajectory(self):
        if self.trajectory_sent:
            return

        msg = JointTrajectory()
        
        msg.joint_names = [
            'shoulder_pan_joint', 
            'shoulder_lift_joint', 
            'elbow_joint', 
            'wrist_joint'
        ]

        point = JointTrajectoryPoint()
        target_angles = [1.57, 0.5, -1.5, -1.0]
        
        point.positions = target_angles
        
        point.time_from_start = Duration(sec=3, nanosec=0)
        
        msg.points = [point]

        self.get_logger().info(f'Bypassing MoveIt! Executing manual IK angles: {target_angles}')
        self.publisher_.publish(msg)
        
        self.trajectory_sent = True
        self.get_logger().info('Trajectory published successfully.')

def main(args=None):
    rclpy.init(args=args)
    node = CustomIKExecutor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()