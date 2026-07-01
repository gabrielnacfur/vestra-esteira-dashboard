"""App Streamlit — Vestra Capital · Esteira de Estratégias.

Renderiza os dashboards HTML auto-contidos (gerados pela esteira) num link
compartilhável, com SELETOR de estudo (ex.: Combinado vs S&P 500).

Os dados sensíveis NÃO vão para o repositório: apenas os dashboards já
consolidados (dashboard_<slug>.html) e o manifesto studies.json.

Deploy: https://share.streamlit.io -> aponte para este repo / app.py
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vestra Capital · Esteira de Estratégias",
    page_icon="📈",
    layout="wide",
)

HERE = Path(__file__).parent


def _check_password() -> bool:
    pwd_expected = st.secrets.get("APP_PASSWORD", None) if hasattr(st, "secrets") else None
    if not pwd_expected:
        return True
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


def _discover_studies() -> dict[str, Path]:
    """Mapeia nome amigável -> caminho do dashboard. Usa studies.json se existir."""
    names = {}
    manifest = HERE / "studies.json"
    slug_to_name = {}
    if manifest.exists():
        try:
            slug_to_name = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception:
            slug_to_name = {}
    studies: dict[str, Path] = {}
    for f in sorted(HERE.glob("dashboard_*.html")):
        slug = f.stem.replace("dashboard_", "")
        label = slug_to_name.get(slug, slug.upper())
        studies[label] = f
    # compat: dashboard.html avulso
    legacy = HERE / "dashboard.html"
    if legacy.exists() and not studies:
        studies["Dashboard"] = legacy
    return studies


def main():
    if not _check_password():
        return
    studies = _discover_studies()
    if not studies:
        st.error("Nenhum dashboard encontrado no repositório. "
                 "Gere com `python -m esteira run` e copie os dashboard_<slug>.html para esta pasta.")
        return

    if len(studies) > 1:
        st.sidebar.markdown("### 📊 Estudo")
        choice = st.sidebar.radio("Selecione o estudo:", list(studies.keys()))
    else:
        choice = next(iter(studies))

    html = studies[choice].read_text(encoding="utf-8")
    components.html(html, height=2600, scrolling=True)


if __name__ == "__main__":
    main()
