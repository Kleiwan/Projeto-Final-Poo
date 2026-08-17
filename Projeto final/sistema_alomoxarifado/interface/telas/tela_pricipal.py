from interface.tela import Tela

class tela_menu_principal(Tela):
    """
    Modulo responsavel por printar o MENU PRINCIPAÇ
    """
    @staticmethod
    def exibir_tela():
        print()
        print('==========MENU DE PRINCIPAL===========')
        print('[1] - Cadastrar Funcionario')
        print('[2] - Materiais')
        print('[3] - Retiradas')
        print('[0] - Sair')
        print('======================================')

