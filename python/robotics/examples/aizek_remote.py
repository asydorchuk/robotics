from robotics.robots.factory import RobotFactory
from robotics.robots.aizek_proxy import AizekProxy
from robotics.zmq import zmq_server


def main():
    robot = RobotFactory.createAizekRobot()
    robot.start()
    proxy = AizekProxy(robot)
    zmq_server.run_zmq_server(proxy)
    robot.stop()
 
if __name__ == '__main__':
    main()
