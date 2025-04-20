import os
import shutil
import random
import re
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Diretório de saída
docs_dir = 'docs'

# Limpeza inicial: remove e recria 'docs/'
if os.path.exists(docs_dir):
    print(f"Removendo diretório existente: {docs_dir}")
    shutil.rmtree(docs_dir)
print(f"Criando diretório de saída: {docs_dir}")
os.makedirs(docs_dir)

# URLs das planilhas Google Sheets (export CSV)
URL_TECNOLOGIAS = (
    'https://docs.google.com/spreadsheets/d/'
    '1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc'
    '/export?format=csv'
)
URL_RECURSOS = (
    'https://docs.google.com/spreadsheets/d/'
    '1lePYinFlYePVYPwwUqy1Xa1r1FF_l3vaAkRxntSvWq4'
    '/export?format=csv&gid=1735795033'
)

# Função para carregar e ordenar registros por título
def load_records(url):
    print(f"Carregando dados de: {url}")
    df = pd.read_csv(url)
    records = df.to_dict(orient='records')
    records.sort(key=lambda x: x.get('titulo', '').lower())
    print(f"  → {len(records)} registros carregados.")
    return records

# Carrega dados das planilhas
tecnologias = load_records(URL_TECNOLOGIAS)
recursos = load_records(URL_RECURSOS)

# Gera opções únicas para dropdowns
drop_categories = sorted({tech['categoria'] for tech in tecnologias})
drop_etapas = sorted({et.strip() for tech in tecnologias for et in tech.get('etapas','').split(';') if et.strip()})
drop_custos = sorted({tech['custo'] for tech in tecnologias})
drop_plataformas = sorted({p.strip() for tech in tecnologias for p in re.split(r'[;,]', tech.get('plataformas','')) if p.strip()})
drop_internet = sorted({tech['requer_internet'] for tech in tecnologias})

# Agrupa tecnologias por categoria
categorias = {}
for tech in tecnologias:
    categorias.setdefault(tech['categoria'], []).append(tech)
# Ordena cada lista de categoria
for lista in categorias.values():
    lista.sort(key=lambda x: x['titulo'].lower())

# Configura ambiente Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# Copiar assets e páginas estáticas
def prepare_output():
    print("Copiando assets e páginas estáticas...")
    shutil.copytree('assets', os.path.join(docs_dir, 'assets'))
    shutil.copytree('imagens', os.path.join(docs_dir, 'imagens'))
    for page in ('sobre.html', 'contato.html', 'equipe.html'):
        print(f"Copiando página: {page}")
        shutil.copy(os.path.join('templates', page), docs_dir)

prepare_output()

# Função de renderização
def render(path, template, context):
    out_file = os.path.join(docs_dir, path)
    print(f"Gerando: {out_file}")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(env.get_template(template).render(context))

# 1) Página inicial
render(
    'index.html',
    'index.html',
    {
        'tecnologias': tecnologias,
        'recursos_aleatorios': random.sample(recursos, min(12, len(recursos))),
        'drop_categories': drop_categories,
        'drop_etapas': drop_etapas,
        'drop_custos': drop_custos,
        'drop_plataformas': drop_plataformas,
        'drop_internet': drop_internet
    }
)

# 2) Páginas de tecnologia (inclui lista completa da categoria)
os.makedirs(os.path.join(docs_dir, 'tecnologias'), exist_ok=True)
for tech in tecnologias:
    categoria_nome = tech['categoria']
    render(
        f"tecnologias/{tech['slug']}.html",
        'tecnologia.html',
        {
            'tecnologia': tech,
            'categoria': categoria_nome,
            'categoria_descricao': tech.get('categoria_descricao', ''),
            'categoria_tecnologias': categorias[categoria_nome]
        }
    )

# 3) Página de recursos
render('recursos.html', 'recursos.html', {'recursos': recursos})

# 4) Mapa do site
mapa = {
    'index': 'index.html',
    'sobre': 'sobre.html',
    'contato': 'contato.html',
    'equipe': 'equipe.html',
    'recursos': 'recursos.html',
    'tecnologias': [f"tecnologias/{t['slug']}.html" for t in tecnologias]
}
render('mapa.html', 'mapa.html', {'mapa': mapa})