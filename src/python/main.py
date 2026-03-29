import os
from pyswip import Prolog

prolog = Prolog()
CRIME_FIXO = "roubo_quadro"

base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(base_dir, "..", "prolog", "sistema.pl")

if not os.path.exists(caminho_arquivo):
    caminho_arquivo = os.path.join(base_dir, "sistema.pl")

try:
    prolog.consult(os.path.abspath(caminho_arquivo))
except Exception as e:
    print(f"Erro ao carregar o arquivo Prolog: {e}")

def ranking_suspeitos():
    print(f"\nRANKING PARA: {CRIME_FIXO.upper()}\n")
    resultados = list(prolog.query(f"ranking({CRIME_FIXO}, Lista)"))
    
    if not resultados or not resultados[0]["Lista"]:
        print("Sem dados disponiveis.")
        return
    
    lista = resultados[0]["Lista"]
    for item in lista:
        score = item[0]
        pessoa = item[1].decode('utf-8') if isinstance(item[1], bytes) else item[1]
        
        nivel = "ALTA" if score >= 8 else "MEDIA" if score >= 4 else "BAIXA"
        print(f"{nivel} suspeita -> {pessoa.capitalize()} ({score} pontos)")

def explicar():
    nome = input("\nNome do suspeito para analise detalhada: ").lower()
    
    try:
        res_p = list(prolog.query(f"pontuacao_total({nome}, {CRIME_FIXO}, P)"))
        res_n = list(prolog.query(f"nivel_suspeita({nome}, {CRIME_FIXO}, N)"))

        if res_p and res_n:
            print(f"\n" + "="*40)
            print(f"RELATORIO INVESTIGATIVO: {nome.upper()}")
            print("="*40)
            
            res_prof = list(prolog.query(f"profissao({nome}, X)"))
            res_dig = list(prolog.query(f"situacao_digital({nome}, X)"))
            res_alibi = list(prolog.query(f"alibi_status({nome}, X)"))
            
           
            def limpar(val): 
                return val.decode('utf-8') if isinstance(val, bytes) else val

            profissao = limpar(res_prof[0]['X']) if res_prof else "Nao informada"
            digital = limpar(res_dig[0]['X']) if res_dig else "Nenhuma"
            alibi = limpar(res_alibi[0]['X']) if res_alibi else "Desconhecido"

            print(f"[-] Profissao: {profissao}")
            print(f"[-] Evidencia Digital: {digital}")
            print(f"[-] Status do Alibi: {alibi}")
            print("-" * 20)
            print(f"[>] PONTUACAO TOTAL: {res_p[0]['P']} pontos")
            print(f"[>] NIVEL DE RISCO: {res_n[0]['N'].upper()}")
            print("="*40)
        else:
            print("\n[!] Suspeito nao localizado na base de dados.")
    except Exception as e:
        print(f"\n[!] Erro durante a consulta: {e}")

def inferencia_reversa():
    print(f"\nANALISE PROFISSIONAL PARA: {CRIME_FIXO.upper()}")
    
    perfil = list(prolog.query(f"perfil_necessario({CRIME_FIXO}, P)"))
    if perfil and perfil[0]["P"]:
        profs = [p.decode('utf-8') if isinstance(p, bytes) else p for p in perfil[0]["P"]]
        print(f"Profissoes exigidas pelo caso: {', '.join(profs)}")
    
    autores = list(prolog.query(f"possivel_autor({CRIME_FIXO}, X)"))
    print("\nINDIVIDUOS COM CAPACIDADE TECNICA:")
    if autores:
        for a in autores:
            nome = a["X"].decode('utf-8') if isinstance(a["X"], bytes) else a["X"]
            print(f"- {nome.capitalize()}")
    else:
        print("- Nenhum individuo possui o perfil completo exigido.")

def menu():
    while True:
        print("\n\033[1mSISTEMA DE INVESTIGACAO FORENSE\033[0m")
        print(f"Caso: {CRIME_FIXO}")
        print("1 - Ver ranking de suspeitos")
        print("2 - Analisar suspeito")
        print("3 - Ver requisitos e possiveis autores")
        print("4 - Sair")

        op = input("\nSelecione uma opção: ")

        if op == "1":
            ranking_suspeitos()
        elif op == "2":
            explicar()
        elif op == "3":
            inferencia_reversa()
        elif op == "4":
            print("Encerrando sistema...")
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    menu()