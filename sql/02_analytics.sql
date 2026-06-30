DROP MATERIALIZED VIEW IF EXISTS analytics.indicadores_mensais;

CREATE MATERIALIZED VIEW analytics.indicadores_mensais AS
SELECT
    date_trunc('month', data)::date                              AS mes,
    avg(valor) FILTER (WHERE serie = 'inadimplencia_total')      AS inadimplencia_total,
    avg(valor) FILTER (WHERE serie = 'inadimplencia_pf')         AS inadimplencia_pf,
    avg(valor) FILTER (WHERE serie = 'inadimplencia_pj')         AS inadimplencia_pj,
    avg(valor) FILTER (WHERE serie = 'endividamento_familias')   AS endividamento_familias,
    avg(valor) FILTER (WHERE serie = 'comprometimento_renda')    AS comprometimento_renda,
    avg(valor) FILTER (WHERE serie = 'spread_total')             AS spread_total,
    avg(valor) FILTER (WHERE serie = 'selic_meta')               AS selic_meta,
    avg(valor) FILTER (WHERE serie = 'ipca')                     AS ipca
FROM raw.observacoes
GROUP BY date_trunc('month', data)
ORDER BY mes;

-- Indice unico no mes
CREATE UNIQUE INDEX IF NOT EXISTS idx_indicadores_mes
    ON analytics.indicadores_mensais (mes);