import streamlit as st
from pyswip import Prolog
import os
import random

CRIME_ALVO = "roubo_quadro"
SUSPEITOS  = ["larissa", "maria", "laura"]
LOCAIS     = ["sala_principal", "sala_seguranca", "corredor"]
HORAS      = [8, 9, 10, 11, 12]
DIGITAIS   = ["mensagens_apagadas", "historico_apagado", "fotos_recentes"]
PROFISSOES = ["restauradora", "curadora", "historiadora"]

@st.cache_resource
def carregar_prolog():
    p = Prolog()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(base_dir, "sistema.pl")
    if not os.path.exists(caminho):
        caminho = os.path.join(base_dir, "..", "prolog", "sistema.pl")
    
    if os.path.exists(caminho):
        p.consult(os.path.abspath(caminho))
    else:
        st.error("Arquivo sistema.pl não encontrado!")
        st.stop()
    return p

prolog = carregar_prolog()

def limpar(val):
    return val.decode("utf-8") if isinstance(val, bytes) else val

def randomizar_atributos():
    for s in SUSPEITOS:
        list(prolog.query(f"retractall(presente({s},_,_))"))
        list(prolog.query(f"retractall(situacao_digital({s},_))"))
        list(prolog.query(f"retractall(profissao({s},_))"))
        list(prolog.query(f"retractall(alibi_status({s},_))"))

    # GARANTE A REGRA: 2 sim, 1 nao
    status_alibis = ["sim", "sim", "nao"]
    random.shuffle(status_alibis)

    for i, s in enumerate(SUSPEITOS):
        list(prolog.query(f"assertz(presente({s},{random.choice(LOCAIS)},{random.choice(HORAS)}))"))
        list(prolog.query(f"assertz(situacao_digital({s},{random.choice(DIGITAIS)}))"))
        list(prolog.query(f"assertz(profissao({s},{random.choice(PROFISSOES)}))"))
        list(prolog.query(f"assertz(alibi_status({s},{status_alibis[i]}))"))

if "inicializado" not in st.session_state:
    randomizar_atributos()
    st.session_state["inicializado"] = True

st.set_page_config(page_title="Forense - Streamlit", layout="wide")
st.title("SISTEMA DE INVESTIGAÇÃO")

if st.button("Gerar Nova Rodada"):
    randomizar_atributos()
    st.success("Novas evidências geradas (2 com álibi, 1 sem)!")

st.divider()
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Ranking de Suspeita")
    res_ranking = list(prolog.query(f"ranking({CRIME_ALVO}, Lista)"))
    if res_ranking and res_ranking[0]["Lista"]:
        for item in res_ranking[0]["Lista"]:
            st.write(f"**{limpar(item[1]).capitalize()}**: {float(item[0]):.1f} pontos")

with col2:
    st.subheader("Análise Detalhada")
    nome_sel = st.selectbox("Suspeito:", [s.capitalize() for s in SUSPEITOS]).lower()

    if nome_sel:
        res_total = list(prolog.query(f"pontuacao_total({nome_sel}, {CRIME_ALVO}, T)"))
        if res_total:
            total = float(res_total[0]["T"])
            st.metric("Pontuação Total", f"{total:.1f}")

            prof = limpar(list(prolog.query(f"profissao({nome_sel}, X)"))[0]["X"])
            dig  = limpar(list(prolog.query(f"situacao_digital({nome_sel}, X)"))[0]["X"])
            ali  = limpar(list(prolog.query(f"alibi_status({nome_sel}, X)"))[0]["X"])
            v_loc = float(list(prolog.query(f"pontuacao_local({nome_sel}, {CRIME_ALVO}, P)"))[0]["P"])

            st.table({
                "Evidência": ["Profissão", "Digital", "Álibi", "Localização"],
                "Status": [prof, dig, ali, "Detectado"],
                "Pontos": [
                    float(list(prolog.query(f"pontuacao_profissao({nome_sel}, P)"))[0]["P"]),
                    float(list(prolog.query(f"pontuacao_digital({nome_sel}, P)"))[0]["P"]),
                    float(list(prolog.query(f"pontuacao_alibi({nome_sel}, P)"))[0]["P"]),
                    v_loc
                ]
            })

st.divider()
if st.checkbox("Verificar Possíveis Autores (Perfil Técnico)"):
    autores = list(prolog.query(f"possivel_autor({CRIME_ALVO}, X)"))
    if autores:
        lista = [limpar(a["X"]).capitalize() for a in autores]
        st.warning(f"Indivíduos aptos para o crime: {', '.join(lista)}")