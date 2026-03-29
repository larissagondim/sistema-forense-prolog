import os
import random
from pyswip import Prolog

BOLD  = "\033[1m"
RESET = "\033[0m"

prolog = Prolog()
CRIME_FIXO = "roubo_quadro"

SUSPEITOS  = ["larissa", "maria", "laura"]
LOCAIS     = ["sala_principal", "sala_seguranca", "corredor"]
HORAS      = [8, 9, 10, 11, 12]
DIGITAIS   = ["mensagens_apagadas", "historico_apagado", "fotos_recentes"]
PROFISSOES = ["restauradora", "curadora", "historiadora"]

base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(base_dir, "sistema.pl")
if not os.path.exists(caminho_arquivo):
    caminho_arquivo = os.path.join(base_dir, "..", "prolog", "sistema.pl")

try:
    prolog.consult(os.path.abspath(caminho_arquivo))
except Exception as e:
    print(f"Erro ao carregar o arquivo Prolog: {e}")

def limpar(val):
    return val.decode("utf-8") if isinstance(val, bytes) else val

def randomizar_atributos():
    for s in SUSPEITOS:
        list(prolog.query(f"retractall(presente({s},_,_))"))
        list(prolog.query(f"retractall(situacao_digital({s},_))"))
        list(prolog.query(f"retractall(profissao({s},_))"))
        list(prolog.query(f"retractall(alibi_status({s},_))"))

    # GARANTE A REGRA: 2 com álibi e 1 sem
    status_alibis = ["sim", "sim", "nao"]
    random.shuffle(status_alibis)

    for i, s in enumerate(SUSPEITOS):
        local = random.choice(LOCAIS)
        hora  = random.choice(HORAS)
        list(prolog.query(f"assertz(presente({s},{local},{hora}))"))
        
        digital = random.choice(DIGITAIS)
        list(prolog.query(f"assertz(situacao_digital({s},{digital}))"))
        
        prof = random.choice(PROFISSOES)
        list(prolog.query(f"assertz(profissao({s},{prof}))"))
        
        list(prolog.query(f"assertz(alibi_status({s},{status_alibis[i]}))"))

def ranking_suspeitos():
    print(f"\nRANKING PARA: {CRIME_FIXO.upper()}\n")
    resultados = list(prolog.query(f"ranking({CRIME_FIXO}, Lista)"))
    if not resultados or not resultados[0]["Lista"]:
        print("Sem dados disponiveis.")
        return
    lista = resultados[0]["Lista"]
    for item in lista:
        score  = item[0]
        pessoa = limpar(item[1])
        print(f"{pessoa.capitalize()} ({score} pontos)")

def explicar():
    nome = input("\nNome do suspeito para analise detalhada: ").lower()
    try:
        res_p = list(prolog.query(f"pontuacao_total({nome}, {CRIME_FIXO}, P)"))
        if res_p:
            print(f"\n{'='*40}")
            print(f"RELATORIO INVESTIGATIVO: {nome.upper()}")
            print("="*40)
            
            res_prof  = list(prolog.query(f"profissao({nome}, X)"))
            res_dig   = list(prolog.query(f"situacao_digital({nome}, X)"))
            res_alibi = list(prolog.query(f"alibi_status({nome}, X)"))
            res_presenca = list(prolog.query(f"presente({nome}, Local, Hora)"))

            profissao = limpar(res_prof[0]["X"])  if res_prof  else "Nao informada"
            digital   = limpar(res_dig[0]["X"])   if res_dig   else "Nenhuma"
            alibi     = limpar(res_alibi[0]["X"]) if res_alibi else "Desconhecido"

            if res_presenca:
                local = limpar(res_presenca[0]["Local"])
                hora  = res_presenca[0]["Hora"]
            else:
                local = "Desconhecido"
                hora  = "?"

            print(f"[-] Profissao:        {profissao}")
            print(f"[-] Evidencia Digital:{digital}")
            print(f"[-] Status do Alibi:  {alibi}")
            print(f"[-] Local/Horario:    {local} às {hora}h")
            print("-"*20)
            print(f"[>] PONTUACAO TOTAL:  {res_p[0]['P']} pontos")
            print("="*40)
        else:
            print("\n[!] Suspeito nao localizado na base de dados.")
    except Exception as e:
        print(f"\n[!] Erro durante a consulta: {e}")

def inferencia_reversa():
    print(f"\nANALISE PROFISSIONAL PARA: {CRIME_FIXO.upper()}")
    perfil = list(prolog.query(f"perfil_necessario({CRIME_FIXO}, P)"))
    if perfil and perfil[0]["P"]:
        profs = [limpar(p) for p in perfil[0]["P"]]
        print(f"Profissoes exigidas pelo caso: {', '.join(profs)}")
    autores = list(prolog.query(f"possivel_autor({CRIME_FIXO}, X)"))
    print("\nINDIVIDUOS COM CAPACIDADE TECNICA:")
    if autores:
        for a in autores:
            print(f"- {limpar(a['X']).capitalize()}")
    else:
        print("- Nenhum individuo possui o perfil completo exigido.")

def menu():
    randomizar_atributos()
    while True:
        print(f"\n{BOLD}SISTEMA DE INVESTIGACAO FORENSE{RESET}")
        print(f"Caso: {CRIME_FIXO}")
        print("1 - Ver ranking de suspeitos")
        print("2 - Analisar suspeito")
        print("3 - Ver requisitos e possiveis autores")
        print("4 - Nova rodada")
        print("5 - Sair")
        op = input("\nSelecione uma opcao: ")
        if op == "1": ranking_suspeitos()
        elif op == "2": explicar()
        elif op == "3": inferencia_reversa()
        elif op == "4": randomizar_atributos()
        elif op == "5": break
        else: print("Opcao invalida.")

if __name__ == "__main__":
    menu()