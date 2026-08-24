class Funcionario:
    """Representa um funcionário do almoxarifado."""

    def __init__(self, nome: str, funcionario_id: int, setor: str):
        self._nome = nome
        self._funcionario_id = funcionario_id
        self._setor = setor

    @property
    def nome(self):
        return self._nome

    @property
    def funcionario_id(self):
        return self._funcionario_id

    @property
    def setor(self):
        return self._setor

    def printar(self) -> None:
        print(f"Nome: {self.nome} | ID: {self.funcionario_id} | Setor: {self.setor}")