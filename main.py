import time

import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale

import serial
from PIL import Image, ImageTk
from decision_tree import decision_tree

# Global variable to store the current frame
current_frame = None
arduino_data = None

# Setup serial communication with Arduino
arduino = serial.Serial(port='/dev/cu.usbserial-A50285BI', baudrate=115200, timeout=1)
time.sleep(2)


def button_detection():
    print("Mulai Deteksi")


def send_data(data):
    arduino.write((data + '\n').encode())  # Kirim data ke Arduino


def read_data():
    if arduino.in_waiting > 0:  # Cek apakah ada data masuk
        return arduino.readline().decode().strip()  # Baca data yang masuk
    return None


# Fungsi untuk mengupdate tampilan berdasarkan slider HSV
def update_image(*args):  # Accept the argument passed by Scale
    global current_frame, arduino_data
    if current_frame is None:
        return

    # Ambil nilai dari slider
    lower_h = lower_h_slider.get()
    lower_s = lower_s_slider.get()
    lower_v = lower_v_slider.get()
    upper_h = upper_h_slider.get()
    upper_s = upper_s_slider.get()
    upper_v = upper_v_slider.get()

    # Rentang HSV berdasarkan nilai slider
    lower_hsv = np.array([lower_h, lower_s, lower_v])
    upper_hsv = np.array([upper_h, upper_s, upper_v])

    # Deteksi segitiga terbesar
    processed_frame, angle_degrees, h, w = detect_largest_triangle(current_frame.copy(), lower_hsv, upper_hsv)

    # Resize gambar ke 200x200
    resized_frame = cv2.resize(processed_frame, (720, 480))

    # Konversi gambar ke format yang bisa ditampilkan di Tkinter
    img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(image=img)

    # Update tampilan gambar
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # deg_label.config(text=f"Sudut: {angle_degrees:.2f} deg")
    # h_label.config(text=f"Tinggi: {h:.2f} px")
    # w_label.config(text=f"Lebar: {w:.2f} px")
    #

    arduino_data = read_data()
    if arduino_data:
        # print(f"Data dari Arduino: {arduino_data}")
        if arduino_data == "reset":
            # reset_label.config(text=f"Reset: True")
            result_label.config(text="Timer/Granul\ntidak Ditemukan", fg="red")
            send_data("nogranul")
        else:
            # reset_label.config(text=f"Reset: False")
            timer_result.config(text=f"Timer Result: {arduino_data}")
            if angle_degrees != 0:
                result = decision_tree(angle_degrees, float(arduino_data))
                if result == "bagus":
                    result_label.config(text=f"Bagus", fg="green", font=("Arial", 32),)
                    result_label.place(x=560, y=540)
                    send_data("good")
                else:
                    result_label.config(text=f"Tidak Bagus", fg="red", font=("Arial", 32),)
                    result_label.place(x=560, y=540)
                    send_data("nogood")


# Fungsi untuk mendeteksi segitiga terbesar berdasarkan warna
def detect_largest_triangle(frame, lower_hsv, upper_hsv):
    global angle_degrees, h, w
    angle_degrees = 0  # Initialize angle_degrees to a default value
    h = 0
    w = 0
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    largest_triangle = None

    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 3:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_triangle = approx

    if largest_triangle is not None:
        x, y, w, h = cv2.boundingRect(largest_triangle)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if w != 0:
            angle_radians = np.arctan(h / w)
            angle_degrees = np.degrees(angle_radians)
        else:
            angle_degrees = 0

        cv2.putText(frame, f"Tinggi: {h} px", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Panjang: {w} px", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Sudut: {angle_degrees:.2f} deg", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0),
                    2)
        cv2.putText(frame, "Granul", (x, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame, angle_degrees, h, w


# Fungsi untuk menangani stream video
def video_stream():
    global current_frame
    # Buka webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Ambil frame dari webcam
        ret, frame = cap.read()

        if not ret:
            break

        # Simpan frame saat ini
        current_frame = frame

        # Update gambar di Tkinter
        update_image()

        # Break jika Tkinter window ditutup
        root.update_idletasks()
        root.update()

    cap.release()


# Setup Tkinter
root = tk.Tk()
root.title("Deteksi Sudut Granul")

# Buat frame untuk membungkus seluruh UI dengan padding
ui_frame = tk.Frame(root, padx=20, pady=20)
ui_frame.grid(row=0, column=0)

# Label untuk menampilkan gambar
image_label = tk.Label(ui_frame)
image_label.grid(row=0, column=0, columnspan=6)

# Slider untuk HSV Lower dan Upper
lower_h_slider = Scale(ui_frame, from_=0, to=179, orient="horizontal", label="Lower H", command=update_image)
lower_h_slider.set(0)
lower_h_slider.grid(row=1, column=0)

lower_s_slider = Scale(ui_frame, from_=0, to=255, orient="horizontal", label="Lower S", command=update_image)
lower_s_slider.set(0)
lower_s_slider.grid(row=1, column=1)

lower_v_slider = Scale(ui_frame, from_=0, to=255, orient="horizontal", label="Lower V", command=update_image)
lower_v_slider.set(0)
lower_v_slider.grid(row=1, column=2)

upper_h_slider = Scale(ui_frame, from_=0, to=179, orient="horizontal", label="Upper H", command=update_image)
upper_h_slider.set(179)
upper_h_slider.grid(row=2, column=0)

upper_s_slider = Scale(ui_frame, from_=0, to=255, orient="horizontal", label="Upper S", command=update_image)
upper_s_slider.set(255)
upper_s_slider.grid(row=2, column=1)

upper_v_slider = Scale(ui_frame, from_=0, to=255, orient="horizontal", label="Upper V", command=update_image)
upper_v_slider.set(255)
upper_v_slider.grid(row=2, column=2)

# info_label = tk.Label(ui_frame, text="Hasil: ", font=("Arial", 12), anchor="w")
# info_label.place(x=515, y=480)
#
# deg_label = tk.Label(ui_frame, text="Sudut: 0.00 deg", font=("Arial", 12), anchor="w")
# deg_label.place(x=515, y=500)
#
# h_label = tk.Label(ui_frame, text="Tinggi: 0.00 px", font=("Arial", 12), anchor="w")
# h_label.place(x=515, y=520)
#
# w_label = tk.Label(ui_frame, text="Lebar: 0.00 px", font=("Arial", 12), anchor="w")
# w_label.place(x=515, y=540)
#
result_label = tk.Label(ui_frame, text="Granul\ntidak Ditemukan", font=("Arial", 24), anchor="w")
result_label.place(x=515, y=540)

timer_result = tk.Label(ui_frame, text='Timer Result: ')
timer_result.place(x=510, y=500)

# reset_label = tk.Label(ui_frame, text="| Reset: ")
# reset_label.place(x=650, y=500)

# Mulai stream video
video_stream()

# Jalankan aplikasi Tkinter
root.mainloop()

arduino.close()
