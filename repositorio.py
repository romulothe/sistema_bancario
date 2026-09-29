from conexao import conectar


def inserir_cliente(cpf, nome, data_nascimento, endereco, senha_hash):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO clientes (
                    cpf,

                    nome,

                    data_nascimento,

                    endereco,

                    senha_hash
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cpf, nome, data_nascimento, endereco, senha_hash),
            )
        conn.commit()


def buscar_cliente_por_cpf(cpf):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id_cliente,

                    cpf,

                    nome,

                    data_nascimento,

                    endereco,

                    senha_hash

                FROM clientes

                WHERE cpf = %s
                """,
                (cpf,),
            )
            return cur.fetchone()


def inserir_conta(id_cliente, numero):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO contas (
                    id_cliente,

                    numero
                )
                VALUES (%s, %s)
                """,
                (id_cliente, numero),
            )
        conn.commit()


def buscar_conta_por_cliente(id_cliente):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id_conta,

                    agencia,

                    numero,

                    saldo,

                    limite,

                    limite_saques

                FROM contas

                WHERE id_cliente = %s

                ORDER BY id_conta

                LIMIT 1
                """,
                (id_cliente,),
            )
            return cur.fetchone()


def inserir_transacao(id_conta, tipo, valor):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transacoes (
                    id_conta,

                    tipo,

                    valor
                )
                VALUES (%s, %s, %s)
                """,
                (id_conta, tipo, valor),
            )
            cur.execute(
                """
                UPDATE contas

                SET saldo = saldo + %s

                WHERE id_conta = %s
                """,
                (valor if tipo == "Deposito" else -valor, id_conta),
            )
        conn.commit()


def contar_saques_hoje(id_conta):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*)

                FROM transacoes

                WHERE id_conta = %s

                    AND tipo = 'Saque'

                    AND data_hora::date = CURRENT_DATE
                """,
                (id_conta,),
            )
            return cur.fetchone()[0]


def listar_transacoes(id_conta):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tipo,

                    valor,

                    data_hora

                FROM transacoes

                WHERE id_conta = %s

                ORDER BY data_hora
                """,
                (id_conta,),
            )
            return cur.fetchall()


def proximo_numero_conta():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(numero), 0) + 1 FROM contas")
            return cur.fetchone()[0]


def listar_todas_contas():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    contas.agencia,

                    contas.numero,

                    clientes.nome

                FROM contas

                JOIN clientes ON clientes.id_cliente = contas.id_cliente

                ORDER BY contas.numero
                """
            )
            return cur.fetchall()


def transferir_entre_contas(id_conta_origem, id_conta_destino, valor):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transacoes (
                    id_conta,

                    tipo,

                    valor
                )
                VALUES (%s, %s, %s)
                """,
                (id_conta_origem, "Transferencia Enviada", valor),
            )
            cur.execute(
                """
                UPDATE contas

                SET saldo = saldo - %s

                WHERE id_conta = %s
                """,
                (valor, id_conta_origem),
            )
            cur.execute(
                """
                INSERT INTO transacoes (
                    id_conta,

                    tipo,

                    valor
                )
                VALUES (%s, %s, %s)
                """,
                (id_conta_destino, "Transferencia Recebida", valor),
            )
            cur.execute(
                """
                UPDATE contas

                SET saldo = saldo + %s

                WHERE id_conta = %s
                """,
                (valor, id_conta_destino),
            )
        conn.commit()


def atualizar_senha(cpf, senha_hash):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE clientes

                SET senha_hash = %s

                WHERE cpf = %s
                """,
                (senha_hash, cpf),
            )
        conn.commit()