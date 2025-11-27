import numpy as np

def perform_topsis(matrix, weights, impacts):
    """
    Fungsi untuk menjalankan algoritma TOPSIS lengkap dengan detail per langkah.
    """
    
    # Validasi input array
    if not matrix or len(matrix) == 0:
        return {}
        
    matrix = np.array(matrix, dtype=float)
    weights = np.array(weights, dtype=float)
    impacts = np.array(impacts)

    # 1. Normalisasi matriks
    # Hitung pembagi (akar dari penjumlahan kuadrat kolom)
    divisors = np.sqrt(np.sum(matrix**2, axis=0))
    
    # Pencegahan error jika ada kolom bernilai 0 semua (hindari divide by zero)
    divisors[divisors == 0] = 1 
    
    norm_matrix = matrix / divisors

    # 2. Normalisasi terbobot
    weighted_matrix = norm_matrix * weights

    # 3. Menentukan solusi ideal positif dan negatif
    ideal_positive = np.zeros(weighted_matrix.shape[1])
    ideal_negative = np.zeros(weighted_matrix.shape[1])

    for i in range(weighted_matrix.shape[1]):
        col_values = weighted_matrix[:, i]
        if impacts[i] == 1: # Benefit (Makin besar makin bagus)
            ideal_positive[i] = np.max(col_values)
            ideal_negative[i] = np.min(col_values)
        else: # Cost (Makin kecil makin bagus)
            ideal_positive[i] = np.min(col_values)
            ideal_negative[i] = np.max(col_values)

    # 4. Menghitung jarak ke solusi ideal (Euclidean Distance)
    dist_positive = np.sqrt(np.sum((weighted_matrix - ideal_positive)**2, axis=1))
    dist_negative = np.sqrt(np.sum((weighted_matrix - ideal_negative)**2, axis=1))

    # 5. Menghitung skor preferensi
    # Mencegah pembagian dengan nol
    denominator = dist_positive + dist_negative
    score = np.zeros(len(dist_positive))
    
    non_zero_idx = denominator != 0
    score[non_zero_idx] = dist_negative[non_zero_idx] / denominator[non_zero_idx]

    # 6. Merangking (Opsional, di Laravel biasanya di-sort sendiri juga bisa)
    ranking = np.argsort(score)[::-1]

    # === BAGIAN PENTING: MENGEMBALIKAN SEMUA DATA UNTUK VIEW LARAVEL ===
    # .tolist() wajib digunakan agar bisa diubah jadi JSON oleh Flask
    return {
        'scores': score.tolist(),
        'ranking': ranking.tolist(),
        
        # Data tambahan untuk tabel detail:
        'normalized_matrix': norm_matrix.tolist(),
        'weighted_matrix': weighted_matrix.tolist(),
        'ideal_positive': ideal_positive.tolist(),
        'ideal_negative': ideal_negative.tolist(),
        'dist_positive': dist_positive.tolist(),
        'dist_negative': dist_negative.tolist()
    }