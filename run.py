from waitress import serve
from app import app

print("Servidor iniciado en http://localhost:5000")
print("Presiona Ctrl+C para detener")
serve(app, host="0.0.0.0", port=5000, threads=4, channel_timeout=300)