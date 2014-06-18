class RedbotMotorActor(object):
    # TODO(asydorchuk): load constants from the config file.
    
    _MAXIMUM_FREQUENCY = 128

    def __init__(self, gpio, power_pin, direction_pin_1, direction_pin_2):
        self.gpio = gpio
        self.power_pin = power_pin
        self.direction_pin_1 = direction_pin_1
        self.direction_pin_2 = direction_pin_2

        self.gpio.setup(power_pin, self.gpio.OUT)
        self.gpio.setup(direction_pin_1, self.gpio.OUT)
        self.gpio.setup(direction_pin_2, self.gpio.OUT)

        self.motor_controller = self.gpio.PWM(
            self.power_pin, self._MAXIMUM_FREQUENCY)

    def _setDirectionForward(self):
        self.gpio.output(self.direction_pin_1, True)
        self.gpio.output(self.direction_pin_2, False)

    def _setDirectionBackward(self):
        self.gpio.output(self.direction_pin_1, False)
        self.gpio.output(self.direction_pin_2, True)

    def start(self):
        self.gpio.output(self.direction_pin_1, False)
        self.gpio.output(self.direction_pin_2, False)
        self.motor_controller.start(0.0)
        self.relative_power = 0.0

    def stop(self):
        self.gpio.output(self.direction_pin_1, False)
        self.gpio.output(self.direction_pin_2, False)
        self.motor_controller.stop()
        self.relative_power = 0.0

    def setPower(self, relative_power):
        if relative_power < 0:
            self._setDirectionBackward()
        else:
            self._setDirectionForward()
        self.motor_controller.ChangeDutyCycle(100.0 * abs(relative_power))
        self.relative_power = relative_power
