"""
Rotas para categorias de livros.
Versão: v1
"""
import logging
from flask import Blueprint, Response
from typing import Tuple

from api.utils import (
    carregar_livros,
    lista_categorias,
    resposta_erro,
    resposta_sucesso,
)
from core.cache import cache

# Configura logging
logger = logging.getLogger(__name__)

router = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300)
def get_categories() -> Tuple[Response, int]:
    """
    Lista todas as categorias de livros disponíveis.

    ---
    get:
      description: Retorna lista de categorias únicas
      responses:
        200:
          description: Lista de categorias
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()

        # Pega as categorias únicas
        categorias = lista_categorias(livros)

        # Retorna a lista de categorias
        return resposta_sucesso(dados=categorias)

    except Exception as e:
        logger.error(f"Erro ao listar categorias: {e}")
        return resposta_erro(
            "Erro interno ao processar a requisição.",
            codigo_status=500
        )
