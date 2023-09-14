from bmp280 import BMP280
import smbus2

class I2C:
    def __init__(self):
        self.bus = smbus2.SMBus(1) # 1 para Raspberry Pi 3
        self.bmp280 = BMP280(i2c_dev=self.bus)

    def get_temperatura(self):
        temperatura = self.bmp280.get_temperature()
        return round(temperatura, 2)