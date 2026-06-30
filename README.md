# Vestra Capital — Esteira de Estratégias (dashboard)

Dashboard consolidado da esteira de estratégias multiestratégica / multi-ativo
da Vestra Capital. App em Streamlit que renderiza o relatório HTML auto-contido.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar (link compartilhável)

1. Suba este diretório para um repositório no GitHub.
2. Vá em https://share.streamlit.io → **New app** → escolha o repo, branch `main`, arquivo `app.py`.
3. (Opcional) Para proteger com senha: em **Advanced settings → Secrets**, adicione:
   ```toml
   APP_PASSWORD = "suaSenhaForte"
   ```
4. Deploy → você recebe um link `https://<app>.streamlit.app` para enviar aos gestores.

## Atualizar os números

O `dashboard.html` é gerado pela esteira (`python -m esteira run`). Para atualizar
o dashboard publicado, substitua o `dashboard.html` desta pasta e faça `git push` —
o Streamlit Cloud re-deploya automaticamente.

> Documento interno de pesquisa. Não constitui recomendação de investimento.
> Resultados de backtest não garantem retornos futuros.
