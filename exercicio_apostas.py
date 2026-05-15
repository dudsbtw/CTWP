
# === Helper de verificacao (pode ignorar) ===
# A funcao `verifica` compara o seu valor com a resposta correta (que
# fica escondida em formato de hash). Voce nao precisa entender ela -
# se voce errou, ela imprime "Valor errado: voce colocou X" e o assert
# logo abaixo dispara.
import hashlib
def verifica(valor, codigo):
    valores = [valor]
    if isinstance(valor, list):
        valores = [sorted(valor)]
    elif isinstance(valor, int) and not isinstance(valor, bool):
        valores.append(float(valor))
    elif isinstance(valor, float):
        valores.append(int(valor))
    respostas = [hashlib.sha224(str(valor).encode('utf-8')).hexdigest() == codigo for valor in valores]
    if not any(respostas):
        print(f'Valor errado: voce colocou "{valor}" na variavel')
        return False
    return True
# fim do helper


'''
EXPLICACAO

Bem-vindo ao exercicio de apostas! Vamos modelar dois jogadores -
Marcos e Dalva - que apostam em items (jogos, eventos). Cada um tem
um saldo de dinheiro e uma lista de apostas pendentes (apostas que
ainda nao foram resolvidas).

NOVIDADE: nesse exercicio, as funcoes NAO acessam variaveis globais.
Tudo o que a funcao precisa entra por parametro, e o resultado sai
pelo `return`. Quem chama a funcao e que reatribui as variaveis.

Exemplo do estilo (vai aparecer ao longo do exercicio):

    saldo_marcos = funcao_que_calcula(saldo_marcos, ...)

Assim, a variável saldo_marcos é atualizada através do retorno da função

Isso e diferente dos exercicios anteriores (album, restaurante,
republica), onde as funcoes mexiam em listas globais diretamente.

ESTRUTURAS

Cada aposta e uma lista de 2 elementos: [item, valor].

    aposta = ["lakers", 10]   # apostou 10 reais em "lakers"

A lista de apostas e uma lista de listas:

    apostas_marcos = [["lakers", 10], ["vasco", 5]]

Quando os items sao resolvidos, chega uma "lista de resultados":
cada resultado tambem e uma lista de 2 elementos, mas o segundo e
True (ganhou) ou False (perdeu):

    resultados = [["lakers", True], ["vasco", False]]
'''


# ===== FASE 1 - Aquecimento: lendo apostas e resultados =====

apostas_exemplo = [["lakers", 10], ["vasco", 5], ["lakers", 3]]
resultados_exemplo = [["lakers", True], ["vasco", False]]

'''
EXERCICIO

Considere as listas acima

Preencha as variaveis usando uma EXPRESSAO Python que produz o
valor (em vez de escrever o valor literal direto). 

Se nao conseguir, pode comecar escrevendo o valor para ver o teste passar,
mas depois tente escrever a expressao

1) Qual o item da PRIMEIRA aposta de apostas_exemplo? (string)

   Dica: e apostas_exemplo[0][0]. O primeiro [0] pega a '["lakers",10]' 
   (que eh ela mesma uma listinha de 2 elementos), o segundo [0]
   pega o primeiro elemento dessa listinha ("lakers").
'''
item_da_primeira_aposta = apostas_exemplo[0][0]

'''
2) Qual o VALOR da primeira aposta de apostas_exemplo? (numero)
'''
valor_da_primeira_aposta = apostas_exemplo[0][1]

'''
3) Quantas apostas tem em apostas_exemplo? (numero)
'''
quantas_apostas_marcos = len(apostas_exemplo)

'''
4) O "lakers" ganhou em resultados_exemplo? (True ou False)

   Dica: olhe a resultado do lakers. Que indice ela tem em
   resultados_exemplo? E dentro dela, em que posicao esta o
   True/False?
'''
lakers_ganhou = resultados_exemplo[0][1]

