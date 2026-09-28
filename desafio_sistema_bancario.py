import textwrap
from datetime import datetime
from repositorio import buscar_cliente_por_cpf, buscar_conta_por_cliente, contar_saques_hoje, inserir_cliente, inserir_conta, inserir_transacao, listar_transacoes, proximo_numero_conta, listar_todas_contas


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def recuperar_conta_cliente(cliente):
    conta = buscar_conta_por_cliente(cliente[0])

    if not conta:
        print("\nCliente não possui conta!")
        return

    return conta


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))

    if valor <= 0:
        print("\nOperação inválida! O valor informado não é válido.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    inserir_transacao(conta[0], "Deposito", valor)

    print(f"\nDepósito de R$: {valor:.2f} realizado com sucesso!")


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    id_conta, agencia, numero, saldo, limite, limite_saques = conta

    numero_saques = contar_saques_hoje(id_conta)

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if valor <= 0:
        print("\nOperação inválida! O valor informado não é válido.")

    elif excedeu_saldo:
        print("\nOperação inválida! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print(f"\nOperação inválida! O valor do saque excede o limite de R$: {limite:.2f} por saque.")

    elif excedeu_saques:
        print("\nOperação inválida! Número máximo de saques diário excedido.")

    else:
        inserir_transacao(id_conta, "Saque", valor)
        print(f"\nSaque de R$: {valor:.2f} realizado com sucesso!")


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    id_conta, agencia, numero, saldo, limite, limite_saques = conta

    print("\n================ EXTRATO ================")
    transacoes = listar_transacoes(id_conta)

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for tipo, valor, data_hora in transacoes:
            extrato += (
                f"\n{tipo}:"
                f"\n\tR$ {valor:.2f}"
                f"\n\t{data_hora.strftime('%d/%m/%Y %H:%M:%S')}\n"
            )

    print(extrato, end="")
    print(f"\nSaldo:\n\tR$ {saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente_existente = buscar_cliente_por_cpf(cpf)

    if cliente_existente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento_texto = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº, bairro, cidade/sigla estado): ")

    try:
        data_nascimento = datetime.strptime(data_nascimento_texto, "%d-%m-%Y").date()
    except ValueError:
        print("\nData de nascimento inválida! Use o formato dd-mm-aaaa.")
        return

    inserir_cliente(cpf, nome, data_nascimento, endereco)

    print("\nCliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    inserir_conta(cliente[0], numero_conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    for agencia, numero, nome in listar_todas_contas():
        print("=" * 100)
        print(
            textwrap.dedent(
                f"""\
                    Agência:\t{agencia}
                    C/C:\t\t{numero}
                    Titular:\t{nome}
                """
            )
        )


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = proximo_numero_conta()
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()