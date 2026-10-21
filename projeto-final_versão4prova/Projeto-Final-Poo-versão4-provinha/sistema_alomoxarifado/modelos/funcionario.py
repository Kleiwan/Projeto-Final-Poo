class Funcionario:
    """
    Representa um funcionário do almoxarifado.

    Além dos dados cadastrais, o funcionário sabe se está autorizado a
    retirar materiais (``pode_retirar``) e é o único responsável por
    alterar essa permissão. Retirar a permissão não apaga o cadastro nem
    as retiradas já registradas por ele.
    """

    def __init__(self, nome: str, id: int, setor: str, pode_retirar: bool = True) -> None:
        self._nome = nome
        self._id = id
        self._setor = setor
        self._pode_retirar = pode_retirar

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def id(self) -> int:
        return self._id

    @property
    def setor(self) -> str:
        return self._setor

    @property
    def pode_retirar(self) -> bool:
        """Indica se o funcionário está autorizado a retirar materiais."""
        return self._pode_retirar

    def conceder_permissao(self) -> None:
        """Autoriza o funcionário a retirar materiais."""
        self._pode_retirar = True

    def retirar_permissao(self) -> None:
        """Remove a autorização do funcionário para retirar materiais."""
        self._pode_retirar = False

    def printar(self) -> None:
        situacao = "AUTORIZADO" if self.pode_retirar else "NAO AUTORIZADO"
        print(
            f"Nome: {self.nome} | ID: {self.id} | Setor: {self.setor} "
            f"| Permissao de retirada: {situacao}"
        )
