import math
import time

from robotics.robots.aizek_robot import AizekRobot
from robotics.controllers.pid_controller import PIDController


def uni_to_diff(v, w):
    R = 0.032
    L = 0.1
    vel_l = (2.0 * v - L * w) / (2.0 * R)
    vel_r = (2.0 * v + L * w) / (2.0 * R)
    return vel_l, vel_r


def uni_to_power(v, w):
    MX = 0.5
    MN = 0.4
    if v == 0.0:
        if w > 0.0:
            power_l = -MX
            power_r = MX
        else:
            power_l = MX
            power_r = -MX
    elif v > 0.0:
        if w == 0.0:
            power_l = MX
            power_r = MX
        elif w > 0.0:
            power_l = MN
            power_r = MX
        else:
            power_l = MX
            power_r = MN
    else:
        raise NotImplementedError
    return power_l, power_r


def main():
    # 0.2, 0.004, 0.01
    controller = PIDController(0.2, 0.005, 0.01)
    robot = AizekRobot()
    robot.start()

    robot.setGoal(0.0, 0.0, 0.75 * math.pi)
    prev_time = time.time()
    while abs(robot.phi) > 0.01 * math.pi:
        dlradians, drradians = robot.readVelocitySensors()
        robot.updatePosition(dlradians, drradians)
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time
        target_linear_velocity = 0.0
        target_angular_velocity = -robot.phi
        #target_angular_velocity = controller.step(-robot.phi, dt, 0.05)
        vel_l, vel_r = uni_to_power(target_linear_velocity, target_angular_velocity)
        print 'dt %s, robot phi %s' % (dt, robot.phi)
        print 'vel_l %s, vel_r %s' % (vel_l, vel_r)
        robot.setControl(vel_l, vel_r)
        time.sleep(0.1)

    robot.stop()
    print 'Robot x: %s, y: %s, phi: %s' % (robot.pos_x, robot.pos_y, robot.phi)


if __name__ == '__main__':
    main()
