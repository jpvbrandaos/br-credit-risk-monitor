import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(
    page_title="Monitor de Crédito e Risco do Brasil",
    page_icon="📊",
    layout="wide",
)

# Paleta unica, usada em TODOS os graficos para dar identidade visual.
AZUL = "#2563EB"     # primeira serie
AMBAR = "#F59E0B"    # segunda serie
PALETA = [AZUL, AMBAR]


@st.cache_data
def carregar():
    return pd.read_csv("data/processed/indicadores.csv", parse_dates=["mes"])


df = carregar()


def grafico_linha(dados, colunas, y_titulo, altura=340):
    """colunas: {coluna_do_csv: nome_amigavel}. Grafico de linha com a paleta padrao."""
    d = (
        dados.melt(id_vars="mes", value_vars=list(colunas), var_name="col", value_name="valor")
        .assign(Indicador=lambda x: x["col"].map(colunas))
        .dropna(subset=["valor"])
    )
    dominio = list(colunas.values())
    return (
        alt.Chart(d)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=alt.X("mes:T", title="Mês"),
            y=alt.Y("valor:Q", title=y_titulo),
            color=alt.Color(
                "Indicador:N", title="",
                scale=alt.Scale(domain=dominio, range=PALETA[: len(dominio)]),
                legend=alt.Legend(orient="top"),
            ),
            tooltip=[
                alt.Tooltip("mes:T", title="Mês"),
                alt.Tooltip("Indicador:N", title="Indicador"),
                alt.Tooltip("valor:Q", title="Valor", format=".2f"),
            ],
        )
        .properties(height=altura)
        .interactive()
    )


# ---------------- Barra lateral ----------------
anos = df["mes"].dt.year
ano_min, ano_max = int(anos.min()), int(anos.max())
with st.sidebar:
    st.header("Filtros")
    faixa = st.slider("Período dos gráficos", ano_min, ano_max, (ano_min, ano_max))
    st.markdown("---")
    st.caption(
        "Dados mensais do Banco Central (SGS). Os cartões e a defasagem usam a série "
        "inteira; o filtro acima afeta apenas os gráficos de linha."
    )

dff = df[df["mes"].dt.year.between(*faixa)]

# ---------------- Cabeçalho ----------------
st.title("Monitor de Crédito e Risco do Brasil")
st.caption(
    "A saúde do crédito no país num lugar só: inadimplência, endividamento das famílias, "
    "juros e spread bancário. Fonte: Banco Central (SGS), de 2010 até o mês mais recente."
)

# ---------------- Retrato atual (KPIs) ----------------
base = df.dropna(subset=["inadimplencia_total"]).reset_index(drop=True)
hoje = base.iloc[-1]
ano = base.iloc[-13] if len(base) > 13 else base.iloc[0]

st.subheader(f"Retrato de {hoje['mes'].strftime('%m/%Y')}")


def card(coluna, rotulo, campo, inverter=False):
    delta = hoje[campo] - ano[campo]
    coluna.metric(
        rotulo,
        f"{hoje[campo]:.2f}%",
        f"{delta:+.2f} p.p. em 12 meses",
        delta_color="inverse" if inverter else "normal",
    )


k = st.columns(4)
card(k[0], "Inadimplência total", "inadimplencia_total", inverter=True)
card(k[1], "Inadimplência PF", "inadimplencia_pf", inverter=True)
card(k[2], "Selic (meta)", "selic_meta")
card(k[3], "Spread bancário", "spread_total", inverter=True)
st.caption("Variação em pontos percentuais nos últimos 12 meses. "
           "Em inadimplência e spread, a seta vermelha para cima indica piora.")

# ---------------- Fase do ciclo ----------------
d_inad = base["inadimplencia_total"].iloc[-1] - base["inadimplencia_total"].iloc[-4]
d_selic = base["selic_meta"].iloc[-1] - base["selic_meta"].iloc[-4]
if d_selic > 0 and d_inad <= 0:
    fase, texto, tipo = "Aperto monetário", "os juros subiram e a inadimplência ainda não reagiu.", "warning"
elif d_inad > 0:
    fase, texto, tipo = "Deterioração do crédito", "a inadimplência vem subindo, sinal de crédito sob pressão.", "warning"
elif d_selic < 0 and d_inad < 0:
    fase, texto, tipo = "Recuperação", "juros e inadimplência caindo juntos.", "success"
