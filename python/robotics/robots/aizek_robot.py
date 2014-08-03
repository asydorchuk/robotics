import math


class AizekRobot(object):
    '''Aizek is the first generation differential wheel robot.

    The class implements software interface over robot's hardware.

    Example usage:
        robot = AizekRobot()
        robot.start()
        robot.setControl(0.6, 0.6)
        time.sleep(0.5)
        robot.stop()
    '''

    def __init__(self, left_motor, right_motor, wheel_encoder,
                 left_distance_sensor, front_distance_sensor,
                 right_distance_sensor, wheel_radius, wheel_distance):
        """Setup hardware interfaces."""
        self.lmotor = left_motor
        self.rmotor = right_motor
        self.wencoder = wheel_encoder
        self.lsensor = left_distance_sensor
        self.fsensor = front_distance_sensor
        self.rsensor = right_distance_sensor
        self.R = wheel_radius
        self.L = wheel_distance

        self.prev_lradians = self.wencoder.getLeftWheelRadiansTotal()
        self.prev_rradians = self.wencoder.getRightWheelRadiansTotal()
        self.pos_x, self.pos_y, self.phi = 0.0, 0.0, 0.0
        self.lmotor_power, self.rmotor_power = 0.0, 0.0

    def resetPosition(self):
        """Reset robot position to origin."""
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.phi = phi

    def setPosition(self, x, y, phi):
        """Set robot position.

        Args:
            x: x coordinate of the goal (in meters).
            y: y coordinate of the goal (in meters).
            phi: robot direction in the goal position (in radians).
        """
        self.pos_x = x
        self.pos_y = y
        self.phi = phi

    def setGoal(self, x, y, phi):
        """Set robot position relative to the goal position.

        Args:
            x: x coordinate of the goal (in meters).
            y: y coordinate of the goal (in meters).
            phi: robot direction in the goal position (in radians).
        """
        self.pos_x = -x
        self.pos_y = -y
        self.phi = -phi

    def normalizeAngle(self, angle):
        """Normalize the angle within the [-Pi, Pi] range.
   
        Args:
            angle: angle to be normalized (in radians).
        Returns:
            Normalized angle.
        """
        angle %= 2.0 * math.pi
        if angle > math.pi:
            angle -= 2.0 * math.pi
        if angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def updatePosition(self, dlradians, drradians):
        """Update the robot position according to the travelled distance.

        Args:
            dlradians: distance in radians travelled by the left wheel.
            drradians: distance in radians travelled by the right wheel.
        """
        if dlradians == 0.0 and drradians == 0.0:
            return

        distance = self.R * 0.5 * (drradians + dlradians)
        dphi = self.R / self.L * (drradians - dlradians)
        delta = abs(drradians) - abs(dlradians)

        if delta > 0.0:
            radius = abs(distance / dphi)
            circle_x = self.pos_x - radius * math.sin(self.phi)
            circle_y = self.pos_y + radius * math.cos(self.phi)
            circle_phi = self.normalizeAngle(1.5 * math.pi + self.phi + dphi)

            self.pos_x = circle_x + radius * math.cos(circle_phi)
            self.pos_y = circle_y + radius * math.sin(circle_phi)
            self.phi = self.normalizeAngle(self.phi + dphi)
        elif delta < 0.0:
            radius = abs(distance / dphi)
            circle_x = self.pos_x + radius * math.sin(self.phi)
            circle_y = self.pos_y - radius * math.cos(self.phi)
            circle_phi = self.normalizeAngle(0.5 * math.pi + self.phi + dphi)

            self.pos_x = circle_x + radius * math.cos(circle_phi)
            self.pos_y = circle_y + radius * math.sin(circle_phi)
            self.phi = self.normalizeAngle(self.phi + dphi)
        else:
            self.pos_x += distance * math.cos(self.phi)
            self.pos_y += distance * math.sin(self.phi)
            self.phi = self.normalizeAngle(self.phi + dphi)

    def start(self):
        """Start the robot motors."""
        self.lmotor_power = 0.0
        self.lmotor.start()
        self.rmotor_power = 0.0
        self.rmotor.start()

    def stop(self):
        """Stop the robot motors."""
        self.lmotor_power = 0.0
        self.lmotor.stop()
        self.rmotor_power = 0.0
        self.rmotor.stop()

    def setControl(self, lmotor_power, rmotor_power):
        """Set power supplied onto robot motors.

        Args:
           lmotor_power: power to be set on left motor (from range [0, 1]).
           rmotor_power: power to be set on right motor (from range [0, 1]).
        """
        self.lmotor_power = lmotor_power
        self.lmotor.setPower(lmotor_power)
        self.rmotor_power = rmotor_power
        self.rmotor.setPower(rmotor_power)

    def readVelocitySensors(self):
        """Read distance travelled by the wheels since the last measurement.

        Returns:
            tuple, that contains distance travelled by the left and right
                wheel respectively (in radians).
        """
        lradians = self.wencoder.getLeftWheelRadiansTotal()
        rradians = self.wencoder.getRightWheelRadiansTotal()

        dlradians = lradians - self.prev_lradians
        if self.lmotor_power < 0.0:
            dlradians = -dlradians
        drradians = rradians - self.prev_rradians
        if self.rmotor_power < 0.0:
            drradians = -drradians

        self.prev_lradians = lradians
        self.prev_rradians = rradians

        data = (dlradians, drradians)
        return data

    def readDistanceSensors(self):
        """Read measurements from the distance sensors.

        Returns:
            tuple, that contains distance from the left, front and right
                distance sensors respectively (in meters).
        """
        data = (
            self.lsensor.readDistance(),
            self.fsensor.readDistance(),
            self.rsensor.readDistance(),
        )
        return data
