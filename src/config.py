import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # le o arquivo .env e joga as variaveis no ambiente
RAIZ = Path(__file__).resolve().parents[1]
DATA_RAW = RAIZ / "data" / "raw"
DATA_PROCESSED = RAIZ / "data" / "processed"
SQL_DIR = RAIZ / "sql"

# Conexao com o Postgres, lida do .env. 
DATABASE_URL = os.environ.get("DATABASE_URL")

# Data de coleta
DATA_INICIAL = "01/01/2010"
JANELA_ANOS = 9  # a API recusa series diarias com mais de ~10 anos por chamada

# Series do projeto: nome amigavel -> codigo no SGS/BACEN.
SERIES = {
    "inadimplencia_total": 21082,
    "inadimplencia_pf": 21084,
    "inadimplencia_pj": 21083,
    "endividamento_familias": 29037,
    "comprometimento_renda": 29034,
    "spread_total": 20783,
    "selic_meta": 432,
    "ipca": 433,
}