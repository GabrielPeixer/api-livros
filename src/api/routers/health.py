"""
Rotas para verificação de saúde da API.
"""
from flask import Blueprint, Response
from typing import Tuple

from api.utils import resposta_sucesso

router = Blueprint('health', __name__, url_prefix='/api')


@router.route('/health', methods=['GET'])
def health_check() -> Tuple[Response, int]:
    """
    Verifica se a API está funcionando.

    Returns:
        Tuple[Response, int]: Resposta JSON com status operacional.
    """
    # Cria os dados de saúde
    dados = {
        'servico': 'api-livros',
        'estado': 'operacional'
    }
    # Retorna resposta de sucesso
    return resposta_sucesso(dados=dados)


@router.route('/ping', methods=['GET'])
def ping() -> Tuple[Response, int]:
    """
    Testa a conexão com a API.

    ---
    get:
      description: Retorna pong para testar conectividade
      responses:
        200:
          description: Conexão OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  estado:
                    type: string
                    example: sucesso
                  dados:
                    type: string
                    example: pong
    """
    return resposta_sucesso(dados="pong")
