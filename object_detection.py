import cv2
import numpy as np

# Buka stream video dari webcam
cap = cv2.VideoCapture(0)


# Fungsi untuk mendeteksi objek dan mengatur tinggi, panjang, serta sudut tangen
def detect_object_and_angle(frame):
    # Konversi ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Tentukan rentang HSV untuk warna objek yang akan di deteksi
    lower_hsv = np.array([35, 100, 100])  # Rentang bawah HSV
    upper_hsv = np.array([85, 255, 255])  # Rentang atas HSV

    # Buat mask berdasarkan rentang warna
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

    # Cari kontur dari mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop melalui setiap kontur yang ditemukan
    for contour in contours:
        # buat bounding box untuk setiap kontur
        x, y, w, h = cv2.boundingRect(contour)

        # Gambar reactangle di sekitar objek yang terdeteksi
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Hitung sudut tangen
        if w != 0:  # Hindari pembagian dengan nol
            angle_radians = np.arctan(h / w)  # Sudut dalam radian
            angle_degrees = np.degrees(angle_radians)  # Konversi ke dalam derajat
        else:
            angle_degrees = 0

        # Tampilkan tinggi, panjang dan sudut tangen objek
        cv2.putText(frame, f"Tinggi: {h} px", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Panjang: {w} px", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Sudut: {angle_degrees:.2f} deg", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0),
                    2)

    return frame


# Loo[ untuk menangkap frame secara realtime
while True:
    # Baca frame dari webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Deteksi objek dan hitung sudut tangen di frame saat ini
    result_frame = detect_object_and_angle(frame)

    # Tampilkan hasil frame dengan bounding box dan sudut tangen
    cv2.imshow('Real-time Object Detection with Tangent Angle', result_frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan resource kamara dan tutup jendela
cap.release()
cv2.destroyAllWindows()





