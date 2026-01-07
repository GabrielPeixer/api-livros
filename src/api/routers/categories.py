"""
Rotas para categorias de livros.
"""
import logging
from flask import Blueprint

from api.utils import (
    carregar_livros,
    lista_categorias,
    resposta_erro,
    resposta_sucesso,
)
from core.cache import cache

logger = logging.getLogger(__name__)

router = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300)
def get_categories():
    """Lista todas as categorias."""
    try:
        livros = carregar_livros()
        categorias = lista_categorias(livros)
        return resposta_sucesso(dados=categorias)

    except Exception as e:
        logger.error(f"Erro ao listar categorias: {e}")
        return resposta_erro("Erro interno", codigo_status=500)
