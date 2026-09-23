from interface.tela import Tela

class Tela_Retirada(Tela):
    """
    Modulo responsavel por exibir o menu de RETIRADAS
    """
    @staticmethod
    def exibir_tela():
        print()
        print('=========MENU DE RETIRADAS=========')
        print('[1] - Registrar retiradas')
        print('[2] - Listar retiradas')
        print('[3] - Consultar retiradas')
        print('[4] - Consultar retirada de um funcionario')
        print('[5] - Consultar retirada de material')
        print('[6] - Consultar estoque'),
        print('[0] - Voltar')
        print('======================================')
