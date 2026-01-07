"""
Rotas para gerenciamento de livros.
"""
import logging
from flask import Blueprint, request

from api.utils import (
    carregar_livros,
    paginar_lista,
    resposta_erro,
    resposta_sucesso,
)
from core.cache import cache

logger = logging.getLogger(__name__)

router = Blueprint('books', __name__, url_prefix='/api/v1/books')


@router.route('/', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_books():
    """Lista todos os livros com paginação."""
    try:
        livros = carregar_livros()

        if not livros:
            return resposta_sucesso(
                dados=[],
                meta={"pagina": 1, "total_itens": 0}
            )

        # Pega parâmetros de paginação
        try:
            pagina = int(request.args.get('page', 1))
            por_pagina = int(request.args.get('per_page', 20))

            if pagina < 1 or por_pagina < 1:
                raise ValueError("Valores inválidos")

        except ValueError:
            return resposta_erro(
                "Parâmetros de paginação inválidos",
                codigo_status=400
            )

        itens_pagina, meta = paginar_lista(livros, pagina, por_pagina)
        return resposta_sucesso(dados=itens_pagina, meta=meta)

    except Exception as e:
        logger.error(f"Erro ao listar livros: {e}")
        return resposta_erro("Erro interno", codigo_status=500)


@router.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """Retorna um livro pelo ID."""
    try:
        livros = carregar_livros()

        if book_id < 1 or book_id > len(livros):
            return resposta_erro('Livro não encontrado', codigo_status=404)

        livro = livros[book_id - 1]
        livro['id'] = book_id
        return resposta_sucesso(dados=livro)

    except Exception as e:
        logger.error(f"Erro ao buscar livro {book_id}: {e}")
        return resposta_erro("Erro interno", codigo_status=500)


@router.route('/search', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def search_books():
    """Busca livros por título ou categoria."""
    try:
        livros = carregar_livros()

        titulo = request.args.get('title', '').strip().lower()
        categoria = request.args.get('category', '').strip().lower()

        # Se não tem filtro, retorna todos
        if not titulo and not categoria:
            return resposta_sucesso(
                dados=livros,
                meta={"total_resultados": len(livros)}
            )

        # Filtra os livros
        resultado = []
        for livro in livros:
            titulo_livro = livro.get('title', '').lower()
            categoria_livro = livro.get('category', '').lower()

            titulo_ok = not titulo or titulo in titulo_livro
            categoria_ok = not categoria or categoria in categoria_livro

            if titulo_ok and categoria_ok:
                resultado.append(livro)

        return resposta_sucesso(
            dados=resultado,
            meta={"total_resultados": len(resultado)}
        )

    except Exception as e:
        logger.error(f"Erro ao buscar livros: {e}")
        return resposta_erro("Erro interno", codigo_status=500)
