# Sistema de Almoxarifado — Versão 6

Sistema de gerenciamento de almoxarifado desenvolvido em Python, utilizando Programação Orientada a Objetos (POO), SQLAlchemy e banco de dados relacional.

A versão 6 dá continuidade às versões anteriores do projeto, reorganizando sua estrutura e utilizando o SQLAlchemy ORM para realizar a persistência dos dados. O sistema permite gerenciar funcionários, materiais, entradas e retiradas, aplicando regras de negócio para controlar o estoque e as movimentações.

## 1. Tecnologias utilizadas

- **Python 3.10 ou superior**
- **SQLAlchemy 2.x:** mapeamento objeto-relacional (ORM).
- **PyMySQL:** conexão com o MySQL.
- **python-dotenv:** leitura das variáveis de ambiente.
- **SQLite:** banco de dados local utilizado como configuração padrão.
- **MySQL 8:** banco de dados relacional utilizado na versão V2.

## 2. Estrutura do projeto

```text
Projeto-Final-Poo-Versao-6/
│
├── dados/
│   └── .gitkeep
│
├── excecoes/
│   ├── __init__.py
│   └── almoxarifado_error.py
│
├── interface/
│
├── modelos/
│   ├── __init__.py
│   ├── base.py
│   ├── entrada.py
│   ├── funcionario.py
│   ├── material.py
│   └── retirada.py
│
├── persistencia/
│   ├── __init__.py
│   └── banco.py
│
├── servicos/
│   ├── entrada_service.py
│   ├── funcionario_service.py
│   ├── material_service.py
│   └── retirada_service.py
│
├── testes/
│   ├── consultar_banco.py
│   ├── teste_sistema.py
│   └── teste_v6.py
│
├── .env.example
├── .gitignore
├── aplicacao.py
├── main.py
├── README.md
├── requirements.txt
└── VERSAO_6_NOTAS.md
```

### Organização das responsabilidades

- **modelos:** definem as entidades do sistema e seu mapeamento para as tabelas do banco.
- **servicos:** concentram as operações e regras de negócio.
- **persistencia:** configura a conexão e as sessões do banco de dados.
- **interface:** contém os componentes da interface do sistema.
- **excecoes:** reúne as exceções específicas do projeto.
- **testes:** contém os arquivos utilizados para verificar o funcionamento do sistema.
- **dados:** diretório utilizado para armazenar o banco SQLite local, quando essa configuração estiver ativa.

## 3. Instalação e execução

