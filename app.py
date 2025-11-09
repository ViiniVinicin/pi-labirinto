"""
Aplicação wrapper.

Mantemos um pequeno `app.py` na raiz para manter compatibilidade com instruções
anteriores. Ele apenas importa e roda a app do `server.app`.
"""
from server.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
