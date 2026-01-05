"""
Rotas para verificação de saúde da API.
Versão: v1
"""
import logging
from pathlib import Path
from flask import Blueprint, Response
from typing import Tuple

from api.utils import carregar_livros, resposta_sucesso

# Configura logging
logger = logging.getLogger(__name__)

router = Blueprint('health', __name__, url_prefix='/api/v1')


@router.route('/health', methods=['GET'])
def health_check() -> Tuple[Response, int]:
    """
    Verifica status da API e conectividade com os dados.

    Returns:
        Tuple[Response, int]: Resposta JSON com status operacional.
    """
    # Verifica se o arquivo de dados existe
    from core.config import Config
    data_file = Config.CSV_FILE
    dados_disponiveis = Path(data_file).exists()

    # Tenta carregar os livros para verificar conectividade
    try:
        livros = carregar_livros()
        total_livros = len(livros)
        dados_status = "ok" if total_livros > 0 else "vazio"
    except Exception as e:
        logger.error(f"Erro ao verificar dados: {e}")
        dados_status = "erro"
        total_livros = 0

    # Cria os dados de saúde
    dados = {
        'servico': 'api-livros',
        'versao': 'v1',
        'estado': 'operacional',
        'dados': {
            'arquivo_existe': dados_disponiveis,
            'status': dados_status,
            'total_registros': total_livros
        }
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
    """
    return resposta_sucesso(dados="pong")
