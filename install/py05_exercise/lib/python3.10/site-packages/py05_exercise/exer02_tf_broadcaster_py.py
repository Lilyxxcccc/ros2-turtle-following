#把乌龟的位姿，转换成 TF 坐标变换
#广播 turtle1 和 turtle2 的坐标关系

from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
import tf_transformations
from turtlesim.msg import Pose

class TurtleFrameBroadcaster(Node):
     
    def __init__(self):
        super().__init__('turtle_frame_broadcaster_py')

        #这个节点通过参数决定监听哪只乌龟
        self.declare_parameter('turtle_name', 'turtle1')
        self.turtlename = self.get_parameter('turtle_name').get_parameter_value().string_value

        #创建TF广播对象
        self.br = TransformBroadcaster(self)

        self.subscription = self.create_subscription(
            Pose,
            self.turtlename+ '/pose',
            self.handle_turtle_pose,
            1)
        self.subscription

    def handle_turtle_pose(self, msg):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtlename

        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        #欧拉角转四元数
        q = tf_transformations.quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.br.sendTransform(t)

def main():
    rclpy.init()
    
    node = TurtleFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    rclpy.shutdown()