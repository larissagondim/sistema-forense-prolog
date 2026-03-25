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
def get_suspeitos(crime: str = "roubo_quadro"):
    with prolog_lock:
        resultados = []
        query = list(prolog.query(f"ranking({crime}, Lista)", maxresult=1))
        if not query:
            raise HTTPException(status_code=404, detail="Crime não encontrado")

        # ranking returns list of tuples (Pontuacao, Pessoa) em ordem desc
        for pontuacao, pessoa in query[0]["Lista"]:
            nivel = list(prolog.query(f"nivel_suspeita({pessoa}, {crime}, N)", maxresult=1))
            nivel_text = nivel[0]["N"] if nivel else "desconhecido"
            resultados.append({"nome": str(pessoa), "pontuacao": float(pontuacao), "nivel": str(nivel_text)})
        return resultados


@app.get("/api/explicacao/{nome}")
def get_explicacao(nome: str):
    with prolog_lock:
        crime: str = "roubo_quadro"
        resultado = list(prolog.query(f"explica({nome.lower()}, {crime}, Texto)", maxresult=1))
        if not resultado:
            raise HTTPException(status_code=404, detail="Explicação não encontrada")
        return {"nome": nome.lower(), "texto": str(resultado[0]["Texto"])}


@app.get("/api/explicacao/{crime}/{nome}")
def get_explicacao_crime(crime: str, nome: str):
    with prolog_lock:
        resultado = list(prolog.query(f"explica({nome.lower()}, {crime}, Texto)", maxresult=1))
        if not resultado:
            raise HTTPException(status_code=404, detail="Explicação não encontrada")
        return {"nome": nome.lower(), "texto": str(resultado[0]["Texto"])}
