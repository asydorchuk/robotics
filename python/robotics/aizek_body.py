import math

from RPi import GPIO as gpio

from actors.redbot_motor_actor import RedbotMotorActor
from controllers.pid_controller import PIDController
from interfaces.spi.mcp3008_spi_interface import MCP3008SpiInterface
from sensors.redbot_wheel_encoder_sensor import RedbotWheelEncoderSensor
from sensors.sharp_ir_distance_sensor import SharpIrDistanceSensor


def uni_to_diff(v, w):
    R = 0.032
    L = 0.1
    vel_l = (2.0 * v - L * w) / (2.0 * R)
    vel_r = (2.0 * v + L * w) / (2.0 * R)
    return vel_l, vel_r


class AizekBody(object):
    '''Aizek is the first generation differential wheel robot.

    The class implements software interface over robot's hardware.
    '''

    def __init__(self):
        gpio.setmode(gpio.BOARD)

        spi = MCP3008SpiInterface(0)
        self.lmotor = RedbotMotorActor(gpio, 8, 10, 12)
        self.rmotor = RedbotMotorActor(gpio, 11, 13, 15)
        self.wencoder = RedbotWheelEncoderSensor(spi)

        self.lsensor = SharpIrDistanceSensor(spi, 5)
        self.fsensor = SharpIrDistanceSensor(spi, 4)
        self.rsensor = SharpIrDistanceSensor(spi, 3)

        self.prev_lradians, self.prev_rradians = self.readVelocitySensors()
        self.pos_x, self.pos_y, self.phi = 0.0, 0.0, 0.0
        self.lmotor_power, self.rmotor_power = 0.0, 0.0
        self.R = 0.032
        self.L = 0.1

    def setGoal(self, x, y):
        self.pos_x = -x
        self.pos_y = -y

    def updatePosition(self):
        lradians, rradians = self.readVelocitySensors()
        delta_lradians = lradians - self.prev_lradians
        self.prev_lradians = lradians
        if self.lmotor_power < 0.0:
            delta_lradians = -delta_lradians
        delta_rradians = rradians - self.prev_rradians
        self.prev_rradians = rradians
        if self.rmotor_power < 0.0:
            delta_rradians = -delta_rradians
        if delta_lradians == 0.0 and delta_rradians == 0.0:
            return

        distance = self.R * 0.5 * (delta_rradians + delta_lradians)
        delta_phi = self.R / self.L * (delta_rradians - delta_lradians)
        radius = distance / delta_phi

        if delta_phi > 0.0:
            circle_x = self.pos_x - radius * math.sin(self.phi)
            circle_y = self.pos_y + radius * math.cos(self.phi)
            circle_phi = (11.5 * math.pi + self.phi + delta_phi) % (2.0 * math.pi)

            self.pos_x = circle_x + radius * math.cos(circle_phi)
            self.pos_y = circle_y + radius * math.sin(circle_phi)
            self.phi = (12.0 * math.pi + self.phi + delta_phi) % (2.0 * math.pi)
        else:
            circle_x = self.pos_x + radius * math.sin(self.phi)
            circle_y = self.pos_y - radius * math.cos(self.phi)
            circle_phi = (12.5 * math.pi + self.phi - delta_phi) % (2.0 * math.pi)

            self.pos_x = circle_x + radius * math.cos(circle_phi)
            self.pos_y = circle_y + radius * math.sin(circle_phi)
            self.phi = (2.0 * math.pi + self.phi - delta_phi) % (2.0 * math.pi)

    def start(self):
        self.lmotor_power = 0.0
        self.lmotor.start()
        self.rmotor_power = 0.0
        self.rmotor.start()

    def stop(self):
        self.lmotor_power = 0.0
        self.lmotor.stop()
        self.rmotor_power = 0.0
        self.rmotor.stop()

    def setControl(self, lmotor_power, rmotor_power):
        self.lmotor_power = lmotor_power
        self.lmotor.setPower(lmotor_power)
        self.rmotor_power = rmotor_power
        self.rmotor.setPower(rmotor_power)

    def readVelocitySensors(self):
        data = (
            self.wencoder.getLeftWheelRadiansTotal(),
            self.wencoder.getRightWheelRadiansTotal(),
        )
        return data

    def readDistanceSensors(self):
        data = (
            self.lsensor.readDistance(),
            self.fsensor.readDistance(),
            self.rsensor.readDistance(),
        )
        return data


def main():
    #controller = PIDController(0.1, 0.002, 0.005)
    robot = AizekBody()
    robot.start()
    robot.updatePosition()
    robot.stop()


if __name__ == '__main__':
  main()
