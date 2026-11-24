from machine import Pin, UART
from time import sleep

class GPS():
    def __init__(self, TX, RX):
        self.gps = UART(0, baudrate = 9600, tx = TX, rx = RX)
    
    def print_data(self):
        data = self.gps.readline()
        if data:
            print(data.strip())
        
    def print_coords(self):
        data = self.gps.readline()

        if not data:
            return None

        try:
            data = data.decode("ascii", "ignore").strip()
            data_split = data.split(",")

            if data_split[0] not in ("$GPGGA", "$GNGGA"):
                return None

            if len(data_split) < 7:
                return None

            if data_split[6] == "0":
                return None

            latitude = data_split[2]
            latitude_dir = data_split[3]
            longitude = data_split[4]
            longitude_dir = data_split[5]

            if not latitude or not longitude:
                return None

            latitude = self.convert_coords(latitude, latitude_dir)
            longitude = self.convert_coords(longitude, longitude_dir)

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
    
if __name__ == "__main__":
    gps = GPS(0, 1)
    
    try:
        while True:
            coords = gps.print_coords()

            if coords:
                latitude, longitude = coords

                print("Latitude:", latitude , "Longitude:", longitude)

            sleep(0.1)
    except KeyboardInterrupt:
        print("Code stopped")
