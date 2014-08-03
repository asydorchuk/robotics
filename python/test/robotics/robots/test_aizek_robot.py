import math
import mock
import unittest

from robotics.robots.aizek_robot import AizekRobot


class TestAizekRobot(unittest.TestCase):
    ROBOT_WHEEL_RADIUS = 0.025
    ROBOT_WHEEL_DISTANCE = 0.1

    def setUp(self):
        self.lmotor = mock.Mock()
        self.rmotor = mock.Mock()
        self.wencoder = mock.Mock()
        self.lsensor = mock.Mock()
        self.fsensor = mock.Mock()
        self.rsensor = mock.Mock()
        self.robot = AizekRobot(
            left_motor=self.lmotor,
            right_motor=self.rmotor,
            wheel_encoder=self.wencoder,
            left_distance_sensor=self.lsensor,
            front_distance_sensor=self.fsensor,
            right_distance_sensor=self.rsensor,
            wheel_radius=self.ROBOT_WHEEL_RADIUS,
            wheel_distance=self.ROBOT_WHEEL_DISTANCE, 
        )

    def testUpdatePositionRotationMovement1(self):
        self.robot.updatePosition(-0.5 * math.pi, 0.5 * math.pi)

        self.assertAlmostEqual(0.0, self.robot.pos_x)
        self.assertAlmostEqual(0.0, self.robot.pos_y)
        self.assertAlmostEqual(0.25 * math.pi, self.robot.phi)

    def testUpdatePositionRotationMovement2(self):
        self.robot.updatePosition(0.0, 0.5 * math.pi)
        self.assertAlmostEqual(0.125 * math.pi, self.robot.phi)

        self.robot.updatePosition(0.5 * math.pi, 0.0)
        self.assertAlmostEqual(0.0, self.robot.phi)

    def testUpdatePositionRotationMovement3(self):
        self.robot.updatePosition(0.0, 5 * math.pi)
        self.assertAlmostEqual(-0.75 * math.pi, self.robot.phi)

    def testUpdatePositionRotationMovement4(self):
        self.robot.updatePosition(0.0, 99 * math.pi)
        self.assertAlmostEqual(0.75 * math.pi, self.robot.phi)

        self.robot.updatePosition(104 * math.pi, 0.0)
        self.assertAlmostEqual(0.75 * math.pi, self.robot.phi)

    def testUpdatePositionRotationMovement5(self):
        self.robot.updatePosition(23.75 * math.pi, 23.75 * math.pi)
        self.assertAlmostEqual(0.0, self.robot.phi)

    def testUpdatePositionLinearMovement1(self):
        self.robot.setPosition(0.0, 0.0, 0.25 * math.pi)
        self.robot.updatePosition(math.pi, math.pi)

        self.assertAlmostEqual(0.025 / math.sqrt(2.0) * math.pi, self.robot.pos_x)
        self.assertAlmostEqual(0.025 / math.sqrt(2.0) * math.pi, self.robot.pos_y)
        self.assertAlmostEqual(0.25 * math.pi, self.robot.phi)

        self.robot.updatePosition(2 * math.pi, -2 * math.pi)
        self.robot.updatePosition(math.pi, math.pi)

        self.assertAlmostEqual(0.0, self.robot.pos_x)
        self.assertAlmostEqual(0.0, self.robot.pos_y)
        self.assertAlmostEqual(-0.75 * math.pi, self.robot.phi)

    def testUpdatePositionCurvedMovement1(self):
        self.robot.updatePosition(0.0, 2 * math.pi)

        self.assertAlmostEqual(0.05, self.robot.pos_x)
        self.assertAlmostEqual(0.05, self.robot.pos_y)
        self.assertAlmostEqual(0.5 * math.pi, self.robot.phi)

    def testUpdatePositionCurvedMovement2(self):
        self.robot.updatePosition(0.0, -2 * math.pi)

        self.assertAlmostEqual(-0.05, self.robot.pos_x)
        self.assertAlmostEqual(0.05, self.robot.pos_y)
        self.assertAlmostEqual(-0.5 * math.pi, self.robot.phi)

    def testUpdatePositionCurvedMovement3(self):
        self.robot.updatePosition(2 * math.pi, 0.0)

        self.assertAlmostEqual(0.05, self.robot.pos_x)
        self.assertAlmostEqual(-0.05, self.robot.pos_y)
        self.assertAlmostEqual(-0.5 * math.pi, self.robot.phi)

    def testUpdatePositionCurvedMovement4(self):
        self.robot.updatePosition(-2 * math.pi, 0.0)

        self.assertAlmostEqual(-0.05, self.robot.pos_x)
        self.assertAlmostEqual(-0.05, self.robot.pos_y)
        self.assertAlmostEqual(0.5 * math.pi, self.robot.phi)
