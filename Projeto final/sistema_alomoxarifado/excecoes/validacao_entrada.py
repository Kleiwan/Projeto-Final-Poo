def ler_inteiro(mensagem: str, apenas_positivos: bool = False) -> int:
    while True:
        try:
            valor = int(input(mensagem))
            if apenas_positivos and valor <= 0:
                print('Erro: O ID deve ser um número positivo maior que zero.')
                continue
            return valor
        except ValueError:
            print('Erro: O valor digitado deve ser um número inteiro válido. Tente novamente.')

def ler_texto(mensagem: str) -> str:
    while True:
        texto = input(mensagem).strip()
        
        if not texto:
            print("Erro: O campo não pode ser vazio. Tente novamente.")
            continue
            
        if not texto.replace(" ", "").isalpha():
            print("Erro: O campo não pode conter números ou caracteres especiais.")
            continue
            
        return texto