from interface.telas import tela_funcionario
from interface.menu import Menu_base
from dados import almoxarifado
from excecoes.validacao_funcionario import id_invalido
from excecoes.validacao_entrada import ler_inteiro, ler_texto


class Op_Funcionarios(Menu_base):

    @staticmethod
    def exibir_menu_especial():
        while True:
            tela_funcionario.Tela_Funcionario.exibir_tela()

            deve_voltar = Op_Funcionarios.escolha()
            if deve_voltar:
                break

    @staticmethod


    def escolha():
        op = input('Digite a opcao que voce deseja: ')
    
        if op == '1':
            funcionario_id = ler_inteiro('Digite o ID do funcionario: ', apenas_positivos=True)
 
            nome = ler_texto('Digite o nome do funcionario: ')


            setor = ler_texto('Digite o setor do funcionario: ')

            almoxarifado.cadastrar_funcionario(nome, funcionario_id, setor)

        elif op == '2':
                almoxarifado.listar_funcionarios()        
        elif op == '3':
                almoxarifado.consultar_funcionario()
        elif op == '4':
                almoxarifado.consultar_retirada_lista()
                pass
        elif op == '0':
                return True
        else:
                print('Opcao invalida!')
            
        return False