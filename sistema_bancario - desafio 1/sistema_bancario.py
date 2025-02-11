menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido!")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if saldo <= 0:
            print("Operação falhou! Seu saldo não é positivo.")
            continue

        if excedeu_saldo:
           print("Operação falhou! Você não tem saldo suficiente.")
           continue

        if excedeu_limite:
           print(f"Operação falhou! Você não pode sacar mais de R$ {limite:.2f}.")
           continue        

        if excedeu_saques:
           print(f"Operação falhou! Você não pode sacar mais de {LIMITE_SAQUES} vezes por dia.")
           continue

        elif valor > 0 and saldo > valor and valor <= limite:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        
        else:
            print("Operação falhou! O valor informado é inválido!")      

    elif opcao == "e":
        print("\n========== EXTRATO ==========")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("\n=============================")
    
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a opção desejada.")