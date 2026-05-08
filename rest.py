import sys

def acha_indice(lista, item):
    i = 0
    for e in lista:
        if e == item:
            return i
        i = i + 1

produtos = []
precos = []

def cadastra(nome, preco):
    produtos.append(nome)
    precos.append(preco)

def preco_de(nome):
    i = acha_indice(produtos, nome)
    return precos[i]

def muda_preco(nome, novo_preco):
    i = acha_indice(produtos, nome)
    precos[i] = novo_preco

def total_pedido(pedido):
    total = 0
    for e in pedido:
        total = total + preco_de(e)
    return total

pedidos = []

def cria_pedido():
    pedidos.append([])
    idUltimoPedido = len(pedidos) - 1
    return idUltimoPedido

def adiciona_ao_pedido(indice, produto):
    pedidos[indice].append(produto)

def remove_do_pedido(indice, produto):
    pedidos[indice].remove(produto)

def receita_do_dia():
    receita = 0
    for e in pedidos:
        receita = receita + total_pedido(e)
    return receita

def menu_principal():
    print("=== RESTAURANTE - MENU PRINCIPAL ===")
    print("1. Produtos")
    print("2. Pedidos")
    print("3. Calcular receita do dia")
    print("4. Sair")

    opcao = input("Opção: ")

    if opcao == "1":
        menu_produtos()

    elif opcao == "2":
        menu_pedidos()

    elif opcao == "3":
        menu_receita()

    elif opcao == "4":
        sys.exit()

    else:
        print("Opção inválida")
        menu_principal()

def menu_produtos():
    print()
    print("--- PRODUTOS ---")
    print("1. Cadastrar produto")
    print("2. Alterar preço de produto")
    print("3. Ver todos os produtos e preços")
    print("4. Voltar")

    opcao = input("Opção: ")

    if opcao == "1":
        nome = input("Nome do produto: ")
        preco = int(input("Preco: "))
        cadastra(nome, preco)
        print(f"Produto '{nome}' cadastrado com preco {preco}.")
        menu_produtos()

    elif opcao == "2":
        print(f"Produtos: {produtos}")
        nome = input("Qual o nome do produto? ")
        preco = int(input("Qual vai ser o preço novo? "))
        muda_preco(nome, preco)
        menu_produtos()

    elif opcao == "3": 
        print(f"Produtos: {produtos}")
        print(f"Preços:   {precos}")
        menu_produtos()

    elif opcao == "4":
        menu_principal()
    
    else:
        print("Opção inválida")
        menu_produtos()

def menu_pedidos():
    print()
    print("--- PEDIDOS ---")
    print("1. Criar novo pedido")
    print("2. Adicionar produto a pedido")
    print("3. Remover produto de pedido")
    print("4. Ver todos os pedidos")
    print("5. Voltar")

    opcao = input("Opção: ")

    if opcao == "1":
        indice = cria_pedido()
        print(f"Pedido criado com indice {indice}.")
        menu_pedidos()

    elif opcao == "2":
        indice = int(input("Indíce do pedido: "))
        produto = input("Nome do produto: ")
        adiciona_ao_pedido(indice, produto)
        print(f"  Produto '{produto}' adicionado ao pedido {indice}.")
        menu_pedidos()

    elif opcao == "3":
        indice = int(input("Indíce do pedido: "))
        produto = input("Nome do produto: ")
        remove_do_pedido(indice, produto)
        menu_pedidos()

    elif opcao == "4":
        print(f"Pedidos: {pedidos}")
        menu_pedidos()
    
    elif opcao == "5":
        menu_principal()
    
    else:
        print("Opção inválida")
        menu_pedidos()

def menu_receita():
    print(f"Valor total dos pedidos do dia: {receita_do_dia()}")
    menu_principal()

def main():
    menu_principal()

main()
