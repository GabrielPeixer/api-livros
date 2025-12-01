"""
Rotas da API para gerenciamento de livros.
"""
import logging
from flask import Blueprint, request, Response
from typing import Tuple

from api.utils import (
    carregar_livros,
    lista_categorias,
    paginar_lista,
    resposta_erro,
    resposta_sucesso,
)
from core.cache import cache

# Configura logging
logger = logging.getLogger(__name__)

router = Blueprint('books', __name__, url_prefix='/api/books')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_books() -> Tuple[Response, int]:
    """
    Lista todos os livros com paginação.

    ---
    get:
      description: Retorna lista paginada de livros
      parameters:
        - name: page
          in: query
          type: integer
          default: 1
        - name: per_page
          in: query
          type: integer
          default: 20
      responses:
        200:
          description: Lista de livros
          content:
            application/json:
              schema:
                type: object
                properties:
                  estado:
                    type: string
                    example: sucesso
                  dados:
                    type: array
                    items:
                      type: object
                      properties:
                        title:
                          type: string
                        price:
                          type: number
                        rating:
                          type: integer
                        availability:
                          type: string
                  meta:
                    type: object
                    properties:
                      pagina:
                        type: integer
                      por_pagina:
                        type: integer
                      total_itens:
                        type: integer
                      total_paginas:
                        type: integer
    """
    try:
        # Carrega a lista de livros do CSV
        livros = carregar_livros()

        # Se não tiver livros, retorna lista vazia
        if not livros:
            logger.info("Nenhum livro encontrado no banco de dados.")
            return resposta_sucesso(
                dados=[],
                meta={"pagina": 1, "total_itens": 0}
            )

        # Pega os parâmetros da requisição com validação básica
        try:
            pagina = int(request.args.get('page', 1))
            por_pagina = int(request.args.get('per_page', 20))

            if pagina < 1 or por_pagina < 1:
                raise ValueError("Paginação deve ser positiva.")

        except ValueError as e:
            logger.warning(f"Parâmetros de paginação inválidos: {e}")
            return resposta_erro(
                "Parâmetros de paginação inválidos. "
                "Devem ser inteiros positivos.",
                codigo_status=400
            )

        # Pagina a lista
        itens_pagina, meta = paginar_lista(livros, pagina, por_pagina)

        # Retorna a resposta de sucesso
        return resposta_sucesso(dados=itens_pagina, meta=meta)

    except Exception as e:
        logger.error(f"Erro ao listar livros: {e}")
        return resposta_erro(
            "Erro interno ao processar a requisição.",
            codigo_status=500
        )


@router.route('/<string:title>', methods=['GET'])
def get_book_by_title(title: str) -> Tuple[Response, int]:
    """
    Busca um livro pelo título.

    ---
    get:
      description: Retorna detalhes de um livro específico
      parameters:
        - name: title
          in: path
          type: string
          required: true
      responses:
        200:
          description: Livro encontrado
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
                      title:
                        type: string
                      price:
                        type: number
                      rating:
                        type: integer
                      availability:
                        type: string
        404:
          description: Livro não encontrado
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
                    example: Livro não encontrado
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()

        # Procura o livro pelo título (case insensitive)
        # Nota: Isso não é eficiente para grandes datasets,
        # idealmente usaríamos um banco de dados ou índice
        for livro in livros:
            if livro.get('title', '').lower() == title.lower():
                # Se encontrou, retorna o livro
                return resposta_sucesso(dados=livro)

        # Se não encontrou, retorna erro
        logger.info(f"Livro não encontrado: {title}")
        return resposta_erro('Livro não encontrado', codigo_status=404)

    except Exception as e:
        logger.error(f"Erro ao buscar livro '{title}': {e}")
        return resposta_erro(
            "Erro interno ao processar a requisição.",
            codigo_status=500
        )


@router.route('/categories', methods=['GET'])
def get_categories() -> Tuple[Response, int]:
    """
    Lista todas as categorias disponíveis.

    ---
    get:
      description: Retorna lista de categorias únicas
      responses:
        200:
          description: Lista de categorias
          content:
            application/json:
              schema:
                type: object
                properties:
                  estado:
                    type: string
                    example: sucesso
                  dados:
                    type: array
                    items:
                      type: string
                      example: Travel
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
