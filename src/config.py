import os
from pathlib import Path
from dotenv import load_dotenv

# Raiz do projeto (este arquivo esta em src/, entao subimos um nivel).
RAIZ = Path(__file__).resolve().parents[1]

# Le o .env a partir da RAIZ do projeto (e nao do diretorio atual). Assim
# funciona rodando da raiz com 'python -m ...' e tambem de um notebook em
# notebooks/, que tem outro diretorio de trabalho.
load_dotenv(RAIZ / ".env")

DATA_RAW = RAIZ / "data" / "raw"
DATA_PROCESSED = RAIZ / "data" / "processed"
SQL_DIR = RAIZ / "sql"

# Conexao com o Postgres, lida do .env. NUNCA escreva senha no codigo.
DATABASE_URL = os.environ.get("DATABASE_URL")

# A partir de quando coletar; e o tamanho da janela de download.
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
