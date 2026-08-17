class Retirada:
         """
        Representa a retirada de uma quantidade de
        determinado material por um funcionario.
        """
def __init__(self,funcionario, material, qtd, momento):
        self.funcionario = funcionario
        self.material = material
        self.qtd = qtd
        self.momento = momento 

def __str__(self):
        return (
            f"Funcionario: {self.funcionario}"
            f"Material: {self.material}"
            f"Quantidade: {self.qtd}"
            f"Momento:{self.momento}"
        )