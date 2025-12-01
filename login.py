"""Fluxo simples de login com chave de ativação.
O usuário digita a chave no terminal e o script valida com os valores da configuração.
"""
import os
import sys
from getpass import getpass

BASE_DIR = os.path.dirname(__file__)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.core import config


def solicitar_chave():
    """Pede a chave de ativação ao usuário usando input mascarado."""
    try:
        return getpass("Digite sua chave de ativação: ")
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
        return None


def validar_chave():
    tentativas = 3
    while tentativas > 0:
        chave = solicitar_chave()
        if chave is None:
            return False
        if not chave.strip():
            print("A chave não pode estar vazia. Tente novamente.\n")
            tentativas -= 1
            continue
        if chave.strip() == config.ACTIVATION_KEY:
            print("Acesso liberado! Chave válida.")
            return True
        print("Chave incorreta. Verifique se recebeu a chave certa e tente novamente.\n")
        tentativas -= 1
    print("Número máximo de tentativas atingido. Aguarde um momento antes de tentar de novo.")
    return False


if __name__ == "__main__":
    validar_chave()
