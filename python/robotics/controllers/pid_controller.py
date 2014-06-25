def PIDController(object):

    def __init__(
            self,
            proportional_factor,
            integral_factor,
            derivative_factor):
        self.proportional_factor = proportional_factor
        self.integral_factor = integral_factor
        self.derivative_factor = derivative_factor
        self.accumulated_integral = 0.0
        self.previous_value_delta = 0.0

    def step(self, value_delta, time_delta):
        self.accumulated_integral += value_delta * time_delta
        derivative = (value_delta - self.previous_value_delta) / time_delta
        value = self.proportional_factor * value_delta + \
            self.integral_factor * self.accumulated_integral + \
            self.derivative_factor * derivative
        self.previous_value_delta = value_delta
        return value
