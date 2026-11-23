# Notas da Versão 6

Base: Projeto-Final-Poo-v-5-sqlalchemy.zip.

Mudanças funcionais:
- nova entidade ORM `Entrada` e `EntradaService`;
- campos de categoria, unidade, estoque inicial/mínimo e situação em materiais;
- situação e data de cadastro em funcionários;
- observação nos eventos de entrada e retirada;
- edição cadastral de funcionários e materiais;
- ativação/inativação sem apagar históricos;
- entrada/reposição registrada com responsável;
- exclusão protegida quando há entradas ou retiradas relacionadas;
- quantidades com `Numeric(10,2)`/Decimal para precisão de estoque;
- configuração de banco por `DATABASE_URL` (SQLite padrão e MySQL opcional).

Arquivos centrais alterados: `modelos/funcionario.py`, `modelos/material.py`, `modelos/retirada.py`, `modelos/entrada.py`, `persistencia/banco.py`, `servicos/funcionario_service.py`, `servicos/material_service.py`, `servicos/retirada_service.py`, `servicos/entrada_service.py`, `aplicacao.py` e menus/telas.

Validação executada:
- `python -m unittest testes.teste_sistema -v`: 8 testes aprovados.
- `python -m unittest testes.teste_v6 -v`: 4 testes aprovados.
