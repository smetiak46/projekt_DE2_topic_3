import time
from machine import I2C, Pin

MPU_add = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT0 = 0x43
i2c = I2C(0, sda= Pin(4), scl= Pin(5), freq= 100000)
GYRO_SCALE_MODIFIER_250DEG = 131.0

class MPU_gyro:    
    
    def __init__(self):
        #zobudenie MPU 
        i2c.writeto_mem(MPU_add, PWR_MGMT_1, b'\x00')

    def w_to_degree(self, high, low):
        
        #pridanie zaporneho znamienka pri vypise hodnot
        value = (high << 8) | low
        
        if value > 32767:
            value -= 65536
        return value
    
    def gyro_read(self):
        
        data = i2c.readfrom_mem(MPU_add, GYRO_XOUT0, 6)
        
        x = self.w_to_degree(data[0], data[1])
        y = self.w_to_degree(data[2], data[3])
        z = self.w_to_degree(data[4], data[5])
        
        x_deg = x/GYRO_SCALE_MODIFIER_250DEG
        y_deg = y/GYRO_SCALE_MODIFIER_250DEG
        z_deg = z/GYRO_SCALE_MODIFIER_250DEG
        
        return x_deg, y_deg, z_deg
        
mpu_gyro = MPU_gyro()

while True:
    
    x_deg, y_deg, z_deg = mpu_gyro.gyro_read()
    
    print("X:", x_deg, "degree")
    print("Y:", y_deg, "degree" )
    print("Z:", z_deg, "degree")
    print("---------")
    time.sleep(1)

