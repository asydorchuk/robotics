class SharpIrDistanceSensor(object):

    def __init__(self, spi_interface, pin_id):
        self.spi_interface = spi_interface
        self.pin_id = pin_id

    def _voltageToMeters(self, voltage):
        return 67.84 / (voltage - 3) - 0.04

    def readDistance(self):
        '''Returns distance in meters.'''
        voltage = self.spi_interface.read(self.pin_id)
        distance = self._voltageToMeters(voltage)
        return distance
