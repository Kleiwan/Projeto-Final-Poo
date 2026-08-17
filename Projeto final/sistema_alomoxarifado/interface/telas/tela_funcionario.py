from interface.tela import Tela

class Tela_Funcionario(Tela):
    """
    Modulo responsavel por exibir o menu de FUNCIONARIOS
    """
    @staticmethod
    def exibir_tela():
        print()
        print('=========MENU DE FUNCIONARIOS=========')
        print('[1] - Cadastrar funcionarios')
        print('[2] - Listar funcionarios')
        print('[3] - Consultar funcionario')
        print('[4] - Consultar retirada de material')
        print('[0] - Voltar')
        print('======================================')

    
