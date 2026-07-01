import pandas as pd
from src.ingestion.baixar_dados import gerar_janelas


def test_periodo_curto_vira_uma_janela():
    assert len(gerar_janelas("01/01/2020", "31/12/2024", anos=9)) == 1


def test_nenhuma_janela_passa_do_limite():
    # Garante que respeitamos o limite da API para series diarias.
    for ini, fim in gerar_janelas("01/01/2000", "31/12/2024", anos=9):
        di = pd.to_datetime(ini, format="%d/%m/%Y")
        df = pd.to_datetime(fim, format="%d/%m/%Y")
        assert (df - di).days <= 9 * 366


def test_janelas_cobrem_o_periodo_sem_buraco():
    janelas = gerar_janelas("01/01/2010", "31/12/2024", anos=9)
    assert janelas[0][0] == "01/01/2010"
    assert janelas[-1][1] == "31/12/2024"