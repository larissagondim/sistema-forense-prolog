from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyswip import Prolog
import os
import random
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

prolog = Prolog()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
caminho = os.path.join(base_dir, "prolog", "sistema.pl")
prolog.consult(caminho)

CRIME = "roubo_quadro"
SUSPECTS = ["larissa", "maria", "laura"]
LOCAIS = ["sala_principal", "sala_seguranca", "corredor"]
HORAS = [8, 9, 10, 11, 12]
DIGITAIS = ["mensagens_apagadas", "historico_apagado", "fotos_recentes"]
PROFISSOES = ["restauradora", "curadora", "historiadora"]

prolog_lock = threading.Lock()


def query_one(q):
    r = list(prolog.query(q))
    return r[0] if r else None


def limpar(val):
    return val.decode("utf-8") if isinstance(val, bytes) else str(val)


def randomizar():
    for s in SUSPECTS:
        list(prolog.query(f"retractall(presente({s},_,_))"))
        list(prolog.query(f"retractall(situacao_digital({s},_))"))
        list(prolog.query(f"retractall(profissao({s},_))"))
        list(prolog.query(f"retractall(alibi_status({s},_))"))

    alibis = ["sim", "sim", "nao"]
    locs = LOCAIS[:]
    digs = DIGITAIS[:]
    profs = PROFISSOES[:]
    random.shuffle(alibis)
    random.shuffle(locs)
    random.shuffle(digs)
    random.shuffle(profs)

    for i, s in enumerate(SUSPECTS):
        list(prolog.query(f"assertz(presente({s},{locs[i]},{random.choice(HORAS)}))"))
        list(prolog.query(f"assertz(situacao_digital({s},{digs[i]}))"))
        list(prolog.query(f"assertz(profissao({s},{profs[i]}))"))
        list(prolog.query(f"assertz(alibi_status({s},{alibis[i]}))"))


with prolog_lock:
    randomizar()


def get_detalhes(nome):
    loc = query_one(f"presente({nome}, X, _)")
    dig = query_one(f"situacao_digital({nome}, X)")
    prof = query_one(f"profissao({nome}, X)")
    ali = query_one(f"alibi_status({nome}, X)")
    p_loc = query_one(f"pontuacao_local({nome}, {CRIME}, P)")
    p_dig = query_one(f"pontuacao_digital({nome}, P)")
    p_prof = query_one(f"pontuacao_profissao({nome}, P)")
    p_ali = query_one(f"pontuacao_alibi({nome}, P)")

    return {
        "local": limpar(loc["X"]) if loc else "desconhecido",
        "digital": limpar(dig["X"]) if dig else "desconhecido",
        "profissao": limpar(prof["X"]) if prof else "desconhecido",
        "alibi": limpar(ali["X"]) if ali else "desconhecido",
        "pontos_local": int(p_loc["P"]) if p_loc else 0,
        "pontos_digital": int(p_dig["P"]) if p_dig else 0,
        "pontos_profissao": int(p_prof["P"]) if p_prof else 0,
        "pontos_alibi": int(p_ali["P"]) if p_ali else 0,
    }


@app.get("/api/suspeitos")
def get_suspeitos():
    with prolog_lock:
        resultados = []
        for nome in SUSPECTS:
            r = query_one(f"pontuacao_total({nome}, {CRIME}, T)")
            if r:
                detalhes = get_detalhes(nome)
                resultados.append({
                    "nome": nome,
                    "pontuacao": int(r["T"]),
                    "detalhes": detalhes,
                })
        resultados.sort(key=lambda x: x["pontuacao"], reverse=True)
        return resultados


@app.post("/api/nova-rodada")
def nova_rodada():
    with prolog_lock:
        randomizar()
    return {"status": "ok"}
