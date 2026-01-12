"""
WSGI entry point para Railway deployment.
"""
import sys
from pathlib import Path

# Adiciona src ao path para poder importar
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from api.main import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
