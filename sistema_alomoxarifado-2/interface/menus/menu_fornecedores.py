from typing import Optional

from interface.telas.tela_fornecedores import TelaFornecedor
from interface.menu import Menu_base
from servicos import fornecedor_service
from excecoes.almoxarifado__error import (
    FornecedorComMateriaisError,
    FornecedorJaCadastradoError,
    FornecedorNaoEncontradoError,
    PersistenciaError,
)


def _texto_ou_none(mensagem: str) -> Optional[str]:
    """Lê um texto; se o usuário apenas pressionar Enter, retorna None (manter valor atual)."""
    texto = input(mensagem).strip()
    return texto if texto else None


class Op_Fornecedores(Menu_base):
    """Menu responsável pela interação com o usuário para operações de fornecedores."""

    @staticmethod
    def exibir_menu_especial() -> None:
        while True:
            TelaFornecedor.exibir_tela()

            deve_voltar = Op_Fornecedores.escolha()
            if deve_voltar:
                break

    @staticmethod
    def escolha() -> bool:
        op = input('Digite a opcao que voce deseja: ')
        try:
            if op == '0':
                return True
            elif op == '1':
                id_fornecedor = int(input('Digite o ID do fornecedor: '))
                nome = input('Digite o nome do fornecedor: ')
                contato = input('Digite o contato do fornecedor: ')
                fornecedor_service.cadastrar(id_fornecedor, nome, contato)
                print('Fornecedor cadastrado com sucesso!')
            elif op == '2':
                fornecedores = fornecedor_service.listar()
                if not fornecedores:
                    print('\nNenhum fornecedor cadastrado.')
                else:
                    print('\n=== LISTA DE FORNECEDORES ===')
                    for fornecedor in fornecedores:
                        fornecedor.printar()
                    print('=============================')
            elif op == '3':
                id_fornecedor = int(input('Digite o ID do fornecedor: '))
                fornecedor_service.consultar(id_fornecedor).printar()
            elif op == '4':
                id_fornecedor = int(input('Digite o ID do fornecedor: '))
                fornecedor_service.consultar(id_fornecedor).printar()
                print('(Pressione Enter para manter o valor atual)')
                nome = _texto_ou_none('Novo nome: ')
                contato = _texto_ou_none('Novo contato: ')
                fornecedor_service.editar(id_fornecedor, nome, contato)
                print('Fornecedor atualizado com sucesso!')
            elif op == '5':
                id_fornecedor = int(input('Digite o ID do fornecedor: '))
                fornecedor_service.remover(id_fornecedor)
                print('Fornecedor removido com sucesso!')
            else:
                print('Opcao invalida!')
        except (
            FornecedorJaCadastradoError,
            FornecedorNaoEncontradoError,
            FornecedorComMateriaisError,
            PersistenciaError,
        ) as erro:
            print(f'Erro: {erro}')
        except ValueError:
            print('Erro: valor numerico invalido.')

        return False
