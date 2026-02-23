"""
WSGI entry point for production deployment
Gunicorn ile çalıştırmak için
"""
import os
from main import app, socketio

# Render.com için port
port = int(os.environ.get('PORT', 5001))

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
