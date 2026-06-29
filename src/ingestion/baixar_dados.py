import time
import requests
import pandas as pd

from src.config import SERIES, DATA_RAW, DATA_INICIAL, JANELA_ANOS
from src.log import get_logger

log = get_logger("ingestao")
BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"


# Gerador de janelas no tempo
def gerar_janelas(data_inicial, data_final, anos=JANELA_ANOS):
    """Quebra o periodo em janelas de no máximo 'n' anos."""

    d_inicio = pd.to_datetime(data_inicial, format = "%d/%m/%Y")
    d_final = pd.to_datetime(data_final, format = "%d/%m/%Y")

    janelas = []
    
    while d_inicio <= d_final:
        fim_janela = min(
            d_inicio + pd.DateOffset(years = anos),
            d_final
        )
        janelas.append(
            (d_inicio.strftime("%d/%m/%Y"), 
            fim_janela.strftime("%d/%m/%Y"))
        )

        d_inicio = fim_janela + pd.DateOffset(days=1)
    
    return janelas 

# Baixar os dados
def baixar_intervalo(codigo, data_inicial, data_final, tentativas=3):
    url = BASE_URL.format(codigo = codigo)
    parametros = {
        "formato" : "json",
        "dataInicial" : data_inicial,
        "dataFinal" : data_final
    }

    for tentativa in range(1 ,tentativas + 1):
        try:
            resposta = requests.get(url, parametros, timeout=30)
            resposta.raise_for_status()
            return resposta.json()
        except requests.exceptions.RequestException as erro :
            if tentativa == tentativas:
                raise
            espera = 5 * tentativa
            log.warning("falhou (tentativa %s): %s. Repetindo em %ss...", tentativa, erro, espera)
            time.sleep(espera)

def baixar_serie(codigo, data_inicial = DATA_INICIAL):
    # Baixa a série toda e junta as janelas
    hoje = pd.Timestamp.today().strftime("%d/%m/%Y")

    partes = []
    for inicio, fim in gerar_janelas(data_inicial, hoje):
        partes.extend(baixar_intervalo(codigo, inicio, fim))

    #transformar em dataframe
    df = pd.DataFrame(partes)

    #Conversão de texto para datetime/numeric
    df['data'] = pd.to_datetime(df['data'], format = "%d/%m/%Y")
    df['valor'] = pd.to_numeric(df['valor'], errors= "coerce")

    return df.drop_duplicates(subset="data").sort_values("data").reset_index(drop=True)

def main():
    DATA_RAW.mkdir(parents=True, exist_ok= True)
    for nome, codigo in SERIES.items():
        log.info("Baixando a série %s (código %s) ...", nome, codigo)
        df = baixar_serie(codigo)
        df.to_csv(DATA_RAW/ f"{nome}.csv", index = False)
        log.info("%s linhas salvas", len(df))
        time.sleep(1)

if __name__ == "__main__":
    main()






#def main()