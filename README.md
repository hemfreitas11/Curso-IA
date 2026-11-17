# Estudos do curso de IA

Os projetos e materiais estão organizados assim:

- [`agente-adk-streamlit/`](agente-adk-streamlit/README.md): assistente de estudos com Google ADK, Streamlit, Groq e MCP, citado na aula 5.4.
- [`projeto-final/`](projeto-final/README.md): assistente da loja, projeto final da aula 6.3.
- [`README-PROVAS.md`](README-PROVAS.md): instruções das provas de revisão.
- [`README-conteudo-curso.md`](README-conteudo-curso.md): mapa dos conteúdos das aulas.

## Abrir o chat do agente

No terminal, a partir desta pasta:

```powershell
cd agente-adk-streamlit
uv sync
Copy-Item .env.example .env
# Preencha GROQ_API_KEY no .env (somente na primeira configuração).
uv run streamlit run app.py
```

Se o `.env` já existir, não o sobrescreva. Veja os detalhes no README do agente.
