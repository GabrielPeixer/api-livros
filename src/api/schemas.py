# Esquemas de dados (opcional - não usado no código simplificado)
# Aqui você pode definir a estrutura dos dados se quiser validação extra

class BookSchema:
    """Define como um livro deve ser estruturado"""
    def __init__(self, title, price, availability, rating):
        self.title = title
        self.price = price
        self.availability = availability
        self.rating = rating
