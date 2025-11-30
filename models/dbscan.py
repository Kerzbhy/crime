import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import davies_bouldin_score

def perform_dbscan(data_input, eps=0.5, min_samples=5):
    
    # 1. Cek Data Kosong
    if not data_input or len(data_input) == 0:
        return {"clusters": {}, "dbi": 0}

    # 2. Ubah data mentah ke Pandas DataFrame
    df = pd.DataFrame(data_input)

    # 3. Preprocessing (Sama seperti sebelumnya, Numerik saja)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), ['lat', 'lon', 'rugi'])
        ],
        remainder='drop' 
    )

    # 4. Terapkan transformasi (Fit & Transform)
    # data_scaled adalah Matrix angka 0-1
    data_scaled = preprocessor.fit_transform(df)

    # 5. Jalankan DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_scaled)
    labels = db.labels_

    # === 6. HITUNG DAVIES-BOULDIN INDEX (VALIDASI) ===
    # Syarat DBI: Harus terbentuk minimal 2 kelompok label yang berbeda
    # (Misal: Cluster 0 dan Noise -1, atau Cluster 0 dan Cluster 1).
    # Jika hanya terbentuk 1 cluster saja (misal semua data dianggap Noise), DBI tidak bisa dihitung.
    
    unique_labels = set(labels)
    dbi_score = 0.0
    
    if len(unique_labels) > 1:
        try:
            # Hitung nilai validitas
            dbi_score = davies_bouldin_score(data_scaled, labels)
        except Exception as e:
            # Fallback jika terjadi error matematika
            dbi_score = 0.0
            print("Error Calculating DBI:", e)
    else:
        # Jika cuma 1 label (contoh: semua Noise), nilainya dianggap 0
        dbi_score = 0.0

    # === 7. SUSUN OUTPUT ===
    # Struktur berubah: Kita kirim "clusters" dan "dbi" secara terpisah
    
    grouped_clusters = {}
    for i, label in enumerate(labels):
        lbl = str(label)
        
        if lbl not in grouped_clusters:
            grouped_clusters[lbl] = []
        
        # Masukkan data asli ke dalam grup clusternya
        grouped_clusters[lbl].append(data_input[i])

    return {
        "clusters": grouped_clusters,
        "dbi": float(dbi_score)
    }