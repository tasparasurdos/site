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
    print(f"  → {len(records)} registros carregados e ordenados.")
    return records

# Carrega dados
tecnologias = load_records(URL_TECNOLOGIAS)
recursos = load_records(URL_RECURSOS)

# Gera listas únicas para dropdowns
cats = sorted({tech['categoria'] for tech in tecnologias})
etaps = sorted({et.strip() for tech in tecnologias for et in tech.get('etapas','').split(';') if et.strip()})
custos = sorted({tech['custo'] for tech in tecnologias})
plats = sorted({p.strip() for tech in tecnologias for p in re.split(r'[;,]', tech.get('plataformas','')) if p.strip()})
internets = sorted({tech['requer_internet'] for tech in tecnologias})

# Agrupa tecnologias por categoria
categorias = {}
for tech in tecnologias:
    categorias.setdefault(tech['categoria'], []).append(tech)
# Ordena cada grupo
for items in categorias.values():
    items.sort(key=lambda x: x['titulo'].lower())

# Prepara Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# Copiar assets e estáticos
def prepare_output():
    print("Copiando assets e páginas estáticas...")
    shutil.copytree('assets', os.path.join(docs_dir, 'assets'))
    shutil.copytree('imagens', os.path.join(docs_dir, 'imagens'))
    for page in ('sobre.html','contato.html','equipe.html'):
        print(f"Copiando página: {page}")
        shutil.copy(os.path.join('templates', page), docs_dir)

prepare_output()

# Função para renderizar templates
def render(name, tpl, ctx):
    out_path = os.path.join(docs_dir, name)
    print(f"Gerando: {out_path}")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(env.get_template(tpl).render(ctx))

# 1) index.html
render('index.html', 'index.html', {
    'tecnologias': tecnologias,
    'recursos_aleatorios': random.sample(recursos, min(12, len(recursos))),
    'drop_categories': cats,
    'drop_etapas': etaps,
    'drop_custos': custos,
    'drop_plataformas': plats,
    'drop_internet': internets
})

# 2) páginas de tecnologia
os.makedirs(os.path.join(docs_dir, 'tecnologias'), exist_ok=True)
for tech in tecnologias:
    rels = [t for t in categorias[tech['categoria']] if t['slug'] != tech['slug']]
    related = random.sample(rels, min(3, len(rels))) if rels else []
    render(f"tecnologias/{tech['slug']}.html", 'tecnologia.html', {
        'tecnologia': tech,
        'relacionados': related
    })

# 3) categorias
for cat, items in categorias.items():
    render(f"categoria_{cat.replace(' ', '_')}.html", 'categoria.html', {
        'categoria': cat,
        'descricao': items[0].get('categoria_descricao', ''),
        'tecnologias': items
    })

# 4) recursos.html
render('recursos.html', 'recursos.html', {'recursos': recursos})

# 5) mapa.html
mapa = {
    'index': 'index.html',
    'sobre': 'sobre.html',
    'contato': 'contato.html',
    'equipe': 'equipe.html',
    'recursos': 'recursos.html',
    'categorias': [f"categoria_{c.replace(' ', '_')}.html" for c in cats],
    'tecnologias': [f"tecnologias/{t['slug']}.html" for t in tecnologias]
}
render('mapa.html', 'mapa.html', {'mapa': mapa})
