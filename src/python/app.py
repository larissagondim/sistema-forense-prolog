import streamlit as st
from pyswip import Prolog
import os

prolog = Prolog()

base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(base_dir, "sistema.pl")

if not os.path.exists(caminho_arquivo):
    caminho_arquivo = os.path.join(base_dir, "..", "prolog", "sistema.pl")

prolog.consult(os.path.abspath(caminho_arquivo))

st.set_page_config(page_title="Sistema Forense", layout="wide")

st.title("Sistema de Investigacao Forense")

try:
    crimes = [c["C"] for c in prolog.query("crime(C)")]
    crime_selecionado = st.selectbox("Selecione o crime", crimes)
except:
    st.error("Erro ao carregar base Prolog")
    st.stop()

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ranking de Suspeitos")
    if st.button("Gerar Ranking"):
        resultado = list(prolog.query(f"ranking({crime_selecionado}, Lista)"))
        
        if not resultado or not resultado[0]["Lista"]:
            st.info("Nenhum dado encontrado")
        else:
            lista = resultado[0]["Lista"]
            for item in lista:
                score = item[0]
                pessoa = item[1]

                if score >= 8:
                    st.error(f"ALTA SUSPEITA: {pessoa} - Pontos: {score}")
                elif score >= 4:
                    st.warning(f"MEDIA SUSPEITA: {pessoa} - Pontos: {score}")
                else:
                    st.success(f"BAIXA SUSPEITA: {pessoa} - Pontos: {score}")

with col2:
    st.subheader("Explicacao")
    nome = st.text_input("Nome do suspeito")
    if st.button("Analisar"):
        if nome:
            try:
                query = f"explica({nome.lower()}, {crime_selecionado}, Texto)"
                res = list(prolog.query(query))
                if res:
                    st.text_area("Resultado:", res[0]["Texto"], height=200)
                else:
                    st.warning("Suspeito nao encontrado")
            except:
                st.error("Erro na consulta")

st.divider()
st.subheader("Inferencia Reversa")

if st.button("Ver Perfil e Autores"):
    perfil = list(prolog.query(f"perfil_necessario({crime_selecionado}, P)"))
    if perfil:
        st.write("Requisitos:", perfil[0]["P"])
    
    autores = list(prolog.query(f"possivel_autor({crime_selecionado}, X)"))
    if autores:
        st.write("Pessoas com capacidade tecnica:")
        for a in autores:
            st.write("-", a["X"])
    else:
        st.info("Nenhum autor compativel encontrado")