import sqlite3
import random
from datetime import datetime, timedelta
 
random.seed(42)
 
conn = sqlite3.connect('../esg_impact.db')
cursor = conn.cursor()
 
cursor.execute('DROP TABLE IF EXISTS fato_beneficiarios')
cursor.execute('DROP TABLE IF EXISTS dim_projetos')
 
cursor.execute('''
CREATE TABLE dim_projetos (
    projeto_id INTEGER PRIMARY KEY,       -- ID único do projeto (1, 2, 3...)
    nome_projeto TEXT,                    -- Nome legível do projeto
    eixo_esg TEXT,                        -- Categoria ESG do projeto
    orcamento_anual REAL,                 -- Orçamento em formato decimal/float
    cidade TEXT,                          -- Localidade do hub
    gerente_responsavel TEXT              -- Nome da pessoa gestora
)
''')
 
cursor.execute('''
CREATE TABLE fato_beneficiarios (
    beneficiario_id INTEGER PRIMARY KEY,  -- ID único do beneficiário (1 a 1000)
    projeto_id INTEGER,                   -- Chave estrangeira ligando ao projeto
    data_cadastro TEXT,                   -- Data em que entrou no programa (YYYY-MM-DD)
    status_retencao_6m INTEGER,           -- Indicador binário: 1 = reteve, 0 = evadiu
    renda_inicial_brl REAL,               -- Renda no momento zero (R$)
    renda_pos_6m_brl REAL,                -- Renda após 6 meses (R$)
    horas_capacitacao INTEGER,            -- Carga horária acumulada
    FOREIGN KEY (projeto_id) REFERENCES dim_projetos(projeto_id)
)
''')
 
eixos = ['Educação & Tech', 'Gestão de Resíduos & Circularidade', 'Agricultura Urbana', 'Inclusão Financeira']
cidades = ['Campinas, SP', 'São Paulo, SP', 'Hortolândia, SP', 'Sumaré, SP']
gerentes = ['Ana Souza', 'Carlos Lima', 'Mariana Costa', 'Rafael Mendes']
 
projetos_data = []
for i in range(1, 11):
    projetos_data.append((
        i,
        f'Hub de Impacto {i:02d}',
        random.choice(eixos),
        round(random.uniform(40000, 140000), 2),
        random.choice(cidades),
        random.choice(gerentes)
    ))
 
cursor.executemany('INSERT INTO dim_projetos VALUES (?, ?, ?, ?, ?, ?)', projetos_data)
 
data_inicio_base = datetime(2025, 1, 1)
beneficiarios_data = []
 
for b_id in range(1, 1001):
    p_id = random.randint(1, 10)
    d_cadastro = (data_inicio_base + timedelta(days=random.randint(0, 350))).strftime('%Y-%m-%d')
    horas = random.choice([15, 30, 45, 60, 90])
    retencao = 1 if (horas >= 45 and random.random() < 0.75) or (random.random() < 0.35) else 0
    renda_ini = round(random.uniform(1100, 2200), 2)
    delta_renda = round(renda_ini * random.uniform(0.12, 0.40) * retencao, 2)
    renda_pos = renda_ini + delta_renda
 
    beneficiarios_data.append((
        b_id, p_id, d_cadastro, retencao, renda_ini, renda_pos, horas
    ))
 
cursor.executemany('INSERT INTO fato_beneficiarios VALUES (?, ?, ?, ?, ?, ?, ?)', beneficiarios_data)
 
conn.commit()
conn.close()
 
print("Banco 'esg_impact.db' populado com sucesso!")