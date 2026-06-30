-- Pergunta 1 — inadimplência subindo ou caindo, PF ou PJ.
SELECT
    mes,
    inadimplencia_pf,
    inadimplencia_pj,
    inadimplencia_pf - inadimplencia_pj                          AS gap_pf_pj,
    inadimplencia_pf - LAG(inadimplencia_pf, 12) OVER (ORDER BY mes) AS variacao_pf_12m
FROM analytics.indicadores_mensais
WHERE inadimplencia_pf IS NOT NULL
ORDER BY mes;