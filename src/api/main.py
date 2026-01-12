"""
Ponto de entrada da API Flask.
"""
import logging
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, send_from_directory  # noqa: E402
from api.routers.books import router as books_router  # noqa: E402
from api.routers.categories import router as categories_router  # noqa: E402
from api.routers.health import router as health_router  # noqa: E402
from api.routers.stats import router as stats_router  # noqa: E402
from api.routers.ml import router as ml_router  # noqa: E402
from core.config import Config  # noqa: E402
from core.cache import cache  # noqa: E402
from core.db import db  # noqa: E402
from core.logging_config import setup_logging  # noqa: E402

setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)


def create_app():
    """Cria a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões
    cache.init_app(app)
    db.init_app(app)

    # Registra rotas
    app.register_blueprint(books_router)
    app.register_blueprint(categories_router)
    app.register_blueprint(health_router)
    app.register_blueprint(stats_router)
    app.register_blueprint(ml_router)

    @app.route('/docs')
    def docs():
        """Serve a documentação Swagger."""
        # Obtém o diretório raiz do projeto (pai de src)
        project_root = Path(__file__).resolve().parents[2]
        docs_dir = project_root / 'docs'
        if not docs_dir.exists():
            logger.error(f"Diretório docs não encontrado: {docs_dir}")
            return {"erro": "Documentação não encontrada"}, 404
        return send_from_directory(docs_dir, 'index.html')

    @app.route('/openapi.json')
    def openapi_spec():
        """Serve a especificação OpenAPI."""
        # Obtém o diretório raiz do projeto (pai de src)
        project_root = Path(__file__).resolve().parents[2]
        docs_dir = project_root / 'docs'
        if not docs_dir.exists():
            logger.error(f"Diretório docs não encontrado: {docs_dir}")
            return {"erro": "Especificação não encontrada"}, 404
        return send_from_directory(docs_dir, 'openapi.json')

    return app


app = create_app()

if __name__ == "__main__":
    logger.info(f"Iniciando servidor em {Config.API_HOST}:{Config.API_PORT}")
    app.run(debug=Config.DEBUG, host=Config.API_HOST, port=Config.API_PORT)
