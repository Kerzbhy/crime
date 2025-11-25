# models/topsis.py

import numpy as np

def perform_topsis(matrix, weights, impacts):
    """
    Fungsi untuk menjalankan algoritma TOPSIS.
    - matrix: Matriks keputusan (numpy array m x n).
    - weights: Bobot untuk setiap kriteria (list atau numpy array).
    - impacts: Jenis kriteria, +1 untuk benefit, -1 untuk cost (list).
    """
    matrix = np.array(matrix, dtype=float)
    weights = np.array(weights, dtype=float)
    impacts = np.array(impacts)

    # 1. Normalisasi matriks
    norm_matrix = matrix / np.sqrt(np.sum(matrix**2, axis=0))

    # 2. Normalisasi terbobot
    weighted_matrix = norm_matrix * weights

    # 3. Menentukan solusi ideal positif dan negatif
    ideal_positive = np.zeros(weighted_matrix.shape[1])
    ideal_negative = np.zeros(weighted_matrix.shape[1])

    for i in range(weighted_matrix.shape[1]):
        if impacts[i] == 1: # Benefit
            ideal_positive[i] = np.max(weighted_matrix[:, i])
            ideal_negative[i] = np.min(weighted_matrix[:, i])
        else: # Cost
            ideal_positive[i] = np.min(weighted_matrix[:, i])
            ideal_negative[i] = np.max(weighted_matrix[:, i])

    # 4. Menghitung jarak ke solusi ideal
    dist_positive = np.sqrt(np.sum((weighted_matrix - ideal_positive)**2, axis=1))
    dist_negative = np.sqrt(np.sum((weighted_matrix - ideal_negative)**2, axis=1))

    # 5. Menghitung skor preferensi
    score = dist_negative / (dist_positive + dist_negative)

    # 6. Merangking alternatif (ranking dari yang terbesar ke terkecil)
    ranking = np.argsort(score)[::-1]

    return {
        'scores': score.tolist(),
        'ranking': ranking.tolist()
    }