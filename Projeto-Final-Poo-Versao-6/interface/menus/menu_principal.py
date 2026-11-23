from aplicacao import Aplicacao
from interface.telas.tela_pricipal import tela_menu_principal
from interface.menus.menu_funcionarios import Op_Funcionarios
from interface.menus.menu_materiais import Op_Materiaes
from interface.menus.menu_retirada import Op_Retirada
from interface.menu import Menu_base


class Op_MenuInit(Menu_base):
    """Menu principal: encaminha para os menus de cada área."""

    def __init__(self, aplicacao: Aplicacao) -> None:
        self.__funcionarios = Op_Funcionarios(aplicacao)
        self.__materiais = Op_Materiaes(aplicacao)
        self.__retiradas = Op_Retirada(aplicacao)

    def exibir_menu_especial(self) -> None:
        while True:
            tela_menu_principal.exibir_tela()
            deve_sair = self.escolha()
            if deve_sair:
                print('Saindo do sistema...')
                break

    def escolha(self) -> bool:
        op = input('Digite a opcao que voce deseja: ')
        if op == '1':
            self.__funcionarios.exibir_menu_especial()
        elif op == '2':
            self.__materiais.exibir_menu_especial()
        elif op == '3':
            self.__retiradas.exibir_menu_especial()
        elif op == '0':
            return True
        else:
            print('Opcao invalida!')
        return False
