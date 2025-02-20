import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta  # Correção: usar _numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        return True

    # Novo método para realizar transações
    def realizar_transacao(self, transacao):
        transacao.registrar(self)


class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\nAgência:\t{self.agencia}\nC/C:\t\t{self.numero_conta}\nTitular:\t{self.cliente.nome}"""


class Cliente:
    def __init__(self, tipo_cliente, nome, numero_documento, data_registro, endereco):
        self.tipo_cliente = tipo_cliente
        self.nome = nome
        self.numero_documento = numero_documento
        self.data_registro = data_registro
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"""\nTipo de Cliente:\t{self.tipo_cliente}\nNome:\t\t{self.nome}\nNúmero do documento:\t{self.numero_documento}\nData de Registro:\t{self.data_registro}\nEndereço:\t\t{self.endereco}"""


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nco]\tNova conta
    [lco]\tListar contas
    [ncl]\tNovo cliente
    [lcl]\tListar clientes
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def filtrar_cliente(numero_documento, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.numero_documento == numero_documento]
    return clientes_filtrados[0] if clientes_filtrados else None


def filtrar_conta(numero_conta, contas):
    # Garantindo a comparação entre strings
    contas_filtradas = [conta for conta in contas if str(conta.numero_conta) == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(contas):
    numero_conta = input("Informe o número da conta: ")
    conta = filtrar_conta(numero_conta, contas)
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta.realizar_transacao(transacao)


def sacar(contas):
    numero_conta = input("Informe o número da conta: ")
    conta = filtrar_conta(numero_conta, contas)  # Correção: buscar conta e não cliente
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta.realizar_transacao(transacao)


def exibir_extrato(clientes):
    numero_documento = input("Informe a identificação (CPF ou CNPJ) do cliente: ")
    cliente = filtrar_cliente(numero_documento, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    tipos = {"1": "CPF", "2": "CNPJ"}
    tipo_cliente = input("Informe 1 para Pessoa Física e 2 para Pessoa Jurídica: ")
    if tipo_cliente not in tipos:
        print("\n@@@ Opção errada! Informe 1 para Pessoa Física e 2 para Pessoa Jurídica @@@")
        return
    numero_documento = input(f"Informe o {tipos[tipo_cliente]} (somente número): ")
    if filtrar_cliente(numero_documento, clientes):
        print(f"\n@@@ Já existe cliente com esse {tipos[tipo_cliente]}! @@@")
        return
    dados_cliente = {
        "tipo_cliente": tipo_cliente,
        "nome": input("Informe o nome completo: ") if tipo_cliente == "1" else input("Informe a razão social completa: "),
        "data_registro": input("Informe a data de nascimento (dd-mm-aaaa): ") if tipo_cliente == "1" else input("Informe a data de registro (dd-mm-aaaa): "),
        "numero_documento": numero_documento,
        "endereco": input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    }
    clientes.append(Cliente(**dados_cliente))
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    numero_documento = input("Informe a identificação (CPF ou CNPJ) do cliente: ")
    cliente = filtrar_cliente(numero_documento, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def listar_clientes(clientes):
    for cliente in clientes:
        print("=" * 100)
        print(textwrap.dedent(str(cliente)))


def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "d":
            depositar(contas)  # Passa a lista de contas
        elif opcao == "s":
            sacar(contas)      # Passa a lista de contas
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "ncl":
            criar_cliente(clientes)
        elif opcao == "nco":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lco":
            listar_contas(contas)
        elif opcao == "lcl":
            listar_clientes(clientes)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
