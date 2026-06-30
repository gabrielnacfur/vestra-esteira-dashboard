"""App Streamlit — Vestra Capital · Esteira de Estratégias.

Renderiza o dashboard HTML auto-contido (gerado pela esteira) num link
compartilhável. Os dados sensíveis NÃO vão para o repositório: apenas o
dashboard.html já consolidado (com gráficos e tabelas embutidos).

Deploy: https://share.streamlit.io -> aponte para este repo / app.py
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vestra Capital · Esteira de Estratégias",
    page_icon="📈",
    layout="wide",
)

HERE = Path(__file__).parent
DASHBOARD = HERE / "dashboard.html"

# Senha simples opcional (defina APP_PASSWORD nos Secrets do Streamlit p/ ativar)
def _check_password() -> bool:
    pwd_expected = st.secrets.get("APP_PASSWORD", None) if hasattr(st, "secrets") else None
    if not pwd_expected:
        return True  # sem senha configurada -> acesso livre
    if st.session_state.get("auth_ok"):
        return True
    st.markdown("### 🔒 Vestra Capital — acesso restrito")
    pwd = st.text_input("Senha", type="password")
    if pwd:
        if pwd == pwd_expected:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Senha incorreta.")
    return False


def main():
    if not _check_password():
        return
    if not DASHBOARD.exists():
        st.error("dashboard.html não encontrado no repositório. "
                 "Gere com `python -m esteira run` e copie reports/dashboard.html para esta pasta.")
        return
    html = DASHBOARD.read_text(encoding="utf-8")
    components.html(html, height=2600, scrolling=True)


if __name__ == "__main__":
    main()
