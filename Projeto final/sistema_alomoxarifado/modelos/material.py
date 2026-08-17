from abc import ABC, abstractmethod

class Material(ABC):
    def __init__(self, codigo: str, nome: str, qt_material: float):
        codigo = codigo
        nome = nome
        qt_material = qt_material
    
    @abstractmethod
    def A_regulacao(qt_material):
        pass

