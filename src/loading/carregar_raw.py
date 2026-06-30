import pandas as pd
from sqlalchemy import text

from src.config import SERIES, DATA_RAW
from src.db import get_engine
from src.log import get_logger

log = get_logger("carga")


def carregar():
    """Le os CSVs brutos e empilha tudo em raw.observacoes (formato longo)."""
    quadros = []
    for nome in SERIES:
        df = pd.read_csv(DATA_RAW / f"{nome}.csv", parse_dates=["data"])
        df["serie"] = nome
        quadros.append(df[["serie", "data", "valor"]])
    longo = pd.concat(quadros, ignore_index=True)

    engine = get_engine()
    with engine.begin() as conn: 
        conn.execute(text("TRUNCATE raw.observacoes"))
        longo.to_sql("observacoes", conn, schema="raw", if_exists="append", index=False)
    log.info("Carregadas %s observacoes em raw.observacoes", len(longo))


if __name__ == "__main__":
    carregar()