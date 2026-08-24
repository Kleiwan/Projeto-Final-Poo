## Integrantes do grupo e sistema
Integrantes: Rafael Joaquim, Layse Oliveira e Kleiwan Paulo

## Sobre o sistema
Almoxarifado
 A ideia é ter um sistma  que ajude a controlar funcionários, materiais e as retiradas que cada funcionário faz do estoque. O projeto ficou dividido em várias classes,  junto com o processo que a gente seguiu pra desenvolver.

Como pensamos o projeto
Primeiro a gente fez o código, definindo as classes e o que cada uma ia fazer. Depois que já tinha uma boa parte da estrutura pronta, a gente fez um diagrama ER usando Mermaid, pra visualizar melhor como o projeto tava ficando organizado. Nesse diagrama,, o funcionário aparece com um id, que é a chave primária dele, além do nome e do setor. O material aparece com um código, que funciona como chave primária, além do nome e da quantidade em estoque. Já a retirada tem um id como chave primária e a quantidade retirada. Os relacionamentos são: um funcionário realiza várias retiradas, e uma retirada contém um ou mais materiais. Esse diagrama ajudou bastante a confirmar que a estrutura das classes fazia sentido e a visualizar melhor como as partes do sistema se conectavam.

Como executar:
Pra rodar o sistema é só executar o arquivo principal do projeto, com o comando python main.py. Daí o usuário cai no menu principal, de onde dá pra acessar os menus de funcionários, materiais e retiradas.
As classes principais
A classe Funcionario representa um funcionário do almoxarifado. Joaquim e kleiwan foramm quem trabalhou mais nela. Ela guarda o nome, o ID e o setor do funcionário, usando a decoração propriedade pra deixar esses dados protegidos, ou seja, só dá pra acessar por métodos específicos, e não direto. Também tem o método impressora, que mostra as informações do funcionário já formatadas, no padrão em que aparecem o nome, o ID e o setor separados por barras.
A classe Material é meio diferente das outras porque é abstrata, usando os recursos ABC e método abstrato do Python. Ou seja, ela funciona como um modelo pra outras classes de material que a gente ainda pode criar, obrigando elas a terem um método de regulação de quantidade, chamado A_regulação. Ela guarda código, nome e quantidade do material.

A classe Retirada representa uma retirada de material feita por um funcionário. Guarda quem retirou, qual material, a quantidade e o momento em que isso aconteceu. Tem um método str que organiza tudo isso num texto formatado.

A classe Almoxarifado é a classe central do sistema, que junta e organiza as outras. Ela guarda a lista de funcionários cadastrados e tem as funções principais do sistema. A função cadastrar_funcionario cadastra um funcionário novo, checando antes se o ID já existe pra não duplicar. A função listar_funcionarios mostra todos os funcionários cadastrados, ou avisa se não tem nenhum. A função buscar_funcionario procura um funcionário pelo ID e é usada por dentro de outras funções. E a função consultar_funcionario pede o ID pro usuário e mostra os dados daquele funcionário. Eu ajudei a montar algumas dessas funções, principalmente as de busca e consulta.

A parte da interface
Pra deixar o sistema mais fácil de usar, a gente fez telas separadas de menu, cada uma numa classe. As classes Tela_Funcionario, TelaMaterial, Tela_Retirada e tela_menu_principal só imprimem os menus na tela, tipo cadastrar, listar, consultar e voltar. Elas não têm lógica nenhuma, só mostram as opções.

Já as classes Op_Funcionarios, Op_Materiaes, Op_Retirada e Op_MenuInit são as que cuidam da lógica dos menus. Elas ficam num loop chamando a tela certa, pegando a opção que a pessoa digitou e chamando a função correspondente lá do Almoxarifado. Por exemplo, a classe Op_Funcionarios chama cadastrar_funcionario, listar_funcionarios e consultar_funcionario, dependendo da opção escolhida.

A classe Op_MenuInit é o menu principal do sistema. Ela mostra as opções de ir pros menus de funcionários, materiais e retiradas, além da opção de sair, e direciona a pessoa pra cada um desses menus de acordo com o que ela escolher.

Considerações finais
O projeto ainda tá em desenvolvimento. Algumas partes de material e retirada nos menus ainda estão sem lógica implementada. Mesmo assim, a estrutura já tá bem definida, com as classes que representam os dados, que são Funcionario, Material e Retirada, a classe que organiza tudo, que é Almoxarifado, e as classes de interface que mostram os menus e recebem a interação do usuário. Foi um trabalho em equipe, com cada um focando numa parte do projeto.

## Diagrama Entidade-Relacionamento

```mermaid
erDiagram

    FUNCIONARIO {
        int id
    }

    MATERIAL {
        int codigo
        string nome
        int qt_material
    }

    SETOR {
        string nome
    }

    RETIRADA {
        int id
        int qtd
        datetime dt_hora
    }

    FUNCIONARIO ||--o{ RETIRADA : "realiza"
    MATERIAL ||--o{ RETIRADA : "registra"
    SETOR ||--o{ FUNCIONARIO : "possui"