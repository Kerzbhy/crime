import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer

def perform_dbscan(data_input, eps=0.5, min_samples=5):
    
    # 1. Cek Data Kosong
    if not data_input or len(data_input) == 0:
        return {}

    # 2. Ubah data mentah ke Pandas DataFrame
    df = pd.DataFrame(data_input)

    
    preprocessor = ColumnTransformer(
        transformers=[
            # Normalisasi Angka (MinMaxScaler)
            # Hanya memproses Lat, Lon, dan Rugi agar range-nya 0 s/d 1
            ('num', MinMaxScaler(), ['lat', 'lon', 'rugi'])
        ],
        # 'drop' artinya kolom yang tidak disebut (seperti 'jenis') dibuang dari perhitungan matriks
        remainder='drop' 
    )

    # 4. Terapkan transformasi (Fit & Transform)
    # Sekarang matrix ini murni angka 3 dimensi (lat, lon, rugi)
    data_scaled = preprocessor.fit_transform(df)

    # 5. Jalankan DBSCAN pada data yang sudah Dinormalisasi
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_scaled)
    labels = db.labels_

    # 6. Susun kembali output
    clusters = {}
    
    for i, label in enumerate(labels):
        lbl = str(label)
        
        if lbl not in clusters:
            clusters[lbl] = []
        
        # Masukkan data asli (termasuk jenis kejahatan yg tadi di-skip) ke hasil
        clusters[lbl].append(data_input[i])

    return clusters