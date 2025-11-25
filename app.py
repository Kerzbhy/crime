from flask import Flask
from routes.api import cluster_api

app = Flask(__name__)
app.register_blueprint(cluster_api, url_prefix='/api')

# --- TAMBAHAN: Agar halaman utama tidak 404 ---
@app.route('/')
def index():
    return "Halo! Server API Crime Zone sudah aktif. Silakan akses via Laravel."
# -----------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=5001)