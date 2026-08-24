def id_invalido():
    if id <= 0:
        raise ValueError("ID inválido. O ID deve ser um número positivo.")