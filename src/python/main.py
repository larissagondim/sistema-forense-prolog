from pyswip import Prolog
import time 

prolog = Prolog()
prolog.consult("../prolog/sistema.pl")


def listar_culpados():
    print("\n🔍 Suspeitos identificados:\n")
    resultados = list(prolog.query("culpado(X)"))

    if resultados:
        for r in resultados:
            print("-", r["X"])
    else:
        print("Nenhum suspeito encontrado.")


def explicar_suspeito():
    nome = input("\nDigite o nome do suspeito: ").lower()

    try:
        time.sleep(1)
        resultado = list(prolog.query(f"explica_texto({nome}, Texto)"))

        if resultado:
            print("\n" + resultado[0]["Texto"])
        else:
            print("Suspeito não encontrado.")
    except Exception as e:
        print("Erro:", e)


def menu():
    while True:
        print("\nSISTEMA FORENSE | MENU")
        print("1 - Listar culpados")
        print("2 - Explicar suspeito")
        print("3 - Sair")

        op = input("\nEscolha uma opção: ")

        if op == "1":
            time.sleep(1)
            listar_culpados()
        elif op == "2":
            time.sleep(1)
            explicar_suspeito()
        elif op == "3":
            print("Encerrando sistema...")
            time.sleep(2)
            print("Obrigada por utilizar!")
            time.sleep(2)
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()