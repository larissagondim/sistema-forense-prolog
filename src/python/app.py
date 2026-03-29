import streamlit as st
from pyswip import Prolog
import os

prolog = Prolog()
CRIME_ALVO = "roubo_quadro"

# Configuração de caminho
base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_prolog = os.path.join(base_dir, "..", "prolog", "sistema.pl")

if os.path.exists(caminho_prolog):
    prolog.consult(caminho_prolog)
else:
    # Fallback para o mesmo diretório
    caminho_prolog = os.path.join(base_dir, "sistema.pl")
    if os.path.exists(caminho_prolog):
        prolog.consult(caminho_prolog)
    else:
        st.error("Arquivo sistema.pl nao encontrado.")
        st.stop()

st.set_page_config(page_title="Investigacao Forense", layout="wide")

st.title("Sistema de investigacao: Roubo do Quadro")
st.divider()

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Ranking geral")
    if st.button("Atualizar ranking"):
        res = list(prolog.query(f"ranking({CRIME_ALVO}, Lista)"))
        if res and res[0]["Lista"]:
            for score, pessoa in res[0]["Lista"]:
                nome = pessoa.decode('utf-8') if isinstance(pessoa, bytes) else pessoa
                if score >= 8:
                    st.error(f"{nome.upper()}: {score} pontos (ALTA)")
                elif score >= 4:
                    st.warning(f"{nome.upper()}: {score} pontos (MEDIA)")
                else:
                    st.success(f"{nome.upper()}: {score} pontos (BAIXA)")

with col2:
    st.subheader("Consulta individual de cada suspeito")
    nome_input = st.text_input("Digite o nome do suspeito").lower()
    
    if st.button("Exibir dados"):
        if nome_input:
            p_local = list(prolog.query(f"pontuacao_local({nome_input}, {CRIME_ALVO}, P)"))
            p_digital = list(prolog.query(f"pontuacao_digital({nome_input}, P)"))
            p_prof = list(prolog.query(f"pontuacao_profissao({nome_input}, P)"))
            p_alibi = list(prolog.query(f"pontuacao_alibi({nome_input}, P)"))
            
            res_prof = list(prolog.query(f"profissao({nome_input}, X)"))
            res_dig = list(prolog.query(f"situacao_digital({nome_input}, X)"))
            res_alibi = list(prolog.query(f"alibi_status({nome_input}, X)"))
            
            res_total = list(prolog.query(f"pontuacao_total({nome_input}, {CRIME_ALVO}, Total)"))
            res_nivel = list(prolog.query(f"nivel_suspeita({nome_input}, {CRIME_ALVO}, Nivel)"))

            if res_total:
                st.markdown(f"### Relatorio: {nome_input.upper()}")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Pontuacao Total", res_total[0]['Total'])
                c2.metric("Nivel de Risco", res_nivel[0]['Nivel'].upper())
                
                st.write("---")
                st.write("**Detalhamento de Evidencias:**")

                prof = res_prof[0]['X'] if res_prof else "Nao informada"
                dig = res_dig[0]['X'] if res_dig else "Nenhuma"
                ali = res_alibi[0]['X'] if res_alibi else "Desconhecido"
                
                dados = {
                    "Categoria": ["Profissao", "Evidencia Digital", "Presenca no Local", "Alibi"],
                    "Status": [prof, dig, "Identificada", ali],
                    "Pontos": [
                        p_prof[0]['P'] if p_prof else 0,
                        p_digital[0]['P'] if p_digital else 0,
                        p_local[0]['P'] if p_local else 0,
                        p_alibi[0]['P'] if p_alibi else 0
                    ]
                }
                st.table(dados)
            else:
                st.error("Suspeito não encontrado na base de dados.")

st.divider()

if st.checkbox("Verificar requisitos profissionais do Crime"):
    perfil = list(prolog.query(f"perfil_necessario({CRIME_ALVO}, P)"))
    if perfil:
        profs = [p.decode('utf-8') if isinstance(p, bytes) else p for p in perfil[0]['P']]
        st.info(f"O crime exige conhecimento de: {', '.join(profs)}")
        
    autores = list(prolog.query(f"possivel_autor({CRIME_ALVO}, X)"))
    if autores:
        lista = [a['X'].decode('utf-8') if isinstance(a['X'], bytes) else a['X'] for a in autores]
        st.write(f"Individuos que possuem todas as profissoes: {', '.join(lista)}")
    else:
        st.write("Nenhum suspeito possui o conjunto completo de profissoes exigidas.")