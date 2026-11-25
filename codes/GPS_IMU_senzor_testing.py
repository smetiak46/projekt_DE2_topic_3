
import time
from machine import I2C, Pin, UART
from sh1106 import SH1106_I2C


# ==========================================
# I2C INITIALIZATION
# ==========================================

# I2C0 - MPU6050 + OLED 1
i2c = I2C(
    0,
    sda=Pin(4),
    scl=Pin(5),
    freq=100000
)


# ==========================================
# MPU6050 GYROSCOPE
# ==========================================

MPU_add = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT0 = 0x43

GYRO_SCALE_MODIFIER_250DEG = 131.0


class MPU_gyro:

    def __init__(self):
        # Wake up MPU6050
        i2c.writeto_mem(
            MPU_add,
            PWR_MGMT_1,
            b'\x00'
        )

    def w_to_degree(self, high, low):

        value = (high << 8) | low

        # Convert to signed 16-bit value
        if value > 32767:
            value -= 65536

        return value

    def gyro_read(self):

        data = i2c.readfrom_mem(
            MPU_add,
            GYRO_XOUT0,
            6
        )

        x = self.w_to_degree(data[0], data[1])
        y = self.w_to_degree(data[2], data[3])
        z = self.w_to_degree(data[4], data[5])

        x_deg = x / GYRO_SCALE_MODIFIER_250DEG
        y_deg = y / GYRO_SCALE_MODIFIER_250DEG
        z_deg = z / GYRO_SCALE_MODIFIER_250DEG

        return x_deg, y_deg, z_deg


mpu_gyro = MPU_gyro()


# ==========================================
# MPU6050 ACCELEROMETER
# ==========================================

class MPU_ACC:

    def __init__(self):

        self.i2c = i2c
        self.MPU_ADDR = 0x68

    def read_raw_data(self, reg):

        data = self.i2c.readfrom_mem(
            self.MPU_ADDR,
            reg,
            2
        )

        value = (data[0] << 8) | data[1]

        if value > 32767:
            value -= 65536

        return value

    def read_acc(self):

        acc_x = self.read_raw_data(0x3B)
        acc_y = self.read_raw_data(0x3D)
        acc_z = self.read_raw_data(0x3F)

        Ax = (acc_x / 16384.0) * 9.81
        Ay = (acc_y / 16384.0) * 9.81
        Az = (acc_z / 16384.0) * 9.81

        return Ax, Ay, Az


mpu_acc = MPU_ACC()


# ==========================================
# GPS MODULE
# ==========================================

class GPS:

    def __init__(self, TX, RX):

        self.gps = UART(
            0,
            baudrate=9600,
            tx=TX,
            rx=RX
        )

    def print_data(self):

        data = self.gps.readline()

        if data:
            print(data.strip())

    def print_coords(self):

        data = self.gps.readline()

        if not data:
            return None

        try:

            data = data.decode(
                "ascii",
                "ignore"
            ).strip()

            data_split = data.split(",")

            if data_split[0] not in ("$GPGGA", "$GNGGA"):
                return None

            if len(data_split) < 7:
                return None

            # Check GPS fix
            if data_split[6] == "0":
                return None

            latitude = data_split[2]
            latitude_dir = data_split[3]

            longitude = data_split[4]
            longitude_dir = data_split[5]

            if not latitude or not longitude:
                return None

            latitude = self.convert_coords(
                latitude,
                latitude_dir
            )

            longitude = self.convert_coords(
                longitude,
                longitude_dir
            )

            return latitude, longitude

        except (ValueError, IndexError):
            return None

    def convert_coords(self, coordinate, direction):

        if direction in ("N", "S"):

            degrees = int(coordinate[:2])
            minutes = float(coordinate[2:])

        else:

            degrees = int(coordinate[:3])
            minutes = float(coordinate[3:])

        decimal = degrees + minutes / 60

        if direction in ("S", "W"):
            decimal *= -1

        return decimal


# GPS UART0
gps = GPS(
    TX=0,
    RX=1
)


# ==========================================
# OLED 1 - I2C0
# GYROSCOPE + ACCELEROMETER
# ==========================================

class OLED_1:

    def __init__(self):

        self.i2c = i2c

        self.oled = SH1106_I2C(
            self.i2c,
            128,
            64,
            addr=0x3C
        )

    def write_OLED(self, x_deg, y_deg, z_deg, Ax, Ay, Az):

        self.oled.fill(0)

        # Gyroscope
        self.oled.text("GYROSCOPE", 0, 0)

        self.oled.text(
            "X: {:.1f}".format(x_deg),
            0, 10
        )

        self.oled.text(
            "Y: {:.1f}".format(y_deg),
            0, 20
        )

        self.oled.text(
            "Z: {:.1f}".format(z_deg),
            0, 30
        )

        # Accelerometer
        self.oled.text("ACCELEROMETER", 0, 40)

        self.oled.text(
            "X:{:.1f} Y:{:.1f}".format(Ax, Ay),
            0, 50
        )

        self.oled.text(
            "Z:{:.1f}".format(Az),
            0, 58
        )

        self.oled.show()


# ==========================================
# OLED 2 - I2C1
# GPS COORDINATES
# ==========================================

class OLED_2:

    def __init__(self):

        self.i2c = I2C(
            1,
            sda=Pin(26),
            scl=Pin(27),
            freq=100000
        )

        self.oled = SH1106_I2C(
            self.i2c,
            128,
            64,
            addr=0x3C
        )

    def write_OLED_2(self, latitude, longitude):

        self.oled.fill(0)

        # GPS
        self.oled.text("GPS COORDINATES", 0, 0)

        self.oled.text("LAT:", 0, 20)

        self.oled.text(
            "{:.5f}".format(latitude),
            0, 30
        )

        self.oled.text("LONG:", 0, 45)

        self.oled.text(
            "{:.5f}".format(longitude),
            0, 55
        )

        self.oled.show()


# ==========================================
# OLED INITIALIZATION
# ==========================================

oled = OLED_1()
oled_2 = OLED_2()


# ==========================================
# MAIN PROGRAM
# ==========================================

while True:

    # --------------------------------------
    # READ GYROSCOPE
    # --------------------------------------

    x_deg, y_deg, z_deg = mpu_gyro.gyro_read()

    print("GYROSCOPE")

    print("X:", x_deg, "deg/s")
    print("Y:", y_deg, "deg/s")
    print("Z:", z_deg, "deg/s")


    # --------------------------------------
    # READ ACCELEROMETER
    # --------------------------------------

    Ax, Ay, Az = mpu_acc.read_acc()

    print("ACCELEROMETER")

    print("X:", Ax, "m/s^2")
    print("Y:", Ay, "m/s^2")
    print("Z:", Az, "m/s^2")

    print("----------------------")


    # --------------------------------------
    # READ GPS
    # --------------------------------------

    coords = gps.print_coords()

    if coords is not None:

        latitude, longitude = coords

        oled_2.write_OLED_2(
            latitude,
            longitude
        )

        print(
            "Latitude:", latitude,
            "Longitude:", longitude
        )


    # --------------------------------------
    # UPDATE OLED 1
    # --------------------------------------

    oled.write_OLED(
        x_deg, y_deg, z_deg,
        Ax, Ay, Az
    )

    time.sleep(0.5)
