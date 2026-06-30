-- Pergunta 4 — defasagem ótima entre juros e inadimplência
WITH base AS (
    SELECT mes, inadimplencia_total, selic_meta
    FROM analytics.indicadores_mensais
    WHERE inadimplencia_total IS NOT NULL
),
defasagens AS (
    SELECT
        g.k,
        b.inadimplencia_total,
        LAG(b.selic_meta, g.k) OVER (PARTITION BY g.k ORDER BY b.mes) AS selic_defasada
    FROM base b
    CROSS JOIN generate_series(0, 18) AS g(k)
)
SELECT
    k AS meses_de_defasagem,
    round(corr(inadimplencia_total, selic_defasada)::numeric, 3) AS correlacao
FROM defasagens
GROUP BY k
ORDER BY correlacao DESC;