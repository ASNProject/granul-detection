import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

# Contoh dataset
data = {
    'tangen': [30, 45, 60, 90, 120, 150, 180],
    'time': [1.2, 0.9, 1.5, 2.0, 2.3, 1.7, 1.0],
    'result': ['bagus', 'bagus', 'tidak bagus', 'bagus', 'tidak bagus', 'tidak bagus', 'bagus']
}

# Convert to pandas dataframe
df = pd.DataFrame(data)

# Pisahkan fitur (X) dan tangen (y)
X = df[['tangen', 'time']]  # Fitur input: sudut tangen dan waktu
y = df['result']  # Target output = bagus dan tidak bagus

# Pisahkan data training dan testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Inisialisasi model Decision Tree
model = DecisionTreeClassifier()

# Latih model menggunakan data training
model.fit(X_train, y_train)

# Prediksi menggunakan data testing
y_pred = model.predict(X_test)

# Evaluasi model
print("Akurasi: ", metrics.accuracy_score(y_test, y_pred))

# Prediksi data baru
new_tangen = 75
new_time = 1.8
new_input = pd.DataFrame([[new_tangen, new_time]], columns=['tangen', 'time'])

prediction = model.predict(new_input)
print(f'Prediksi untuk sudut tangen {new_tangen} dan watku {new_time}: ', prediction[0])
