import textwrap
from datetime import datetime
from autenticacao import gerar_hash_senha, verificar_senha
from repositorio import buscar_cliente_por_cpf, buscar_conta_por_cliente, contar_saques_hoje, inserir_cliente, inserir_conta, inserir_transacao, listar_transacoes, proximo_numero_conta, listar_todas_contas, transferir_entre_contas, atualizar_senha

def menu_inicial():
    menu = """\n
    ================ MENU ================
    [login]\tEntrar
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def menu_conta(nome):
    menu = f"""\n
    ============ Olá, {nome}! ============
    [d]\tDepositar
    [s]\tSacar
    [t]\tTransferir
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [ts]\tTrocar senha
    [sair]\tSair da conta
    [q]\tSair do sistema
    => """
    return input(textwrap.dedent(menu))


def recuperar_conta_cliente(cliente):
    conta = buscar_conta_por_cliente(cliente[0])

    if not conta:
        print("\nCliente não possui conta!")
        return

    return conta


def fazer_login():
    cpf = input("Informe o CPF: ")
    senha = input("Informe a senha: ")

    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente or not verificar_senha(senha, cliente[-1]):
        print("\nCPF ou senha inválidos!")
        return None

    print(f"\nBem-vindo(a), {cliente[2]}!")
    return cliente


def depositar(cliente):
    valor = float(input("Informe o valor do depósito: "))

    if valor <= 0:
        print("\nOperação inválida! O valor informado não é válido.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    inserir_transacao(conta[0], "Deposito", valor)

    print(f"\nDepósito de R$: {valor:.2f} realizado com sucesso!")


def sacar(cliente):
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


def transferir(cliente):
    conta_origem = recuperar_conta_cliente(cliente)
    if not conta_origem:
        return

    cpf_destino = input("Informe o CPF da conta de destino: ")
    cliente_destino = buscar_cliente_por_cpf(cpf_destino)

    if not cliente_destino:
        print("\nCliente de destino não encontrado!")
        return

    conta_destino = recuperar_conta_cliente(cliente_destino)
    if not conta_destino:
        return

    id_conta_origem, agencia_origem, numero_origem, saldo_origem, limite, limite_saques = conta_origem
    id_conta_destino = conta_destino[0]

    if id_conta_origem == id_conta_destino:
        print("\nOperação inválida! Não é possível transferir para a mesma conta.")
        return

    valor = float(input("Informe o valor da transferência: "))

    if valor <= 0:
        print("\nOperação inválida! O valor informado não é válido.")
        return

    if valor > saldo_origem:
        print("\nOperação inválida! Você não tem saldo suficiente.")
        return

    transferir_entre_contas(id_conta_origem, id_conta_destino, valor)

    print(f"\nTransferência de R$: {valor:.2f} realizada com sucesso!")


def exibir_extrato(cliente):
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


def trocar_senha(cliente):
    senha_atual = input("Informe a senha atual: ")

    if not verificar_senha(senha_atual, cliente[-1]):
        print("\nSenha atual incorreta!")
        return

    nova_senha = input("Informe a nova senha: ")
    confirmacao_nova_senha = input("Confirme a nova senha: ")

    if nova_senha != confirmacao_nova_senha:
        print("\nAs senhas não coincidem!")
        return

    senha_hash = gerar_hash_senha(nova_senha)
    atualizar_senha(cliente[1], senha_hash)

    print("\nSenha alterada com sucesso!")


def criar_cliente():
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

    senha = input("Crie uma senha: ")
    confirmacao_senha = input("Confirme a senha: ")

    if senha != confirmacao_senha:
        print("\nAs senhas não coincidem!")
        return

    senha_hash = gerar_hash_senha(senha)

    inserir_cliente(cpf, nome, data_nascimento, endereco, senha_hash)

    print("\nCliente criado com sucesso!")


def criar_conta(cliente):
    numero_conta = proximo_numero_conta()
    inserir_conta(cliente[0], numero_conta)

    print("\nConta criada com sucesso!")


def listar_contas():
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
    cliente_logado = None

    while True:
        if not cliente_logado:
            opcao = menu_inicial()

            if opcao == "login":
                cliente_logado = fazer_login()

            elif opcao == "nu":
                criar_cliente()

            elif opcao == "q":
                break

            else:
                print("\nOperação inválida, por favor selecione novamente a operação desejada.")

        else:
            opcao = menu_conta(cliente_logado[2])

            if opcao == "d":
                depositar(cliente_logado)

            elif opcao == "s":
                sacar(cliente_logado)

            elif opcao == "t":
                transferir(cliente_logado)

            elif opcao == "e":
                exibir_extrato(cliente_logado)

            elif opcao == "nc":
                criar_conta(cliente_logado)

            elif opcao == "lc":
                listar_contas()

            elif opcao == "sair":
                cliente_logado = None

            elif opcao == "q":
                break

            else:
                print("\nOperação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()