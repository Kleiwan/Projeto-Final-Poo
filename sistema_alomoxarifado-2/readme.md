# Sistema de Almoxarifado — Terceira Versão — Rafael Joaquim da Silva, Layse Vitória de Lima Oliveira e Kleiwan Paulo Justino Ludugero 

## Sobre o projeto
O projeto tem como objetivo ajudar a gerenciar um almoxarifado, de forma que tudo possa ser armazenado e organizado de forma mais simples. O sistema permite cadastrar itens e usuarios além de gerenciar os mesmos para melhor controle. OS gerenciamentos possiveis são: Cadastrar usuario, listar usuario e buscar usuario; Cadastrar itens, retirar itens e listar os mesmos.

## Arquitetura

Na terceira versão foi adicionada a camada de **persistência**: os dados
deixam de existir apenas em memória e passam a ser gravados em arquivos
JSON, ficando disponíveis novamente na próxima execução. A arquitetura
evoluiu de 4 para 5 camadas:

```
   INTERFACE
       |
       ▼
    SERVIÇOS
       |
       ▼
   APLICAÇÃO
       |
       ▼
  PERSISTÊNCIA
       |
       ▼
 ARQUIVOS JSON
```

Os serviços **não conhecem os arquivos JSON**: eles pedem a gravação à
aplicação (`Almoxarifado`), que delega o trabalho à camada de persistência.

```
Tela → Service → Aplicação → Persistência → JSON
```

## Estrutura de pastas

```
sistema_alomoxarifado/
├── main.py
├── almoxarifado.py            # aplicação: dados em memória + coordena carregar/salvar
│
├── modelos/
│   ├── fornecedor.py
│   ├── funcionario.py
│   ├── material.py
│   └── retirada.py
│
├── servicos/
│   ├── __init__.py             # instancia os serviços compartilhados
│   ├── fornecedor_service.py
│   ├── funcionario_service.py
│   ├── material_service.py
│   └── retirada_service.py
│
├── persistencia/
│   ├── arquivo_json.py             # leitura/gravação segura de um .json
│   ├── validacao.py                # validação dos dados simples lidos
│   ├── fornecedor_persistencia.py
│   ├── funcionario_persistencia.py
│   ├── material_persistencia.py
│   └── retirada_persistencia.py
│
├── dados/                      # criada automaticamente na primeira execução
│   ├── fornecedores.json
│   ├── funcionarios.json
│   ├── materiais.json
│   └── retiradas.json
│
├── excecoes/
│   └── almoxarifado__error.py
│
└── interface/
    ├── menu.py
    ├── tela.py
    ├── menus/
    │   ├── menu_principal.py
    │   ├── menu_fornecedores.py
    │   ├── menu_funcionarios.py
    │   ├── menu_materiais.py
    │   └── menu_retirada.py
    └── telas/
        ├── tela_pricipal.py
        ├── tela_fornecedores.py
        ├── tela_funcionario.py
        ├── tela_materiais.py
        └── tela_retiradas.py
```

## Responsabilidades

- **Modelos**: representam os objetos do domínio e seus comportamentos
  próprios. `Material` controla sua própria quantidade em estoque
  (`adicionar_estoque` / `retirar_estoque`), levantando exceções quando
  uma operação é inválida. `Retirada` passou a ter um `id` próprio.
- **Aplicação (`Almoxarifado`)**: mantém as listas de funcionários,
  materiais e retiradas em memória, com atributos privados e acesso
  controlado por propriedades/métodos. Ao ser criada chama
  `carregar_dados()`; expõe `salvar_funcionarios()`, `salvar_materiais()`,
  `salvar_retiradas()` e `salvar_dados()`.
- **Serviços**: coordenam operações e regras de negócio. Por exemplo,
  `RetiradaService.registrar` localiza o funcionário e o material,
  verifica a quantidade e o estoque, cria a retirada, adiciona à
  aplicação e solicita a gravação. Os serviços nunca abrem arquivos JSON.
