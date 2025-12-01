# API de Recomendação de Livros

Este projeto fornece uma API para consultar dados de livros extraídos do site [Books to Scrape](https://books.toscrape.com/). O projeto foi refatorado seguindo boas práticas de desenvolvimento Python.

## Estrutura do Projeto

- `src/api`: Código da API Flask.
- `src/core`: Configurações centrais e utilitários.
- `src/scraping`: Scripts de web scraping.
- `data`: Armazenamento de dados (CSV).
- `tests`: Testes automatizados.

## Configuração do Ambiente

### 1. Pré-requisitos

- Python 3.8 ou superior.
- Git.

### 2. Criar um Ambiente Virtual

Recomendamos o uso de um ambiente virtual para isolar as dependências.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo `.env.example` para `.env` e ajuste conforme necessário.

```bash
cp .env.example .env
```

Exemplo de variáveis no `.env`:
```ini
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=True
SITE_URL=https://books.toscrape.com/
```

## Execução

### 1. Coleta de Dados (Scraping)

Para coletar os dados dos livros e salvar em `data/books.csv`:

```bash
python src/scraping/scraper.py
```

### 2. Executar a API

Para iniciar o servidor de desenvolvimento:

```bash
python src/api/main.py
```

A API estará disponível em `http://localhost:5000`.

## Documentação da API

A documentação interativa (Swagger UI) está disponível em:
`http://localhost:5000/docs`

## Testes

Para executar os testes automatizados:

```bash
pytest
```

Para verificar o estilo do código (Linting):

```bash
flake8 src tests
```

## Deploy

Para implantar em produção:

1.  Certifique-se de que `DEBUG=False` no arquivo `.env`.
2.  Use um servidor WSGI como Gunicorn ou Waitress (Windows).

**Exemplo com Waitress (Windows):**
```bash
pip install waitress
waitress-serve --port=5000 --call src.api.main:create_app
```

**Exemplo com Gunicorn (Linux):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.main:create_app()"
```

## Desenvolvimento

- **Linting:** O código segue o estilo PEP 8. Recomendamos usar `flake8` ou `black` para manter a consistência.
- **Logs:** Logs estruturados são gerados no console e (opcionalmente) em arquivos, configurados em `src/core/logging_config.py`.
- `GET /api/stats/` - Mostra estatísticas gerais (total de livros, preços, etc)
- `GET /api/stats/category/<categoria>` - Estatísticas de uma categoria específica

## Estrutura do Projeto

```
book-recommendation-api/
├── src/
│   ├── api/              # Código da API Flask
│   │   ├── main.py       # Arquivo principal da API
│   │   └── routers/      # Rotas/endpoints
│   ├── scraping/         # Código de web scraping
│   │   ├── scraper.py    # Script que extrai os dados
│   │   └── storage.py    # Salva os dados em CSV
│   └── core/             # Configurações
├── data/
│   └── books.csv         # Dados extraídos
├── docs/
│   └── openapi.yaml      # Documentação da API
├── tests/                # Testes
└── requirements.txt      # Bibliotecas necessárias
```

## O que o projeto faz?

1. Web Scraping: Extrai dados de livros do site books.toscrape.com
2. Armazena em CSV**: Salva os dados localmente para consulta
3. API REST: Disponibiliza os dados através de endpoints HTTP
4. Documentação: Swagger automático para testar a API

## Exemplos de Uso

### Listar livros (com Python)
```python
import requests

response = requests.get('http://localhost:5000/api/books/')
livros = response.json()
print(livros)
```

### Ver estatísticas
```python
import requests

response = requests.get('http://localhost:5000/api/stats/')
stats = response.json()
print(f"Total de livros: {stats['total_livros']}")
print(f"Preço médio: {stats['preco_medio']}")
```

## Rodar os testes

```bash
pytest tests/
```

## Notas

- O scraping é limitado a 5 páginas por padrão (pode mudar no código)
- Os dados são salvos em `data/books.csv`
- A API roda na porta 5000
