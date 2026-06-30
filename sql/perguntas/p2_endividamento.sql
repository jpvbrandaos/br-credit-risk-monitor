-- Pergunta 2: endividamento e comprometimento da renda
SELECT
    mes,
    endividamento_familias,
    comprometimento_renda
FROM analytics.indicadores_mensais
WHERE endividamento_familias IS NOT NULL
ORDER BY mes;

-- Correlacao geral entre as duas (roda separado):
-- SELECT corr(endividamento_familias, comprometimento_renda)
-- FROM analytics.indicadores_mensais;