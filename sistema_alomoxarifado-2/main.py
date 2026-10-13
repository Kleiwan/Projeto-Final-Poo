from excecoes.almoxarifado__error import PersistenciaError


def main() -> None:
    # Os serviços (e, por consequência, a aplicação) são criados ao importar
    # a interface, e é nesse momento que os arquivos JSON são carregados.
    # Por isso o import fica dentro do try: se algum arquivo estiver
    # corrompido, a interface mostra uma mensagem em vez de um traceback.
    try:
        from interface.menus.menu_principal import Op_MenuInit
    except PersistenciaError as erro:
        print(f'Erro ao carregar os dados: {erro}')
        print('Corrija ou remova o arquivo indicado (pasta "dados") e execute novamente.')
        return

    Op_MenuInit.exibir_menu_especial()


if __name__ == '__main__':
    main()
