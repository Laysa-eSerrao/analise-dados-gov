"""
Análise de Dados Abertos do Governo Brasileiro
Dataset: Gastos públicos federais (Portal da Transparência)
Autora: Laysa Serrão
"""
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
import os
 
warnings.filterwarnings("ignore")
 
# Configurações visuais 
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#161b22",
    "axes.edgecolor":   "#30363d",
    "axes.labelcolor":  "#e6edf3",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#e6edf3",
    "grid.color":       "#21262d",
    "grid.linestyle":   "--",
    "grid.alpha":       0.5,
    "font.family":      "DejaVu Sans",
    "figure.dpi":       150,
})
 
AZUL      = "#1A51F4"
AZUL_CLARO= "#6ccfff"
DESTAQUE  = "#f78166"
VERDE     = "#3fb950"
AMARELO   = "#d29922"
 
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
# 1. Geração de dataset simulado (estrutura real do Portal da Transparência) 
def gerar_dataset(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """
    Simula a estrutura do dataset de gastos federais do Portal da Transparência.
    Em um projeto real, substitua pela leitura do CSV baixado em:
    https://portaldatransparencia.gov.br/download-de-dados
    """
    rng = np.random.default_rng(seed)
 
    orgaos = {
        "Ministério da Educação":       0.22,
        "Ministério da Saúde":          0.20,
        "Ministério da Defesa":         0.15,
        "Ministério da Infraestrutura": 0.12,
        "Ministério da Ciência e TI":   0.10,
        "Ministério do Trabalho":       0.09,
        "Ministério da Fazenda":        0.07,
        "Outros":                       0.05,
    }
 
    categorias = ["Pessoal", "Custeio", "Investimento",
                  "Transferências", "Benefícios Sociais"]
 
    anos  = [2020, 2021, 2022, 2023, 2024]
    meses = list(range(1, 13))
 
    orgao_list = rng.choice(list(orgaos.keys()), size=n,
                            p=list(orgaos.values()))
    cat_list   = rng.choice(categorias, size=n)
    ano_list   = rng.choice(anos, size=n)
    mes_list   = rng.choice(meses, size=n)
 
    base_values = {
        "Ministério da Educação":       8e8,
        "Ministério da Saúde":          9e8,
        "Ministério da Defesa":         6e8,
        "Ministério da Infraestrutura": 5e8,
        "Ministério da Ciência e TI":   3e8,
        "Ministério do Trabalho":       4e8,
        "Ministério da Fazenda":        2e8,
        "Outros":                       1e8,
    }
 
    valores = np.array([
        rng.lognormal(mean=np.log(base_values[o]), sigma=0.4)
        for o in orgao_list
    ])
 
    df = pd.DataFrame({
        "orgao":      orgao_list,
        "categoria":  cat_list,
        "ano":        ano_list,
        "mes":        mes_list,
        "valor_r":    valores,
    })
 
    df["data"] = pd.to_datetime(
        df["ano"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2) + "-01"
    )
    df["valor_bi"] = df["valor_r"] / 1e9
 
    return df
 
 
# 2. Limpeza e estatísticas descritivas
def limpeza_e_descritiva(df: pd.DataFrame) -> pd.DataFrame:
    print("\n📋 INFORMAÇÕES DO DATASET")
    print(f"  Registros : {len(df):,}")
    print(f"  Período   : {df['ano'].min()} – {df['ano'].max()}")
    print(f"  Órgãos    : {df['orgao'].nunique()}")
    print(f"  Nulos     : {df.isnull().sum().sum()}")
 
    print("\n📊 ESTATÍSTICAS DESCRITIVAS (Valor em R$ Bilhões)")
    desc = df.groupby("orgao")["valor_bi"].agg(["mean", "median", "std", "sum"])
    desc.columns = ["Média", "Mediana", "Desvio Padrão", "Total"]
    desc = desc.sort_values("Total", ascending=False)
    print(desc.round(2).to_string())
 
    return df
 
 
# 3. Visualizações 
def plot_gastos_por_orgao(df: pd.DataFrame):
    totais = (df.groupby("orgao")["valor_bi"]
                .sum()
                .sort_values(ascending=True))
 
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(totais.index, totais.values,
                   color=[AZUL if i < len(totais) - 1 else DESTAQUE
                          for i in range(len(totais))],
                   edgecolor="none", height=0.6)
 
    for bar, val in zip(bars, totais.values):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                f"R$ {val:.1f}B", va="center", fontsize=9, color="#e6edf3")
 
    ax.set_xlabel("Total (R$ Bilhões)", labelpad=10)
    ax.set_title("Gastos Totais por Órgão Federal (2020–2024)",
                 fontsize=13, fontweight="bold", pad=15, color="#e6edf3")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"R$ {x:.0f}B"))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/01_gastos_por_orgao.png")
    plt.close()
    print("  ✅ 01_gastos_por_orgao.png")
 
 
