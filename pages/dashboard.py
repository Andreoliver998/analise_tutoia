import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Dashboard Tutóia/MA", layout="wide")

# =========================================
# 📂 CARREGAR ARQUIVO
# =========================================
BASE_DIR = Path(__file__).resolve().parents[1]
data_path = BASE_DIR / "datasets" / "despesas_2025.csv"

if not data_path.exists():
    st.error(f"❌ Arquivo não encontrado: {data_path}")
    st.stop()

df = pd.read_csv(data_path, encoding="latin1", sep=";")

# =========================================
# 🧹 TRATAR DADOS
# =========================================
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Ano"] = df["Data"].dt.year
df["Mes"] = df["Data"].dt.month_name()

for col in ["Valor Empenhado", "Valor Liquidado", "Valor Pago"]:
    df[col] = df[col].astype(str).str.replace('.', '').str.replace(',', '.')
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================================
# 🎚️ FILTROS
# =========================================
st.sidebar.title("⚙️ Filtros")
anos = sorted(df["Ano"].dropna().unique())
ano = st.sidebar.selectbox("Selecione o ano", anos)

fornecedores = sorted(df["Nome Fornecedor"].dropna().unique())
forn = st.sidebar.multiselect("Fornecedor(es)", fornecedores)

df_filt = df[df["Ano"] == ano]
if forn:
    df_filt = df_filt[df_filt["Nome Fornecedor"].isin(forn)]

# =========================================
# 📈 MÉTRICAS
# =========================================
st.title("📊 Painel Financeiro — Tutóia/MA")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Empenhado", f"R$ {df_filt['Valor Empenhado'].sum():,.2f}")
col2.metric("📦 Liquidado", f"R$ {df_filt['Valor Liquidado'].sum():,.2f}")
col3.metric("✅ Pago", f"R$ {df_filt['Valor Pago'].sum():,.2f}")
col4.metric("⚠️ A Pagar", f"R$ {(df_filt['Valor Empenhado'].sum() - df_filt['Valor Pago'].sum()):,.2f}")

st.divider()

# =========================================
# 🏆 TOP FORNECEDORES
# =========================================
st.subheader("🏅 Top 10 Fornecedores (por valor pago)")

top = (
    df_filt.groupby("Nome Fornecedor")["Valor Pago"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    top,
    title="Top 10 Fornecedores",
    orientation="h",
    labels={"value": "Valor Pago", "index": "Fornecedor"},
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# 📄 TABELA + DOWNLOAD
# =========================================
st.subheader("📄 Tabela detalhada")
st.dataframe(df_filt)

st.download_button(
    "⬇️ Baixar dados filtrados",
    df_filt.to_csv(index=False).encode("utf-8"),
    "dados_filtrados.csv",
    mime="text/csv"
)
