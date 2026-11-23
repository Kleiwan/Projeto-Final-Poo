
erDiagram
    FUNCIONARIOS ||--o{ RETIRADAS : realiza
    FUNCIONARIOS ||--o{ ENTRADAS : registra
    MATERIAIS ||--o{ RETIRADAS : movimenta
    MATERIAIS ||--o{ ENTRADAS : recebe

    FUNCIONARIOS {
        int id PK
        varchar nome
        varchar setor
        boolean pode_retirar
        boolean ativo
        datetime data_cadastro
    }

    MATERIAIS {
        varchar codigo PK
        varchar nome
        varchar categoria
        varchar unidade_medida
        decimal estoque_inicial
        decimal quantidade
        decimal estoque_minimo
        boolean bloqueado
        varchar motivo_bloqueio
        boolean ativo
    }

    RETIRADAS {
        bigint id PK
        int funcionario_id FK
        varchar material_codigo FK
        decimal quantidade
        datetime momento
        varchar observacao
    }

    ENTRADAS {
        bigint id PK
        int funcionario_id FK
        varchar material_codigo FK
        decimal quantidade
        datetime momento
        varchar observacao
    }
