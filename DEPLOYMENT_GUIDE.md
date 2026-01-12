# Guia de Deploy - API de Livros

## Deploy Rápido no Railway

### Método 1: UI do Railway (Mais Fácil)

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha o repositório `GabrielPeixer/api-livros`
6. Railway fará tudo automaticamente:
   - Detecta o `Dockerfile`
   - Faz build da imagem
   - Faz deploy do container
   - Atribui domínio público
7. Acesse: `https://api-livros-xxxx.railway.app/docs`

### Método 2: CLI do Railway

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy a partir do repositório local
railway up
```

---

## Variáveis de Ambiente

As variáveis de environment já estão configuradas no **Dockerfile** para production:

```dockerfile
ENV FLASK_ENV=production
ENV DEBUG=False
ENV API_HOST=0.0.0.0
ENV API_PORT=5000
```

Você pode sobrescrever no Railway dashboard se necessário, na aba **Variables**.

## Estrutura de Deployment

```
Seu Repositório GitHub
        ↓
Railway Pull do código
        ↓
Detecta Dockerfile
        ↓
Build da imagem Docker
        ↓
Cria container
        ↓
Executa aplicação
        ↓
Expõe em URL pública
```

---

## Verificar se está funcionando

```bash
curl https://api-livros-xxxx.railway.app/api/v1/health
```

Resposta esperada:
```json
{
  "estado": "sucesso",
  "dados": {
    "servico": "api-livros",
    "versao": "v1",
    "estado": "operacional"
  }
}
```

---

## Logs e Monitoramento

No dashboard do Railway:
- Deployments: Histórico de deploys
- Logs: Logs em tempo real do container
- Metrics: CPU, memória, requisições
- Settings: Redeploy, remover projeto

---

## Atualizar em Produção

Simples: Faça `git push` para o `main` e Railway redeploya automaticamente!

```bash
git add .
git commit -m "Atualização da API"
git push origin main
# Railway vai detectar a mudança e fazer deploy automaticamente
```

---

## Arquivos de Configuração

Estes arquivos permitem o deploy automático:

- Dockerfile: Define como a aplicação é containerizada
  - Usa Python 3.11-slim (leve e seguro)
  - Instala dependências automaticamente
  - Executa com Gunicorn (production-ready)

- wsgi.py: Ponto de entrada WSGI na raiz
  - Permite que o Railway detecte a aplicação
  - Importa a factory do Flask

- railway.json: Configurações específicas do Railway (opcional)
  - Define builder como Dockerfile
  - Configurações de restart

- .dockerignore: Otimiza a imagem Docker
  - Exclui arquivos desnecessários (node_modules, .git, etc)
  - Reduz tempo de build e tamanho da imagem

---
- Verificar logs no Railway
- Confirmar que `API_PORT=5000` está na variável de ambiente

### Domínio não funciona
- Aguarde 2-3 minutos após deploy
- Verifique no dashboard se há erros

### Erro ao fazer push
- Confirme que está no branch `main`
- Railway só faz deploy automático do `main`

---

## Arquivos de Configuração

- Dockerfile: Defines como a aplicação é containerizada
- railway.json: Configurações específicas do Railway (opcional)
- .dockerignore: Arquivos excluídos do container

---

## Documentação Adicional

- [Railway Docs](https://docs.railway.app/)
- [Docker Docs](https://docs.docker.com/)
- [API Documentation](README.md#documentação-da-api)