assert verifica(item_da_primeira_aposta, 'e02f4067e3d539f513e6b65fdd08a121a6491bcc35ed49384957319c'), 'item_da_primeira_aposta incorreta'
assert verifica(valor_da_primeira_aposta, '3aac67cd73162d439f9947d61357a1b62432f0ca84b7f435f4177a8c'), 'valor_da_primeira_aposta incorreta'
assert verifica(quantas_apostas_marcos, '4cfc3a1811fe40afa401b25ef7fa0379f1f7c1930a04f8755d678474'), 'quantas_apostas_marcos incorreta'
assert verifica(lakers_ganhou, 'b45899583510159617e22fca2b6f561a09289be12ccb30f6df8d4a11'), 'lakers_ganhou incorreta'
print('Exercicio lendo apostas e resultados: OK')


'''
EXERCICIO

Calculo a mao. Considere ainda:

    apostas_exemplo = [["lakers", 10], ["vasco", 5], ["lakers", 3]]
    resultados_exemplo = [["lakers", True], ["vasco", False]]

Regra do jogo: quando uma aposta GANHA (item resolvido como True),
o jogador recebe o valor apostado MULTIPLICADO POR 2 (eh como receber
de volta o que apostou + um premio igual). Se a aposta
PERDE (False), o jogador nao recebe nada (o saldo ja tinha sido
descontado na hora da aposta).

Olhe aposta por aposta de apostas_exemplo:
    - lakers, 10 -> ganhou -> recebe 20
    - vasco,  5  -> perdeu -> recebe 0
    - lakers, 3  -> ganhou -> recebe 6

Quanto Marcos recebe NO TOTAL nessa rodada de resultados? (numero)
'''
ganho_marcos_a_mao = 26

assert verifica(ganho_marcos_a_mao, '958d42a83cf840cde79922f0795fd6ac7da4d2df828edc32244bb3ba'), 'ganho_marcos_a_mao incorreta'

# Ja a dalva fez a seguinte aposta:
apostas_exemplo = [["lakers", 3], ["vasco", 50], ["vasco", 13]]
# qual foi o ganho dela?
ganho_dalva_a_mao = 6

assert verifica(ganho_dalva_a_mao, '31da1a042dc910775ed8b487afbdafd929a7afdeaadc660cb963bd26'), 'ganho_dalva_a_mao incorreta'

print('Exercicio calculo a mao: OK')


# ===== FASE 2 - A funcao aposta =====

'''
EXPLICACAO

Vamos comecar a escrever as funcoes. Lembre-se: as funcoes
desse exercicio NAO acessam variaveis globais. Recebem tudo por
parametro.

A primeira funcao e `aposta`. Quando um jogador faz uma aposta:
    - o valor apostado SAI do saldo dele (desconta)
    - a aposta entra na lista de apostas pendentes (.append)

Repare: esses dois efeitos sao de tipos diferentes em Python:
    - saldo e um numero (inteiro). Numeros sao IMUTAVEIS - voce
      nao consegue mudar o saldo "por dentro" da funcao. Por isso
      a funcao retorna o novo saldo, e quem chama reatribui.
    - apostas e uma lista. Listas sao MUTAVEIS - quando voce passa
      a lista por parametro, .append() modifica a mesma lista que
      esta la fora. Nao precisa retornar.

E por isso a funcao tem essa cara: muta a lista (sem retornar a
lista) e retorna o novo saldo.
'''


'''
EXERCICIO

Faca a funcao aposta(saldo, apostas, item, valor) que:
    - faz apostas.append([item, valor])  (adiciona a aposta na lista)
    - retorna saldo - valor               (novo saldo, ja descontado)

Repare que a funcao NAO retorna a lista de apostas - ela so muta a
lista que veio por parametro.

    >>> saldo = 100
    >>> apostas_jose = []
    >>> saldo = aposta(saldo, apostas_jose, "lakers", 10)
    >>> saldo
    90
    >>> apostas_jose
    [["lakers", 10]]
    >>> saldo = aposta(saldo, apostas_jose, "vasco", 5)
    >>> saldo
    85
    >>> apostas_jose
    [["lakers", 10], ["vasco", 5]]
'''
def aposta(saldo, apostas, item, valor):
    apostas.append([item, valor])
    saldo = saldo - valor
    return saldo
    

