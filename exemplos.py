
# ============================================
# EXEMPLO 1: Como extrair livros do site
# ============================================

print("EXEMPLO 1: Extraindo livros do site")
print("-" * 40)

from scraping.scraper import extrair_livros, salvar_csv

# Extrai os livros
livros = extrair_livros()

# Mostra os primeiros 3 livros
print(f"Total extraído: {len(livros)} livros\n")
print("Primeiros 3 livros:")
for i, livro in enumerate(livros[:3], 1):
    print(f"{i}. {livro['title']} - £{livro['price']}")

# Salva em CSV
salvar_csv(livros)

print("\n")

# ============================================
# EXEMPLO 2: Como carregar os dados do CSV
# ============================================

print("EXEMPLO 2: Carregando dados do CSV")
print("-" * 40)

import pandas as pd

# Carrega o CSV
df = pd.read_csv('data/books.csv')

print(f"Total de livros: {len(df)}")
print(f"Preço médio: £{df['price'].mean():.2f}")
print(f"Livro mais caro: {df.loc[df['price'].idxmax(), 'title']}")
print(f"Livro mais barato: {df.loc[df['price'].idxmin(), 'title']}")

print("\n")

# ============================================
# EXEMPLO 3: Como filtrar livros
# ============================================

print("EXEMPLO 3: Filtrando livros")
print("-" * 40)

# Livros com rating 5
livros_5_estrelas = df[df['rating'] == 5]
print(f"Livros com 5 estrelas: {len(livros_5_estrelas)}")

# Livros mais baratos que £20
livros_baratos = df[df['price'] < 20]
print(f"Livros abaixo de £20: {len(livros_baratos)}")

# Livros disponíveis
livros_disponiveis = df[df['availability'] == 'In stock']
print(f"Livros em estoque: {len(livros_disponiveis)}")

print("\n")

# ============================================
# EXEMPLO 4: Como fazer paginação
# ============================================

print("EXEMPLO 4: Paginação de resultados")
print("-" * 40)

def paginar(lista, pagina=1, por_pagina=5):
    """Retorna apenas os itens de uma página"""
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    return lista[inicio:fim]

# Converte para lista
todos_livros = df.to_dict('records')

# Pega primeira página (5 livros)
pagina_1 = paginar(todos_livros, pagina=1, por_pagina=5)
print("Página 1 (primeiros 5 livros):")
for livro in pagina_1:
    print(f"  - {livro['title']}")

print("\n")

# ============================================
# EXEMPLO 5: Estatísticas simples
# ============================================

print("EXEMPLO 5: Calculando estatísticas")
print("-" * 40)

# Distribuição de ratings
print("Distribuição de avaliações:")
for rating in range(1, 6):
    qtd = len(df[df['rating'] == rating])
    print(f"  {rating} estrelas: {qtd} livros")

# Top 5 mais caros
print("\nTop 5 livros mais caros:")
top_5_caros = df.nlargest(5, 'price')
for idx, livro in top_5_caros.iterrows():
    print(f"  £{livro['price']:.2f} - {livro['title']}")

print("\n")

# ============================================
# EXEMPLO 6: Como usar a API (com requests)
# ============================================

print("EXEMPLO 6: Fazendo requisições à API")
print("-" * 40)
print("(Execute 'python src/api/main.py' em outro terminal primeiro!)")

import requests

# URL base da API
BASE_URL = "http://localhost:5000/api"

try:
    # Teste 1: Health check
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status da API: {response.json()['status']}")
    
    # Teste 2: Buscar livros
    response = requests.get(f"{BASE_URL}/books/?page=1&per_page=3")
    livros = response.json()
    print(f"\nTotal de livros: {livros['total']}")
    print(f"Mostrando página {livros['page']}:")
    for livro in livros['data']:
        print(f"  - {livro['title']}")
    
    # Teste 3: Estatísticas
    response = requests.get(f"{BASE_URL}/stats/")
    stats = response.json()
    print(f"\nPreço médio: £{stats['preco_medio']:.2f}")
    
except Exception as e:
    print(f"Erro: {e}")
    print("Certifique-se de que a API está rodando!")

print("\n" + "="*50)
print("FIM DOS EXEMPLOS")
print("="*50)
