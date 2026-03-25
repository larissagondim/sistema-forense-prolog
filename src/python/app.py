import streamlit as st
from pyswip import Prolog
import os

# config prolog
prolog = Prolog()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
caminho = os.path.join(base_dir, "prolog", "sistema.pl")
prolog.consult(caminho)

st.set_page_config(page_title="Sistema Forense", layout="wide")

st.title("Sistema de Investigação Forense Avançado")

crimes = [c["C"] for c in prolog.query("crime(C)")]
crime = st.selectbox("Selecione o crime", crimes)

st.subheader("Ranking de Suspeitos")

if st.button("Gerar ranking"):
    resultado = list(prolog.query(f"ranking({crime}, Lista)"))

    if resultado:
        lista = resultado[0]["Lista"]
        st.write(lista)
        for item in lista:
            try:
                item = item.strip().lstrip(',')
                item = item.replace('(', '').replace(')', '')
                score_str, pessoa = item.split(',')
                score = round(float(score_str.strip()), 2)
                pessoa = pessoa.strip()

            except:
                continue

            if score >= 0.7:
                st.error(f"ALERTA! {pessoa} — {score}")
            elif score >= 0.4:
                st.warning(f"CUIDADO! {pessoa} — {score}")
            else:
                st.info(f"OK! {pessoa} — {score}")


st.subheader("Explicação")

nome = st.text_input("Nome do suspeito")

if st.button("Explicar"):
    if nome:
        query = f"explica({nome.lower()}, {crime}, Texto)"
        resultado = list(prolog.query(query))

        if resultado:
            st.code(resultado[0]["Texto"])
        else:
            st.warning("Não encontrado")


st.subheader("Inferência Reversa")

if st.button("Gerar perfil do criminoso"):
    perfil = list(prolog.query(f"perfil_necessario({crime}, P)"))
    st.json(perfil[0]["P"])

    autores = list(prolog.query(f"possivel_autor({crime}, X)"))

    st.write("Possíveis autores:")
    for a in autores:
        st.write("-", a["X"])