# teste 1: primeira aposta
saldo_t = 100
apostas_t = []
saldo_t = aposta(saldo_t, apostas_t, "lakers", 10)
assert saldo_t == 90, f'apos aposta de 10, saldo deveria ser 90, obteve {saldo_t}'
assert apostas_t == [["lakers", 10]], f'apostas errado: {apostas_t}'

# teste 2: segunda aposta
saldo_t = aposta(saldo_t, apostas_t, "vasco", 5)
assert saldo_t == 85, f'apos aposta de 5, saldo deveria ser 85, obteve {saldo_t}'
assert apostas_t == [["lakers", 10], ["vasco", 5]], f'apostas errado: {apostas_t}'

# teste 3: aposta no mesmo item de novo (deve aparecer duas vezes na lista)
saldo_t = aposta(saldo_t, apostas_t, "lakers", 3)
assert saldo_t == 82, f'saldo deveria ser 82, obteve {saldo_t}'
assert apostas_t == [["lakers", 10], ["vasco", 5], ["lakers", 3]], f'apostas errado: {apostas_t}'

print('Exercicio aposta: OK')


# ===== FASE 3 - O helper ganhou =====

'''
EXERCICIO

Antes de fazer a funcao que atualiza o saldo, vamos fazer uma
funcao auxiliar que vai ajudar.

Faca a funcao ganhou(item, resultados) que percorre a lista de
resultados procurando pelo item, e:
    - se achar, retorna o resultado (True ou False) que esta junto
    - se nao achar, retorna False (item ainda nao foi resolvido)

Lembre que cada resultado e uma lista [item, True/False]. Entao:
    - resultado[0] eh o item
    - resultado[1] eh o resultado (True/False)

Dica: use um for para percorrer resultados. Para cada resultado, se
resultado[0] == item, retorne resultado[1].

    >>> ganhou("lakers", [["lakers", True], ["vasco", False]])
    True
    >>> ganhou("vasco", [["lakers", True], ["vasco", False]])
    False
    >>> ganhou("palmeiras", [["lakers", True], ["vasco", False]])
    False
    (palmeiras nao aparece nas resultados - retorna False)
    >>> ganhou("lakers", [])
    False
    (lista resultados vazia)
'''
def ganhou(item, resultados):
    for resultado in resultados:
        if resultado[0] == item:
            return resultado[1]
    return False

assert ganhou("lakers", [["lakers", True], ["vasco", False]]) == True, 'ganhou("lakers", ...) deveria ser True'
assert ganhou("vasco", [["lakers", True], ["vasco", False]]) == False, 'ganhou("vasco", ...) deveria ser False'
assert ganhou("palmeiras", [["lakers", True], ["vasco", False]]) == False, 'ganhou de item nao resolvido deveria ser False'
assert ganhou("lakers", []) == False, 'ganhou com resultados vazia deveria ser False'
assert ganhou("lakers", [["vasco", True], ["lakers", True]]) == True, 'ganhou deveria achar lakers mesmo nao sendo o primeiro'

print('Exercicio ganhou: OK')


# ===== FASE 4 - novo_saldo =====

