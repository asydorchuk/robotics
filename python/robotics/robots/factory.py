from RPi import GPIO as gpio

from robotics.actors.redbot_motor_actor import RedbotMotorActor
from robotics.interfaces.spi.mcp3008_spi_interface import MCP3008SpiInterface
from robotics.robots.aizek_robot import AizekRobot
from robotics.sensors.redbot_wheel_encoder_sensor import RedbotWheelEncoderSensor
from robotics.sensors.sharp_ir_distance_sensor import SharpIrDistanceSensor


class RobotFactory(object):

    @staticmethod
    def createAizekRobot():
        gpio.setmode(gpio.BOARD)
        lmotor = RedbotMotorActor(gpio, 8, 10, 12)
        rmotor = RedbotMotorActor(gpio, 11, 13, 15)

        spi = MCP3008SpiInterface(0)
        wencoder = RedbotWheelEncoderSensor(spi)
        lsensor = SharpIrDistanceSensor(spi, 5)
        fsensor = SharpIrDistanceSensor(spi, 4)
        rsensor = SharpIrDistanceSensor(spi, 3)

        wheel_radius = 0.032
        wheel_distance = 0.1

        robot = AizekRobot(
            left_motor=lmotor,
            right_motor=rmotor,
            wheel_encoder=wencoder,
            left_distance_sensor=lsensor,
            front_distance_sensor=fsensor,
            right_distance_sensor=rsensor,
            wheel_radius=wheel_radius,
            wheel_distance=wheel_distance,
        )
        return robot
