import streamlit as st
from pyswip import Prolog
import os

# config prolog

prolog = Prolog()

base_dir = os.path.dirname(os.path.dirname(__file__))
caminho = os.path.join(base_dir, "prolog", "sistema.pl")

prolog.consult(caminho)

# interface 

st.title("Sistema de Investigação Forense")
st.write("Sistema especialista em Prolog para análise de suspeitos.")

# listagem de culpados 

if st.button("Listar culpados"):
    resultados = list(prolog.query("culpado(X)"))

    if resultados:
        st.success("Suspeitos identificados:")
        for r in resultados:
            st.write(f"- {r['X']}")
    else:
        st.warning("Nenhum suspeito encontrado.")

# explicação do suspeito 

nome = st.text_input("Digite o nome do suspeito:")

if st.button("Explicar suspeito"):
    if nome:
        try:
            query = f"explica_texto({nome.lower()}, Texto)"
            resultado = list(prolog.query(query))

            if resultado:
                texto = resultado[0]["Texto"]
                st.text(texto)
            else:
                st.warning("Suspeito não encontrado.")
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Digite um nome primeiro.")