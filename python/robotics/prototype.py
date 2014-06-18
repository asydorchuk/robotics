import time

from RPi import GPIO as gpio

from actors.redbot_motor_actor import RedbotMotorActor
from sensors.redbot_wheel_encoder_sensor import RedbotWheelEncoderSensor


def main():
  gpio.setmode(gpio.BOARD)
  lmotor = RedbotMotorActor(gpio, 8, 10, 12)
  wencoder = RedbotWheelEncoderSensor()

  print 'Number of left wheel ticks: %s' % wencoder.getLeftWheelTicks()
  print 'Let\'s workout a bit'

  lmotor.start()
  lmotor.setPower(0.2)
  time.sleep(1)
  lmotor.stop()

  print 'Number of left wheel ticks: %s' % wencoder.getLeftWheelTicks()

if __name__ == '__main__':
  main()