'''
EXERCICIO

Faca a funcao novo_saldo(saldo, apostas, resultados) que retorna o
saldo atualizado depois de uma rodada de resultados.

Para cada aposta na lista apostas:
    - se o item da aposta GANHOU (use a funcao ganhou que voce ja
      fez), some valor * 2 no saldo
    - se nao ganhou, nao faz nada

Importante: a funcao NAO modifica a lista apostas. So calcula o
novo saldo e retorna.

Dica: use um for para percorrer apostas. Cada elemento e uma lista
[item, valor], entao aposta[0] e o item e aposta[1] e o valor.

    >>> apostas = [["lakers", 10], ["vasco", 5], ["palmeiras", 20]]
    >>> resultados = [["lakers", True], ["vasco", False]]
    >>> novo_saldo(100, apostas, resultados)
    120
    (lakers ganhou: +20; vasco perdeu: 0; palmeiras nao resolvido: 0;
     saldo final = 100 + 20 = 120)

    >>> novo_saldo(100, apostas, [])
    100
    (nenhum resultado na lista - saldo nao muda)

    >>> novo_saldo(100, apostas, [["lakers", True], ["vasco", True], ["palmeiras", True]])
    170
    (todos ganharam: +20 +10 +40 = 70; saldo = 100 + 70 = 170)
'''
def novo_saldo(saldo, apostas, resultados):
    ganhos = 0
    for aposta in apostas:
        if ganhou(aposta[0], resultados):
            ganhos = ganhos + aposta[1] * 2
    return ganhos + saldo

apostas_t = [["lakers", 10], ["vasco", 5], ["palmeiras", 20]]

# 1: mistura
res = [["lakers", True], ["vasco", False]]
assert novo_saldo(100, apostas_t, res) == 120, f'novo_saldo com mistura deveria ser 120, obteve {novo_saldo(100, apostas_t, res)}'

# 2: nenhuma resultado
assert novo_saldo(100, apostas_t, []) == 100, 'novo_saldo sem resultados deveria deixar saldo igual'

# 3: todos perderam
todos_perderam = [["lakers", False], ["vasco", False], ["palmeiras", False]]
assert novo_saldo(100, apostas_t, todos_perderam) == 100, 'novo_saldo com todos perdendo deveria deixar saldo igual'

# 4: todos ganharam
todos_ganharam = [["lakers", True], ["vasco", True], ["palmeiras", True]]
assert novo_saldo(100, apostas_t, todos_ganharam) == 170, f'novo_saldo com todos ganhando deveria ser 170, obteve {novo_saldo(100, apostas_t, todos_ganharam)}'

# 5: nao deve modificar a lista de apostas
apostas_antes = [["lakers", 10], ["vasco", 5]]
apostas_copia = [["lakers", 10], ["vasco", 5]]
novo_saldo(100, apostas_antes, [["lakers", True]])
assert apostas_antes == apostas_copia, 'novo_saldo NAO deveria modificar a lista apostas'

print('Exercicio novo_saldo: OK')


# ===== FASE 5 - apostas_pendentes =====

'''
EXERCICIO

Faca a funcao apostas_pendentes(apostas, resultados) que retorna
uma NOVA lista contendo so as apostas cujo item AINDA NAO foi
resolvido (nao aparece em resultados - nem como True, nem como False).

Importante: aqui voce NAO usa a funcao ganhou. Aqui o que importa
e se o item APARECE em resultados, nao se ele ganhou.

Dica: crie uma lista vazia `pendentes`. Percorra apostas. Para cada
aposta, percorra resultados pra ver se o item da aposta esta la.
Se NAO esta, faca pendentes.append(aposta).

A funcao NAO deve modificar a lista apostas original.

    >>> apostas = [["lakers", 10], ["vasco", 5], ["palmeiras", 20]]
    >>> resultados = [["lakers", True], ["vasco", False]]
    >>> apostas_pendentes(apostas, resultados)
    [["palmeiras", 20]]
    (lakers e vasco resolvidos, palmeiras nao)

    >>> apostas_pendentes(apostas, [])
    [["lakers", 10], ["vasco", 5], ["palmeiras", 20]]
    (nenhuma resultado - todas continuam pendentes)

    >>> apostas_pendentes(apostas, [["lakers", True], ["vasco", False], ["palmeiras", True]])
    []
    (todas resolvidas)
'''
def apostas_pendentes(apostas, resultados):
    pass

apostas_t = [["lakers", 10], ["vasco", 5], ["palmeiras", 20]]

