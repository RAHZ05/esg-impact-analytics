import sqlite3
import pandas as pd
import os
 
db_path = '../esg_impact.db'
os.makedirs('../data', exist_ok=True)
 
conn = sqlite3.connect(db_path)
 
print("=== VALIDAÇÃO DE MÉTRICAS (SQL) ===")
query_validacao = '''
SELECT
    p.eixo_esg,
    COUNT(b.beneficiario_id) as total_beneficiarios,
    ROUND(AVG(b.status_retencao_6m) * 100, 2) as taxa_retencao_pct,
    ROUND(AVG(b.renda_pos_6m_brl - b.renda_inicial_brl), 2) as delta_medio_renda_brl
FROM fato_beneficiarios b
JOIN dim_projetos p ON b.projeto_id = p.projeto_id
GROUP BY p.eixo_esg
ORDER BY taxa_retencao_pct DESC;
'''
df_val = pd.read_sql_query(query_validacao, conn)
print(df_val.to_string(index=False))
 
print("\n" + "="*40 + "\n")
 
df_dim = pd.read_sql_query('SELECT * FROM dim_projetos', conn)
df_fato = pd.read_sql_query('SELECT * FROM fato_beneficiarios', conn)
 
df_dim.to_csv('../data/dim_projetos.csv', index=False)
df_fato.to_csv('../data/fato_beneficiarios.csv', index=False)
 
conn.close()
print("CSVs exportados com sucesso para '../data/'!")
 