def plot_evolucao_anual(df: pd.DataFrame):
    top4 = (df.groupby("orgao")["valor_bi"]
              .sum()
              .nlargest(4)
              .index.tolist())
 
    anual = (df[df["orgao"].isin(top4)]
             .groupby(["ano", "orgao"])["valor_bi"]
             .sum()
             .reset_index())
 
    cores = [AZUL, AZUL_CLARO, DESTAQUE, VERDE]
 
    fig, ax = plt.subplots(figsize=(10, 5))
    for orgao, cor in zip(top4, cores):
        subset = anual[anual["orgao"] == orgao]
        ax.plot(subset["ano"], subset["valor_bi"],
                marker="o", linewidth=2.5, color=cor,
                label=orgao.replace("Ministério d", "Min. d"))
        ax.fill_between(subset["ano"], subset["valor_bi"],
                        alpha=0.08, color=cor)
 
    ax.set_title("Evolução Anual dos Gastos — Top 4 Órgãos",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Total (R$ Bilhões)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"R$ {x:.0f}B"))
    ax.legend(fontsize=8, framealpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/02_evolucao_anual.png")
    plt.close()
    print("  ✅ 02_evolucao_anual.png")
 
 
def plot_distribuicao_categoria(df: pd.DataFrame):
    cat_totais = (df.groupby("categoria")["valor_bi"]
                    .sum()
                    .sort_values(ascending=False))
 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
 
    # Pizza
    cores_pizza = [AZUL, AZUL_CLARO, VERDE, AMARELO, DESTAQUE]
    wedges, texts, autotexts = ax1.pie(
        cat_totais.values, labels=cat_totais.index,
        autopct="%1.1f%%", colors=cores_pizza,
        startangle=140, pctdistance=0.75,
        wedgeprops={"edgecolor": "#0d1117", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("#0d1117")
    ax1.set_title("Distribuição por Categoria", fontweight="bold")
 
    # Barras
    ax2.bar(cat_totais.index, cat_totais.values,
            color=cores_pizza, edgecolor="none")
    ax2.set_title("Volume por Categoria (R$ Bi)", fontweight="bold")
    ax2.set_ylabel("R$ Bilhões")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:.0f}B"))
    ax2.tick_params(axis="x", rotation=20)
    ax2.spines[["top", "right"]].set_visible(False)
 
    plt.suptitle("Análise por Categoria de Gasto", fontsize=14,
                 fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/03_categorias.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 03_categorias.png")
 
 
def plot_heatmap_mensal(df: pd.DataFrame):
    pivot = (df[df["orgao"].isin(
                    df.groupby("orgao")["valor_bi"].sum().nlargest(5).index)]
               .groupby(["mes", "orgao"])["valor_bi"]
               .mean()
               .unstack("orgao"))
 
    pivot.columns = [c.replace("Ministério d", "Min. d") for c in pivot.columns]
    pivot.index = ["Jan","Fev","Mar","Abr","Mai","Jun",
                   "Jul","Ago","Set","Out","Nov","Dez"]
 
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.heatmap(pivot, ax=ax, cmap="Blues", linewidths=0.4,
                linecolor="#0d1117", annot=True, fmt=".1f",
                cbar_kws={"label": "Média R$ Bilhões"})
    ax.set_title("Média de Gastos por Mês — Top 5 Órgãos",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/04_heatmap_mensal.png")
    plt.close()
    print("  ✅ 04_heatmap_mensal.png")
 
 
def plot_analise_estatistica(df: pd.DataFrame):
    """Teste de correlação e regressão linear entre ano e gastos totais."""
    anual = df.groupby("ano")["valor_bi"].sum().reset_index()
 
    slope, intercept, r, p, se = stats.linregress(
        anual["ano"], anual["valor_bi"])
 
    x_line = np.linspace(anual["ano"].min(), anual["ano"].max(), 100)
    y_line = slope * x_line + intercept
 
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(anual["ano"], anual["valor_bi"],
               color=AZUL_CLARO, s=120, zorder=5, label="Gasto anual")
    ax.plot(x_line, y_line, color=DESTAQUE, linewidth=2,
            label=f"Regressão linear  (R²={r**2:.3f})")
 
    for _, row in anual.iterrows():
        ax.text(row["ano"], row["valor_bi"] + 0.3,
                f"R$ {row['valor_bi']:.1f}B",
                ha="center", fontsize=8, color="#e6edf3")
 
    ax.set_title("Regressão Linear — Tendência dos Gastos Federais",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Total (R$ Bilhões)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"R$ {x:.0f}B"))
    ax.legend(fontsize=9, framealpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
 
    texto = (f"slope = {slope:.2f}  |  intercept = {intercept:.1f}\n"
             f"R² = {r**2:.4f}  |  p-value = {p:.4f}")
    ax.text(0.02, 0.05, texto, transform=ax.transAxes,
            fontsize=8, color="#8b949e",
            bbox={"boxstyle": "round", "facecolor": "#161b22", "alpha": 0.8})
 
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/05_regressao_linear.png")
    plt.close()
    print("  ✅ 05_regressao_linear.png")
 
    print(f"\n📈 REGRESSÃO LINEAR")
    print(f"  Coeficiente angular : {slope:.2f} (crescimento médio anual em R$ Bi)")
    print(f"  R²                  : {r**2:.4f}")
    print(f"  p-value             : {p:.4f} {'✅ significativo' if p < 0.05 else '⚠️ não significativo'}")
 
 
# Main
if __name__ == "__main__":
    print("🔵 Iniciando análise de dados abertos do governo...\n")
 
    df = gerar_dataset()
    df = limpeza_e_descritiva(df)
 
    print("\n🎨 Gerando visualizações...")
    plot_gastos_por_orgao(df)
    plot_evolucao_anual(df)
    plot_distribuicao_categoria(df)
    plot_heatmap_mensal(df)
    plot_analise_estatistica(df)
 
    print(f"\n✅ Análise concluída! Gráficos salvos em /{OUTPUT_DIR}/")
 
