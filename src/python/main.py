# imports necessários
from pyswip import Prolog
import time

# configurando prolog
prolog = Prolog()
prolog.consult("../prolog/sistema.pl")

# função principal para listagem de suspeitos
def listar_suspeitos():
    print("\nANÁLISE DE SUSPEITOS\n")

    resultados = list(prolog.query("pontuacao(X, P), nivel_suspeita(X, N)"))

    if resultados:
        for r in resultados:
            nome = r["X"]
            pontos = r["P"]
            nivel = r["N"]

            if nivel == "alta":
                print(f"🚨 {nome} | Pontos: {pontos} | ALTA suspeita")
            elif nivel == "media":
                print(f"⚠️ {nome} | Pontos: {pontos} | MÉDIA suspeita")
            else:
                print(f"ℹ️ {nome} | Pontos: {pontos} | BAIXA suspeita")
    else:
        print("Nenhum suspeito encontrado.")

# função para listagem de culpados
def listar_culpados():
    print("\nCULPADOS IDENTIFICADOS\n")

    resultados = list(prolog.query("culpado(X)"))

    if resultados:
        for r in resultados:
            print("-", r["X"])
    else:
        print("Nenhum culpado encontrado.")

# função para mostrar a explicação de cada suspeito
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
        print("1 - Analisar suspeitos")
        print("2 - Listar culpados")
        print("3 - Explicar suspeito")
        print("4 - Sair")

        op = input("\nEscolha uma opção: ")

        if op == "1":
            time.sleep(1)
            listar_suspeitos()
        elif op == "2":
            time.sleep(1)
            listar_culpados()
        elif op == "3":
            time.sleep(1)
            explicar_suspeito()
        elif op == "4":
            print("Encerrando sistema...")
            time.sleep(1)
            print("Obrigada por utilizar!")
            time.sleep(1)
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()