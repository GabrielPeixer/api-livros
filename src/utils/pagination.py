# Funções auxiliares para paginação
# (opcional - não usado no código simplificado)


def paginar(lista, pagina=1, por_pagina=20):
    """
    Retorna apenas os itens de uma página específica

    Exemplo:
        livros = [1, 2, 3, 4, 5, 6]
        paginar(livros, pagina=1, por_pagina=2)  # Retorna [1, 2]
        paginar(livros, pagina=2, por_pagina=2)  # Retorna [3, 4]
    """
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    return lista[inicio:fim]
