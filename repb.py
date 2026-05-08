import sys

contas = []

def adiciona_conta(descricao, valor, participantes):
    contas.append([descricao, valor, participantes])

def quanto_deve(nome):
    total = 0
    for conta in contas:
        if nome in conta[2]:
            total = total + (conta[1] / len(conta[2]))
    return total

def main():
    while True:
        print()
        print("=== REPUBLICA ===")
        print("1. Adicionar conta")
        print("2. Quanto alguem deve")
        print("3. Sair")
        opcao = input("Opcao: ")

        if opcao == "1":
            descricao = input("  Descricao da conta: ")
            valor = float(input("  Valor: "))
            nomes_str = input("  Quem dividiu (nomes separados por espaco): ")
            participantes = nomes_str.split()
            adiciona_conta(descricao, valor, participantes)
            print(f"  Conta '{descricao}' adicionada.")
        elif opcao == "2":
            nome = input("Qual o nome da pessoa? ")
            qt = quanto_deve(nome)
            print(f"{nome} deve R${qt}")
        elif opcao == "3":
            sys.exit()
        else:
            print("Opcao invalida")

# Para rodar a interface CLI, descomente a linha abaixo:
main()
assert False, "se você ainda não fez o menu, descomente a linha acima, veja como ele esta e complete ele. Se já fez, delete essa linha"

'''
EXERCICIO: implemente as opcoes 2 e 3 no menu. Para implementar a opcao 2, basta editar dentro do elif

elif opcao == "2":
    print("opcao nao implementada") <- editar aqui

E para a opcao 3

elif opcao == "3":
    print("opcao nao impementada") <- editar aqui
        
'''
# ===== FASE 3 - Funcionalidades extras =====



'''
Agora, vamos fazer uma funcao que recebe uma lista de contas e retorna os integrantes da casa.
'''

contas.clear()
adiciona_conta("pizza", 30, ["ana", "bruno"])
adiciona_conta("uber", 20, ["ana", "carla"])


def integrantes():
    pass #implemente a funcao aqui

_aplica('integrantes') #essa linha só serve para o professor testar o exercicio em casa. Pode ignorar ou deletar
assert len(integrantes()) == 3, "a casa atualmente tem 3 integrantes. Cuidado"
assert "ana" in integrantes(), "ana é um dos integrantes"
assert "bruno" in integrantes(), "bruno é um dos integrantes"
assert "carla" in integrantes(), "carla é um dos integrantes"


adiciona_conta("internet", 90, ["ana", "bruno", "carla", "daniel"])

assert len(integrantes()) == 4
assert "ana" in integrantes(), "ana é um dos integrantes"
assert "bruno" in integrantes(), "bruno é um dos integrantes"
assert "carla" in integrantes(), "carla é um dos integrantes"
assert "daniel" in integrantes(), "daniel é um dos integrantes"

print("Exercicio integrantes: OK")

# terminado o exercicio dos integrantes, acrescente eles no menu, da seguinte forma:
# agora, quando quisermos perguntar o valor de uma divida, em vez de aceitar
# um input de string para o nome, liste todos os nomes possiveis
# e aceite um numero de usuario
# por exemplo, voce poderia imprimir
# 1. ana
# 2. bruno
# 3. carla
# 4. daniel
# e aceitar os numeros 1,2,3 e 4 como resposta.
# se o usuario digitar outra coisa, exiba novamente a lista e requisite uma nova entrada

print('\n=== PARABENS! Todos os exercicios completos! Já atualizou o menu pra usar os integrantes? ===')
