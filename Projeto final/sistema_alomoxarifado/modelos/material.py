class Material:

    def __init__(self, codigo: str, nome: str, qt_material: int):
        self._codigo = codigo
        self._nome = nome
        self._qt_material = qt_material

    @property
    def nome(self):
        return self._nome

    @property
    def codigo(self):
        return self._codigo

    @property
    def qt_material(self):
        return self._qt_material

    @qt_material.setter
    def qt_material(self, valor):
        self._qt_material = valor
    
    def printar_material(self) -> None:
        print(f"Nome: {self.nome} | ID: {self.codigo} | Quantidade: {self.qt_material}")

