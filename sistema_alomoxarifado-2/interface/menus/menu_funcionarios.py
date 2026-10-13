from typing import Optional

from interface.telas import tela_funcionario
from interface.menu import Menu_base
from servicos import funcionario_service, retirada_service
from excecoes.almoxarifado__error import (
    FuncionarioComRetiradasError,
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
    PersistenciaError,
)


def _texto_ou_none(mensagem: str) -> Optional[str]:
    """Lê um texto; se o usuário apenas pressionar Enter, retorna None (manter valor atual)."""
    texto = input(mensagem).strip()
    return texto if texto else None


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
            elif op == '5':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                funcionario_service.consultar(id_funcionario).printar()
                print('(Pressione Enter para manter o valor atual)')
                nome = _texto_ou_none('Novo nome: ')
                setor = _texto_ou_none('Novo setor: ')
                funcionario_service.editar(id_funcionario, nome, setor)
                print('Funcionário atualizado com sucesso!')
            elif op == '6':
                id_funcionario = int(input('Digite o ID do funcionario: '))
                funcionario_service.remover(id_funcionario)
                print('Funcionário removido com sucesso!')
            elif op == '0':
                return True
            else:
                print('Opcao invalida!')
        except (
            FuncionarioJaCadastradoError,
            FuncionarioNaoEncontradoError,
            FuncionarioComRetiradasError,
            PersistenciaError,
        ) as erro:
            print(f'Erro: {erro}')
        except ValueError:
            print('Erro: valor numerico invalido.')

        return False
