# Testes simples para verificar se tudo funciona

import os
import sys

# Adiciona o diretório src ao path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🧪 TESTANDO O PROJETO\n")
print("=" * 50)

# Teste 1: Verifica se o CSV existe
print("\n✓ Teste 1: Verificando se o arquivo de dados existe...")
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'books.csv')
if os.path.exists(csv_path):
    print("  ✅ Arquivo books.csv encontrado!")
else:
    print("  ❌ Arquivo não encontrado. Execute o scraper primeiro!")
    print("     python src/scraping/scraper.py")

# Teste 2: Tenta carregar os dados
print("\n✓ Teste 2: Tentando carregar os dados...")
try:
    import pandas as pd
    df = pd.read_csv(csv_path)
    print(f"  ✅ {len(df)} livros carregados com sucesso!")
    print(f"  Colunas: {', '.join(df.columns.tolist())}")
except Exception as e:
    print(f"  ❌ Erro ao carregar: {e}")

# Teste 3: Verifica se o Flask está instalado
print("\n✓ Teste 3: Verificando bibliotecas instaladas...")
try:
    import flask
    print(f"  ✅ Flask versão {flask.__version__}")
except ImportError:
    print("  ❌ Flask não instalado. Execute: pip install flask")

try:
    import pandas
    print(f"  ✅ Pandas versão {pandas.__version__}")
except ImportError:
    print("  ❌ Pandas não instalado. Execute: pip install pandas")

try:
    import requests
    print(f"  ✅ Requests versão {requests.__version__}")
except ImportError:
    print("  ❌ Requests não instalado. Execute: pip install requests")

try:
    import bs4  # noqa: F401
    print("  ✅ BeautifulSoup instalado")
except ImportError:
    print(
        "  ❌ BeautifulSoup não instalado. Execute: pip install beautifulsoup4"
    )


# Teste 4: Verifica estrutura de pastas
print("\n✓ Teste 4: Verificando estrutura do projeto...")
folders = ['src', 'src/api', 'src/scraping', 'data']
for folder in folders:
    path = os.path.join(os.path.dirname(__file__), '..', folder)
    if os.path.exists(path):
        print(f"  ✅ Pasta '{folder}' existe")
    else:
        print(f"  ❌ Pasta '{folder}' não encontrada")

print("\n" + "=" * 50)
print("🎉 TESTES CONCLUÍDOS!")
print("\nPróximos passos:")
print("1. Se há erros, corrija-os")
print("2. Execute: python src/scraping/scraper.py")
print("3. Execute: python src/api/main.py")
print("4. Acesse: http://localhost:5000/api/health")
