-- Cria os dois schemas da arquitetura: bruto e analitico.
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Tabela bruta em formato longo. A chave (serie, data) impede duplicar
-- a mesma observacao e deixa a recarga idempotente.
CREATE TABLE IF NOT EXISTS raw.observacoes (
    serie  text    NOT NULL,
    data   date    NOT NULL,
    valor  numeric,
    CONSTRAINT pk_observacoes PRIMARY KEY (serie, data)
);
