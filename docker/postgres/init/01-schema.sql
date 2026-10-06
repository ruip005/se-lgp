-- Corre só na PRIMEIRA criação do volume. Para reaplicar: docker compose down -v
-- Sem dados pessoais nem imagens (RNF-04): só métricas e texto.

CREATE TABLE IF NOT EXISTS run (
    id          BIGSERIAL PRIMARY KEY,
    started_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    mode        TEXT NOT NULL CHECK (mode IN ('local', 'hybrid')),
    host        TEXT,
    model_ver   TEXT,
    notes       TEXT
);

-- RF-11: métricas por previsão
CREATE TABLE IF NOT EXISTS prediction (
    id          BIGSERIAL PRIMARY KEY,
    run_id      BIGINT NOT NULL REFERENCES run(id) ON DELETE CASCADE,
    ts          TIMESTAMPTZ NOT NULL DEFAULT now(),
    label       TEXT,
    confidence  REAL,
    latency_ms  REAL,
    accepted    BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_prediction_run ON prediction(run_id);

-- RF-13: histórico de frases
CREATE TABLE IF NOT EXISTS phrase (
    id          BIGSERIAL PRIMARY KEY,
    run_id      BIGINT REFERENCES run(id) ON DELETE SET NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    glosses     TEXT NOT NULL,
    text_pt     TEXT
);
