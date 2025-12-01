# Menu rápido para executar scraping, API ou limpar dados
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "books.csv"


def run_scraper():
    """Executa o script que coleta os livros."""
    print("\nExtraindo livros...")
    os.system("python src/scraping/scraper.py")


def run_api():
    """Inicia a API Flask."""
    print("\nSubindo API...")
    os.system("python src/api/main.py")


def run_both():
    """Roda scraping e depois sobe a API."""
    run_scraper()
    run_api()


def purge_data():
    """Apaga o CSV gerado pelo scraper."""
    if CSV_PATH.exists():
        CSV_PATH.unlink()
        print(f"Removido: {CSV_PATH}")
    else:
        print("Nenhum arquivo para remover.")


ACTIONS = {
    "1": ("Extrair dados", run_scraper),
    "2": ("Iniciar API", run_api),
    "3": ("Fazer tudo", run_both),
    "4": ("Purge (apagar CSV)", purge_data),
}


def show_menu():
    """Imprime o menu com as opções básicas."""
    print("\n=== API DE LIVROS ===")
    for key, (label, _) in ACTIONS.items():
        print(f"{key} - {label}")


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "purge":
        purge_data()
        return

    show_menu()
    choice = input("Escolha: ")
    action = ACTIONS.get(choice)

    if action:
        action[1]()
    else:
        print("Opção inválida")


if __name__ == "__main__":
    main()
