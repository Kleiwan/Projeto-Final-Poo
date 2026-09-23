from interface.telas import tela_funcionario
from interface.menu import Menu_base
from servicos import funcionario_service, retirada_service
from excecoes.almoxarifado__error import (
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
)


class Op_Funcionarios(Menu_base):
    """Menu responsável pela interação com o usuário para operações de funcionários."""

    @staticmethod
    def exibir_menu_especial() -> None:
        while True:
            tela_funcionario.Tela_Funcionario.exibir_tela()

            deve_voltar = Op_Funcionarios.escolha()
            if deve_voltar:
                break

    @staticmethod
    def escolha() -> bool:
        op = input('Digite a opcao que voce deseja: ')
        try:
            if op == '1':
                nome = input('Digite o nome do funcionario: ')
                id_funcionario = int(input('Digite o id do funcionario: '))
                setor = input('Digite o setor do funcionario: ')
                funcionario_service.cadastrar(nome, id_funcionario, setor)
                print('Funcionário cadastrado com sucesso!')
            elif op == '2':
                funcionarios = funcionario_service.listar()
                if not funcionarios:
                    print('\nNenhum funcionario cadastrado.')
                else:
                    print('\n=== LISTA DE FUNCIONARIOS ===')
                    for funcionario in funcionarios:
                        funcionario.printar()
                    print('=============================')
            elif op == '3':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                funcionario = funcionario_service.consultar(id_funcionario)
                funcionario.printar()
            elif op == '4':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                retiradas = retirada_service.consultar_por_funcionario(id_funcionario)
                if not retiradas:
                    print('\nNenhuma retirada encontrada para esse funcionario.')
                else:
                    print('\n=== RETIRADAS DO FUNCIONARIO ===')
                    for retirada in retiradas:
                        print(retirada)
                    print('=================================')
            elif op == '0':
                return True
            else:
                print('Opcao invalida!')
        except (FuncionarioJaCadastradoError, FuncionarioNaoEncontradoError) as erro:
            print(f'Erro: {erro}')

        return False
