"""
Módulo para extração de dados de livros do site Books to Scrape.
"""
import csv
import logging
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

# Ajusta o path para permitir importar o módulo de configurações
# Idealmente, este script deve ser executado como um módulo
# (python -m src.scraping.scraper)
caminho_src = Path(__file__).resolve().parents[1]
if str(caminho_src) not in sys.path:
    sys.path.insert(0, str(caminho_src))

from core import config  # noqa: E402
from core.logging_config import setup_logging  # noqa: E402

# Inicializa o logging
setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)

# Constantes
MAX_PAGINAS = 5
TIMEOUT_REQUISICAO = 10
SEGUNDOS_PAUSA = 1
MAPEAMENTO_RATING = {
    'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}


def _carregar_robots(url_base: str) -> Optional[RobotFileParser]:
    """
    Baixa e analisa o arquivo robots.txt para respeitar as regras do site.

    Args:
        url_base (str): A URL base do site.

    Returns:
        Optional[RobotFileParser]: O objeto parser ou None se falhar.
    """
    robots = RobotFileParser()
    robots_url = urljoin(url_base, "robots.txt")
    try:
        logger.info(f"Buscando robots.txt de {robots_url}")
        robots.set_url(robots_url)
        robots.read()
        return robots
    except Exception as e:
        logger.warning(f"Não foi possível ler robots.txt: {e}")
        return None


def _processar_pagina(
    soup: BeautifulSoup,
    base_url: Optional[str] = None,
    session: Optional[requests.Session] = None
) -> List[Dict[str, Any]]:
    """
    Extrai dados dos livros de uma página HTML analisada.

    Args:
        soup (BeautifulSoup): O conteúdo HTML analisado.
        base_url (Optional[str]): A URL da página atual
                                  (para resolver links relativos).
        session (Optional[requests.Session]): A sessão de requests
                                              para buscar detalhes.

    Returns:
        List[Dict[str, Any]]: Uma lista de dicionários contendo
                              dados dos livros.
    """
    itens = []
    produtos = soup.select('article.product_pod')

    for livro in produtos:
        try:
            titulo = livro.h3.a.get('title', '').strip()

            preco_bruto = livro.select_one('p.price_color').text.replace(
                '£', ''
            ).strip()
            try:
                preco = float(preco_bruto)
            except ValueError:
                logger.warning(
                    f"Formato de preço inválido para '{titulo}': {preco_bruto}"
                )
                preco = 0.0

            disponibilidade = livro.select_one(
                'p.instock.availability'
            ).text.strip()

            tag_rating = livro.select_one('p.star-rating')
            if tag_rating and len(tag_rating['class']) > 1:
                classe_rating = tag_rating['class'][1]
            else:
                classe_rating = 'Zero'
            rating = MAPEAMENTO_RATING.get(classe_rating, 0)

            # Opcional: Buscar categoria da página de detalhes
            categoria = ''
            link_rel = (
                livro.h3.a.get('href') if livro.h3 and livro.h3.a else ''
            )

            if base_url and session and link_rel:
                try:
                    detalhe_url = urljoin(base_url, link_rel)
                    # Usa um timeout curto para detalhes para não atrasar muito
                    detalhe = session.get(
                        detalhe_url, timeout=TIMEOUT_REQUISICAO
                    )
                    if detalhe.status_code == 200:
                        detalhe_soup = BeautifulSoup(
                            detalhe.text, 'html.parser'
                        )
                        breadcrumb_anchors = detalhe_soup.select(
                            'ul.breadcrumb li a'
                        )
                        if len(breadcrumb_anchors) >= 3:
                            categoria = breadcrumb_anchors[-1].text.strip()
                        elif len(breadcrumb_anchors) > 1:
                            categoria = breadcrumb_anchors[1].text.strip()
                except Exception as e:
                    logger.debug(
                        f"Falha ao buscar categoria para '{titulo}': {e}"
                    )

            itens.append({
                'title': titulo,
                'price': preco,
                'availability': disponibilidade,
                'rating': rating,
                'category': categoria
            })

        except Exception as e:
            logger.error(f"Erro ao processar item do livro: {e}")
            continue

    return itens


def extrair_livros(
    max_paginas: int = MAX_PAGINAS
) -> List[Dict[str, Any]]:
    """
    Percorre as páginas do site e extrai dados dos livros.

    Args:
        max_paginas (int): O número máximo de páginas para percorrer.

    Returns:
        List[Dict[str, Any]]: Uma lista de todos os livros extraídos.
    """
    url_base = config.SITE_URL.rstrip('/') + '/'
    sessao = requests.Session()
    sessao.headers['User-Agent'] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )

    robots = _carregar_robots(url_base)
    livros = []

    logger.info(
        f"Iniciando extração de {url_base} por {max_paginas} páginas."
    )

    for pagina in range(1, max_paginas + 1):
        url_pagina = urljoin(url_base, f"catalogue/page-{pagina}.html")

        if robots and not robots.can_fetch('*', url_pagina):
            logger.warning(
                f"Pulando {url_pagina} (não permitido por robots.txt)"
            )
            continue

        try:
            logger.info(f"Extraindo página {pagina}: {url_pagina}")
            resposta = sessao.get(url_pagina, timeout=TIMEOUT_REQUISICAO)
            resposta.raise_for_status()

            soup = BeautifulSoup(resposta.text, 'html.parser')
            novos_livros = _processar_pagina(soup, url_pagina, sessao)
            livros.extend(novos_livros)

            logger.info(
                f"Encontrados {len(novos_livros)} livros na página {pagina}."
            )

            time.sleep(SEGUNDOS_PAUSA)

        except requests.RequestException as erro:
            logger.error(f"Erro ao acessar {url_pagina}: {erro}")
            # Decide se para ou continua.
            # Parar pode ser mais seguro se o site estiver fora do ar.
            break

    logger.info(f"Total de livros extraídos: {len(livros)}")
    return livros


def salvar_csv(
    livros: List[Dict[str, Any]],
    arquivo: str = str(config.CSV_FILE)
) -> None:
    """
    Salva a lista de livros em um arquivo CSV.

    Args:
        livros (List[Dict[str, Any]]): A lista de livros para salvar.
        arquivo (str): O caminho para o arquivo CSV de saída.
    """
    if not livros:
        logger.warning("Nenhum dado para salvar.")
        return

    caminho = Path(arquivo)
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with caminho.open('w', encoding='utf-8', newline='') as arquivo_csv:
            fieldnames = livros[0].keys()
            escritor = csv.DictWriter(arquivo_csv, fieldnames=fieldnames)
            escritor.writeheader()
            escritor.writerows(livros)

        logger.info(f"Dados salvos com sucesso em {arquivo}")

    except IOError as e:
        logger.error(f"Erro ao salvar CSV: {e}")


if __name__ == "__main__":
    dados = extrair_livros()
    salvar_csv(dados)