else:
    fase, texto, tipo = "Estável", "sem movimento forte nos últimos meses.", "info"

st.subheader("Em que fase do ciclo o país está")
getattr(st, tipo)(f"**{fase}.** {texto}")

st.divider()

# ---------------- Séries ----------------
st.header("Como os indicadores evoluíram")

st.subheader("Inadimplência: pessoa física x pessoa jurídica")
st.caption("Parcela da carteira de crédito com pagamento em atraso. A da pessoa física costuma ficar bem acima da jurídica.")
st.altair_chart(
    grafico_linha(dff, {"inadimplencia_pf": "Pessoa física", "inadimplencia_pj": "Pessoa jurídica"},
                  "% da carteira em atraso"),
    use_container_width=True,
)

st.subheader("Endividamento e comprometimento de renda das famílias")
st.caption("Endividamento é o quanto a família deve em relação à renda de um ano. "
           "Comprometimento é a fatia da renda mensal que já vai para pagar dívida.")
st.altair_chart(
    grafico_linha(dff, {"endividamento_familias": "Endividamento", "comprometimento_renda": "Comprometimento"},
                  "% da renda"),
    use_container_width=True,
)

st.subheader("Spread bancário e Selic")
st.caption("O spread é a diferença entre o juro cobrado do cliente e o custo de captação do banco. Nem sempre acompanha a Selic.")
st.altair_chart(
    grafico_linha(dff, {"spread_total": "Spread", "selic_meta": "Selic"}, "% ao ano"),
    use_container_width=True,
)

st.divider()

# ---------------- Defasagem (destaque) ----------------
st.header("A relação entre juros e inadimplência")
lags = pd.DataFrame({"defasagem": range(0, 19)})
lags["correlacao"] = [df["inadimplencia_total"].corr(df["selic_meta"].shift(k)) for k in range(0, 19)]
melhor = int(lags.loc[lags["correlacao"].idxmax(), "defasagem"])

st.markdown(
    f"#### A inadimplência reage à Selic com cerca de **{melhor} meses** de defasagem."
)
st.caption("Correlação entre a inadimplência de hoje e a Selic de alguns meses atrás. "
           "O pico marca em quantos meses a relação é mais forte, o que dá um sinal antecipado de risco.")
st.altair_chart(
    alt.Chart(lags).mark_bar(color=AZUL).encode(
        x=alt.X("defasagem:O", title="Defasagem (meses)"),
        y=alt.Y("correlacao:Q", title="Correlação"),
        tooltip=[alt.Tooltip("defasagem:O", title="Meses"),
                 alt.Tooltip("correlacao:Q", title="Correlação", format=".3f")],
    ).properties(height=300),
    use_container_width=True,
)

st.divider()

# ---------------- Conclusões ----------------
st.header("Principais conclusões")
st.markdown(
    f"""
A inadimplência da pessoa física é estruturalmente mais alta e mais volátil que a da jurídica, e voltou a subir desde o fundo de 2020.

As famílias estão mais endividadas e comprometendo uma fatia maior da renda, as duas nos maiores níveis da série nos últimos anos.

O spread só acompanha a Selic em parte, e em vários momentos sobe por conta própria, sinal de prêmio de risco além do juro básico.

A inadimplência reage à Selic com cerca de {melhor} meses de defasagem, o que ajuda a antecipar o risco de crédito quase um ano à frente.

O país está hoje em fase de {fase.lower()}, na esteira do juro alto dos últimos anos.
"""
)

with st.expander("Metodologia e fonte"):
    st.markdown(
        """
Os dados vêm do Sistema Gerenciador de Séries Temporais (SGS) do Banco Central do Brasil,
coletados via API pública. O dado bruto é guardado como veio da fonte, tratado e unificado
numa tabela mensal dentro de um banco PostgreSQL, e as análises são feitas em SQL.

A **fase do ciclo** é uma regra simples e transparente (não um modelo): combina a direção
da inadimplência e da Selic nos últimos três meses. A **defasagem** é obtida testando a
correlação da inadimplência com a Selic de 0 a 18 meses atrás e escolhendo a mais forte.

Os números são agregados no nível do país e passam por revisões periódicas do Banco Central.
"""
    )

st.divider()
st.caption("Projeto de portfólio de João Pedro Vieira Brandão. Dados: Banco Central do Brasil (SGS).")
