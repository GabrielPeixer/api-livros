from src.api.main import app


app.config['TESTING'] = True
client = app.test_client()


def test_health_check_returns_ok():
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["estado"] == "sucesso"
    assert payload["dados"]["servico"] == "api-livros"
    assert payload["dados"]["estado"] == "operacional"


def test_books_endpoint_returns_list_even_without_data(tmp_path, monkeypatch):
    # Força load_books a devolver lista vazia para testar o formato de resposta
    from api import utils

    monkeypatch.setattr(
        utils, "CAMINHO_DADOS", tmp_path / "missing.csv", raising=False
    )
    response = client.get("/api/books/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["estado"] == "sucesso"
    assert payload["dados"] == []
    assert payload["meta"]["pagina"] == 1


def test_stats_endpoint_handles_empty_dataset(tmp_path, monkeypatch):
    from api import utils

    monkeypatch.setattr(
        utils, "CAMINHO_DADOS", tmp_path / "missing.csv", raising=False
    )
    response = client.get("/api/stats/")
    assert response.status_code == 200
    stats = response.get_json()["dados"]
    assert stats["total_livros"] == 0
    assert stats["preco_medio"] == 0
