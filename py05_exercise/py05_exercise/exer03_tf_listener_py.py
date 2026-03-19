#从 TF 里查目标相对位置，再把这个相对位置变成速度指令

import math
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class TurtleFrameListener(Node):

    def __init__(self):
        super().__init__('turtle_frame_listener_py')

        #声明参数
        self.declare_parameter('target_frame', 'turtle2')
        self.declare_parameter('source_frame', 'turtle1')
        self.declare_parameter('stop_distance', 0.5)
        self.declare_parameter('linear_gain', 0.5)
        self.declare_parameter('angular_gain', 1.0)
        self.declare_parameter('max_linear_speed', 2.0)
        self.declare_parameter('max_angular_speed', 2.0)

        #读取参数
        self.target_frame = self.get_parameter('target_frame').get_parameter_value().string_value
        self.source_frame = self.get_parameter('source_frame').get_parameter_value().string_value
        self.stop_distance=self.get_parameter('stop_distance').value
        self.linear_gain=self.get_parameter('linear_gain').value
        self.angular_gain=self.get_parameter('angular_gain').value
        self.stop_distance = self.get_parameter('stop_distance').value
        self.max_linear_speed = self.get_parameter('max_linear_speed').value
        self.max_angular_speed = self.get_parameter('max_angular_speed').value

        
        self.tf_buffer = Buffer()
        # 创建tf监听器；
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.publisher = self.create_publisher(Twist, self.target_frame + '/cmd_vel', 1)

        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        
        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                now)
        except TransformException as ex:
            self.get_logger().info(
                '%s 到 %s 坐标变换异常！' % (self.source_frame,self.target_frame))
            return

        #turtle2的速度指令

        #（x,y)目标在当前乌龟坐标系下的位置
        x=trans.transform.translation.x
        y=trans.transform.translation.y

        distance=math.sqrt(x**2+y**2) 
        angle=math.atan2(y,x) #方向角

        msg = Twist()
        
        #停止逻辑
        if distance<self.stop_distance:
            msg.linear.x=0.0
            msg.angular.z=0.0
        else:
            angular_speed=self.angular_gain*angle
            linear_speed=self.linear_gain*distance

            #加速度上限,正常按距离算速度
            msg.linear.x=min(self.max_linear_speed,linear_speed)

            #角速度上限,正常按角度算转向速度
            msg.angular.z=max(-self.max_angular_speed,min(self.max_angular_speed,angular_speed))

        self.publisher.publish(msg)

def main():
    rclpy.init()
    
    node = TurtleFrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

  
    rclpy.shutdown()