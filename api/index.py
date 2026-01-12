"""
Ponto de entrada para deploy no Vercel (serverless).

Este arquivo é necessário porque o Vercel precisa de um arquivo específico
na pasta 'api/' para funcionar com Python. Ele basicamente importa e configura
a mesma aplicação Flask que já temos, mas adaptada para o ambiente serverless.

Autor: Gabriel Peixer - Engenheiro de Machine Learning Jr.
"""
import sys
from pathlib import Path

# Adiciona a pasta 'src' ao path do Python para conseguir importar os módulos
# Isso é necessário porque o Vercel executa a partir da raiz do projeto
root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir / "src"))

# Importações do Flask e dos módulos da API
from flask import Flask, send_from_directory
from api.routers.books import router as books_router
from api.routers.categories import router as categories_router
from api.routers.health import router as health_router
from api.routers.stats import router as stats_router
from api.routers.ml import router as ml_router
from core.config import Config
from core.cache import cache
from core.db import db
from core.logging_config import setup_logging

# Configura o sistema de logs
setup_logging(log_level="INFO")


def create_app():
    """
    Cria e configura a aplicação Flask.
    
    Essa função é um padrão chamado 'Application Factory' que permite
    criar múltiplas instâncias da aplicação (útil para testes).
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa as extensões do Flask
    # - cache: para armazenar resultados em memória e melhorar performance
    # - db: conexão com o banco de dados SQLAlchemy
    cache.init_app(app)
    db.init_app(app)

    # Registra os blueprints (rotas organizadas por funcionalidade)
    # Cada router cuida de um grupo de endpoints relacionados
    app.register_blueprint(books_router)        # Endpoints de livros
    app.register_blueprint(categories_router)   # Endpoints de categorias
    app.register_blueprint(health_router)       # Endpoint de health check
    app.register_blueprint(stats_router)        # Endpoints de estatísticas
    app.register_blueprint(ml_router)           # Endpoints de Machine Learning

    @app.route('/docs')
    def docs():
        """Serve a página de documentação Swagger UI."""
        docs_dir = root_dir / 'docs'
        return send_from_directory(docs_dir, 'index.html')

    @app.route('/openapi.json')
    def openapi_spec():
        """Serve o arquivo de especificação OpenAPI (usado pelo Swagger)."""
        docs_dir = root_dir / 'docs'
        return send_from_directory(docs_dir, 'openapi.json')

    @app.route('/')
    def home():
        """
        Endpoint raiz da API.
        Retorna informações básicas e links úteis.
        """
        return {
            "message": "API de Recomendação de Livros",
            "versao": "1.0.0",
            "documentacao": "/docs",
            "health_check": "/health",
            "autor": "Gabriel Peixer - ML Engineer Jr."
        }

    return app


# O Vercel exige que a variável se chame 'app' para funcionar
# Não mude esse nome!
app = create_app()

# Isso só executa quando rodamos o arquivo diretamente (python api/index.py)
# No Vercel, ele importa o 'app' diretamente, então esse bloco é ignorado
if __name__ == "__main__":
    app.run(debug=True, port=5000)
