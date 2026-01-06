"""
Rotas de saúde da API.
"""
import logging
from pathlib import Path
from flask import Blueprint

from api.utils import carregar_livros, resposta_sucesso

logger = logging.getLogger(__name__)

router = Blueprint('health', __name__, url_prefix='/api/v1')


@router.route('/health', methods=['GET'])
def health_check():
    """Verifica se a API está funcionando."""
    from core.config import Config
    data_file = Config.CSV_FILE
    dados_disponiveis = Path(data_file).exists()

    try:
        livros = carregar_livros()
        total_livros = len(livros)
        dados_status = "ok" if total_livros > 0 else "vazio"
    except Exception as e:
        logger.error(f"Erro ao verificar dados: {e}")
        dados_status = "erro"
        total_livros = 0

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

    return resposta_sucesso(dados=dados)


@router.route('/ping', methods=['GET'])
def ping():
    """Testa conexão com a API."""
    return resposta_sucesso(dados="pong")
