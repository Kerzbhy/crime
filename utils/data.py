# utils/data.py

import pandas as pd

def get_crime_data_from_csv(filepath):
    """
    Contoh fungsi untuk membaca data dari file CSV.
    """
    df = pd.read_csv(filepath)
    # Anda bisa melakukan preprocessing di sini
    return df

# Anda juga bisa menambahkan fungsi untuk koneksi database di sini