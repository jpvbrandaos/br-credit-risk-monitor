import pandas as pd
from sqlalchemy import text

from src.config import SQL_DIR, DATA_PROCESSED
from src.db import get_engine
from src.log import get_logger

log = get_logger("analytics")


def construir():
    """Roda o 02_analytics.sql (cria a matview) e exporta para CSV."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text((SQL_DIR / "02_analytics.sql").read_text(encoding="utf-8")))

    with engine.connect() as conn:
        df = pd.read_sql(
            "SELECT * FROM analytics.indicadores_mensais ORDER BY mes", conn
        )

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PROCESSED / "indicadores.csv", index=False)
    log.info("analytics.indicadores_mensais: %s meses. CSV exportado.", len(df))


if __name__ == "__main__":
    construir()