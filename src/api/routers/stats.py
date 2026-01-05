"""
Rotas para estatísticas dos livros.
Versão: v1
"""
import logging
from flask import Blueprint, Response
from typing import Tuple

from api.utils import (
    carregar_livros,
    resposta_sucesso,
    resposta_erro,
    lista_categorias,
    estatisticas_precos
)
from core.cache import cache

# Configura logging
logger = logging.getLogger(__name__)

router = Blueprint('stats', __name__, url_prefix='/api/v1/stats')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300)
def get_stats() -> Tuple[Response, int]:
    """
    Retorna estatísticas básicas dos livros.

    ---
    get:
      description: Estatísticas gerais dos livros
      responses:
        200:
          description: Estatísticas calculadas
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()

        if not livros:
            return resposta_sucesso(dados={
                "total_livros": 0,
                "preco_medio": 0.0,
                "preco_minimo": 0.0,
                "preco_maximo": 0.0
            })

        # Calcula estatísticas
        stats = estatisticas_precos(livros)

        # Retorna as estatísticas
        return resposta_sucesso(dados=stats)

    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}")
        return resposta_erro(
            "Erro ao calcular estatísticas.",
            codigo_status=500
        )


@router.route('/category/<string:category>', methods=['GET'])
def get_category_stats(category: str) -> Tuple[Response, int]:
    """
    Retorna estatísticas de uma categoria específica.

    ---
    get:
      description: Estatísticas de livros de uma categoria
      parameters:
        - name: category
          in: path
          type: string
          required: true
      responses:
        200:
          description: Estatísticas da categoria
        404:
          description: Categoria não encontrada
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()
        # Se não tiver livros, retorna zeros
        if not livros:
            return resposta_sucesso(
                dados={'total_livros': 0, 'categoria': category}
            )

        # Pega a lista de categorias disponíveis
        categorias = lista_categorias(livros)
        # Verifica se a categoria existe
        if category not in categorias:
            return resposta_erro('Categoria não encontrada', codigo_status=404)

        # Filtra os livros da categoria
        livros_filtrados = [
            livro for livro in livros
            if livro.get('category') == category
        ]

        # Calcula as estatísticas para a categoria
        stats = estatisticas_precos(livros_filtrados)
        stats['categoria'] = category
        # Retorna as estatísticas
        return resposta_sucesso(dados=stats)

    except Exception as e:
        logger.error(
            f"Erro ao calcular estatísticas da categoria {category}: {e}"
        )
        return resposta_erro(
            "Erro interno ao processar a requisição.",
            codigo_status=500
        )
