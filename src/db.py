from sqlalchemy import create_engine
from src.config import DATABASE_URL


def get_engine():
    """Cria o engine do SQLAlchemy a partir da URL do .env."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL nao definida. Crie o arquivo .env (veja o Passo 3).")
    return create_engine(DATABASE_URL, future=True)
