# 📊 Análise de Dados Abertos do Governo Brasileiro
 
> Análise exploratória e estatística dos gastos públicos federais com base nos dados abertos do Portal da Transparência do Governo Federal.
 
---
 
## 🎯 Objetivo
 
Explorar e visualizar os padrões de gastos públicos federais brasileiros, identificando tendências por órgão, categoria e período — aplicando técnicas de análise estatística e visualização de dados com Python.
 
---
 
## 📁 Estrutura do Projeto
 
```
analise-dados-gov/
│
├── data/                    # Datasets (CSV baixados do Portal da Transparência)
│   └── README.md            # Instruções para download dos dados reais
│
├── src/
│   └── analise.py           # Script principal de análise
│
├── notebooks/               # Análises exploratórias em Jupyter Notebook
│
├── outputs/                 # Gráficos e visualizações gerados
│   ├── 01_gastos_por_orgao.png
│   ├── 02_evolucao_anual.png
│   ├── 03_categorias.png
│   ├── 04_heatmap_mensal.png
│   └── 05_regressao_linear.png
│
├── requirements.txt
└── README.md
```
 
---
 
## 📈 Análises Realizadas
 
### 1. Gastos Totais por Órgão Federal
Comparativo do volume total de gastos entre os principais ministérios no período de 2020 a 2024.
 
### 2. Evolução Anual — Top 4 Órgãos
Série temporal dos 4 ministérios com maior volume de gastos, evidenciando tendências de crescimento ou redução ao longo dos anos.
 
### 3. Distribuição por Categoria de Gasto
Análise da composição dos gastos federais em categorias como Pessoal, Custeio, Investimento, Transferências e Benefícios Sociais — via gráfico de pizza e barras.
 
### 4. Heatmap de Sazonalidade Mensal
Mapa de calor cruzando meses do ano com os principais órgãos, revelando padrões sazonais nos gastos públicos.
 
### 5. Regressão Linear — Tendência Temporal
Análise estatística da tendência dos gastos federais ao longo do tempo, com cálculo de R², p-value e coeficiente angular.
 
---
 
## 🛠️ Tecnologias Utilizadas
 
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4c72b0?style=for-the-badge&logo=python&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
 
---
 
## 🚀 Como Executar
 
**Pré-requisitos:** Python 3.10+ instalado
 
```bash
# 1. Clone o repositório
git clone https://github.com/Laysa-eSerrao/analise-dados-gov.git
cd analise-dados-gov
 
# 2. Instale as dependências
pip install -r requirements.txt
 
# 3. Execute a análise
python src/analise.py
```
 
Os gráficos serão gerados automaticamente na pasta `outputs/`.
 
---
 
## 🗃️ Fonte dos Dados
 
Os dados utilizados seguem a estrutura do **Portal da Transparência do Governo Federal**:
 
🔗 [portaldatransparencia.gov.br/download-de-dados](https://portaldatransparencia.gov.br/download-de-dados)
 
O script atual utiliza dados simulados com a mesma estrutura do portal para fins demonstrativos. Para rodar com dados reais, baixe o CSV correspondente e substitua a chamada `gerar_dataset()` por `pd.read_csv("data/seu_arquivo.csv")`.
 
---
 
## 📊 Visualizações
 
| Gráfico | Descrição |
|---|---|
| `01_gastos_por_orgao.png` | Barras horizontais — total por ministério |
| `02_evolucao_anual.png` | Série temporal — top 4 órgãos |
| `03_categorias.png` | Pizza + barras — distribuição por categoria |
| `04_heatmap_mensal.png` | Heatmap — sazonalidade mensal |
| `05_regressao_linear.png` | Regressão linear — tendência temporal |
 
---
 
## 👩‍💻 Autora
 
**Laysa Serrão**
 
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/laysa-serrão-384214384/)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Laysa-eSerrao)
 
