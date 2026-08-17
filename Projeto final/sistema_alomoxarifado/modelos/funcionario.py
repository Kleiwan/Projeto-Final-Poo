class Funcionario:
    """Representa um funcionário do almoxarifado."""

    def __init__(self, nome: str, id: int, setor: str):
        self._nome = nome
        self._id = id
        self._setor = setor

    @property
    def nome(self):
        return self._nome

    @property
    def id(self):
        return self._id

    @property
    def setor(self):
        return self._setor

    def __str__(self):
        return f"Nome: {self.nome} | ID: {self.id} | Setor: {self.setor}"
        
        