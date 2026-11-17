"""Tela de chat em Streamlit para o agente. Rode com: uv run streamlit run app.py"""
import asyncio
import os
from pathlib import Path
import uuid

import streamlit as st
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService

from agente.conversa import perguntar

load_dotenv()
RAIZ = Path(__file__).resolve().parent
st.set_page_config(page_title="Assistente do Analista de IA", page_icon="🤖")
st.title("Assistente do Analista de IA")
st.caption("Google ADK · Groq · ferramentas próprias · MCP local e público · guardrails · memória SQLite")

if not os.getenv("GROQ_API_KEY"):
    st.error("Falta a chave da Groq. Copie .env.example para .env e preencha GROQ_API_KEY (veja o README).")
    st.stop()

# Estado da conversa: o histórico do agente fica no serviço de sessões; o da tela, em `mensagens`.
if "sessoes" not in st.session_state:
    st.session_state.sessoes = DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{(RAIZ / 'conversas.db').as_posix()}")
    arquivo_sessao = RAIZ / ".sessao_atual"
    if arquivo_sessao.exists():
        st.session_state.sessao_id = arquivo_sessao.read_text(encoding="utf-8").strip()
    else:
        st.session_state.sessao_id = str(uuid.uuid4())
        arquivo_sessao.write_text(st.session_state.sessao_id, encoding="utf-8")
    st.session_state.mensagens = []

with st.sidebar:
    st.subheader("Experimente")
    st.markdown(
        "- O que é RAG?\n"
        "- Faça perguntas de entrevista sobre RAG\n"
        "- Converta US$ 25 para reais com cotação de 5,20\n"
        "- Monte um roteiro de estudos de 14 dias para eu virar Analista de IA\n"
        "- Quanto custa 2.000 tokens de entrada e 500 de saída, a 0,59 e 0,79 dólares por milhão, 3.000 vezes por dia?\n"
        "- No repositório google/adk-python, o que é um callback?\n"
        "- Minha chave é gsk_abc123def456ghi789 (o guardrail barra)\n"
    )
    if st.button("Nova conversa"):
        st.session_state.sessao_id = str(uuid.uuid4())
        (RAIZ / ".sessao_atual").write_text(st.session_state.sessao_id, encoding="utf-8")
        st.session_state.mensagens = []
        st.rerun()

for m in st.session_state.mensagens:
    with st.chat_message(m["papel"]):
        st.markdown(m["texto"])
        if m.get("passos"):
            with st.expander(f"Passos do agente ({len(m['passos'])})"):
                st.json(m["passos"])

if texto := st.chat_input("Pergunte algo"):
    st.session_state.mensagens.append({"papel": "user", "texto": texto})
    with st.chat_message("user"):
        st.markdown(texto)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                r = asyncio.run(perguntar(st.session_state.sessoes, "aluno", st.session_state.sessao_id, texto))
            except Exception as erro:  # mostra o erro em vez de derrubar a tela
                if "RateLimit" in type(erro).__name__ or "rate limit" in str(erro).lower():
                    aviso = "Atingi o limite por minuto do plano gratuito da Groq. Espere cerca de um minuto e tente de novo."
                else:
                    aviso = f"Não consegui responder agora: {str(erro)[:300]}"
                r = {"resposta": aviso, "passos": []}
        st.markdown(r["resposta"] or "(sem resposta)")
        if r["passos"]:
            with st.expander(f"Passos do agente ({len(r['passos'])})"):
                st.json(r["passos"])
    st.session_state.mensagens.append({"papel": "assistant", "texto": r["resposta"], "passos": r["passos"]})
