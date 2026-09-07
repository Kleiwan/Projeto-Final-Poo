class Funcionario:
    """Representa um funcionário do almoxarifado."""

    def __init__(self, nome: str, id: int, setor: str):
        self._nome = nome
        self._id = id
        self._setor = setor

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def id(self) -> int:
        return self._id

    @property
    def setor(self) -> str:
        return self._setor

    def printar(self) -> None:
        print(f"Nome: {self.nome} | ID: {self.id} | Setor: {self.setor}")