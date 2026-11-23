
from machine import Pin, I2C
import time
import math
class MPU_ACC:

#I2C initializaion
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
        self.MPU_ADDR = 0x68
        self.i2c.writeto_mem(self.MPU_ADDR, 0x6B, b'\x00')

#Read Func
    def read_raw_data(self, reg):
        data = self.i2c.readfrom_mem(self.MPU_ADDR, reg, 2)
        value = (data[0] << 8) | data[1]

        if value > 32767:
            value -= 65536

        return value
    def read_acc(self):
        
        acc_x = self.read_raw_data(0x3B)
        acc_y = self.read_raw_data(0x3D)
        acc_z = self.read_raw_data(0x3F)

        Ax = (acc_x / 16384.0)*9.81
        Ay = (acc_y / 16384.0)*9.81
        Az = (acc_z / 16384.0)*9.81
        
        return Ax, Ay, Az
    
mpu_acc = MPU_ACC()

#Main
while True:
    Ax, Ay, Az= mpu_acc.read_acc()
    print("ACCELEROMETER (m/s^2)")
    print("X:", Ax)
    print("Y:", Ay)
    print("Z:", Az)
    print("")

    time.sleep(0.5)
