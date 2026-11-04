"""Configuração do banco de dados SQLite e criação de sessões."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from modelos.base import Base
from modelos import funcionario, material, retirada  # noqa: F401  (registra os modelos)

CAMINHO_BANCO: Path = Path(__file__).resolve().parent.parent / "dados" / "almoxarifado.db"

engine = create_engine(f"sqlite:///{CAMINHO_BANCO.as_posix()}")


def criar_tabelas() -> None:
    """Cria a pasta do banco e as tabelas que ainda não existem."""
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)


def criar_sessao() -> Session:
    """Retorna uma nova sessão associada ao banco configurado."""
    return Session(engine)
