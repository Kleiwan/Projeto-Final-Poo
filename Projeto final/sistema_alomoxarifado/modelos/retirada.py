from datetime import datetime

class Retirada:
    def __init__(self, funcionario, material, qtd):
        self._funcionario = funcionario
        self._material = material
        self._qtd = qtd
        self._momento = datetime.now()

    @property
    def funcionario(self):
        return self._funcionario

    @property
    def material(self):
        return self._material

    @property
    def qtd(self):
        return self._qtd

    @property
    def momento(self):
        return self._momento

    def printar_retirada(self):
        print(f"Funcionario: {self.funcionario.nome} | Material: {self.material.nome} | Quantidade: {self.qtd} | Momento: {self.momento}")