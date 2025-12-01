"""
Ponto de entrada principal para a API Flask.
"""
import logging
import sys
from pathlib import Path

# Adiciona o diretório src ao path para imports funcionarem
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, send_from_directory  # noqa: E402
from api.routers.books import router as books_router  # noqa: E402
from api.routers.health import router as health_router  # noqa: E402
from api.routers.stats import router as stats_router  # noqa: E402
from core.config import Config  # noqa: E402
from core.cache import cache  # noqa: E402
from core.db import db  # noqa: E402
from core.logging_config import setup_logging  # noqa: E402

# Configura logging
setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """
    Factory function para criar a aplicação Flask.

    Args:
        config_class: A classe de configuração a ser usada.

    Returns:
        Flask: A aplicação Flask inicializada.
    """
    app = Flask(__name__)

    # Carrega configurações
    app.config.from_object(config_class)

    # Inicializa extensões
    cache.init_app(app)
    db.init_app(app)

    # Registra as rotas
    app.register_blueprint(books_router)
    app.register_blueprint(health_router)
    app.register_blueprint(stats_router)

    @app.route('/docs')
    def docs():
        """Serve a documentação Swagger UI"""
        docs_dir = Path(app.root_path).parents[1] / 'docs'
        return send_from_directory(docs_dir, 'index.html')

    @app.route('/openapi.json')
    def openapi_spec():
        """Serve a especificação OpenAPI"""
        docs_dir = Path(app.root_path).parents[1] / 'docs'
        return send_from_directory(docs_dir, 'openapi.json')

    return app


app = create_app()

if __name__ == "__main__":
    # Roda o servidor na porta configurada
    logger.info(f"Iniciando servidor em {Config.API_HOST}:{Config.API_PORT}")
    app.run(debug=Config.DEBUG, host=Config.API_HOST, port=Config.API_PORT)
