import pandas as pd
from src.config import DATA_PROCESSED


def carregar_csv():
    return pd.read_csv(DATA_PROCESSED / "indicadores.csv", parse_dates=["mes"])


def test_tem_as_colunas_principais():
    df = carregar_csv()
    assert {"mes", "inadimplencia_total", "selic_meta", "spread_total"}.issubset(df.columns)


def test_um_registro_por_mes():
    df = carregar_csv()
    assert df["mes"].is_unique  # a matview nao pode duplicar mes


def test_valores_plausiveis():
    df = carregar_csv()
    inad = df["inadimplencia_total"].dropna()
    assert inad.between(0, 20).all()  # inadimplencia em % nessa faixa faz sentido