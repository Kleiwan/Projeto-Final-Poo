class Fornecedor:
    """Representa um fornecedor de materiais do almoxarifado."""

    def __init__(self, id: int, nome: str, contato: str) -> None:
        self.__id = id
        self.__nome = nome
        self.__contato = contato

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def contato(self) -> str:
        return self.__contato

    def atualizar(self, nome: str, contato: str) -> None:
        """Altera os dados editáveis do fornecedor (o ID nunca muda)."""
        self.__nome = nome
        self.__contato = contato

    def printar(self) -> None:
        print(f"ID: {self.id} | Nome: {self.nome} | Contato: {self.contato}")
