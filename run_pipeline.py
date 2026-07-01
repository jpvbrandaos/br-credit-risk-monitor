"""Roda o pipeline inteiro: ingestao -> schema -> carga -> analytics -> export."""
from sqlalchemy import text

from src.config import SQL_DIR
from src.db import get_engine
from src.log import get_logger
from src.ingestion.baixar_dados import main as baixar
from src.loading.carregar_raw import carregar
from src.processing.construir_analytics import construir

log = get_logger("pipeline")


def aplicar_schema():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text((SQL_DIR / "01_schema.sql").read_text(encoding="utf-8")))
    log.info("Schema aplicado (raw, analytics).")


def main():
    log.info("== 1/4 Ingestao ==");  baixar()
    log.info("== 2/4 Schema ==");    aplicar_schema()
    log.info("== 3/4 Carga ==");     carregar()
    log.info("== 4/4 Analytics =="); construir()
    log.info("Pipeline concluido com sucesso.")


if __name__ == "__main__":
    main()