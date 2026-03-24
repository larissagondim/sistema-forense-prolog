from pyswip import Prolog

prolog = Prolog()
prolog.consult("sistema.pl")

def listar_culpados():
    print("\nSuspeitos identificados:")
    resultados = list(prolog.query("culpado(X)"))
    
    if resultados:
        for r in resultados:
            print("-", r["X"])
    else:
        print("Nenhum suspeito encontrado.")

def explicar_suspeito():
    nome = input("\nDigite o nome do suspeito desejado: ").lower()
    print()
    
    try:
        list(prolog.query(f"explica({nome})"))
    except:
        print("Erro ao analisar suspeito.")

def menu():
    while True:
        print("\nSISTEMA FORENSE | MENU\n")
        print("1 - Listar culpados")
        print("2 - Explicar suspeito")
        print("3 - Sair")

        op = input("\nEscolha uma opção dentre as 3 disponíveis: ")

        if op == "1":
            listar_culpados()
        elif op == "2":
            explicar_suspeito()
        elif op == "3":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()