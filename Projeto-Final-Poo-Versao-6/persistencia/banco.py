"""Configuração da conexão com o banco usando SQLAlchemy e variáveis de ambiente."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, event
from sqlalchemy.orm import Session

from modelos.base import Base
from modelos import funcionario, material, retirada, entrada  # registra os modelos ORM

# Carrega o .env antes de consultar as configurações.
# O caminho é relativo à raiz do projeto, independentemente da pasta de execução.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ_PROJETO / ".env")

PASTA_DADOS = RAIZ_PROJETO / "dados"
CAMINHO_PADRAO = PASTA_DADOS / "almoxarifado_v6.db"
TIPO_BANCO = os.getenv("DB_DRIVER", "sqlite").strip().lower()

if TIPO_BANCO == "mysql":
    # URL.create trata corretamente senhas com caracteres especiais.
    URL_BANCO = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "almoxarifado_v2"),
        query={"charset": "utf8mb4"},
    )
    engine = create_engine(URL_BANCO, pool_pre_ping=True)
elif TIPO_BANCO == "sqlite":
    caminho_sqlite = Path(os.getenv("ALMOXARIFADO_DB", str(CAMINHO_PADRAO)))
    if not caminho_sqlite.is_absolute():
        caminho_sqlite = RAIZ_PROJETO / caminho_sqlite
    URL_BANCO = URL.create("sqlite", database=str(caminho_sqlite))
    engine = create_engine(URL_BANCO, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def _ativar_chaves_estrangeiras(conexao_dbapi, registro_conexao):
        cursor = conexao_dbapi.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    raise ValueError(
        "DB_DRIVER inválido. Utilize 'sqlite' ou 'mysql' no arquivo .env."
    )


def criar_tabelas():
    """Cria tabelas ausentes; não altera tabelas que já existem."""
    if TIPO_BANCO == "sqlite":
        PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)


def criar_sessao() -> Session:
    """Retorna uma sessão SQLAlchemy vinculada ao banco configurado."""
    return Session(engine)