# 1: mistura
res = [["lakers", True], ["vasco", False]]
assert apostas_pendentes(apostas_t, res) == [["palmeiras", 20]], f'apostas_pendentes com mistura: esperado [["palmeiras", 20]], obteve {apostas_pendentes(apostas_t, res)}'

# 2: nenhuma resultado
assert apostas_pendentes(apostas_t, []) == [["lakers", 10], ["vasco", 5], ["palmeiras", 20]], 'sem resultados, todas as apostas continuam pendentes'

# 3: todas resolvidas
todas = [["lakers", True], ["vasco", False], ["palmeiras", True]]
assert apostas_pendentes(apostas_t, todas) == [], 'com todas resolvidas, pendentes deveria ser []'

# 4: nao deve modificar a lista original
apostas_antes = [["lakers", 10], ["vasco", 5]]
apostas_copia = [["lakers", 10], ["vasco", 5]]
apostas_pendentes(apostas_antes, [["lakers", True]])
assert apostas_antes == apostas_copia, 'apostas_pendentes NAO deveria modificar a lista apostas original'

print('Exercicio apostas_pendentes: OK')


# ===== FASE 6 - Simulacao Marcos e Dalva =====

'''
EXPLICACAO

Leia o bloco abaixo para entender como as duas funcoes que você implementou
fazem a bet funcionar

Repare como a funcao aposta serve pros DOIS 
jogadores - basta chamar com argumentos diferentes.
QUEM CHAMA eh que reatribui as variaveis a cada passo.
'''

# inicio do dia
saldo_marcos = 0
saldo_dalva = 0
apostas_marcos = []
apostas_dalva = []

# depositos (sem funcao, somei direto)
saldo_marcos = saldo_marcos + 100
saldo_dalva = saldo_dalva + 200

# Marcos faz duas apostas
assert saldo_marcos == 100
saldo_marcos = aposta(saldo_marcos, apostas_marcos, "lakers", 10)
saldo_marcos = aposta(saldo_marcos, apostas_marcos, "vasco", 5)
assert saldo_marcos == 85, f'apos 2 apostas, saldo_marcos deveria ser 85, obteve {saldo_marcos}'
assert apostas_marcos == [["lakers", 10], ["vasco", 5]], f'apostas_marcos errado: {apostas_marcos}'

# Dalva faz duas apostas
assert saldo_dalva == 200
saldo_dalva = aposta(saldo_dalva, apostas_dalva, "palmeiras", 30)
saldo_dalva = aposta(saldo_dalva, apostas_dalva, "lakers", 50)
assert saldo_dalva == 120, f'apos 2 apostas, saldo_dalva deveria ser 120, obteve {saldo_dalva}'
assert apostas_dalva == [["palmeiras", 30], ["lakers", 50]], f'apostas_dalva errado: {apostas_dalva}'

# chega a resultado da rodada
resultados = [["lakers", True], ["palmeiras", False]]

'''
EXERCICIO

Antes de rodar as funcoes de atualizacao, PREVEJA o saldo final de
cada jogador apos esta rodada de resultados.

Estado atual:
    - Marcos: saldo 85, apostas [["lakers", 10], ["vasco", 5]]
    - Dalva:  saldo 120, apostas [["palmeiras", 30], ["lakers", 50]]
    - Resultados: [["lakers", True], ["palmeiras", False]]

Lembre: quando uma aposta GANHA (True nos resultados), o jogador
recebe valor * 2. Quando PERDE (False), nao recebe nada. Apostas em
items que NAO aparecem nos resultados continuam pendentes e nao
afetam o saldo agora.

Preencha os valores previstos abaixo. Depois, a simulacao roda e os
asserts seguintes confirmam se a sua previsao bate com o que as
funcoes calculam de fato.
'''
saldo_final_marcos_previsto = 'coloque o valor aqui'
saldo_final_dalva_previsto = 'coloque o valor aqui'

