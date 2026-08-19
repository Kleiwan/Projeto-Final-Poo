```mermaid
erDiagram
    FUNCIONARIO {
        int id PK
        string nome
        string Setor
    }

    MATERIAL {
        int codigo PK
        string nome
        int qt_material
    }

    RETIRADA {
        int id PK
        int qtd
    }

    %% Relacionamentos e Cardinalidades
    FUNCIONARIO ||--|{ RETIRADA : realiza
    MATERIAL ||--|{ RETIRADA : contem