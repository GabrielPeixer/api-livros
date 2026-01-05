"""
Rotas da API para gerenciamento de livros.
Versão: v1
"""
import logging
from flask import Blueprint, request, Response
from typing import Tuple

from api.utils import (
    carregar_livros,
    paginar_lista,
    resposta_erro,
    resposta_sucesso,
)
from core.cache import cache

# Configura logging
logger = logging.getLogger(__name__)

router = Blueprint('books', __name__, url_prefix='/api/v1/books')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_books() -> Tuple[Response, int]:
    """
    Lista todos os livros disponíveis na base de dados.

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


@router.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id: int) -> Tuple[Response, int]:
    """
    Retorna detalhes completos de um livro específico pelo ID.

    ---
    get:
      description: Retorna detalhes de um livro específico
      parameters:
        - name: book_id
          in: path
          type: integer
          required: true
      responses:
        200:
          description: Livro encontrado
        404:
          description: Livro não encontrado
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()

        # Verifica se o ID é válido (1-indexed)
        if book_id < 1 or book_id > len(livros):
            logger.info(f"Livro não encontrado com ID: {book_id}")
            return resposta_erro('Livro não encontrado', codigo_status=404)

        # Retorna o livro pelo índice (ID é 1-indexed)
        livro = livros[book_id - 1]
        livro['id'] = book_id
        return resposta_sucesso(dados=livro)

    except Exception as e:
        logger.error(f"Erro ao buscar livro com ID {book_id}: {e}")
        return resposta_erro(
            "Erro interno ao processar a requisição.",
            codigo_status=500
        )


@router.route('/search', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def search_books() -> Tuple[Response, int]:
    """
    Busca livros por título e/ou categoria.

    ---
    get:
      description: Busca livros com filtros
      parameters:
        - name: title
          in: query
          type: string
          required: false
        - name: category
          in: query
          type: string
          required: false
      responses:
        200:
          description: Lista de livros encontrados
    """
    try:
        # Carrega a lista de livros
        livros = carregar_livros()

        # Pega os parâmetros de busca
        titulo_busca = request.args.get('title', '').strip().lower()
        categoria_busca = request.args.get('category', '').strip().lower()

        # Se não tiver nenhum parâmetro, retorna todos
        if not titulo_busca and not categoria_busca:
            return resposta_sucesso(
                dados=livros,
                meta={"total_resultados": len(livros)}
            )

        # Filtra os livros
        livros_filtrados = []
        for livro in livros:
            titulo_livro = livro.get('title', '').lower()
            categoria_livro = livro.get('category', '').lower()

            # Verifica se o título contém a busca
            titulo_match = not titulo_busca or titulo_busca in titulo_livro
            # Verifica se a categoria contém a busca
            categoria_match = (
                not categoria_busca or categoria_busca in categoria_livro
            )

            # Se ambos os critérios forem atendidos, adiciona
            if titulo_match and categoria_match:
                livros_filtrados.append(livro)

        return resposta_sucesso(
            dados=livros_filtrados,
            meta={"total_resultados": len(livros_filtrados)}
        )

    except Exception as e:
        logger.error(f"Erro ao buscar livros: {e}")
        return resposta_erro(
            "Erro interno ao processar a requisição.",
            codigo_status=500
        )
