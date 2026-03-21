#请求turtlesim在某个位置生成叫turtle2的新乌龟

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn

class TurtleSpawnClient(Node):

    def __init__(self):
        super().__init__('turtle_spawn_client_py')

        #声明并获取参数
        self.x = self.declare_parameter("x",2.0) #新乌龟x坐标
        self.y = self.declare_parameter("y",2.0)
        self.theta = self.declare_parameter("theta",0.0) #新乌龟朝向角
        self.turtle_name = self.declare_parameter("turtle_name","turtle2") #新乌龟名字

        #创建客户端对象，用来连接/spawn服务
        self.cli=self.create_client(Spawn,'/spawn')

        #等待服务连接；
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('服务连接中，请稍候...')

        #创建一个服务请求对象
        self.req = Spawn.Request()

    def send_request(self):

        #把参数值填入请求对象中

        #把参数 x 填到 self.req.x
        self.req.x = self.get_parameter("x").get_parameter_value().double_value
        
        self.req.y = self.get_parameter("y").get_parameter_value().double_value
        
        self.req.theta = self.get_parameter("theta").get_parameter_value().double_value
        
        self.req.name = self.get_parameter("turtle_name").get_parameter_value().string_value

        self.future = self.cli.call_async(self.req)

def main():
    rclpy.init()
    client=TurtleSpawnClient()
    client.send_request()

    #让节点保持运行，直到服务响应回来
    rclpy.spin_until_future_complete(client,client.future)
    try:
        response = client.future.result()
    except Exception as e:
        client.get_logger().info(
            '服务请求失败： %r' % e)
    else:
        if len(response.name) == 0:
            client.get_logger().info(
                '乌龟重名了，创建失败！')
        else:
            client.get_logger().info(
                '乌龟%s被创建' % response.name)
            
    rclpy.shutdown()

if __name__ == '__main__':
    main()
