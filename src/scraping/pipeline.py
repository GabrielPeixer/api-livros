# Pipeline completo: extrai dados e salva em CSV
from scraping.scraper import extrair_livros, salvar_csv


def executar_pipeline():
    """
    Executa todo o processo de coleta de dados:
    1. Extrai os livros do site
    2. Salva em CSV
    """
    print("=== INICIANDO PIPELINE DE DADOS ===")

    # Passo 1: Extrai os dados
    print("\n[1/2] Extraindo dados do site...")
    livros = extrair_livros()

    # Passo 2: Salva em CSV
    print("\n[2/2] Salvando dados...")
    salvar_csv(livros)

    print("\n=== PIPELINE CONCLUÍDO COM SUCESSO ===")


if __name__ == "__main__":
    executar_pipeline()
