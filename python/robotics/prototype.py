import time

from RPi import GPIO as gpio

from actors.redbot_motor_actor import RedbotMotorActor
from sensors.redbot_wheel_encoder_sensor import RedbotWheelEncoderSensor


def main():
  gpio.setmode(gpio.BOARD)
  lmotor = RedbotMotorActor(gpio, 8, 10, 12)
  rmotor = RedbotMotorActor(gpio, 11, 13, 15)
  wencoder = RedbotWheelEncoderSensor()

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

  gpio.cleanup()

if __name__ == '__main__':
  main()
