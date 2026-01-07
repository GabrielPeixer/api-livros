"""
Rotas para Machine Learning.
"""
import logging
from flask import Blueprint, request

from api.utils import carregar_livros, resposta_sucesso, resposta_erro
from core.cache import cache

logger = logging.getLogger(__name__)

router = Blueprint('ml', __name__, url_prefix='/api/v1/ml')

# Mapeamento de rating texto para número
RATING_MAP = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}


def extrair_features(livro):
    """Extrai features de um livro para ML."""
    # Pega o rating como número
    rating_texto = livro.get('rating', 'One')
    if isinstance(rating_texto, int):
        rating = rating_texto
    else:
        rating = RATING_MAP.get(rating_texto, 1)

    # Pega o preço
    preco = livro.get('price', 0.0)
    if isinstance(preco, str):
        preco = float(preco.replace('£', ''))

    # Verifica se tem estoque
    disponibilidade = livro.get('availability', '')
    em_estoque = 'in stock' in disponibilidade.lower() if disponibilidade else False

    return {
        'id': livro.get('id', 0),
        'titulo': livro.get('title', ''),
        'categoria': livro.get('category', 'Desconhecida'),
        'preco': round(preco, 2),
        'rating': rating,
        'em_estoque': em_estoque
    }


@router.route('/features', methods=['GET'])
@cache.cached(timeout=300)
def get_features():
    """Retorna features dos livros para ML."""
    try:
        livros = carregar_livros()

        if not livros:
            return resposta_erro("Nenhum livro encontrado", codigo_status=404)

        # Pega limit e offset da query
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Aplica offset e limit
        livros_filtrados = livros[offset:]
        if limit:
            livros_filtrados = livros_filtrados[:limit]

        # Extrai features
        features = []
        for livro in livros_filtrados:
            features.append(extrair_features(livro))

        return resposta_sucesso(dados={
            "total": len(livros),
            "retornados": len(features),
            "features": features
        })

    except Exception as e:
        logger.error(f"Erro ao extrair features: {e}")
        return resposta_erro("Erro ao processar", codigo_status=500)


@router.route('/training-data', methods=['GET'])
@cache.cached(timeout=300)
def get_training_data():
    """Retorna dados para treinar modelo de ML."""
    try:
        livros = carregar_livros()

        if not livros:
            return resposta_erro("Nenhum livro encontrado", codigo_status=404)

        # Monta as features e labels
        features = []
        labels = []

        for livro in livros:
            f = extrair_features(livro)
            # Vetor de features simples
            features.append([f['preco'], f['rating']])
            labels.append(f['rating'])

        # Qual campo é o target
        target = request.args.get('target', default='rating')
        if target == 'price':
            labels = [extrair_features(l)['preco'] for l in livros]

        return resposta_sucesso(dados={
            "features": features,
            "labels": labels,
            "num_amostras": len(features),
            "colunas": ["preco", "rating"]
        })

    except Exception as e:
        logger.error(f"Erro ao preparar training data: {e}")
        return resposta_erro("Erro ao processar", codigo_status=500)


@router.route('/predictions', methods=['POST'])
def receive_predictions():
    """Recebe predições de um modelo externo."""
    try:
        # Valida se tem JSON
        if not request.is_json:
            return resposta_erro("Precisa enviar JSON", codigo_status=400)

        dados = request.get_json()

        # Valida campos obrigatórios
        if 'model_name' not in dados:
            return resposta_erro(
                "Campo 'model_name' é obrigatório",
                codigo_status=400
            )

        if 'predictions' not in dados:
            return resposta_erro(
                "Campo 'predictions' é obrigatório",
                codigo_status=400
            )

        # Pega os dados
        model_name = dados['model_name']
        predictions = dados['predictions']

        if not isinstance(predictions, list):
            return resposta_erro(
                "'predictions' deve ser uma lista",
                codigo_status=400
            )

        logger.info(
            f"Recebido {len(predictions)} predições do modelo {model_name}"
        )

        return resposta_sucesso(dados={
            "mensagem": "Predições recebidas",
            "modelo": model_name,
            "quantidade": len(predictions)
        })

    except Exception as e:
        logger.error(f"Erro ao receber predições: {e}")
        return resposta_erro("Erro ao processar", codigo_status=500)
