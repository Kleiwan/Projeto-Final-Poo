"""Configuração do banco de dados SQLite e criação de sessões."""

import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from modelos.base import Base
from modelos import funcionario, material, retirada  # noqa: F401  (registra os modelos)

CAMINHO_PADRAO: Path = Path(__file__).resolve().parent.parent / "dados" / "almoxarifado.db"

# Permite apontar para outro arquivo (usado pelos testes para não tocar no banco principal).
CAMINHO_BANCO: Path = Path(os.environ.get("ALMOXARIFADO_DB", CAMINHO_PADRAO))

engine = create_engine(f"sqlite:///{CAMINHO_BANCO.as_posix()}")


@event.listens_for(engine, "connect")
def _ativar_chaves_estrangeiras(conexao_dbapi, registro_conexao) -> None:
    """Ativa as chaves estrangeiras em toda nova conexão SQLite (desligadas por padrão)."""
    cursor = conexao_dbapi.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def criar_tabelas() -> None:
    """Cria a pasta do banco e as tabelas que ainda não existem."""
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)


def criar_sessao() -> Session:
    """Retorna uma nova sessão associada ao banco configurado."""
    return Session(engine)
