from flask import Blueprint, request, jsonify
# Import fungsi logika yang ada di folder models
from models.dbscan import perform_dbscan
# Jika Anda punya file models/topsis.py, import juga (jika tidak, baris ini bisa dihapus)
from models.topsis import perform_topsis 

# --- PENTING: Mendefinisikan Variable Blueprint ---
cluster_api = Blueprint('cluster_api', __name__)

@cluster_api.route('/dbscan', methods=['POST'])
def handle_dbscan():
    req_data = request.get_json()

    # Validasi: Kita mencari key 'data' sekarang
    if not req_data or 'data' not in req_data:
        return jsonify({"error": "Request body harus berisi 'data' yang lengkap"}), 400

    raw_data = req_data.get('data') # Data lengkap (lat, lon, jenis, rugi)
    
    # Ambil parameter, set default eps lebih kecil (0.2) karena pakai Normalisasi (MinMaxScaler)
    eps = float(req_data.get('eps', 0.2))
    min_samples = int(req_data.get('min_samples', 3))

    try:
        # Panggil fungsi perform_dbscan yang sudah kita update di models/dbscan.py
        result = perform_dbscan(raw_data, eps, min_samples)
        return jsonify(result), 200
    except Exception as e:
        # Print error ke terminal flask agar bisa dibaca jika ada masalah
        print("Error DBSCAN:", str(e))
        return jsonify({"error": str(e)}), 500

@cluster_api.route('/topsis', methods=['POST'])
def handle_topsis():
    data = request.get_json()

    if not data or not all(k in data for k in ['matrix', 'weights', 'impacts']):
        return jsonify({"error": "Request body harus berisi 'matrix', 'weights', dan 'impacts'"}), 400
    
    matrix = data.get('matrix')
    weights = data.get('weights')
    impacts = data.get('impacts')
    
    try:
        # Panggil fungsi dari model topsis
        result = perform_topsis(matrix, weights, impacts)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500