### 3.1. Clonar o projeto

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd Projeto-Final-Poo-Versao-6
```

### 3.2. Criar o ambiente virtual

```bash
python -m venv venv
```

Ativar no Windows:

```powershell
venv\Scripts\activate
```

### 3.3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 3.4. Executar o sistema

```bash
python main.py
```

## 4. Configuração do banco de dados

O projeto permite utilizar SQLite ou MySQL. A escolha é realizada por meio das variáveis de ambiente definidas no arquivo `.env`.

### 4.1. Configuração com SQLite

O SQLite é a configuração padrão quando a variável `DB_DRIVER` não está definida.

O banco local é criado no diretório `dados/`, utilizando o nome:

```text
almoxarifado_v6.db
```

Não é necessário instalar ou configurar um servidor externo para utilizar essa opção.

### 4.2. Configuração com MySQL

Para utilizar o banco MySQL V2, é necessário:

1. Instalar e iniciar o MySQL Server 8.
2. Abrir o MySQL Workbench.
3. Executar o script SQL da versão 2, disponibilizado na entrega do projeto.
4. Criar o arquivo `.env` na raiz do projeto.
5. Configurar as variáveis de conexão.

O banco utilizado nesta configuração é:

```text
almoxarifado_v2
```

#### Arquivo `.env`

Crie uma cópia do arquivo `.env.example` e renomeie-a para `.env`.

Preencha as configurações:

```env
DB_DRIVER=mysql
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=almoxarifado_v2
```

**Importante:** substitua `sua_senha` pela senha configurada no seu MySQL. Não compartilhe esse arquivo nem envie suas credenciais ao GitHub.

O arquivo `.env` deve permanecer listado no `.gitignore`.

### 4.3. Como a conexão funciona

A conexão é configurada em `persistencia/banco.py`, utilizando:

- `python-dotenv` para carregar as variáveis de ambiente;
- `SQLAlchemy` para criar o mecanismo de conexão;
- `PyMySQL` como driver de comunicação com o MySQL;
- `Session` para gerenciar as operações com o banco.

O método `criar_tabelas()` utiliza `Base.metadata.create_all(engine)` para criar tabelas ausentes. Ele não substitui o script SQL V2 nem realiza migrações automáticas de estruturas já existentes.

## 5. Banco de dados V2

A versão 2 do banco de dados utiliza quatro tabelas principais:

| Tabela | Finalidade |
|---|---|
| `funcionarios` | Armazena os funcionários e suas permissões. |
| `materiais` | Armazena os materiais e suas informações de estoque. |
| `retiradas` | Registra as retiradas de materiais. |
| `entradas` | Registra as entradas de materiais. |

### 5.1. Relacionamentos

- Um funcionário pode estar associado a várias retiradas.
- Um material pode aparecer em várias retiradas.
- Um funcionário pode registrar várias entradas.
- Um material pode aparecer em várias entradas.

As tabelas `retiradas` e `entradas` possuem chaves estrangeiras que as relacionam às tabelas `funcionarios` e `materiais`.

### 5.2. Massa de dados

O banco V2 foi verificado no MySQL Workbench e apresenta a seguinte quantidade de registros:

| Tabela | Registros |
|---|---:|
| Funcionários | 100 |
| Materiais | 100 |
| Retiradas | 2.400 |
| Entradas | 400 |
| **Total** | **3.000** |

### 5.3. Diagrama Entidade-Relacionamento

O DER do banco de dados V2 está disponível no arquivo:

```text
DER_Almoxarifado_V2.pdf
```

O documento apresenta as entidades, seus atributos, as chaves primárias, as chaves estrangeiras e os relacionamentos entre as tabelas.

## 6. Funcionalidades do sistema

O sistema contempla operações de gerenciamento de:

### Funcionários
- Cadastro de funcionários.
- Consulta de funcionários.
- Edição de informações.
- Ativação e desativação.
- Controle da permissão para retirar materiais.

### Materiais
- Cadastro de materiais.
- Consulta de materiais.
- Edição de informações.
- Ativação e desativação.
- Controle de estoque mínimo.
- Bloqueio e desbloqueio de materiais.

### Entradas
- Registro de entrada de materiais.
- Consulta de entradas registradas.
- Atualização do estoque após uma entrada.

### Retiradas
- Registro de retirada de materiais.
- Consulta de retiradas registradas.
- Atualização do estoque após uma retirada.

## 7. Regras de negócio

O sistema aplica validações para manter a consistência das operações:

- Não permitir quantidades inválidas ou negativas.
- Não permitir retiradas superiores ao estoque disponível.
- Respeitar a permissão de retirada dos funcionários.
- Impedir operações com materiais bloqueados ou inativos.
- Considerar o estado ativo ou inativo dos funcionários e materiais.
- Impedir a exclusão de registros que possuam movimentações relacionadas, quando houver restrição de chave estrangeira.
- Atualizar a quantidade em estoque conforme as entradas e retiradas realizadas.

As validações são implementadas nos serviços e complementadas pelas restrições do banco de dados.

## 8. Testes

Os arquivos de teste estão localizados na pasta `testes/`.

Para executar os testes automatizados:

```bash
python -m unittest testes.teste_v6 -v
```

```bash
python -m unittest testes.teste_sistema -v
```

Para executar o arquivo de consulta ao banco:

```bash
python testes/consultar_banco.py
```

A execução dos testes deve ser realizada com o banco configurado corretamente.

## 9. Observações sobre a persistência

O projeto utiliza SQLAlchemy ORM para intermediar as operações entre os objetos Python e as tabelas do banco de dados.

A persistência pode ocorrer no SQLite ou no MySQL, conforme a configuração do arquivo `.env`.

Ao utilizar o MySQL V2, o sistema deve apontar para o banco `almoxarifado_v2`, previamente criado e estruturado pelo script SQL.

## 10. Arquivos da entrega

Os principais documentos e arquivos relacionados ao projeto são:

| Arquivo | Descrição |
|---|---|
| `README.md` | Documentação e instruções do sistema Python. |
| `requirements.txt` | Dependências necessárias para execução. |
| `.env.example` | Modelo de configuração da conexão. |
| `database.sql` | Script SQL do banco de dados V2. |
| `DER_Almoxarifado_V2.pdf` | Diagrama Entidade-Relacionamento. |
| `VERSAO_6_NOTAS.md` | Notas sobre as alterações da versão 6. |

**Atenção:** o script SQL V2 contém comandos de criação e remoção de tabelas para preparar o banco. Antes de executá-lo novamente em um banco que já contém dados, faça uma cópia de segurança.

---

**Projeto:** Sistema de Almoxarifado  
**Versão da aplicação:** 6  
**Versão do banco de dados:** 2