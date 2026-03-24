import streamlit as st
from pyswip import Prolog
import os

# config prolog
prolog = Prolog()

base_dir = os.path.dirname(os.path.dirname(__file__))
caminho = os.path.join(base_dir, "prolog", "sistema.pl")

prolog.consult(caminho)

# interface web

st.title("Sistema de Investigação Forense")
st.write("Sistema especialista em Prolog para análise de suspeitos.")

# lista de suspeitos com nível

if st.button("Analisar suspeitos"):
    resultados = list(prolog.query("pontuacao(X, P), nivel_suspeita(X, N)"))

    if resultados:
        st.success("Resultado da análise:")

        for r in resultados:
            nome = r["X"]
            pontos = r["P"]
            nivel = r["N"]

            if nivel == "alta":
                st.error(f"🚨 {nome} | Pontos: {pontos} | ALTA suspeita")
            elif nivel == "media":
                st.warning(f"⚠️ {nome} | Pontos: {pontos} | MÉDIA suspeita")
            else:
                st.info(f"ℹ️ {nome} | Pontos: {pontos} | BAIXA suspeita")
    else:
        st.warning("Nenhum suspeito encontrado.")

# lista dos culpados

if st.button("Listar culpados"):
    resultados = list(prolog.query("culpado(X)"))

    if resultados:
        st.error("Culpados identificados:")
        for r in resultados:
            st.write(f"- {r['X']}")
    else:
        st.success("Nenhum culpado identificado.")

# explicação

nome = st.text_input("Digite o nome do suspeito:")

if st.button("Explicar suspeito"):
    if nome:
        try:
            query = f"explica_texto({nome.lower()}, Texto)"
            resultado = list(prolog.query(query))

            if resultado:
                texto = resultado[0]["Texto"]
                st.code(texto)
            else:
                st.warning("Suspeito não encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Digite um nome primeiro.")