- **Persistência**: transforma objetos em dados simples e JSON, e o
  processo inverso (`Objeto ↔ Dados simples ↔ JSON`). Não exibe mensagens
  ao usuário; apenas levanta exceções. Usa somente os mecanismos públicos
  da aplicação (propriedades que devolvem cópias das listas).
- **Exceções**: representam violações de regras de negócio
  (`FuncionarioJaCadastradoError`, `MaterialNaoEncontradoError`,
  `EstoqueInsuficienteError`, `QuantidadeInvalidaError`, etc.) e problemas
  de persistência (veja abaixo). Os serviços e a persistência levantam as
  exceções; a interface captura e exibe uma mensagem adequada.
- **Interface**: menus e telas cuidam exclusivamente da interação com
  o usuário, delegando toda a lógica aos serviços.

## Persistência em JSON

Os arquivos ficam na pasta `dados/` (ao lado de `almoxarifado.py`) e são
criados automaticamente quando ainda não existem.

**funcionarios.json**
```json
[
    {"id": 3, "nome": "Ana", "setor": "TI"}
]
```

**fornecedores.json**
```json
[
    {"id": 10, "nome": "Papelaria Sol", "contato": "8499-1111"}
]
```

**materiais.json**
```json
[
    {"codigo": "P01", "nome": "Papel A4", "quantidade": 42.5, "fornecedor_id": 10},
    {"codigo": "C02", "nome": "Caneta", "quantidade": 30.0, "fornecedor_id": null}
]
```

**retiradas.json**
```json
[
    {
        "id": 1,
        "funcionario_id": 3,
        "material_codigo": "P01",
        "quantidade": 7.5,
        "momento": "2026-10-11T21:49:43.123456"
    }
]
```

A retirada **não guarda cópia** do funcionário nem do material: apenas
`funcionario_id` e `material_codigo`, que correspondem às chaves
estrangeiras do modelo lógico. O mesmo vale para o material, que guarda
apenas `fornecedor_id` (ou `null` quando não há fornecedor). Arquivos
antigos sem o campo `fornecedor_id` continuam sendo aceitos.

### Carregamento

```
Iniciar programa
      ↓
Criar aplicação
      ↓
Carregar fornecedores
      ↓
Carregar funcionários
      ↓
Carregar materiais   (fornecedor_id → Fornecedor)
      ↓
Carregar retiradas   (funcionario_id → Funcionario, material_codigo → Material)
      ↓
Iniciar interface
```

Os dados só substituem os da memória se **todos** os arquivos forem lidos
com sucesso.

### Gravação

Cada operação que altera dados solicita a gravação dos arquivos afetados:

```
Cadastrar funcionário → Funcionário criado → Aplicação atualizada → funcionarios.json atualizado
Cadastrar material    → Material criado    → Aplicação atualizada → materiais.json atualizado
Registrar retirada    → Retirada criada    → Aplicação atualizada → materiais.json + retiradas.json atualizados
```

A gravação é feita em arquivo temporário seguido de renomeação, evitando
que uma falha no meio da escrita corrompa os dados já salvos.

### Edição e remoção

Funcionários, materiais e fornecedores podem ser editados e removidos
(a chave — `id` ou `codigo` — nunca é alterada). Em cada edição, campos
deixados em branco mantêm o valor atual. Para que o JSON nunca fique com
um relacionamento apontando para um objeto inexistente, os serviços
aplicam regras de **integridade referencial**:

| Operação | Bloqueada quando | Exceção |
|---|---|---|
| Remover funcionário | possui retiradas | `FuncionarioComRetiradasError` |
| Remover material | possui retiradas | `MaterialComRetiradasError` |
| Remover fornecedor | há materiais vinculados | `FornecedorComMateriaisError` |
| Cadastrar/editar material com fornecedor | fornecedor não existe | `FornecedorNaoEncontradoError` |

Para remover um fornecedor basta antes desvincular (ou remover) os seus
materiais.

### Tratamento de erros de persistência

