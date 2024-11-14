import cv2
import numpy as np


# Fungsi callback untuk trackbar (diperlukan oleh OpenCV)
def nothing(x):
    pass


# Inisialisasi jendela untuk pengaturan HSV dengan slider
cv2.namedWindow("HSV Adjustments")
cv2.createTrackbar("Lower H", "HSV Adjustments", 0, 179, nothing)
cv2.createTrackbar("Lower S", "HSV Adjustments", 0, 255, nothing)
cv2.createTrackbar("Lower V", "HSV Adjustments", 0, 255, nothing)
cv2.createTrackbar("Upper H", "HSV Adjustments", 179, 179, nothing)
cv2.createTrackbar("Upper S", "HSV Adjustments", 255, 255, nothing)
cv2.createTrackbar("Upper V", "HSV Adjustments", 255, 255, nothing)


# Fungsi untuk mendeteksi segitiga terbesar dalam frame
def detect_largest_triangle(frame, lower_hsv, upper_hsv):
    # Konversi ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Buat mask berdasarkan rentang warna
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

    # Cari kontur dari mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    largest_triangle = None

    # Loop melalui setiap kontur yang ditemukan
    for contour in contours:
        # Approximate kontur untuk mendapatkan jumlah sisi
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Jika kontur memiliki 3 titik, maka bentuk tersebut adalah segitiga
        if len(approx) == 3:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_triangle = approx  # Simpan kontur segitiga terbesar

    # Jika ada segitiga yang terdeteksi
    if largest_triangle is not None:
        # Buat bounding box untuk segitiga terbesar
        x, y, w, h = cv2.boundingRect(largest_triangle)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Hitung sudut tangen
        if w != 0:  # Hindari pembagian dengan nol
            angle_radians = np.arctan(h / w)  # Sudut dalam radian
            angle_degrees = np.degrees(angle_radians)  # Konversi ke dalam derajat
        else:
            angle_degrees = 0

        # Tampilkan tinggi, panjang dan sudut tangen segitiga terbesar
        cv2.putText(frame, f"Tinggi: {h} px", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Panjang: {w} px", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame, f"Sudut: {angle_degrees:.2f} deg", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0),
                    2)
        cv2.putText(frame, "Granul", (x, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame


# Baca gambar yang akan digunakan
image_path = "images/images.jpeg"  # Ganti dengan path gambar Anda
frame = cv2.imread(image_path)

while True:
    # Baca nilai dari trackbars
    lower_h = cv2.getTrackbarPos("Lower H", "HSV Adjustments")
    lower_s = cv2.getTrackbarPos("Lower S", "HSV Adjustments")
    lower_v = cv2.getTrackbarPos("Lower V", "HSV Adjustments")
    upper_h = cv2.getTrackbarPos("Upper H", "HSV Adjustments")
    upper_s = cv2.getTrackbarPos("Upper S", "HSV Adjustments")
    upper_v = cv2.getTrackbarPos("Upper V", "HSV Adjustments")

    # Rentang HSV berdasarkan nilai slider
    lower_hsv = np.array([lower_h, lower_s, lower_v])
    upper_hsv = np.array([upper_h, upper_s, upper_v])

    # Deteksi segitiga terbesar pada frame
    result_frame = detect_largest_triangle(frame.copy(), lower_hsv, upper_hsv)

    # Tampilkan hasil deteksi segitiga terbesar
    cv2.imshow("Largest Triangle Detection with Tangent Angle (Adjustable HSV)", result_frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan resource dan tutup semua jendela
cv2.destroyAllWindows()