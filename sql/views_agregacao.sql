-- =====================================================================
-- ESG Impact Pipeline | Views de agregação (SQLite)
-- Modelo estrela: dim_projetos (1) --- (N) fato_beneficiarios
-- Uso: sqlite3 esg_impact.db < sql/views_agregacao.sql
-- =====================================================================

-- KPIs gerais (equivalem aos cards do dashboard)
DROP VIEW IF EXISTS vw_kpis_gerais;
CREATE VIEW vw_kpis_gerais AS
SELECT
    COUNT(*)                                                             AS total_beneficiarios,
    SUM(status_retencao_6m)                                              AS total_retidos,
    ROUND(AVG(status_retencao_6m) * 100, 2)                              AS taxa_retencao_pct,
    ROUND(AVG(renda_pos_6m_brl - renda_inicial_brl), 2)                  AS delta_medio_renda_brl,
    ROUND((SELECT SUM(orcamento_anual) FROM dim_projetos) / COUNT(*), 2) AS custo_por_beneficiario_brl
FROM fato_beneficiarios;

-- Retenção e ganho de renda por eixo ESG
DROP VIEW IF EXISTS vw_retencao_por_eixo;
CREATE VIEW vw_retencao_por_eixo AS
SELECT
    p.eixo_esg,
    COUNT(b.beneficiario_id)                                      AS total_beneficiarios,
    ROUND(AVG(b.status_retencao_6m) * 100, 2)                     AS taxa_retencao_pct,
    ROUND(AVG(b.renda_pos_6m_brl - b.renda_inicial_brl), 2)       AS delta_medio_renda_brl
FROM fato_beneficiarios b
JOIN dim_projetos p ON p.projeto_id = b.projeto_id
GROUP BY p.eixo_esg;

-- Resumo por hub (tabela do dashboard) + custo por beneficiário
DROP VIEW IF EXISTS vw_resumo_por_hub;
CREATE VIEW vw_resumo_por_hub AS
SELECT
    p.projeto_id,
    p.nome_projeto,
    p.eixo_esg,
    p.cidade,
    p.gerente_responsavel,
    p.orcamento_anual,
    COUNT(b.beneficiario_id)                                      AS total_beneficiarios,
    ROUND(AVG(b.status_retencao_6m) * 100, 2)                     AS taxa_retencao_pct,
    ROUND(p.orcamento_anual / COUNT(b.beneficiario_id), 2)        AS custo_por_beneficiario_brl
FROM dim_projetos p
LEFT JOIN fato_beneficiarios b ON b.projeto_id = p.projeto_id
GROUP BY p.projeto_id;

-- Cohort mensal: safra de cadastro -> retenção e ganho de renda
DROP VIEW IF EXISTS vw_cohort_mensal;
CREATE VIEW vw_cohort_mensal AS
SELECT
    SUBSTR(data_cadastro, 1, 7)                                   AS mes_cadastro,
    COUNT(*)                                                      AS total_beneficiarios,
    ROUND(AVG(status_retencao_6m) * 100, 2)                       AS taxa_retencao_pct,
    ROUND(AVG(renda_pos_6m_brl - renda_inicial_brl), 2)           AS delta_medio_renda_brl
FROM fato_beneficiarios
GROUP BY SUBSTR(data_cadastro, 1, 7)
ORDER BY mes_cadastro;

-- Retenção por carga horária de capacitação
DROP VIEW IF EXISTS vw_retencao_por_carga_horaria;
CREATE VIEW vw_retencao_por_carga_horaria AS
SELECT
    horas_capacitacao,
    COUNT(*)                                                      AS total_beneficiarios,
    ROUND(AVG(status_retencao_6m) * 100, 2)                       AS taxa_retencao_pct
FROM fato_beneficiarios
GROUP BY horas_capacitacao
ORDER BY horas_capacitacao;
