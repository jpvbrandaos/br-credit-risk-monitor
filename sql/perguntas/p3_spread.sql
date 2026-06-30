-- pergunta 3: o spread acompanha os juros?
SELECT
    mes,
    spread_total,
    selic_meta,
    corr(spread_total, selic_meta)
        OVER (ORDER BY mes ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS corr_movel_12m
FROM analytics.indicadores_mensais
WHERE spread_total IS NOT NULL
  AND selic_meta  IS NOT NULL
ORDER BY mes;