import streamlit as st
from pathlib import Path
import base64

# ========= CONFIG =========
st.set_page_config(
    page_title="CRM de Vendas",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========= CSS PAINEL =========
def css_app():
    st.markdown("""
    <style>

    /* Remove ícone "keyboard_double_arrow_right" da barra lateral oculta */
    button[kind="header"] {display: none !important;}

    body { background-color:#0e1117 !important; }

    .center-box {
        background: linear-gradient(90deg, #12151e, #161b22, #12151e);
        padding: 25px; border-radius: 12px;
        border: 1px solid #2d323b;
        text-align: center; margin-bottom: 40px;
    }

    .title { font-size: 28px; font-weight: 800; color: #ffffff; }
    .subtitle { font-size: 14px; color: #a6a6a6; margin-top: -4px; }
    .logo-section { text-align:center; margin-top: 40px; margin-bottom: 10px; }
    .logo-text { font-size: 22px; font-weight: 700; color: white; margin-top: 10px; }
    .slogan { font-size: 14px; color: #9fa4ad; margin-top: -5px; }
    </style>
    """, unsafe_allow_html=True)

# ========= LOGO PAINEL =========
def exibir_logo_painel():

    logo_path = Path(__file__).resolve().parent / "img" / "logo_dashboard.png"

    if logo_path.exists():
        with open(logo_path, "rb") as img:
            base = base64.b64encode(img.read()).decode()

        st.markdown(
            f"""
            <div class='logo-section'>
                <img src="data:image/png;base64,{base}" width="280px">
                <div class='logo-text'>Tutóia</div>
                <div class='slogan'>Bem-vindo ao seu painel de gestão</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Logo não encontrada! Coloque o arquivo em: /app/assets/logo_dashboard.png")

# ========= INICIAR SISTEMA DIRETO (sem login) =========
st.session_state.logged = True
css_app()

# ========= HEADER =========
st.markdown("""
<div class='center-box'>
    <div class='title'>📊 Portal da Transparência - Tutóia/MA</div>
    <div class='subtitle'>Acompanhe os gastos públicos da nossa cidade, com dados oficiais.</div>
</div>
""", unsafe_allow_html=True)

# Logo do painel
exibir_logo_painel()

# ✅ Aqui começam as páginas e o dashboard
# Exemplo de mensagem inicial
#st.write("✅ Sistema carregado com sucesso!")
#st.write("🧠 Painel pronto para receber seus gráficos, tabelas e páginas.")
