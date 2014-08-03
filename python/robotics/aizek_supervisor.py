import logging
import math
import time

from robotics.controllers.pid_controller import PIDController
from robotics.robots.factory import RobotFactory


def uni_to_diff(v, w):
    R = 0.032
    L = 0.1
    vel_l = (2.0 * v - L * w) / (2.0 * R)
    vel_r = (2.0 * v + L * w) / (2.0 * R)
    return vel_l, vel_r


def uni_to_power(v, w):
    MX = 0.3
    MN = 0.4
    if v == 0.0:
        if w > 0.0:
            power_l = 0.0
            power_r = MX
        else:
            power_l = MX
            power_r = 0.0
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
    robot = RobotFactory.createAizekRobot()
    robot.start()

    robot.setPosition(0.0, 0.0, 0.0)
    prev_time = time.time()
    target_x = 0.5
    target_y = 0.5

    while True:
        ldistance, fdistance, rdistance = robot.readDistanceSensors()
        print 'Distance l: %s, f: %s, r: %s' % (ldistance, fdistance, rdistance)

        dlradians, drradians = robot.readVelocitySensors()
        robot.updatePosition(dlradians, drradians)
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        dx = target_x - robot.pos_x
        dy = target_y - robot.pos_y
        if abs(dx) < 0.02 and abs(dy) < 0.02:
            print 'Goal reached...'
            break

        dphi = math.atan2(dy, dx) - robot.phi
        if dphi > math.pi:
            dphi -= 2 * math.pi
        if dphi < -math.pi:
            dphi += 2 * math.pi
        print 'x: %s, y: %s, phi: %s' % (robot.pos_x, robot.pos_y, robot.phi)
        print 'dx: %s, dy: %s, dphi: %s' % (dx, dy, dphi)

        if abs(dphi) < 0.06 * math.pi:
            robot.setControl(0.25, 0.25)
        else:
            if dphi > 0.0:
                robot.setControl(0.0, 0.25)
            else:
                robot.setControl(0.25, 0.0)

        time.sleep(0.1)

    robot.stop()
    print 'Robot x: %s, y: %s, phi: %s' % (robot.pos_x, robot.pos_y, robot.phi)


if __name__ == '__main__':
    main()
