import time

from RPi import GPIO as gpio

from actors.redbot_motor_actor import RedbotMotorActor
from sensors.redbot_wheel_encoder_sensor import RedbotWheelEncoderSensor


def main():
  gpio.setmode(gpio.BOARD)
  lmotor = RedbotMotorActor(gpio, 8, 10, 12)
  lmotor.start()
  lmotor.setPower(0.2)
  time.sleep(1)
  lmotor.stop()

if __name__ == '__main__':
  main()
