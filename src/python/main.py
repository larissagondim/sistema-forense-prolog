# imports necessários
from pyswip import Prolog
import time

prolog = Prolog()
prolog.consult("../prolog/sistema.pl")


def escolher_crime():
    crimes = list(prolog.query("crime(C)"))
    lista = [c["C"] for c in crimes]

    print("\nCRIMES DISPONÍVEIS:")
    for i, c in enumerate(lista, 1):
        print(f"{i} - {c}")

    op = int(input("Escolha o crime: "))
    return lista[op - 1]


def ranking_suspeitos():
    crime = escolher_crime()
    print(f"\nRANKING PARA: {crime}\n")

    resultados = list(prolog.query(f"ranking({crime}, Lista)"))

    if resultados:
        for score, pessoa in resultados[0]["Lista"]:
            print(f"{pessoa} -> {round(score, 2)}")
    else:
        print("Sem dados.")


def explicar():
    crime = escolher_crime()
    nome = input("Nome do suspeito: ").lower()

    query = f"explica({nome}, {crime}, Texto)"
    resultado = list(prolog.query(query))

    if resultado:
        print("\n" + resultado[0]["Texto"])
    else:
        print("Não encontrado.")


def inferencia_reversa():
    crime = escolher_crime()

    print("\nPERFIL NECESSÁRIO:")
    perfil = list(prolog.query(f"perfil_necessario({crime}, P)"))
    print(perfil[0]["P"])

    print("\nPOSSÍVEIS AUTORES:")
    autores = list(prolog.query(f"possivel_autor({crime}, X)"))
    for a in autores:
        print("-", a["X"])


def menu():
    while True:
        print("\n=== SISTEMA FORENSE AVANÇADO ===")
        print("1 - Ranking de suspeitos")
        print("2 - Explicar suspeito")
        print("3 - Inferência reversa")
        print("4 - Sair")

        op = input("Opção: ")

        if op == "1":
            ranking_suspeitos()
        elif op == "2":
            explicar()
        elif op == "3":
            inferencia_reversa()
        elif op == "4":
            break
        else:
            print("Inválido")


if __name__ == "__main__":
    menu()