import serial
import time

arduino = serial.Serial(port='/dev/cu.usbserial-0001', baudrate=115200, timeout=1)


def send_data(data):
    arduino.write((data + '\n').encode()) # Kirim data ke arduino


def read_data():
    if arduino.in_waiting > 0: # Cek apakah ada data masuk
        return arduino.readline().decode().strip() # Baca data yang masuk
    return None


time.sleep(2)

try:
    while True:
        # Baca data dari Arduino
        data_from_arduino = read_data()
        if data_from_arduino:
            print(f"From Arduino: {data_from_arduino}")

        # Kirim data ke arduino
        send_data("Hello from python")
        time.sleep(1)
except KeyboardInterrupt:
    print("Program dihentikan")
finally:
    arduino.close()
