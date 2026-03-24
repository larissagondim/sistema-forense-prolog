import streamlit as st
from pyswip import Prolog

prolog = Prolog()
prolog.consult("sistema.pl")

st.title("Sistema de Investigação Forense com Prolog")

st.write("Sistema especialista em Prolog para análise de suspeitos.")

if st.button("Listar Culpados"):
    resultados = list(prolog.query("culpado(X)"))
    
    if resultados:
        st.success("Suspeitos identificados: ")
        for r in resultados:
            st.write(f"- {r['X']}")
    else:
        st.warning("Nenhum suspeito encontrado.")


nome = st.text_input("Digite o nome do suspeito: ")

if st.button("Explicar Suspeito"):
    if nome:
        st.info(f"Analisando: {nome}")
        
        try:
            list(prolog.query(f"explica({nome.lower()})"))
            st.success("Explicação exibida no terminal.")
        except:
            st.error("Erro ao analisar suspeito.")
    else:
        st.warning("Digite um nome primeiro.")