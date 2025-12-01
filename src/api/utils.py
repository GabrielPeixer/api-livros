"""
Funções utilitárias usadas nos roteadores da API.
"""
from __future__ import annotations

import csv
import logging
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Tuple, Optional

from flask import jsonify, Response

from core.config import Config

# Configura logging
logger = logging.getLogger(__name__)

# Caminho fixo para o CSV usado pela API inteira
# Usa a configuração centralizada
CAMINHO_DADOS = Path(Config.CSV_FILE)


def resposta_sucesso(
    dados: Any = None,
    meta: Optional[Dict[str, Any]] = None,
    codigo_status: int = 200
) -> Tuple[Response, int]:
    """
    Monta a resposta padronizada de sucesso.

    Args:
        dados (Any): Os dados a serem retornados.
        meta (Optional[Dict[str, Any]]): Metadados opcionais (ex: paginação).
        codigo_status (int): O código de status HTTP.

    Returns:
        Tuple[Response, int]: A resposta JSON e o código de status.
    """
    # Cria um dicionário com o status e os dados
    resposta = {
        "estado": "sucesso",
        "dados": dados if dados is not None else [],
    }
    # Se tiver metadados, adiciona na resposta
    if meta:
        resposta["meta"] = meta
    # Retorna o JSON e o código de status
    return jsonify(resposta), codigo_status


def resposta_erro(
    mensagem: str,
    codigo_status: int = 400,
    detalhes: Optional[Any] = None
) -> Tuple[Response, int]:
    """
    Formata respostas de erro com um esquema simples.

    Args:
        mensagem (str): A mensagem de erro.
        codigo_status (int): O código de status HTTP.
        detalhes (Optional[Any]): Detalhes adicionais sobre o erro.

    Returns:
        Tuple[Response, int]: A resposta JSON e o código de status.
    """
    # Cria um dicionário com o status de erro e a mensagem
    resposta = {
        "estado": "erro",
        "mensagem": mensagem,
    }
    # Se tiver detalhes, adiciona na resposta
    if detalhes:
        resposta["detalhes"] = detalhes
    # Retorna o JSON e o código de status
    return jsonify(resposta), codigo_status


def _numero_flutuante_seguro(valor: Any) -> float:
    """Converte valor para float de forma segura."""
    try:
        return float(valor)
    except (ValueError, TypeError):
        return 0.0


def _numero_inteiro_seguro(valor: Any) -> int:
    """Converte valor para int de forma segura."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0


def carregar_livros() -> List[Dict[str, Any]]:
    """
    Lê o CSV linha por linha usando apenas a biblioteca padrão.

    Returns:
        List[Dict[str, Any]]: Lista de livros carregados.
    """
    # Verifica se o arquivo existe
    if not CAMINHO_DADOS.exists():
        logger.warning(f"Arquivo de dados não encontrado em: {CAMINHO_DADOS}")
        # Se não existe, retorna lista vazia
        return []

    # Lista para guardar os livros
    livros = []
    try:
        # Abre o arquivo CSV para leitura
        with CAMINHO_DADOS.open("r", encoding="utf-8") as arquivo_csv:
            # Cria um leitor de CSV que lê como dicionários
            leitor = csv.DictReader(arquivo_csv)
            # Para cada linha no CSV
            for linha in leitor:
                # Normaliza os tipos dos campos para que as rotas consigam
                # calcular estatísticas depois
                linha["price"] = _numero_flutuante_seguro(linha.get("price"))

                linha["rating"] = _numero_inteiro_seguro(linha.get("rating"))
                # Adiciona a linha na lista de livros
                livros.append(linha)
    except Exception as e:
        logger.error(f"Erro ao ler arquivo CSV: {e}")
        return []

    # Retorna a lista de livros
    return livros


def paginar_lista(
    itens: List[Dict[str, Any]],
    pagina: int,
    por_pagina: int
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Faz um slice simples da lista e devolve metadados de paginação.

    Args:
        itens (List[Dict[str, Any]]): A lista completa de itens.
        pagina (int): O número da página atual.
        por_pagina (int): O número de itens por página.

    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, int]]: Os itens da página e
                                                     os metadados.
    """

    # Calcula o total de itens
    total = len(itens)
    # Calcula o total de páginas
    if por_pagina:
        total_paginas = max(1, (total + por_pagina - 1) // por_pagina)
    else:
        total_paginas = 1
    # Calcula o início do slice
    inicio = max(0, (pagina - 1) * por_pagina)
    # Calcula o fim do slice
    fim = inicio + por_pagina if por_pagina else total
    # Retorna o slice e os metadados
    return itens[inicio:fim], {
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_itens": total,
        "total_paginas": total_paginas,
    }


def lista_categorias(itens: List[Dict[str, Any]]) -> List[str]:
    """
    Extrai categorias únicas (se existirem).

    Args:
        itens (List[Dict[str, Any]]): A lista de itens.

    Returns:
        List[str]: Lista ordenada de categorias únicas.
    """
    # Cria um conjunto para evitar duplicatas
    categorias = set()
    # Para cada item na lista
    for item in itens:
        # Pega a categoria, se existir
        categoria = item.get("category", "")
        if categoria:
            # Adiciona no conjunto
            categorias.add(categoria)
    # Converte para lista ordenada
    return sorted(list(categorias))


def estatisticas_precos(itens: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula estatísticas simples sobre os preços.

    Args:
        itens (List[Dict[str, Any]]): Lista de livros.

    Returns:
        Dict[str, Any]: Dicionário com estatísticas.
    """
    # Se não tiver itens, retorna zeros
    if not itens:
        return {
            "total_livros": 0,
            "preco_medio": 0,
            "preco_minimo": 0,
            "preco_maximo": 0
        }

    # Lista para guardar os valores válidos
    valores = []
    # Para cada item
    for item in itens:
        # Pega o preço
        preco = item.get("price", 0)
        # Se for número, adiciona na lista
        if isinstance(preco, (int, float)):
            valores.append(preco)

    # Se não tiver valores válidos, retorna zeros
    if not valores:
        return {
            "total_livros": len(itens),
            "preco_medio": 0,
            "preco_minimo": 0,
            "preco_maximo": 0
        }

    # Calcula as estatísticas
    return {
        "total_livros": len(itens),
        "preco_medio": float(mean(valores)),
        "preco_minimo": float(min(valores)),
        "preco_maximo": float(max(valores)),
    }
