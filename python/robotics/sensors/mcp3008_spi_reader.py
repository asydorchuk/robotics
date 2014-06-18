import spidev


class MCP3008SpiReader(object):

  def __init__(self, device_id):
    self.device = spidev.SpiDev()
    self.device.open(0, device_id)
    self.device.max_speed_hz = 1000000

  def read(self, adc_id):
    raw_data = self.device.xfer2([1, 8 + adc_id << 4, 0])
    adc_out = ((raw_data[1] & 3) << 8) + raw_data[2] 
    return adc_out
