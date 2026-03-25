from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyswip import Prolog
import os
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

SUSPECTS = ["larissa", "maria", "laura"]
prolog_lock = threading.Lock()


@app.get("/api/suspeitos")
def get_suspeitos():
    with prolog_lock:
        resultados = []
        for nome in SUSPECTS:
            r = list(prolog.query(f"pontuacao({nome}, P), nivel_suspeita({nome}, N)"))
            if r:
                resultados.append({"nome": nome, "pontuacao": r[0]["P"], "nivel": r[0]["N"]})
        return resultados


@app.get("/api/explicacao/{nome}")
def get_explicacao(nome: str):
    with prolog_lock:
        resultado = list(prolog.query(f"explica_texto({nome.lower()}, Texto)"))
        if not resultado:
            raise HTTPException(status_code=404, detail="Suspeito não encontrado")
        return {"nome": nome.lower(), "texto": resultado[0]["Texto"]}
