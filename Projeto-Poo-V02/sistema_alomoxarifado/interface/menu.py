from abc import ABC, abstractmethod

class Menu_base (ABC):
    """
    Classe base para os menus
    """
    
    @abstractmethod
    def escolha():
        pass

    @abstractmethod
    def exibir_menu_especial():
        pass