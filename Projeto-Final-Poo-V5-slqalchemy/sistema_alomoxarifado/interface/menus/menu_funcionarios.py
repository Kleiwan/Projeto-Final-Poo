from aplicacao import Aplicacao
from interface.telas import tela_funcionario
from interface.menu import Menu_base
from excecoes.almoxarifado__error import (
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
    RemocaoNaoPermitidaError,
)


class Op_Funcionarios(Menu_base):
    """Menu responsável pela interação com o usuário para operações de funcionários."""

    def __init__(self, aplicacao: Aplicacao) -> None:
        self.__aplicacao = aplicacao

    def exibir_menu_especial(self) -> None:
        while True:
            tela_funcionario.Tela_Funcionario.exibir_tela()

            deve_voltar = self.escolha()
            if deve_voltar:
                break

    def escolha(self) -> bool:
        funcionario_service = self.__aplicacao.funcionario_service
        retirada_service = self.__aplicacao.retirada_service

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
            elif op == '5':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                funcionario = funcionario_service.conceder_permissao(id_funcionario)
                print(f'Permissao concedida: {funcionario.nome} agora pode retirar materiais.')
            elif op == '6':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                funcionario = funcionario_service.retirar_permissao(id_funcionario)
                print(f'Permissao retirada: {funcionario.nome} nao pode mais retirar materiais.')
            elif op == '7':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                funcionario_service.remover(id_funcionario)
                print('Funcionario removido com sucesso!')
            elif op == '0':
                return True
            else:
                print('Opcao invalida!')
        except (
            FuncionarioJaCadastradoError,
            FuncionarioNaoEncontradoError,
            RemocaoNaoPermitidaError,
            ValueError,
        ) as erro:
            print(f'Erro: {erro}')

        return False
