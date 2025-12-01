"""
Rotas para estatísticas dos livros.
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

router = Blueprint('stats', __name__, url_prefix='/api/stats')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300)
def get_stats() -> Tuple[Response, int]:
    """
    Retorna estatísticas básicas dos livros.

    ---
    get:
      description: Estatísticas gerais dos livros (preço médio, mínimo,
                   máximo, total)
      responses:
        200:
          description: Estatísticas calculadas
          content:
            application/json:
              schema:
                type: object
                properties:
                  estado:
                    type: string
                    example: sucesso
                  dados:
                    type: object
                    properties:
                      total_livros:
                        type: integer
                        example: 100
                      preco_medio:
                        type: number
                        example: 35.5
                      preco_minimo:
                        type: number
                        example: 10.0
                      preco_maximo:
                        type: number
                        example: 50.0
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
          content:
            application/json:
              schema:
                type: object
                properties:
                  estado:
                    type: string
                    example: sucesso
                  dados:
                    type: object
                    properties:
                      total_livros:
                        type: integer
                        example: 20
                      preco_medio:
                        type: number
                        example: 25.0
                      preco_minimo:
                        type: number
                        example: 15.0
                      preco_maximo:
                        type: number
                        example: 40.0
                      categoria:
                        type: string
                        example: Travel
        404:
          description: Categoria não encontrada
          content:
            application/json:
              schema:
                type: object
                properties:
                  estado:
                    type: string
                    example: erro
                  mensagem:
                    type: string
                    example: Categoria não encontrada
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
