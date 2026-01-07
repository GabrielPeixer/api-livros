"""
Rotas para estatísticas dos livros.
"""
import logging
from flask import Blueprint

from api.utils import (
    carregar_livros,
    resposta_sucesso,
    resposta_erro,
    lista_categorias,
    estatisticas_precos
)
from core.cache import cache

logger = logging.getLogger(__name__)

router = Blueprint('stats', __name__, url_prefix='/api/v1/stats')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300)
def get_stats():
    """Retorna estatísticas básicas dos livros."""
    try:
        livros = carregar_livros()

        if not livros:
            return resposta_sucesso(dados={
                "total_livros": 0,
                "preco_medio": 0.0,
                "preco_minimo": 0.0,
                "preco_maximo": 0.0
            })

        stats = estatisticas_precos(livros)
        return resposta_sucesso(dados=stats)

    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}")
        return resposta_erro("Erro ao calcular estatísticas", codigo_status=500)


@router.route('/overview', methods=['GET'])
@cache.cached(timeout=300)
def get_stats_overview():
    """Retorna visão geral com distribuição de ratings."""
    try:
        livros = carregar_livros()

        if not livros:
            return resposta_sucesso(dados={
                "total_livros": 0,
                "preco_medio": 0.0,
                "preco_minimo": 0.0,
                "preco_maximo": 0.0,
                "distribuicao_ratings": {},
                "total_categorias": 0
            })

        stats = estatisticas_precos(livros)

        # Conta ratings
        distribuicao = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        for livro in livros:
            rating = livro.get('rating', 0)
            if rating in [1, 2, 3, 4, 5]:
                distribuicao[str(rating)] += 1

        stats["distribuicao_ratings"] = distribuicao
        stats["total_categorias"] = len(lista_categorias(livros))

        return resposta_sucesso(dados=stats)

    except Exception as e:
        logger.error(f"Erro ao calcular overview: {e}")
        return resposta_erro("Erro ao calcular estatísticas", codigo_status=500)


@router.route('/category/<string:category>', methods=['GET'])
def get_category_stats(category):
    """Retorna estatísticas de uma categoria."""
    try:
        livros = carregar_livros()

        if not livros:
            return resposta_sucesso(
                dados={'total_livros': 0, 'categoria': category}
            )

        categorias = lista_categorias(livros)
        if category not in categorias:
            return resposta_erro('Categoria não encontrada', codigo_status=404)

        # Filtra livros da categoria
        livros_categoria = []
        for livro in livros:
            if livro.get('category') == category:
                livros_categoria.append(livro)

        stats = estatisticas_precos(livros_categoria)
        stats['categoria'] = category

        return resposta_sucesso(dados=stats)

    except Exception as e:
        logger.error(f"Erro ao calcular stats da categoria {category}: {e}")
        return resposta_erro("Erro interno", codigo_status=500)
