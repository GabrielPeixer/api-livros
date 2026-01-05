# API de Livros 

API RESTful para consulta de dados de livros extraídos do site [Books to Scrape](https://books.toscrape.com/).

## Descrição do Projeto

Este projeto implementa um sistema completo de extração e consulta de dados de livros, composto por:

1. Web Scraping: Script automatizado que extrai dados de livros do site Books to Scrape
2. Armazenamento: Dados salvos localmente em arquivo CSV
3. API REST: Endpoints para consulta de livros, categorias e estatísticas
4. Documentação: Swagger UI para explorar e testar a API

## Arquitetura do Projeto

```
api-livros/
├── src/
│   ├── api/              # Código da API Flask
│   │   ├── main.py       # Ponto de entrada e factory
│   │   ├── utils.py      # Funções auxiliares
│   │   ├── schemas.py    # Esquemas de dados
│   │   └── routers/      # Endpoints organizados por domínio
│   │       ├── books.py  # Rotas de livros
│   │       ├── stats.py  # Rotas de estatísticas
│   │       └── health.py # Rotas de saúde
│   ├── scraping/         # Código de web scraping
│   │   ├── scraper.py    # Extrator de dados
│   │   ├── pipeline.py   # Pipeline de execução
│   │   └── storage.py    # Persistência em CSV
│   └── core/             # Configurações centrais
│       ├── config.py     # Variáveis de ambiente
│       ├── cache.py      # Cache com Flask-Caching
│       ├── db.py         # Configuração do banco
│       └── logging_config.py  # Configuração de logs
├── data/
│   └── books.csv         # Dados extraídos
├── docs/
│   ├── index.html        # Swagger UI
│   ├── openapi.yaml      # Especificação OpenAPI
│   └── openapi.json      # Especificação em JSON
├── tests/                # Testes automatizados
├── requirements.txt      # Dependências
└── README.md
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/GabrielPeixer/api-livros.git
cd api-livros
```

### 2. Criar Ambiente Virtual

Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Variáveis disponíveis:
```ini
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=True
SITE_URL=https://books.toscrape.com/
```

## Execução

### 1. Coletar Dados (Web Scraping)

```bash
python src/scraping/scraper.py
```

Os dados serão salvos em `data/books.csv`.

### 2. Iniciar a API

```bash
python src/api/main.py
```

A API estará disponível em `http://localhost:5000`.

### 3. Acessar Documentação

Abra `http://localhost:5000/docs` para acessar o Swagger UI.

## Documentação da API

### Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/books/` | Lista todos os livros (paginado) |
| `GET` | `/api/books/{title}` | Busca livro por título |
| `GET` | `/api/books/categories` | Lista todas as categorias |
| `GET` | `/api/stats/` | Estatísticas gerais |
| `GET` | `/api/stats/category/{category}` | Estatísticas por categoria |
| `GET` | `/api/health` | Verificação de saúde |
| `GET` | `/api/ping` | Teste de conectividade |

---

### `GET /api/books/`

Lista todos os livros com paginação.

Parâmetros de Query:
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `page` | integer | 1 | Número da página |
| `per_page` | integer | 20 | Itens por página |

Exemplo de Request:
```bash
curl "http://localhost:5000/api/books/?page=1&per_page=5"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": [
    {
      "title": "A Light in the Attic",
      "price": 51.77,
      "availability": "In stock",
      "rating": 3,
      "category": "Poetry"
    },
    {
      "title": "Tipping the Velvet",
      "price": 53.74,
      "availability": "In stock",
      "rating": 1,
      "category": "Historical Fiction"
    }
  ],
  "meta": {
    "pagina": 1,
    "por_pagina": 5,
    "total_itens": 100,
    "total_paginas": 20
  }
}
```

---

### `GET /api/books/{title}`

Busca um livro pelo título (case insensitive).

Parâmetros de Path:
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `title` | string | Título do livro |

Exemplo de Request:
```bash
curl "http://localhost:5000/api/books/A%20Light%20in%20the%20Attic"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": {
    "title": "A Light in the Attic",
    "price": 51.77,
    "availability": "In stock",
    "rating": 3,
    "category": "Poetry"
  }
}
```

Exemplo de Response (404 Not Found):
```json
{
  "estado": "erro",
  "mensagem": "Livro não encontrado"
}
```

---

### `GET /api/books/categories`

Lista todas as categorias disponíveis.

Exemplo de Request:
```bash
curl "http://localhost:5000/api/books/categories"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": [
    "Travel",
    "Mystery",
    "Historical Fiction",
    "Sequential Art",
    "Classics",
    "Philosophy",
    "Romance",
    "Poetry"
  ]
}
```

---

### `GET /api/stats/`

Retorna estatísticas gerais sobre todos os livros.

Exemplo de Request:
```bash
curl "http://localhost:5000/api/stats/"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": {
    "total_livros": 100,
    "preco_medio": 35.07,
    "preco_minimo": 10.00,
    "preco_maximo": 59.99
  }
}
```

---

### `GET /api/stats/category/{category}`

Retorna estatísticas de uma categoria específica.

Parâmetros de Path:
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `category` | string | Nome da categoria |

Exemplo de Request:
```bash
curl "http://localhost:5000/api/stats/category/Travel"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": {
    "total_livros": 11,
    "preco_medio": 42.50,
    "preco_minimo": 15.00,
    "preco_maximo": 55.00,
    "categoria": "Travel"
  }
}
```

Exemplo de Response (404 Not Found):
```json
{
  "estado": "erro",
  "mensagem": "Categoria não encontrada"
}
```

---

### `GET /api/health`

Verifica se a API está operacional.

Exemplo de Request:
```bash
curl "http://localhost:5000/api/health"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": {
    "servico": "api-livros",
    "estado": "operacional"
  }
}
```

---

### `GET /api/ping`

Teste simples de conectividade.

Exemplo de Request:
```bash
curl "http://localhost:5000/api/ping"
```

Exemplo de Response (200 OK):
```json
{
  "estado": "sucesso",
  "dados": "pong"
}
```

---

## Exemplos de Uso com Python

### Listar Livros

```python
import requests

response = requests.get('http://localhost:5000/api/books/', params={
    'page': 1,
    'per_page': 10
})

data = response.json()
print(f"Total de livros: {data['meta']['total_itens']}")

for livro in data['dados']:
    print(f"- {livro['title']} (£{livro['price']})")
```

### Buscar Livro por Título

```python
import requests

titulo = "A Light in the Attic"
response = requests.get(f'http://localhost:5000/api/books/{titulo}')

if response.status_code == 200:
    livro = response.json()['dados']
    print(f"Título: {livro['title']}")
    print(f"Preço: £{livro['price']}")
    print(f"Avaliação: {livro['rating']} estrelas")
else:
    print("Livro não encontrado")
```

### Obter Estatísticas

```python
import requests

response = requests.get('http://localhost:5000/api/stats/')
stats = response.json()['dados']

print(f"Total de livros: {stats['total_livros']}")
print(f"Preço médio: £{stats['preco_medio']:.2f}")
print(f"Preço mínimo: £{stats['preco_minimo']:.2f}")
print(f"Preço máximo: £{stats['preco_maximo']:.2f}")
```

### Estatísticas por Categoria

```python
import requests

categoria = "Travel"
response = requests.get(f'http://localhost:5000/api/stats/category/{categoria}')

if response.status_code == 200:
    stats = response.json()['dados']
    print(f"Categoria: {stats['categoria']}")
    print(f"Total de livros: {stats['total_livros']}")
    print(f"Preço médio: £{stats['preco_medio']:.2f}")
else:
    print("Categoria não encontrada")
```

## Testes

### Executar Testes

```bash
pytest tests/
```

### Verificar Estilo de Código

```bash
flake8 src tests
```

## Deploy

### Produção com Waitress (Windows)

```bash
pip install waitress
waitress-serve --port=5000 --call src.api.main:create_app
```

### Produção com Gunicorn (Linux)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.main:create_app()"
```

## Notas

- O scraping é limitado a 5 páginas por padrão (configurável no código)
- Os dados são salvos em `data/books.csv`
- A API roda na porta 5000 por padrão
- Cache de 5 minutos (300 segundos) em endpoints de listagem

## Licença

Este projeto está licenciado sob a licença MIT.
