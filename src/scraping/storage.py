# Funções simples para salvar e carregar dados
import pandas as pd


def salvar_dados(livros, arquivo='data/books.csv'):
    """Salva a lista de livros em um arquivo CSV"""
    df = pd.DataFrame(livros)
    df.to_csv(arquivo, index=False)
    print(f"Dados salvos em {arquivo}")


def carregar_dados(arquivo='data/books.csv'):
    """Carrega os livros do arquivo CSV"""
    df = pd.read_csv(arquivo)
    return df.to_dict('records')
