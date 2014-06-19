import time

from RPi import GPIO as gpio

from actors.redbot_motor_actor import RedbotMotorActor
from interfaces.spi.mcp3008_spi_interface import MCP3008SpiInterface
from sensors.redbot_wheel_encoder_sensor import RedbotWheelEncoderSensor
from sensors.sharp_ir_distance_sensor import SharpIrDistanceSensor


def check_motors_and_encoders(spi):
    print 'Checking motors and encoders...'
    lmotor = RedbotMotorActor(gpio, 8, 10, 12)
    rmotor = RedbotMotorActor(gpio, 11, 13, 15)
    wencoder = RedbotWheelEncoderSensor(spi)

    print 'Number of left wheel ticks: %s' % wencoder.getLeftWheelTicks()
    print 'NUmber of right wheel ticks: %s' % wencoder.getRightWheelTicks()
    print 'Let\'s workout a bit'

    lmotor.start()
    lmotor.setPower(0.2)

    rmotor.start()
    rmotor.setPower(0.2)

    time.sleep(1)

    lmotor.stop()
    rmotor.stop()

    print 'Number of left wheel ticks: %s' % wencoder.getLeftWheelTicks()
    print 'Number of right wheel ticks: %s' % wencoder.getRightWheelTicks()
    print '\n'


def check_distance_sensors(spi):
    print 'Checking distance sensors...'
    fsensor = SharpIrDistanceSensor(spi, 3)
    lsensor = SharpIrDistanceSensor(spi, 4)
    rsensor = SharpIrDistanceSensor(spi, 5)

    print 'Front sensor distance: %s' % fsensor.readDistance()
    print 'Left sensor distance: %s' % lsensor.readDistance()
    print 'Right sensor distance: %s' % rsensor.readDistance()


def main():
    gpio.setmode(gpio.BOARD)

    spi = MCP3008SpiInterface(0)
    check_motors_and_encoders(spi)
    check_distance_sensors(spi)

    gpio.cleanup()


if __name__ == '__main__':
    main()
