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


@router.route('/overview', methods=['GET'])
@cache.cached(timeout=300)
def get_stats_overview() -> Tuple[Response, int]:
    """
    Retorna estatísticas gerais da coleção com distribuição de ratings.

    ---
    get:
      description: Estatísticas gerais (total, preço médio, distribuição ratings)
      responses:
        200:
          description: Overview estatístico completo
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()

        if not livros:
            return resposta_sucesso(dados={
                "total_livros": 0,
                "preco_medio": 0.0,
                "preco_minimo": 0.0,
                "preco_maximo": 0.0,
                "distribuicao_ratings": {
                    "1_estrela": 0,
                    "2_estrelas": 0,
                    "3_estrelas": 0,
                    "4_estrelas": 0,
                    "5_estrelas": 0
                },
                "total_categorias": 0
            })

        # Calcula estatísticas de preço
        stats = estatisticas_precos(livros)

        # Calcula distribuição de ratings
        distribuicao_ratings = {
            "1_estrela": 0,
            "2_estrelas": 0,
            "3_estrelas": 0,
            "4_estrelas": 0,
            "5_estrelas": 0
        }

        for livro in livros:
            rating = livro.get('rating', 0)
            if rating == 1:
                distribuicao_ratings["1_estrela"] += 1
            elif rating == 2:
                distribuicao_ratings["2_estrelas"] += 1
            elif rating == 3:
                distribuicao_ratings["3_estrelas"] += 1
            elif rating == 4:
                distribuicao_ratings["4_estrelas"] += 1
            elif rating == 5:
                distribuicao_ratings["5_estrelas"] += 1

        # Adiciona distribuição ao stats
        stats["distribuicao_ratings"] = distribuicao_ratings

        # Conta categorias únicas
        categorias = lista_categorias(livros)
        stats["total_categorias"] = len(categorias)

        # Retorna as estatísticas
        return resposta_sucesso(dados=stats)

    except Exception as e:
        logger.error(f"Erro ao calcular overview: {e}")
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