| Situação | Comportamento |
|---|---|
| Arquivo inexistente | Criado automaticamente com lista vazia |
| Arquivo vazio | Tratado como lista vazia |
| JSON inválido | `JsonInvalidoError` |
| Dados incompatíveis com o modelo (campo ausente, tipo errado, ID/código duplicado, quantidade inválida, data inválida) | `DadosIncompativeisError` |
| Relacionamento para objeto inexistente | `RelacionamentoInvalidoError` |
| Falha ao ler/gravar o arquivo (permissão, disco etc.) | `ArquivoPersistenciaError` |

Todas herdam de `PersistenciaError`. A camada de persistência não exibe
mensagens: a interface (`main.py` na inicialização e os menus durante a
execução) captura as exceções e apresenta a mensagem ao usuário. Em caso
de arquivo corrompido, o sistema **não sobrescreve** o arquivo — avisa o
usuário e encerra, para que nenhum dado seja perdido.

## Fluxo testado

```
Cadastrar funcionário
        ↓
Cadastrar material (com estoque inicial)
        ↓
Registrar retirada válida
        ↓
Consultar estoque
        ↓
Tentar retirar quantidade superior ao estoque
        ↓
Exceção (EstoqueInsuficienteError) apresentada pela interface
        ↓
Encerrar e abrir o programa novamente
        ↓
Funcionários, materiais, retiradas e estoque continuam disponíveis
```

## Execução

O ponto de entrada continua sendo o mesmo da primeira versão:

```
python main.py
```
```mermaid
erDiagram
    FUNCIONARIO {
        int id PK
        string nome
        string setor
    }
    MATERIAL {
        string codigo PK
        string nome
        int qt_material
    }
    RETIRADA {
        int id PK
        int quantidade
        datetime data_hora
    }

    FUNCIONARIO ||--o{ RETIRADA : realiza
    MATERIAL ||--o{ RETIRADA : "refere-se"
```
```mermaid
erDiagram
    FUNCIONARIO {
        int id PK
        string nome
        string setor
    }
    MATERIAL {
        string codigo PK
        string nome
        int qt_material
    }
    RETIRADA {
        int id PK
        int quantidade
        datetime data_hora
        int id_funcionario FK
        string codigo_material FK
    }

    FUNCIONARIO ||--o{ RETIRADA : "1:N"
    MATERIAL ||--o{ RETIRADA : "1:N"
```
```mermaid
erDiagram
    FORNECEDOR {
        int id PK
        string nome
        string contato
    }
    MATERIAL {
        string codigo PK
        string nome
        float quantidade
        int fornecedor_id FK "opcional"
    }

    FORNECEDOR |o--o{ MATERIAL : "fornece (1:N)"
```
Na terceira versão foi incluída a entidade FORNECEDOR, com relacionamento 1:N com MATERIAL (um fornecedor fornece vários materiais). Pela mesma regra de transformação, a chave primária do lado "1" migrou como chave estrangeira (`fornecedor_id`) para o lado "N"; ela é opcional, pois um material pode não ter fornecedor.

## Sobre os diagramas
No modelo conceitual (DER), foram identificadas três entidades — FUNCIONARIO, MATERIAL e RETIRADA — conectadas por dois relacionamentos binários do tipo 1:N: "realiza" (entre FUNCIONARIO e RETIRADA) e "refere-se" (entre MATERIAL e RETIRADA).

Na transformação para o modelo lógico relacional, cada entidade do DER originou uma relação (tabela), e seus atributos identificadores (id, codigo) tornaram-se as chaves primárias correspondentes. Como ambos os relacionamentos possuem cardinalidade máxima 1 do lado de FUNCIONARIO e MATERIAL, e cardinalidade máxima N do lado de RETIRADA, aplicou-se a regra de que a chave primária do lado "1" migra como chave estrangeira para a tabela do lado "N". Por isso, a relação RETIRADA recebeu os atributos id_funcionario e codigo_material como chaves estrangeiras, referenciando respectivamente FUNCIONARIO(id) e MATERIAL(codigo). Não foi necessária a criação de tabelas associativas, pois nenhum dos relacionamentos é N:N. 