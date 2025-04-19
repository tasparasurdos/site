# Gerador de Site Estático de Tecnologias Assistivas

Este projeto gera um site estático completo a partir de dados de duas planilhas do Google Sheets (Tecnologias e Recursos). Usando Python, Jinja2, Bootstrap5 e jQuery, ele exporta páginas HTML prontas para serem hospedadas em serviços como GitHub Pages.

Você pode customizar o site final alterando so arquivos do diretório `templates`. A obtenção/tratamento do conteúdo e criação das páginas `.html` é feito a partir do script `main.py`.

---
## Requisitos

- Python 3.7+
- Bibliotecas Python:
  - `pandas`
  - `jinja2`
- Acesso à internet (para baixar os CSVs do Google Sheets)
- Node.js/NPM (opcional, para postar/processar assets)

---
## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```
2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install pandas jinja2
   ```

---
## Uso

Basta executar o script principal para gerar o site:

```bash
python main.py
```

Isso irá:
- Apagar e recriar a pasta `docs/`.
- Baixar e processar as planilhas de Tecnologias e Recursos.
- Copiar assets, imagens e páginas estáticas.
- Renderizar todos os templates em HTML.

O site completo ficará disponível em `docs/`, pronto para deploy.

---
## Configuração de Templates

Os templates usam Jinja2 e possuem placeholders fáceis de identificar:

- **Variáveis**:
  - `tecnologias` (lista de dicionários)
  - `recursos_aleatorios`, `recursos` (lista de dicionários)
  - `drop_categories`, `drop_etapas`, `drop_custos`, `drop_plataformas`, `drop_internet` (listas para dropdowns)
- **Estruturas**:
  - Loops `{% for item in list %}`
  - Condicionais `{% if ... %}`

Personalize o layout ou classes CSS sem alterar a lógica de renderização.

---
## Filtros Interativos

- **Texto**: filtra títulos e descrições.
- **Dropdowns**: Categoria, Etapa de Ensino, Custo, Plataforma e Requer Internet. Podem ser combinados.
- **Limpar Filtros**: botão visível quando um filtro é aplicado.

A lógica está em `assets/scripts.js` usando jQuery e data-attributes.

---
## Deploy

1. Faça deploy da pasta `docs/` em GitHub Pages ou outro host estático.
2. Certifique-se de que o base path (`/`) esteja correto para `assets/` e `imagens/`.

---
## Sobre

Este projeto foi elaborado como resultado de mestrado em computação da UFMS.
