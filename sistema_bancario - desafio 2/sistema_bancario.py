import textwrap

# Criação do menu no terminal
def menu():
    menu = """\n
    ==========MENU==========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")

    else:
        print("@@@ Operação falhou! O valor informado é inválido! @@@")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if saldo <= 0:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    if excedeu_limite:
        print(f"\n@@@ Operação falhou! Você não pode sacar mais de R$ {limite:.2f}. @@@")     

    if excedeu_saques:
        print(f"\n@@@ Operação falhou! Você não pode sacar mais de {limite_saques} vezes por dia. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
    
    else:
        print("@@@ Operação falhou! O valor informado é inválido! @@@")

    return saldo, extrato     

def exibir_extrato(saldo, /, *, extrato):
        print("\n========== EXTRATO ==========")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("\n=============================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário (somente numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("n@@@ Usuário já cadastrado. @@@")
        return None

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - Bairro - Cidade/UF): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    

def criar_conta(AGENCIA, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com suceso! ===")
        return {"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    print("\n=== LISTA DE CONTAS ===")
    for conta in contas:
        print(f"Agência: {conta['agencia']} \n Conta: {conta['numero_conta']} \n Titular: {conta['usuario']['nome']}")
        print("*" * 100)
        print("\n")     

# Função inicializadora
def main():
    # Constantes e valores iniciais
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a opção desejada.")

main()
