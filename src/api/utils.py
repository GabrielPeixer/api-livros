"""
Funções utilitárias da API.
"""
import csv
import logging
from pathlib import Path
from statistics import mean

from flask import jsonify

from core.config import Config

logger = logging.getLogger(__name__)

# Caminho do arquivo CSV
CAMINHO_DADOS = Path(Config.CSV_FILE)


def resposta_sucesso(dados=None, meta=None, codigo_status=200):
    """Monta resposta de sucesso."""
    resposta = {
        "estado": "sucesso",
        "dados": dados if dados is not None else [],
    }
    if meta:
        resposta["meta"] = meta
    return jsonify(resposta), codigo_status


def resposta_erro(mensagem, codigo_status=400, detalhes=None):
    """Monta resposta de erro."""
    resposta = {
        "estado": "erro",
        "mensagem": mensagem,
    }
    if detalhes:
        resposta["detalhes"] = detalhes
    return jsonify(resposta), codigo_status


def _numero_flutuante_seguro(valor):
    """Converte valor para float."""
    try:
        return float(valor)
    except (ValueError, TypeError):
        return 0.0


def _numero_inteiro_seguro(valor):
    """Converte valor para int."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0


def carregar_livros():
    """Lê os livros do arquivo CSV."""
    if not CAMINHO_DADOS.exists():
        logger.warning(f"Arquivo não encontrado: {CAMINHO_DADOS}")
        return []

    livros = []
    try:
        with CAMINHO_DADOS.open("r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                linha["price"] = _numero_flutuante_seguro(linha.get("price"))
                linha["rating"] = _numero_inteiro_seguro(linha.get("rating"))
                livros.append(linha)
    except Exception as e:
        logger.error(f"Erro ao ler CSV: {e}")
        return []

    return livros


def paginar_lista(itens, pagina, por_pagina):
    """Pagina uma lista de itens."""
    total = len(itens)
    
    if por_pagina:
        total_paginas = max(1, (total + por_pagina - 1) // por_pagina)
    else:
        total_paginas = 1
    
    inicio = max(0, (pagina - 1) * por_pagina)
    fim = inicio + por_pagina if por_pagina else total
    
    return itens[inicio:fim], {
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_itens": total,
        "total_paginas": total_paginas,
    }


def lista_categorias(itens):
    """Extrai categorias únicas dos itens."""
    categorias = set()
    for item in itens:
        categoria = item.get("category", "")
        if categoria:
            categorias.add(categoria)
    return sorted(list(categorias))


def estatisticas_precos(itens):
    """Calcula estatísticas de preços."""
    if not itens:
        return {
            "total_livros": 0,
            "preco_medio": 0,
            "preco_minimo": 0,
            "preco_maximo": 0
        }

    valores = []
    for item in itens:
        preco = item.get("price", 0)
        if isinstance(preco, (int, float)):
            valores.append(preco)

    if not valores:
        return {
            "total_livros": len(itens),
            "preco_medio": 0,
            "preco_minimo": 0,
            "preco_maximo": 0
        }

    return {
        "total_livros": len(itens),
        "preco_medio": round(mean(valores), 2),
        "preco_minimo": min(valores),
        "preco_maximo": max(valores),
    }
