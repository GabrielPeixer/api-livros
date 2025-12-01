# Script simples para testar os endpoints da API
import requests
import json

# URL base da API
BASE_URL = "http://localhost:5000"

print("=" * 50)
print("TESTANDO A API DE LIVROS")
print("=" * 50)

# Teste 1: Health Check
print("\n1. Testando /api/health")
try:
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 2: Ping
print("\n2. Testando /api/ping")
try:
    response = requests.get(f"{BASE_URL}/api/ping")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 3: Listar livros (primeira página)
print("\n3. Testando /api/books/ (lista de livros)")
try:
    response = requests.get(f"{BASE_URL}/api/books/")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total de livros: {data.get('total', 0)}")
    print(f"   Livros nesta página: {len(data.get('data', []))}")
    if data.get('data'):
        print(f"   Primeiro livro: {data['data'][0].get('title', 'N/A')}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 4: Listar livros com paginação
print("\n4. Testando /api/books/?page=1&per_page=5")
try:
    response = requests.get(f"{BASE_URL}/api/books/?page=1&per_page=5")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Livros retornados: {len(data.get('data', []))}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 5: Categorias
print("\n5. Testando /api/books/categories")
try:
    response = requests.get(f"{BASE_URL}/api/books/categories")
    print(f"   Status: {response.status_code}")
    data = response.json()
    categorias = data.get('data', [])
    print(f"   Total de categorias: {len(categorias)}")
    if categorias:
        print(f"   Primeiras categorias: {categorias[:3]}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 6: Estatísticas
print("\n6. Testando /api/stats/")
try:
    response = requests.get(f"{BASE_URL}/api/stats/")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Estatísticas: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"   Erro: {e}")

print("\n" + "=" * 50)
print("TESTES CONCLUÍDOS!")
print("=" * 50)
