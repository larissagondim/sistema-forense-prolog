import os
from pyswip import Prolog

prolog = Prolog()

base_dir = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(base_dir, "sistema.pl")

if not os.path.exists(caminho_arquivo):
    caminho_arquivo = os.path.join(base_dir, "..", "prolog", "sistema.pl")

prolog.consult(os.path.abspath(caminho_arquivo))

def escolher_crime():
    crimes = list(prolog.query("crime(C)"))
    lista = [c["C"] for c in crimes]

    print("\nCRIMES DISPONIVEIS:")
    for i, c in enumerate(lista, 1):
        print(f"{i} - {c}")

    while True:
        try:
            op = int(input("Escolha o crime: "))
            if 1 <= op <= len(lista):
                return lista[op - 1]
            else:
                print("Opcao invalida")
        except ValueError:
            print("Digite um numero valido")

def ranking_suspeitos():
    crime = escolher_crime()
    print(f"\nRANKING PARA: {crime.upper()}\n")

    resultados = list(prolog.query(f"ranking({crime}, Lista)"))

    if not resultados or not resultados[0]["Lista"]:
        print("Sem dados.")
        return

    lista = resultados[0]["Lista"]

    for item in lista:
        score = item[0]
        pessoa = item[1]

        if score >= 8:
            nivel = "ALTA"
        elif score >= 4:
            nivel = "MEDIA"
        else:
            nivel = "BAIXA"

        print(f"{nivel} suspeita -> {pessoa} ({score})")

def explicar():
    crime = escolher_crime()
    nome = input("Nome do suspeito: ").lower()

    try:
        query = f"explica({nome}, {crime}, Texto)"
        resultado = list(prolog.query(query))

        if resultado:
            print("\n" + str(resultado[0]["Texto"]))
        else:
            print("Suspeito nao encontrado.")
    except Exception:
        print("Erro ao consultar Prolog.")

def inferencia_reversa():
    crime = escolher_crime()

    print("\nPERFIL NECESSARIO:")
    try:
        perfil = list(prolog.query(f"perfil_necessario({crime}, P)"))
        if perfil and perfil[0]["P"]:
            print("Habilidades:", perfil[0]["P"])
        else:
            print("Nenhum requisito especifico.")
    except Exception:
        print("Erro ao obter perfil")

    print("\nPOSSIVEIS AUTORES:")
    try:
        autores = list(prolog.query(f"possivel_autor({crime}, X)"))
        if autores:
            for a in autores:
                print("-", a["X"])
        else:
            print("Nenhum encontrado.")
    except Exception:
        print("Erro na inferencia")

def menu():
    while True:
        print("\n=== SISTEMA FORENSE AVANCADO ===")
        print("1 - Ranking de suspeitos")
        print("2 - Explicar suspeito")
        print("3 - Inferencia reversa")
        print("4 - Sair")

        op = input("Opcao: ")

        if op == "1":
            ranking_suspeitos()
        elif op == "2":
            explicar()
        elif op == "3":
            inferencia_reversa()
        elif op == "4":
            print("Encerrando...")
            break
        else:
            print("Opcao invalida")

if __name__ == "__main__":
    menu()