-- PostgreSQL: visão operacional das últimas 24 horas.
SELECT
    date_trunc('hour', occurred_at) AS hour,
    COUNT(*) AS processed_events,
    SUM(COUNT(*)) OVER (ORDER BY date_trunc('hour', occurred_at)) AS cumulative_events
FROM processed_events
WHERE occurred_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY date_trunc('hour', occurred_at)
ORDER BY hour;

-- Distribuição de alertas e participação no total.
SELECT
    reason,
    COUNT(*) AS alert_count,
    ROUND(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (), 0), 2) AS share_pct
FROM alerts
GROUP BY reason
ORDER BY alert_count DESC;

-- Atraso observado na quarentena.
SELECT
    COUNT(*) AS late_events,
    MAX(watermark - occurred_at) AS maximum_lateness
FROM late_events
WHERE occurred_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours';

