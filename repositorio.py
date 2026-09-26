from conexao import conectar


def inserir_cliente(cpf, nome, data_nascimento, endereco):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO clientes (
                    cpf,
                    nome,
                    data_nascimento,
                    endereco
                )
                VALUES (%s, %s, %s, %s)
                """,
                (cpf, nome, data_nascimento, endereco),
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

                    endereco

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