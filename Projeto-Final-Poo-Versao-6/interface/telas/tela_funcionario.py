from interface.tela import Tela
class Tela_Funcionario(Tela):
    @staticmethod
    def exibir_tela():
        print("\\n========= MENU DE FUNCIONÁRIOS =========")
        print("[1] Cadastrar")
        print("[2] Listar")
        print("[3] Consultar")
        print("[4] Consultar retiradas")
        print("[5] Conceder permissão")
        print("[6] Retirar permissão ")
        print("[7] Remover")
        print("[8] Editar cadastro")
        print("[9] Ativar/inativar")
        print("[0] Voltar")