assert verifica(saldo_final_marcos_previsto, '6f17c8e6d3ccc5beb34089e2cb28b549845a394250cafc588c179ef0'), 'saldo_final_marcos_previsto incorreto'
assert verifica(saldo_final_dalva_previsto, '92b72c299ad3d40feba03d38004028fb6b8dda64385d450f249753d8'), 'saldo_final_dalva_previsto incorreto'
print('Exercicio previsao do saldo final: OK')

# atualiza Marcos
assert saldo_marcos == 85
saldo_marcos = novo_saldo(saldo_marcos, apostas_marcos, resultados)
apostas_marcos = apostas_pendentes(apostas_marcos, resultados)
# Marcos: lakers ganhou (+20), vasco continua pendente
assert saldo_marcos == 105, f'apos resultado, saldo_marcos deveria ser 105 (85+20), obteve {saldo_marcos}'
assert apostas_marcos == [["vasco", 5]], f'apostas_marcos pendentes deveria ser [["vasco", 5]], obteve {apostas_marcos}'

# atualiza Dalva (mesma resultados - a funcao eh generica!)
assert saldo_dalva == 120
saldo_dalva = novo_saldo(saldo_dalva, apostas_dalva, resultados)
apostas_dalva = apostas_pendentes(apostas_dalva, resultados)
# Dalva: palmeiras perdeu (+0), lakers ganhou (+100)
assert saldo_dalva == 220, f'apos resultado, saldo_dalva deveria ser 220 (120+100), obteve {saldo_dalva}'
assert apostas_dalva == [], f'apostas_dalva pendentes deveria ser [], obteve {apostas_dalva}'

print('Exercicio simulacao Marcos e Dalva: OK')


print('\n=== PARABENS! Todos os exercicios completos! ===')


# ===== FASE 7 - INTERFACE CLI (se voce nao conseguir terminar, fazer em casa) =====
#
# Menu pra usar o sistema de apostas. Para rodar, descomente a linha
# "main()" no final.
#
# Algumas opcoes estao marcadas como [implementar] - sao pra voce
# completar depois.

def main():
    saldo_marcos = 0
    saldo_dalva = 0
    apostas_marcos = []
    apostas_dalva = []

    while True:
        print()
        print("=== APOSTAS ===")
        print(f"saldo Marcos: {saldo_marcos} | apostas: {apostas_marcos}")
        print(f"saldo Dalva:  {saldo_dalva} | apostas: {apostas_dalva}")
        print("1. Marcos deposita")
        print("2. Marcos aposta")
        print("3. Dalva deposita")
        print("4. Dalva aposta")
        print("5. Resolver items")
        print("6. Sair")
        opcao = input("Opcao: ")

        if opcao == "1":
            valor = int(input("  Valor do deposito: "))
            saldo_marcos = saldo_marcos + valor
        elif opcao == "2":
            item = input("  Item: ")
            valor = int(input("  Valor: "))
            saldo_marcos = aposta(saldo_marcos, apostas_marcos, item, valor)
        elif opcao == "3":
            print("  [implementar: deposito da Dalva, igual ao do Marcos]")
        elif opcao == "4":
            print("  [implementar: aposta da Dalva, igual a do Marcos]")
        elif opcao == "5":
            # le uma lista de resultados do usuario
            resultados = []
            while True:
                item = input("  Item resolvido (ou ENTER para terminar): ")
                if item == "":
                    break
                resultado_str = input(f"    {item} ganhou? (s/n): ")
                resultado = (resultado_str == "s") # isso eh um booleano, um True ou False
                resultados.append([item, resultado])
            # atualiza Marcos
            saldo_marcos = novo_saldo(saldo_marcos, apostas_marcos, resultados)
            print("""Veja que estamos fazendo besteira. Se o marcos ganhar uma aposta,
            ele está ganhando dinheiro a cada atualizacao. Devia ganhar soh na primeira
            conserte!""")
            # atualiza Dalva (implementar - mesma coisa pra Dalva)
            print("  [implementar: atualizar Dalva com novo_saldo e apostas_pendentes]")
        elif opcao == "6":
            break
        else:
            print("Opcao invalida")


# Para rodar a interface, descomente:
# main()
