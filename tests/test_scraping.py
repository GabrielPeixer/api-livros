from src.scraping import scraper


def test_parse_page_extracts_expected_fields():
    html = """
    <html>
        <article class="product_pod">
            <h3><a title="Example"/></h3>
            <p class="price_color">£10.00</p>
            <p class="instock availability">In stock</p>
            <p class="star-rating Four"></p>
        </article>
    </html>
    """
    soup = scraper.BeautifulSoup(html, 'html.parser')
    itens = scraper._processar_pagina(soup)
    assert len(itens) == 1
    assert itens[0]['title'] == 'Example'
    assert itens[0]['price'] == 10.0
    assert itens[0]['rating'] == 4


def test_salvar_csv_creates_file(tmp_path):
    livros = [{
        'title': 'Book',
        'price': 5.0,
        'availability': 'In stock',
        'rating': 3
    }]
    destino = tmp_path / 'books.csv'
    scraper.salvar_csv(livros, str(destino))
    assert destino.exists()
    content = destino.read_text(encoding='utf-8')
    assert 'Book' in content
