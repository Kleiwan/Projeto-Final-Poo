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

Iniciar conexão:
- `python -m pip install -r requirements.txt` instala as bibliotecas necessárias no py
- `SHOW DATABASES;` verifica se a database do almoxarifado já existe no sql
- caso não exista, execute o sql, ele criará a database
- - `python -c "from persistencia.banco import engine; from sqlalchemy import text; conexao = engine.connect(); print('Conexão estabelecida!'); print('Banco:', conexao.execute(text('SELECT DATABASE()')).scalar()); conexao.close()"` verifica se a conexão foi realizada por meio do terminal no vscode
- `python main.py` execute e inicie o programa
- `USE almoxarifado_v2;
  SELECT * FROM funcionarios;` execute e teste a conexão com o banco novamente
