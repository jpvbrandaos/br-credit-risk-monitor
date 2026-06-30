-- Pergunta 5 — em que fase do ciclo o país está
WITH movimento AS (
    SELECT
        mes,
        inadimplencia_total,
        selic_meta,
        inadimplencia_total - LAG(inadimplencia_total, 3) OVER (ORDER BY mes) AS d_inad_3m,
        selic_meta          - LAG(selic_meta, 3)          OVER (ORDER BY mes) AS d_selic_3m
    FROM analytics.indicadores_mensais
    WHERE inadimplencia_total IS NOT NULL
)
SELECT
    mes,
    inadimplencia_total,
    selic_meta,
    CASE
        WHEN d_selic_3m > 0 AND d_inad_3m <= 0 THEN 'Aperto monetario'
        WHEN d_inad_3m > 0                     THEN 'Deterioracao do credito'
        WHEN d_selic_3m < 0 AND d_inad_3m < 0  THEN 'Recuperacao'
        ELSE 'Estavel'
    END AS fase_do_ciclo
FROM movimento
ORDER BY mes;