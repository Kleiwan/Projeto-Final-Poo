from abc import ABC, abstractmethod

class Tela(ABC):
    """
    Classe base para todas as exibicoes
    """

    @abstractmethod
    def exibir_tela(self) -> None:
        """
        Metodo para exibir o menu em prompt
        """