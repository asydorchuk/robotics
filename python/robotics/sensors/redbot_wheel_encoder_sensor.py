import math
import threading


class RedbotWheelEncoderThread(threading.Thread):
  # TODO(asydorchuk): extract default pin ids from configuration.
  # TODO(asydorchuk): extract constants to the configuration file.

  _SENSOR_VALUE_DEFAULT = 500.0
  _SENSOR_THRESHOLD_LOW = 300.0
  _SENSOR_THRESHOLD_HIGH = 700.0
  _SENSOR_STATE_UNDEF = 0
  _SENSOR_STATE_LOW = 1
  _SENSOR_STATE_HIGH = 2

  def _pin_state(self, value):
    if value < self._SENSOR_THRESHOLD_LOW:
      return self._SENSOR_STATE_LOW
    if value > self._SENSOR_THRESHOLD_HIGH:
      return self._SENSOR_STATE_HIGH
    return self._SENSOR_STATE_UNDEF

  def __init__(self, spi_interface, ticks, spi_id = 0, lpin_id = 2, rpin_id = 1):
    super(RedbotWheelEncoderThread, self).__init__()
    self.daemon = True
    self.ticks = ticks
    self.lpin_id = lpin_id
    self.rpin_id = rpin_id
    self.lpin_value = self._SENSOR_VALUE_DEFAULT
    self.rpin_value = self._SENSOR_VALUE_DEFAULT
    self.lpin_state = self._SENSOR_STATE_UNDEF
    self.rpin_state = self._SENSOR_STATE_UNDEF
    self.reader = spi_interface

  def run(self):
    while True:
      lpin_value = self.reader.read(self.lpin_id)
      self.lpin_value = lpin_value * 0.33 + self.lpin_value * 0.67
      lpin_state = self._pin_state(self.lpin_value)
      if lpin_state != self._SENSOR_STATE_UNDEF:
        if self.lpin_state != lpin_state:
          self.ticks[0] += 1
        self.lpin_state = lpin_state

      rpin_value = self.reader.read(self.rpin_id)
      self.rpin_value = rpin_value * 0.33 + self.rpin_value * 0.67
      rpin_state = self._pin_state(self.rpin_value)
      if rpin_state != self._SENSOR_STATE_UNDEF:
        if self.rpin_state != rpin_state:
          self.ticks[1] += 1
        self.rpin_state = rpin_state

      self.ticks[2] += 1

class RedbotWheelEncoderSensor(object):
  # TODO(asydorchuk): move constants to the config file.

  _TICKS_PER_WHEEL_CYCLE = 32

  def __init__(self, spi_interface):
    self.ticks = [0, 0, 0]
    self.ticks_to_radians_factor = 2.0 * math.pi / self._TICKS_PER_WHEEL_CYCLE
    worker = RedbotWheelEncoderThread(spi_interface, self.ticks)
    worker.start()    

  def getLeftWheelTicksTotal(self):
    return self.ticks[0]

  def getLeftWheelRadiansTotal(self):
    return self.ticks[0] * self.ticks_to_radians_factor

  def getRightWheelTicksTotal(self):
    return self.ticks[1]

  def getRightWheelRadiansTotal(self):
    return self.ticks[1] * self.ticks_to_radians_factor

  def getMeasurmentsCount(self):
    return self.ticks[2]
